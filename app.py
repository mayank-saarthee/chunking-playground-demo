import csv
import hashlib
import html
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(ROOT / ".cache" / "tiktoken"))
os.environ.setdefault("NLTK_DATA", str(ROOT / ".cache" / "nltk"))
os.environ.setdefault("HAYSTACK_TELEMETRY_ENABLED", "False")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ["DO_NOT_TRACK"] = "1"
os.environ["SCARF_NO_ANALYTICS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import streamlit as st
from chunk_lab import TOOLS, parse_document, run_chunking, strategy_info
from help_content import TOOL_HELP, STRATEGY_HELP, GLOSSARY

st.set_page_config(page_title="Chunking Playground", page_icon="✂️", layout="wide")
st.markdown("""<style>
.block-container {padding-top:2rem; max-width:1500px}
.chunk {border:1px solid #d9dfe7; border-left:4px solid #4f74d9; border-radius:8px; padding:15px; margin:12px 0; background:#fafbfe; color:#202633}
.chunk pre {white-space:pre-wrap; overflow-wrap:anywhere; font:14px/1.6 ui-monospace,monospace; margin-bottom:0}
.chunk small {color:#536179}
.source {white-space:pre-wrap; overflow-wrap:anywhere; font:14px/1.65 ui-monospace,monospace; max-height:450px; overflow:auto; padding:16px; border:1px solid #d9dfe7; border-radius:8px}
mark {background:#ffdf81; color:#202633}
.page-break {display:block; border-top:1px dashed #8b96aa; color:#66748c; font:12px/2 sans-serif; margin:14px 0}
</style>""", unsafe_allow_html=True)

st.title("✂️ Chunking Playground")
st.caption("Upload once. Compare two tools. See exactly where the chunks break.")
st.markdown("**Tool** = the library doing the work. **Strategy** = the rule it uses to divide the document.")


@st.cache_resource(max_entries=12, show_spinner=False)
def cached_parse(name, data, parser, ocr):
    return parse_document(name, data, parser, ocr)


def queue_help(kind, label, tool=None, always=False):
    if not always and not st.session_state.get("auto_help", True):
        return
    tool = tool or st.session_state[f"tool_{label}"]
    strategy = st.session_state[f"strategy_{label}_{tool}"] if kind == "strategy" else None
    st.session_state["help_request"] = dict(kind=kind, label=label, tool=tool, strategy=strategy)


@st.dialog("Understand your selection", width="large")
def explain_selection(request):
    tool, strategy = request["tool"], request["strategy"]
    content = STRATEGY_HELP[(tool, strategy)] if strategy else TOOL_HELP[tool]
    st.caption(f"Panel {request['label']} · {'Strategy' if strategy else 'Tool'}")
    st.subheader(f"{tool} · {strategy}" if strategy else tool)
    st.write(content["meaning"])
    st.markdown("**A simple example**")
    st.info(content["example"])
    st.markdown("**Useful for:** " + content["useful_for"])
    st.markdown("**What to look for:** " + content["watch_for"])
    if strategy:
        units, _, overlap_ok = strategy_info(tool, strategy)
        st.caption(GLOSSARY[units])
        if overlap_ok:
            st.caption("Overlap repeats some text at the end of one chunk at the start of the next, to help preserve context. Zero means no requested overlap.")
    else:
        st.caption("Available strategies: " + ", ".join(TOOLS[tool]))
    if st.button("Got it", type="primary", key="close_help"):
        st.rerun()


def config(label, default_tool, default_strategy):
    st.subheader(label)
    tool = st.selectbox("Chunking tool", list(TOOLS), index=list(TOOLS).index(default_tool), key=f"tool_{label}", on_change=queue_help, args=("tool", label))
    st.button("About this tool", key=f"help_tool_{label}", on_click=queue_help, args=("tool", label, None, True))
    strategies = TOOLS[tool]
    strategy = st.selectbox("Strategy", strategies, index=strategies.index(default_strategy) if default_strategy in strategies else 0, key=f"strategy_{label}_{tool}", on_change=queue_help, args=("strategy", label, tool))
    st.button("About this strategy", key=f"help_strategy_{label}", on_click=queue_help, args=("strategy", label, tool, True))
    units, description, overlap_ok = strategy_info(tool, strategy)
    st.caption(description)
    size = 256
    if units != "none":
        default = 1 if units in {"pages", "paragraphs", "sentences"} else 1000 if units == "characters" else 256
        size = st.number_input(f"Chunk size ({units})", min_value=1, max_value=20000, value=default, step=1 if units in {"pages", "paragraphs", "sentences"} else 32, key=f"size_{label}_{tool}_{strategy}", help=GLOSSARY[units])
    overlap = st.number_input(f"Overlap ({units})", min_value=0, max_value=max(size - 1, 0), value=0, disabled=not overlap_ok, key=f"overlap_{label}_{tool}_{strategy}_{size}", help="Repeat the end of one chunk at the start of the next to preserve context. Zero means no requested overlap. Some strategies do not support it.")
    keep_pages = st.checkbox("Split each page separately first", value=False, disabled=tool in {"Docling", "Unstructured", "Baseline"} or strategy == "Pages", key=f"pages_{label}", help="Ask the text cutter to process each detected page group on its own, so a chunk cannot combine text from different page groups.")
    if tool in {"Docling", "Unstructured"}:
        st.caption(f"Uses {tool}'s native document parser automatically.")
    return dict(tool=tool, strategy=strategy, size=int(size), overlap=int(overlap), keep_pages=keep_pages and tool not in {"Docling", "Unstructured", "Baseline"})


with st.sidebar:
    st.header("Document")
    file_type = st.selectbox("Document type", ["Any supported type", "PDF", "DOCX", "Markdown"])
    extensions = {"Any supported type": ["pdf", "docx", "md", "markdown"], "PDF": ["pdf"], "DOCX": ["docx"], "Markdown": ["md", "markdown"]}[file_type]
    uploaded = st.file_uploader("Upload a document", type=extensions)
    demo = st.selectbox("Or use a sample", ["Markdown", "DOCX", "PDF"])
    sample = ROOT / "samples" / {"Markdown": "demo.md", "DOCX": "demo.docx", "PDF": "demo.pdf"}[demo]
    name, data = (uploaded.name, uploaded.getvalue()) if uploaded is not None else (sample.name, sample.read_bytes())
    st.caption(f"Selected: {name}")
    extraction = st.selectbox("Text extraction for text chunkers", ["Quick text", "Docling", "Unstructured"], help="LangChain, LlamaIndex, Chonkie, Haystack, semchunk and semantic-text-splitter consume extracted text. Docling/Unstructured native chunkers always use their own parser.")
    ocr = st.checkbox("Docling OCR for scanned PDFs", value=False)
    st.caption("PDF pages are physical pages. DOCX page labels depend on explicit breaks or parser markers. Markdown normally has no pages.")
    st.divider()
    st.checkbox("Explain selections automatically", value=True, key="auto_help", help="Show a plain-language popup when you change a tool or strategy. About buttons always let you reopen the guide.")
    st.caption("Processed on the machine running this demo • No AI API key required")
    st.caption("Docling PDF and semantic chunking download open model weights on first use. Installation includes the heavier document libraries.")

left, right = st.columns(2, gap="large")
with left:
    a = config("A", "Baseline", "Paragraphs")
with right:
    b = config("B", "LangChain", "Recursive tokens")

fingerprint = hashlib.sha256(data + json.dumps([name, a, b, extraction, ocr], sort_keys=True).encode()).hexdigest()
if st.button("Compare chunks", type="primary", width="stretch", key="compare_chunks"):
    runs, sources, errors = [], [], []
    for settings in [a, b]:
        parser = settings["tool"] if settings["tool"] in {"Docling", "Unstructured"} else extraction
        try:
            with st.spinner(f"Running {settings['tool']} / {settings['strategy']}… First model downloads can take a few minutes."):
                parsed = cached_parse(name, data, parser, ocr)
                run = run_chunking(parsed, **settings)
                runs.append(run)
                sources.append(parsed)
                errors.append(None)
        except Exception as exc:
            runs.append(None)
            sources.append(None)
            errors.append(f"{type(exc).__name__}: {exc}")
    st.session_state["comparison"] = dict(fingerprint=fingerprint, name=name, runs=runs, sources=sources, errors=errors)

result = st.session_state.get("comparison")
if result is None:
    st.info("A sample is ready. Click Compare chunks, or upload your own PDF, DOCX or Markdown.")
else:
    if result["fingerprint"] != fingerprint:
        st.warning("Settings or document changed. Click Compare chunks to refresh the results below.")
    st.subheader(f"Results · {result['name']}")
    tabs = st.tabs(["Chunks", "Source & boundaries", "Summary & export"])
    with tabs[0]:
        for col, run, source, error, label in zip(st.columns(2, gap="large"), result["runs"], result["sources"], result["errors"], ["A", "B"]):
            with col:
                if error:
                    st.error(error)
                    continue
                st.markdown(f"**{label} · {run['tool']} / {run['strategy']}**")
                chunks = run["chunks"]
                m1, m2, m3 = st.columns(3)
                m1.metric("Chunks", len(chunks))
                m2.metric("Avg tokens", round(sum(c["tokens"] for c in chunks) / len(chunks)) if chunks else 0)
                m3.metric("Chunking", f"{run['chunk_seconds']:.3f}s")
                st.caption(f"Parser: {run['parser']} · Parse time: {run['parse_seconds']:.3f}s · {run['page_basis']}")
                for note in source.notes + run["notes"]:
                    st.caption(note)
                query = st.text_input("Filter chunks by text", key=f"filter_{label}")
                filtered = [chunk for chunk in chunks if query.lower() in chunk["text"].lower()]
                per_page = 10
                max_page = max(1, (len(filtered) + per_page - 1) // per_page)
                page = st.number_input("Result page", min_value=1, max_value=max_page, value=1, key=f"result_page_{label}_{result['fingerprint']}_{query}")
                st.caption(f"Showing {len(filtered)} matching chunks · 10 per result page")
                for chunk in filtered[(page - 1) * per_page:page * per_page]:
                    location = ", ".join(map(str, chunk["pages"])) or "unavailable"
                    overlap_chars = 0
                    if chunk["id"] > 1:
                        prior = chunks[chunk["id"] - 2]
                        if chunk["start"] is not None and prior["end"] is not None:
                            overlap_chars = max(0, min(prior["end"], chunk["end"]) - chunk["start"])
                    escaped_text = html.escape(chunk["text"]).replace("\n", "&#10;")
                    overlap_label = str(overlap_chars) if chunk["start"] is not None and (chunk["id"] == 1 or chunks[chunk["id"] - 2]["end"] is not None) else "unknown"
                    st.html(f'<div class="chunk"><b>Chunk {chunk["id"]}</b><br><small>{chunk["tokens"]} tokens · {chunk["characters"]} characters · page/group {location} · {overlap_label} source characters shared with prior chunk</small><pre>{escaped_text}</pre></div>')
                    with st.expander(f"Metadata · chunk {chunk['id']}"):
                        st.json({key: value for key, value in chunk.items() if key != "text"})
    with tabs[1]:
        for col, run, source, label in zip(st.columns(2, gap="large"), result["runs"], result["sources"], ["A", "B"]):
            with col:
                if run is None:
                    continue
                st.markdown(f"**{label} · {run['tool']} extracted source**")
                chunks = run["chunks"]
                if chunks:
                    selected_id = st.selectbox("Highlight a chunk", [chunk["id"] for chunk in chunks], key=f"highlight_{label}_{result['fingerprint']}")
                    selected = chunks[selected_id - 1]
                    if selected["start"] is not None:
                        start, end = selected["start"], selected["end"]
                        rendered = html.escape(source.text[:start]) + "<mark>" + html.escape(source.text[start:end]) + "</mark>" + html.escape(source.text[end:])
                    else:
                        st.caption("A unique source span is unavailable for this chunk because its text was transformed or repeated. Native metadata appears on the Chunks tab.")
                        rendered = html.escape(source.text)
                    rendered = rendered.replace("\n", "&#10;").replace("\f", '<span class="page-break">PAGE / GROUP BREAK</span>')
                    st.html(f'<div class="source">{rendered}</div>')
                st.caption(source.page_basis + " · offsets refer to extracted text, not original file bytes.")
                st.dataframe([dict(block=i + 1, page_group=block.page, type=block.kind, characters=len(block.text), start=block.start, end=block.end, preview=block.text[:120]) for i, block in enumerate(source.blocks)], hide_index=True, width="stretch")
    with tabs[2]:
        summary, chart, rows = [], [], []
        for label, run in zip(["A", "B"], result["runs"]):
            if run is None:
                continue
            chunks = run["chunks"]
            summary.append({"Run": label, "Tool": run["tool"], "Strategy": run["strategy"], "Parser": run["parser"], "Size unit": run["size_unit"], "Chunk count": len(chunks), "Min tokens": min((c["tokens"] for c in chunks), default=0), "Max tokens": max((c["tokens"] for c in chunks), default=0), "Cross-page chunks": sum(len(c["pages"]) > 1 for c in chunks), "Chunk seconds": run["chunk_seconds"]})
            for chunk in chunks:
                chart.append({"chunk": chunk["id"], "tokens": chunk["tokens"], "run": label + " · " + run["tool"]})
                rows.append({"run": label, "tool": run["tool"], "strategy": run["strategy"], "id": chunk["id"], "tokens": chunk["tokens"], "characters": chunk["characters"], "pages": json.dumps(chunk["pages"]), "source_start": chunk["start"], "source_end": chunk["end"], "text": chunk["text"], "metadata": json.dumps(chunk["metadata"], default=str, ensure_ascii=False)})
        st.dataframe(summary, hide_index=True, width="stretch")
        if chart:
            st.bar_chart(chart, x="chunk", y="tokens", color="run", stack=False)
        st.caption("Token counts use cl100k_base for both runs. Chunk-size units differ by strategy. Times include library initialization; cached parse times reflect the first parse. These are inspection metrics, not retrieval quality scores.")
        export = dict(document=result["name"], tokenizer="cl100k_base", runs=result["runs"], errors=result["errors"])
        buffer = io.StringIO(newline="")
        if rows:
            writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        dl1, dl2 = st.columns(2)
        dl1.download_button("Download comparison JSON", json.dumps(export, indent=2, ensure_ascii=False, default=str), "chunks.json", "application/json", width="stretch")
        dl2.download_button("Download chunks CSV", buffer.getvalue(), "chunks.csv", "text/csv", width="stretch")

with st.expander("Tools researched & what to try first"):
    st.markdown("**Start with Docling Hybrid for structured PDFs/DOCX, and LangChain Recursive tokens as a simple baseline.** There is no universal winner; inspect your own documents. Chonkie is especially useful for comparing dedicated chunkers.")
    st.dataframe([
        {"Tool": "Docling", "Good for": "Layout, tables, native element/hybrid chunking", "Link": "https://docling-project.github.io/docling/concepts/chunking/"},
        {"Tool": "Unstructured", "Good for": "Format-aware elements, title/page boundaries", "Link": "https://docs.unstructured.io/open-source/core-functionality/chunking"},
        {"Tool": "LangChain", "Good for": "Simple recursive/token/Markdown splitters", "Link": "https://docs.langchain.com/oss/python/integrations/splitters"},
        {"Tool": "LlamaIndex", "Good for": "Sentence/token/parent-child chunks", "Link": "https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/"},
        {"Tool": "Haystack", "Good for": "Explicit page/paragraph/word/sentence units", "Link": "https://docs.haystack.deepset.ai/docs/documentsplitter"},
        {"Tool": "Chonkie", "Good for": "Dedicated token, sentence, recursive, semantic chunkers", "Link": "https://github.com/feyninc/chonkie"},
        {"Tool": "semchunk", "Good for": "Lightweight recursive token-budget splitting", "Link": "https://github.com/isaacus-dev/semchunk"},
        {"Tool": "semantic-text-splitter", "Good for": "Rust-backed text/Markdown structural splitting", "Link": "https://github.com/benbrandt/text-splitter"},
    ], hide_index=True, column_config={"Link": st.column_config.LinkColumn("Documentation")}, width="stretch")
    st.markdown("Google Document AI Layout Parser is a managed, billed cloud service, so it is a reference rather than an open-source adapter in this local demo. [Official documentation](https://docs.cloud.google.com/document-ai/docs/layout-parse-chunk). Other notable PDF parsers are [Marker](https://github.com/datalab-to/marker), [MinerU](https://github.com/opendatalab/MinerU), and [PyMuPDF4LLM](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/). Their main role is extraction; downstream chunkers can consume their Markdown. Neural, late and agentic chunking need extra model/inference work and are outside this quick boundary-inspection POC.")

# Consume the request before opening the dialog, so closing it does not reopen it.
help_request = st.session_state.pop("help_request", None)
if help_request:
    explain_selection(help_request)
