"""Plain-language guides for the exact tools and strategies offered in this demo."""


def guide(meaning, example, useful_for, watch_for):
    return dict(meaning=meaning, example=example, useful_for=useful_for, watch_for=watch_for)


TOOL_HELP = {
    "Baseline": guide(
        "A set of simple rules built into this demo. Think of it as cutting a document with a ruler: by paragraph, page, length or heading.",
        "A three-page PDF can become three chunks when you choose Pages and a size of 1.",
        "Understanding the basics and having a simple starting point for comparison.",
        "Simple rules do not work out whether two passages discuss the same topic."),
    "LangChain": guide(
        "A popular toolkit for building applications that use language models. Here we use only its text cutters.",
        "Its recursive cutter first looks for paragraph breaks. If a paragraph is too long, it tries smaller breaks such as words.",
        "A straightforward starting point for splitting text into manageable pieces.",
        "It cuts the text supplied by the selected extraction tool; it does not read the original page layout itself."),
    "LlamaIndex": guide(
        "A toolkit for making documents searchable with AI. Its cutters can keep sentences together or create large chunks with smaller chunks inside them.",
        "A large section about leave policy can have smaller child chunks for annual leave and sick leave.",
        "Comparing sentence-based cutting with several levels of detail.",
        "Hierarchical output includes both larger and smaller versions of the same text, so repeated text is expected."),
    "Chonkie": guide(
        "A toolkit focused on chunking. It offers simple size rules, sentence rules and a local model that looks for changes in topic.",
        "The semantic option may put travel expenses and employee benefits in separate chunks because their subjects differ.",
        "Comparing several cutting approaches within one dedicated toolkit.",
        "Only the Semantic option uses a meaning-based model here. Its first run downloads that model."),
    "Haystack": guide(
        "A toolkit for document search. It lets you split by familiar units such as words, paragraphs, pages or sentences.",
        "With Sentence and a size of 3, it groups up to three sentences into each chunk.",
        "Demonstrating what changes when the unit being counted changes.",
        "Always read the unit beside Chunk size. A size of 3 pages is very different from 3 words."),
    "Docling": guide(
        "A document reader that identifies parts such as headings, paragraphs, lists and tables before creating chunks. Think of it as reading the document's structure first.",
        "A table can stay associated with its heading rather than being cut simply because a page ends.",
        "Documents with headings, tables and more complex layouts.",
        "Its own reader may extract different text from the Quick text reader. PDF processing can be slower on first use."),
    "Unstructured": guide(
        "A document reader that first separates content into elements, such as titles, paragraphs and tables, then groups those elements into chunks.",
        "By title can keep an Expenses section separate from the next section, even when both are short.",
        "Inspecting title boundaries, document elements and page-boundary rules.",
        "Tables are handled separately. Its size setting counts characters, and very long elements may still need cutting."),
    "semchunk": guide(
        "A lightweight cutter that looks for natural text breaks while trying to stay within a token budget.",
        "It tries a paragraph break before cutting a long passage into smaller pieces.",
        "A simple comparison with other cutters that use token limits.",
        "Despite the name, this demo's semchunk option does not use an AI model to compare meanings."),
    "semantic-text-splitter": guide(
        "A fast cutter that follows text structure, such as paragraphs and sentences. Its Markdown option also recognises headings, lists and code.",
        "It can treat a Markdown code block as a unit while fitting content into the chosen size.",
        "Comparing structure-aware cuts in plain text and Markdown.",
        "Here, semantic means following text structure. This option does not use an AI meaning-comparison model."),
}


STRATEGY_HELP = {
    ("Baseline", "Paragraphs"): guide(
        "Keep detected paragraphs or blocks whole, and group the chosen number together.",
        "Size 2 groups two detected blocks into each chunk. A heading or table may count as a block too.",
        "Seeing whether paragraph boundaries are a useful place to cut.",
        "A long paragraph stays long; there is no token limit. PDF paragraphs depend on how the reader extracts whitespace."),
    ("Baseline", "Pages"): guide(
        "Cut at page boundaries, grouping the chosen number of pages together.",
        "A three-page PDF with size 1 gives three page chunks. Size 2 groups the first two pages together.",
        "Showing whether chunks stop at the end of a page.",
        "PDF pages are actual pages. DOCX groups rely on explicit page breaks, not Word's automatic page layout. Ordinary Markdown has no pages."),
    ("Baseline", "Fixed characters"): guide(
        "Cut after a chosen number of characters, including spaces and punctuation.",
        "Size 500 makes pieces of up to 500 characters, even if a sentence continues into the next piece.",
        "Seeing the simplest size-based cutting rule.",
        "It can cut a word or sentence in the middle."),
    ("Baseline", "Markdown headings"): guide(
        "Start a new chunk at each Markdown heading section.",
        "The text under # Travel and the text under # Benefits become separate sections.",
        "Documents organised with Markdown headings.",
        "A very large section stays large; this option has no size limit."),
    ("LangChain", "Recursive characters"): guide(
        "Try larger natural breaks first: paragraphs, then lines, then words, then individual characters if needed.",
        "With a 1,000-character target, a short paragraph stays together; an oversized one is cut into smaller pieces.",
        "A general-purpose starting point that respects common text breaks.",
        "Size counts characters rather than tokens. It follows breaks in extracted text, not the original visual layout."),
    ("LangChain", "Recursive tokens"): guide(
        "Try paragraph and smaller text breaks while measuring size in tokens, the small text pieces counted by language models.",
        "With a 256-token target, short paragraphs can be grouped and long ones broken down.",
        "Preparing manageable text pieces for language-model applications.",
        "The target is not always an exact cap. Read the measured token count on each resulting chunk."),
    ("LangChain", "Fixed tokens"): guide(
        "Cut the token sequence into fixed-size windows, regardless of sentence or paragraph boundaries.",
        "Size 256 and overlap 32 repeats the last 32 tokens when the next window starts.",
        "A direct size-based comparison with natural-boundary cutters.",
        "Sentences can be cut midway. Some unusual characters can also be split during token decoding."),
    ("LangChain", "Markdown headings"): guide(
        "Divide Markdown by heading sections and retain the headings and their context.",
        "## Annual leave starts a section underneath # HR policies, and the heading context appears in metadata.",
        "Text whose headings already describe its topics.",
        "Sections are not further cut to a token limit in this demo."),
    ("LlamaIndex", "Sentence"): guide(
        "Group text into chunks with a token target, trying to keep complete sentences together.",
        "Several short sentences about one policy can fit into a 256-token chunk.",
        "Keeping explanations readable without cutting every sentence midway.",
        "A very long sentence may still need to be cut to fit."),
    ("LlamaIndex", "Tokens"): guide(
        "Use a token budget and text separators to form chunks.",
        "A long passage is broken into pieces near the selected token size, with overlap if requested.",
        "Comparing token-budget cutting with sentence-based cutting.",
        "Token counts are not word counts; one word may contain several tokens."),
    ("LlamaIndex", "Markdown headings"): guide(
        "Use Markdown heading sections as the document's natural divisions.",
        "The section under ## Eligibility becomes a chunk with its heading information.",
        "Documents written as a hierarchy of Markdown headings.",
        "Large sections can remain large because this option does not apply a token cap."),
    ("LlamaIndex", "Hierarchical"): guide(
        "Create several levels: large parent chunks and smaller child chunks within them. Think chapter, section, then short passage.",
        "Size 256 creates levels targeting 1,024, 512 and 256 tokens. Parent and child relationships appear in metadata.",
        "Inspecting both broad context and small pieces of detail.",
        "Both parents and children are returned, so text appears more than once. This is different from Docling's Hierarchical option."),
    ("Chonkie", "Tokens"): guide(
        "Divide text by a fixed token size, with optional overlap.",
        "Size 256 and overlap 32 lets neighbouring chunks share 32 tokens.",
        "A simple comparison based on chunk size.",
        "A size rule does not guarantee complete sentences or a single topic."),
    ("Chonkie", "Sentence"): guide(
        "Group sentences while trying to fit them within the chosen token size.",
        "Several related short sentences can become one chunk instead of one chunk per sentence.",
        "Keeping sentence boundaries in otherwise size-based chunks.",
        "The size control counts tokens, not the number of sentences."),
    ("Chonkie", "Recursive"): guide(
        "Try a series of text-boundary rules, moving to smaller breaks when a piece is too large.",
        "A long paragraph may be broken into sentence-sized or smaller pieces.",
        "Comparing natural-boundary cutting against fixed token windows.",
        "Overlap is unavailable for this option in the demo."),
    ("Chonkie", "Semantic (local model)"): guide(
        "Use a small AI model on the demo server to compare nearby passages and look for changes in topic.",
        "A switch from travel reimbursement to parental leave may become a chunk boundary even without a heading.",
        "Documents where topics change without clear section markers.",
        "Meaning is estimated, so inspect the results. First use downloads the model and can take longer; the model's tokenizer may count differently from the displayed counts."),
    ("Haystack", "Words"): guide(
        "Group a chosen number of words into each chunk.",
        "Size 100 and overlap 10 repeats ten words between neighbouring chunks.",
        "Showing a familiar word-count approach.",
        "Word limits can cut sentences in the middle. Words and tokens are different units."),
    ("Haystack", "Paragraphs"): guide(
        "Group a chosen number of paragraphs, using paragraph breaks in the extracted text.",
        "Size 2 puts two paragraphs into each chunk.",
        "Comparing paragraph-based grouping with page or size-based grouping.",
        "The reader's paragraph breaks affect the result, and long paragraphs can produce large chunks."),
    ("Haystack", "Pages"): guide(
        "Group a chosen number of page-marked text sections into each chunk.",
        "Size 1 keeps each detected page group separate.",
        "Checking whether a page boundary should also be a chunk boundary.",
        "DOCX page labels depend on available explicit breaks or parser markers. Ordinary Markdown has no page markers."),
    ("Haystack", "Sentence"): guide(
        "Group a chosen number of sentences into each chunk.",
        "Size 3 groups three sentences; overlap 1 repeats one sentence in the next chunk.",
        "Demonstrating sentence-count grouping.",
        "Size counts sentences here, while other tools' Sentence strategies usually count tokens."),
    ("Haystack", "Recursive"): guide(
        "Try natural text separators, using smaller breaks as needed to fit a token budget.",
        "A short paragraph may stay together, while a longer one is divided.",
        "Comparing Haystack's recursive rules with other recursive cutters.",
        "Its internal tokenizer may count differently from the common token counts shown in the results."),
    ("Docling", "Hierarchical"): guide(
        "Follow the document's recognised elements, such as paragraphs, lists and tables, and carry their heading context with them.",
        "A paragraph beneath Expenses can become a chunk associated with that heading.",
        "Seeing what the document's own structure looks like as chunks.",
        "This option does not create LlamaIndex-style large and small size levels. Elements can exceed a token target; there is no size control here."),
    ("Docling", "Hybrid"): guide(
        "Start from document elements, then cut oversized elements and combine compatible small ones using a token budget.",
        "Two short paragraphs under the same heading may be combined; a very long paragraph may be split.",
        "Keeping document structure while making chunks more manageable in size.",
        "Heading or caption context can be added to chunk text. There is no fixed-overlap setting for this option."),
    ("Unstructured", "Basic elements"): guide(
        "Group recognised document elements until the character budget is reached, keeping whole elements when possible.",
        "A title and two short paragraphs may fit into one chunk; a table is handled separately.",
        "Seeing how element-aware grouping differs from raw text cutting.",
        "Oversized elements are split. Overlap applies to those split elements rather than every neighbouring chunk."),
    ("Unstructured", "By title"): guide(
        "Respect section titles so content from a new section starts a new chunk, while also applying a character budget.",
        "Expenses and Benefits remain separate even if they are both short sections.",
        "Documents with clear titles that describe each section.",
        "A section can span pages. This demo keeps small titled sections separate instead of combining them."),
    ("Unstructured", "By title + page boundaries"): guide(
        "Respect both section titles and recognised page changes when grouping elements.",
        "A section continuing from PDF page 1 to page 2 is stopped at the page boundary.",
        "Comparing title-only grouping with page-restricted grouping.",
        "Page separation depends on page information supplied by the document reader. Word's automatic pagination is not guaranteed."),
    ("semchunk", "Recursive tokens"): guide(
        "Look for natural text breaks, then smaller breaks as needed, to fit a token budget.",
        "A short paragraph stays together; a paragraph over the budget is divided at smaller breaks.",
        "A lightweight comparison with other recursive token cutters.",
        "This is based on text boundaries and counts, without an AI model judging topic similarity."),
    ("semantic-text-splitter", "Text structure"): guide(
        "Follow text structure, such as paragraphs and sentences, while fitting chunks within a token budget.",
        "Several short sentences may stay together; a larger block is divided at smaller structural breaks.",
        "Plain text with useful paragraph and sentence boundaries.",
        "The word semantic in the tool's name does not mean an AI topic model is running."),
    ("semantic-text-splitter", "Markdown structure"): guide(
        "Use Markdown features, such as headings, lists and code blocks, when deciding where to cut.",
        "A heading and its short explanation may stay together; a large section is divided into smaller pieces.",
        "Markdown documents whose formatting provides useful boundaries.",
        "It follows Markdown structure rather than estimating the meaning of passages with AI."),
}


GLOSSARY = {
    "tokens": "Tokens are small pieces of text counted by language models. A word may contain several tokens; tokens are not the same as words.",
    "characters": "Characters include letters, spaces and punctuation. A 1,000-character limit is a text-length rule.",
    "paragraphs": "Paragraphs are blocks detected by the document reader. Formatting and extraction can affect where a block starts and ends.",
    "sentences": "This size counts sentences. For example, size 3 groups three sentences together.",
    "pages": "PDF pages are physical pages. DOCX page groups depend on explicit breaks or parser markers; ordinary Markdown has no pages.",
    "words": "This size counts words in the extracted text. Word counts differ from the token counts shown on chunk cards.",
    "none": "This strategy follows document structure and has no size control in this demo.",
}
