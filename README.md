# Chunking Playground

A simple Streamlit demo for inspecting how document chunking works. Upload a synthetic PDF, DOCX or Markdown document, choose two tools and strategies, and compare their actual chunks and source boundaries.

The app includes 9 tools and 29 strategies: Docling, LangChain, LlamaIndex, Chonkie, Haystack, Unstructured, semchunk, semantic-text-splitter, and a simple baseline. Tool and strategy selections open explanations in everyday language. Included documents are synthetic examples.

## Cloud deployment

Deploy this dedicated public repository on [Streamlit Community Cloud](https://share.streamlit.io/) using `app.py`, branch `main`, and Python **3.12**. `requirements.txt` contains Linux CPU dependencies; `packages.txt` contains system dependencies. No API keys or private repository access are needed for the application.

The cloud app runs independently of the owner's laptop. Free apps may sleep after 12 hours without traffic and can be woken by a viewer. First use of Docling or semantic chunking downloads models and takes longer. Use synthetic documents for this public testing demo.

## Local run

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Uploaded documents are processed on the server. Parsed documents may remain in a bounded in-memory cache until restart or eviction; parser temporary files are removed after processing. Model downloads are cached locally on the server. This demo inspects chunk boundaries, not retrieval or answer quality.

See [Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) for hosting settings.
