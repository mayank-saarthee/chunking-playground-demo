# Chunking Playground — management demo

Open and share [Chunking Playground](https://chunking-playground-mayank.streamlit.app/). It runs on Streamlit Community Cloud, even when the owner's laptop is off. Viewers do not need to sign in.

Use the included samples or upload **synthetic PDF, DOCX or Markdown documents only**. Select a tool and strategy in each panel, read the explanation popup, then click **Compare chunks** to inspect the boundaries and results.

All 9 tools and 29 strategies remain available. Hosted sample checks passed across all nine tools, including Docling Hybrid, local semantic chunking, PDF upload and explanation popups. These are sample checks, not validation of every strategy on every document.

A free app can sleep after 12 hours without traffic. A viewer can wake it from the browser. First model downloads can take a few minutes; larger documents and simultaneous model runs can reach the free host's resource limits.

Only the new [chunking-playground-demo repository](https://github.com/mayank-saarthee/chunking-playground-demo) was modified. The GitHub connection was limited to public repositories; no private-repository code access was granted. Existing private projects and their settings were left unchanged. Published files contain the app and synthetic samples, excluding credentials, uploaded documents and local model caches.

The playground has no personal-data, login or payment form. Uploads are processed on the hosting server. Native parsers use temporary files removed after processing; parsed results can remain in server memory until cache eviction or restart. Results and downloads are shown in the uploading viewer's session.

Streamlit usage statistics and Haystack, Unstructured and Hugging Face library telemetry are disabled. Hosting-provider access logs remain outside the application's controls.
