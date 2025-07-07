# Requirements Specification: Bringing custom-scraper to Exa MCP Feature Parity

This document outlines the technical requirements to upgrade the custom-scraper MCP server so that it matches or exceeds the core features and LLM-optimized outputs of Exa MCP. The goal is to enable high-frequency, AI-driven research workflows with advanced search, extraction, and structured content delivery.

## 1. Web Search and Discovery

- **Keyword Search:**  
  - Implement web search endpoints that accept queries by keyword, phrase, or question.
  - Integrate with a local or open-source search engine (e.g., SearxNG) to generate relevant URLs for downstream extraction.
  - Support result ranking, snippet extraction, and deduplication.

- **Result Metadata:**  
  - Return structured metadata for each result: title, URL, snippet, source domain, and publication date (if available).

## 2. Content Extraction and Summarization

- **Main Content Extraction:**  
  - Extract the primary article or main content from each URL, filtering out navigation, ads, and boilerplate.
  - Use content extraction libraries (e.g., Readability, Goose, Trafilatura) and fallback to browser automation (Playwright/Chromium) for dynamic sites.

- **Structured Output:**  
  - Output clean Markdown and/or structured JSON with fields for title, author, date, main text, images, tables, and links.
  - Include extracted metadata (e.g., OpenGraph, schema.org, Twitter cards).

- **Summarization:**  
  - Integrate a local LLM or summarization model to generate concise summaries of extracted content.
  - Provide both full text and summary in the response.

- **Multi-Modal Extraction:**  
  - Extract and return images, tables, code blocks, and embedded media as separate fields or attachments.

## 3. Deep and Batch Crawling

- **Multi-Page Crawling:**  
  - Support crawling multiple pages from a single domain or following links up to a configurable depth.
  - Allow batch processing of URL lists.

- **Dynamic Content Support:**  
  - Use browser automation to render and extract content from JavaScript-heavy or infinite-scroll sites.

## 4. Advanced Features

- **Fact Extraction and Highlighting:**  
  - Optionally extract key facts, entities, or answers to user queries from the main content using LLMs or NLP pipelines.

- **Citation and Source Tracking:**  
  - Track and return the provenance of all extracted content, including original URLs and crawl timestamps.

- **Rate Limiting and Throttling:**  
  - Implement configurable rate limits and backoff strategies to avoid IP bans and ensure stable operation.

- **Error Handling:**  
  - Gracefully handle failed fetches, timeouts, and extraction errors, returning informative error messages.

## 5. API and Output Specification

- **Endpoints:**
  - `/search`: Accepts a query, returns a ranked list of results with metadata and snippets.
  - `/extract`: Accepts a URL, returns structured content (Markdown/JSON), summary, and metadata.
  - `/crawl`: Accepts a seed URL and depth, returns batch-extracted content from multiple pages.
  - `/batch`: Accepts a list of URLs, returns extracted content for each.

- **Response Format:**
  - JSON with fields for:
    - `title`, `url`, `snippet`, `main_content`, `summary`, `images`, `tables`, `code_blocks`, `metadata`, `source`, `timestamp`, `error` (if any).

## 6. LLM Optimization

- **Content Cleaning:**  
  - Ensure outputs are free of boilerplate, navigation, and irrelevant sections.
- **Chunking:**  
  - Split long content into LLM-friendly chunks with context-aware boundaries.
- **Prompt-Ready Formatting:**  
  - Provide Markdown and/or JSON outputs that are directly ingestible by LLMs.

## 7. Extensibility and Modularity

- **Pluggable Extraction Pipelines:**  
  - Allow easy addition or replacement of extraction, summarization, and crawling modules.
- **Proxy and Anti-Bot Support:**  
  - Integrate proxy rotation and anti-bot evasion for robust, large-scale scraping.

## 8. Performance and Scalability

- **Asynchronous Processing:**  
  - Use async I/O for high throughput and concurrent requests.
- **Caching:**  
  - Implement result caching to avoid redundant fetches and speed up repeated queries.

## 9. Security and Privacy

- **Local Processing:**  
  - All data should be processed and stored locally unless explicitly configured otherwise.
- **Configurable Data Retention:**  
  - Allow users to set retention policies for cached or extracted data.

## 10. References for Feature Parity

- Exa MCP API documentation and feature set
- Crawl4AI, Firecrawl, ScrapeGraphAI open-source projects for extraction and crawling best practices

**References:**  
 https://docs.exa.ai/reference  
 https://github.com/unclecode/crawl4ai  
 https://github.com/mendableai/firecrawl  
 https://github.com/Zero6992/scrapegraph-ai
