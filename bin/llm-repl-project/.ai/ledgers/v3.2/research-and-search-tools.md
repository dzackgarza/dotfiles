
# Ledger: Research and Search Tools

**Goal:** To provide comprehensive research and search capabilities, including local corpus searching, intelligently sourced internet search, and general web search and fetch functionalities.

## 1. Core Philosophy

- **Comprehensive Information Access:** Enable the AI and user to access information from diverse sources, both local and remote.
- **Source Quality and Relevance:** Prioritize genuine, high-quality content over commercial or low-value results.
- **Contextual Search:** Adapt search strategies based on the user's query and intent.

## 2. Core Functionality

### 2.1. Corpus Searching Plugin

#### Feature

- A `/corpus search <query>` command that allows the user to search for information in a corpus of textbooks, papers, and other documents (e.g., `~/Dropbox/Library`, `~/diss/corpus/data`, `~/Zotero`).

#### Implementation Details

1.  **File Discovery:** Recursively scan specified directories for PDF files.
2.  **Text Extraction:** Check for canonical text extraction or run `pdf->text` extraction on the fly, caching results.
3.  **Search Index:** Index extracted text using a search library (e.g., Whoosh).
4.  **Search Execution:** Search the index for the query and return results with document name, text snippet, and link to the PDF.

### 2.2. Intelligently Sourced Internet Search Plugin

#### Feature

- A `/search <query>` command that performs an intelligently sourced internet search, prioritizing genuine, non-commercial, and enthusiast content.

#### Implementation Details

1.  **Initial Broad Search:** Perform an initial broad search using a standard search API (e.g., Brave, Tavily, Serper).
2.  **Source Filtering and Scoring:** Each URL will be filtered and scored based on:
    -   **Domain-based Filtering:** Blacklists, whitelists, heuristic scoring (e.g., `.edu`, `.org`).
    -   **Content-based Filtering:** Boilerplate detection, ad density, AI-generated content detection.
    -   **Engagement-based Scoring:** Comment analysis, backlink analysis.
3.  **Context-Aware Source Selection:** Adjust filtering and scoring rules based on the user's query.
4.  **Synthesized Answer Generation:** Pass content from top-scoring sources to an LLM to generate a synthesized answer, citing sources.

### 2.3. Web Search and Fetch Tools

#### Feature

- Implement general web search and URL content fetching capabilities to ground AI responses with real-time information from the internet.

#### Implementation Details

1.  **Web Search Tool:**
    -   Support multiple search providers (e.g., DuckDuckGo, Google Search API).
    -   Implement result ranking and filtering.
2.  **Web Fetch Tool:**
    -   Support URL content extraction.
    -   Implement JavaScript rendering support and content cleaning (remove ads, navigation).

## 3. Advanced Features

-   **Fuzzy Search:** Use fuzzy search algorithms for corpus searching.
-   **Natural Language Queries:** Allow users to ask questions in natural language for corpus searching.
-   **Recursive Search:** If initial internet search doesn't yield enough high-quality sources, perform a recursive search.
-   **User-configurable Filtering:** Allow users to customize filtering and scoring rules for internet search.
-   **Integration with RAG:** The corpus search plugin could be used as a tool by the RAG system.
