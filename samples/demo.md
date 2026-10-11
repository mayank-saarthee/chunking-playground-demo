# 1. Document chunking

Chunking divides a document into smaller pieces for retrieval. A page break is a layout boundary, while a paragraph break is a writing boundary. A good demo should show both and make it clear when a chunk spans more than one page.

A fixed character strategy can cut a sentence in the middle. A token strategy measures model tokens rather than words. A recursive strategy first tries larger boundaries such as paragraphs, then smaller boundaries such as lines and spaces. Depending on the available space, a chunk may include several paragraphs or only part of a long paragraph.

This paragraph is intentionally long. Compare the same content with several chunk sizes. Smaller chunks give precise boundaries but may lose useful surrounding context. Larger chunks preserve more context but can mix unrelated details. Overlap repeats a little text between adjacent chunks, which may help a reader follow a sentence that continues across a boundary. Compare the same content with several chunk sizes. Smaller chunks give precise boundaries but may lose useful surrounding context. Larger chunks preserve more context but can mix unrelated details. Overlap repeats a little text between adjacent chunks, which may help a reader follow a sentence that continues across a boundary. Compare the same content with several chunk sizes. Smaller chunks give precise boundaries but may lose useful surrounding context. Larger chunks preserve more context but can mix unrelated details. Overlap repeats a little text between adjacent chunks, which may help a reader follow a sentence that continues across a boundary. Compare the same content with several chunk sizes. Smaller chunks give precise boundaries but may lose useful surrounding context. Larger chunks preserve more context but can mix unrelated details. Overlap repeats a little text between adjacent chunks, which may help a reader follow a sentence that continues across a boundary. Compare the same content with several chunk sizes. Smaller chunks give precise boundaries but may lose useful surrounding context. Larger chunks preserve more context but can mix unrelated details. Overlap repeats a little text between adjacent chunks, which may help a reader follow a sentence that continues across a boundary. 

# 2. Tables and paragraph boundaries

A table should ideally keep its headers alongside its rows. Format-aware tools can detect tables and headings, while a plain text splitter only sees the extracted characters. The parser's output therefore affects every downstream chunker.

The same section can continue onto another page. Page chunking always follows the physical PDF boundary; title-based chunking can continue across that boundary unless the tool is told to preserve pages. Inspect the reported page list on each chunk.

Repeated labels test source mapping: alpha beta gamma. Repeated labels test source mapping: alpha beta gamma.

| Strategy | Boundary |
| --- | --- |
| Page | Physical PDF page |
| Paragraph | Detected paragraph |
| Token | Token budget |
| Hybrid | Elements + token budget |

# 3. Topic change: gardening

Tomatoes need sunlight, water and well-drained soil. A gardener checks the soil before watering and supports taller plants with stakes. This is a deliberate topic change so that semantic chunking has something different to detect.

Compost improves soil structure. Mulch helps keep moisture in the ground. These sentences belong together even if their combined length differs from a fixed character budget.

Try paragraphs versus pages, then recursive tokens versus Docling hybrid. Look at headings, tables, page lists, token counts and highlighted source spans. This demo inspects boundaries; it does not measure answer quality or retrieval accuracy.
