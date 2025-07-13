# LLM Provider Report

This report summarizes the models and rate limits for various LLM providers, based on information available as of July 2025. This aims to provide a clean and easy-to-reference overview, with special notes on models suitable for testing purposes.

**Important Notes:**
*   Rate limits can vary based on your specific account tier, usage history, and region. Always refer to the official provider documentation and your account dashboard for the most accurate and up-to-date information.
*   "N/A" indicates that specific metrics (RPM, TPM, etc.) were not explicitly found in the public documentation or are highly variable.
*   "Suitable for Testing" notes are based on generally generous free/developer tier limits or high performance characteristics.

---

## LLM Provider Models and Rate Limits

| Provider | Model (Latest/Popular) | RPM (Requests/Min) | TPM (Tokens/Min) | RPD (Requests/Day) | TPD (Tokens/Day) | Notes & Suitability for Testing |
| :------- | :--------------------- | :----------------- | :--------------- | :----------------- | :--------------- | :------------------------------ |
| **Google Gemini API** | `gemini-1.5-flash` | 60 (default tier) | 200,000 (default tier) | N/A | N/A | **Highly suitable for testing.** Designed for high throughput. Generous default limits. Higher tiers available. |
| | `gemini-1.5-pro` | 15 (default tier) | 30,000 (default tier) | N/A | N/A | Good for more complex tasks. Limits are lower than Flash but still reasonable for testing. |
| **Hugging Face Inference API** | Various (open-source) | ~few hundred/hour (free) | N/A | N/A | N/A | **Limited suitability for testing.** Free tier limits are vague and restrictive. Not recommended for consistent, high-volume testing. Pro subscription offers higher limits. |
| **Mistral AI API** | `Mistral Small 3.2` | 60 (example) | 500,000 (example) | N/A | 1,000,000 (example) | **Suitable for testing (paid tiers).** Free tier is restrictive. Paid tiers offer higher, but still defined, limits. Check your specific tier. |
| | `Mistral Large 2.1` | Lower than Small | Lower than Small | N/A | N/A | For high-complexity tasks. Limits are generally lower than smaller models. |
| **Groq API** | `llama-3.1-8b-instant` | Varies by tier | Varies by tier | Varies by tier | Varies by tier | **Highly suitable for testing.** Known for extremely low latency and high throughput. Specific limits are on user dashboard. Excellent for performance testing. |
| | `llama-3.3-70b-versatile` | Varies by tier | Varies by tier | Varies by tier | Varies by tier | Similar to 8B, but for larger models. Still very fast. |
| **Together AI API** | `meta-llama/Llama-3.1-8B-Instruct` | Varies by model/tier | Varies by model/tier | N/A | N/A | **Suitable for testing.** Offers a wide range of open-source models. Batch API available for large-scale processing. Check specific model RPS/TPS. |
| | `meta-llama/Llama-3.1-70B-Instruct` | Varies by model/tier | Varies by model/tier | N/A | N/A | |
| **OpenRouter API** | Any model (via unified API) | 1 RPS/credit (paid) | N/A | 50 (free, <10 credits) | N/A | **Suitable for testing (with credits).** Free tier is very restrictive (50 req/day). With purchased credits, offers flexible access to many models for comparative testing. |
| | Free Models (e.g., `deepseek-r1-distill-llama-70b`) | N/A | N/A | 50 (default) | N/A | Very limited for testing without purchasing credits. |
| **Cohere API** | `command-r-plus` | 20 RPM (evaluation) | N/A | N/A | N/A | **Limited suitability for testing (free).** Evaluation keys are restrictive. Production keys offer much higher limits. |
| | `command-r` | 20 RPM (evaluation) | N/A | N/A | N/A | |
| **DeepSeek API** | `deepseek-reasoner` | No explicit limit | No explicit limit | No explicit limit | No explicit limit | **Highly suitable for testing.** Claims no explicit rate limits, allowing for extensive testing. May experience latency during high traffic. |
| | `deepseek-coder` | No explicit limit | No explicit limit | No explicit limit | No explicit limit | |

---

## Models Highly Suitable for Testing Purposes:

These models offer a combination of high speed, generous rate limits (especially in free/developer tiers), or unique characteristics that make them excellent for rapid iteration and extensive testing:

*   **Google Gemini API (`gemini-1.5-flash`):** Exceptional for high throughput and general testing due to its speed and generous default rate limits.
*   **Groq API (all models, e.g., `llama-3.1-8b-instant`):** Unparalleled low latency and high throughput make it ideal for performance-critical testing and rapid development cycles.
*   **DeepSeek API (e.g., `deepseek-reasoner`, `deepseek-coder`):** The claim of no explicit rate limits (with the caveat of potential latency under high load) makes it a strong candidate for large-scale or continuous testing.
*   **OpenRouter API (with purchased credits):** While the free tier is limited, purchasing credits unlocks access to a vast array of models through a single API, making it highly versatile for comparative testing and exploring different LLMs.

These providers offer models that are implicitly much faster than even local TinyLlama (especially Groq and Gemini Flash) and come with rate limits that are either very high or non-existent, making them excellent choices for testing purposes.