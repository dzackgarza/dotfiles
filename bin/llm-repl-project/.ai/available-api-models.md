# Available API Models (2025)

**Last Updated:** 2025-07-10

This document lists all available models for our API keys and their recommended usage patterns.

## Google Gemini API (GEMINI_API_KEY)

### Current Models (2025)
- **gemini-2.5-pro**: Latest flagship model with advanced reasoning (60 RPM free)
- **gemini-2.5-flash**: Optimized speed/performance balance (60 RPM free)
- **gemini-2.5-flash-lite**: Cost-efficient, high-volume tasks
- **gemini-2.0-flash**: Next-gen with tool use, 1M context window
- **gemini-1.5-pro**: Legacy model (deprecated for new projects)
- **gemini-1.5-flash**: Legacy model (deprecated for new projects)

### Recommended Usage
- **Intent Detection**: `gemini-1.5-flash` (if still available) or `gemini-2.5-flash`
- **Complex Reasoning**: `gemini-2.5-pro`
- **High-Volume Tasks**: `gemini-2.5-flash-lite`
- **Tool Use**: `gemini-2.0-flash`

## Mistral AI API (MISTRAL_API_KEY)

### Current Models (2025)
- **magistral-medium**: AI reasoning model with chain-of-thought (June 2025)
- **mistral-medium-3**: Efficiency-focused, $0.40/1M input tokens (May 2025)
- **devstral-small**: Code-specialized model (May 2025)
- **mistral-ocr-2**: Document understanding (2025)
- **mistral-small-3.1**: Efficient smaller model (March 2025)
- **codestral-2**: Advanced code generation (January 2025)
- **mistral-saba**: 24B model for Middle East/South Asia (February 2025)

### Recommended Usage
- **Code Tasks**: `devstral-small` or `codestral-2`
- **Reasoning**: `magistral-medium`
- **General Chat**: `mistral-medium-3`
- **Document Processing**: `mistral-ocr-2`

## Groq API (GROQ_API_KEY)

### Current Models (2025)
- **llama-3.3-70b-versatile**: Latest Llama, replaces 3.0 (30-60 RPM)
- **llama-3.1-8b-instant**: Faster 8B model (30-60 RPM)
- **deepseek-r1-distill-llama-70b**: Reasoning-optimized (30-60 RPM)
- **deepseek-r1-distill-qwen-32b**: Reasoning model (30-60 RPM)
- **qwen3-32b**: Latest Qwen, replaces QWQ-32B

### Deprecated Models (being phased out)
- `mixtral-8x7b-32768` → Use newer models
- `llama3-70b-8192` → Use `llama-3.3-70b-versatile`
- `llama3-8b-8192` → Use `llama-3.1-8b-instant`

### Recommended Usage
- **Fast Chat**: `llama-3.1-8b-instant`
- **Complex Tasks**: `llama-3.3-70b-versatile`
- **Reasoning**: `deepseek-r1-distill-llama-70b`

## Hugging Face API (HUGGING_FACE_API_KEY)

### Access Pattern
- 30-60 RPM depending on model
- Can access any GGUF model on HF Hub
- Direct integration with Ollama

### Key Models Available
- **meta-llama/Llama-4-Scout-17B-16E-Instruct**: Latest Llama 4 (2025)
- **meta-llama/Llama-3.3-70B-Instruct**: Multilingual
- **mistralai/Mistral-Small-3.2-24B-Instruct**: Latest Mistral
- **Various quantized models**: GGUF format for local use

## Together AI API (TOGETHER_AI_API_KEY)

### Current Models (2025)
- **meta-llama/Llama-3.3-70B-Instruct-Turbo**: Default chat model
- **meta-llama/Llama-4-Scout-17B-16E-Instruct**: Vision model
- **meta-llama/Llama-3.1-405B-Instruct**: Largest model
- **deepseek-ai/DeepSeek-R1**: State-of-art reasoning
- **mistralai/Mixtral-8x7B-Instruct-v0.1**: Cost-effective

### Recommended Usage
- **Default Chat**: `Llama-3.3-70B-Instruct-Turbo`
- **Vision Tasks**: `Llama-4-Scout-17B-16E-Instruct`
- **Complex Reasoning**: `DeepSeek-R1`
- **Cost-Effective**: `Mixtral-8x7B-Instruct`

## OpenRouter API (OPENROUTER_API_KEY)

### Premium Models Available
- **anthropic/claude-4-opus**: Latest Claude (breakthrough capabilities)
- **anthropic/claude-3.7-sonnet**: Default model on OpenRouter
- **openai/gpt-4.5-preview**: Latest GPT model
- **openai/gpt-4o-mini**: Cost-effective GPT
- **google/gemini-pro-1.5**: Google's model
- **deepseek/deepseek-chat:free**: Free DeepSeek V3

### Recommended Usage
- **Complex Reasoning**: `claude-4-opus`
- **General Chat**: `claude-3.7-sonnet`
- **Cost-Effective**: `gpt-4o-mini` or `deepseek-chat:free`
- **Coding**: `gpt-4.5-preview`

## DeepSeek API (DEEPSEEK_API_KEY)

### Current Models (2025)
- **deepseek-reasoner** (R1-0528): Latest reasoning model (May 2025)
- **deepseek-chat** (V3-0324): General purpose with improved reasoning (March 2025)

### Model Selection Guide
- **Reasoning Tasks**: `deepseek-reasoner` (math, coding, research)
- **General Tasks**: `deepseek-chat` (writing, summarization, Q&A)

## Cohere API (COHERE_API_KEY)

### Available Models
- **command-r-plus**: Advanced reasoning and tool use
- **command-r**: Standard conversational model
- **embed-english-v3.0**: Text embeddings

### Usage Limits
- 10 RPM, 1M tokens/month (free tier)

## Model Routing Strategy

### By Task Type

**Instruction Routing:**
- Local: `nous-hermes-2-mistral-7b` → Free: `gemini-2.5-flash` → Paid: `gemini-2.5-pro`

**Complex Reasoning:**
- Local: `grok-1.5-quantized` → Free: `deepseek-chat:free` → Paid: `claude-4-opus`

**Code Generation:**
- Local: `llama-3.1-8b` → Free: `devstral-small` → Paid: `gpt-4.5-preview`

**Fast Classification:**
- Local: `mistral-7b-quantized` → Free: `gemini-2.5-flash` → Paid: `gemini-2.5-flash`

### Cost Optimization
1. **Free First**: Use Gemini (60 RPM), Groq (30-60 RPM), DeepSeek free
2. **Cheap Paid**: Mistral ($0.40/1M), Groq premium, Together AI
3. **Premium**: Claude 4, GPT-4.5, Gemini Pro for complex tasks

### Rate Limit Management
- **High Volume**: Gemini (60 RPM), Groq (30-60 RPM)
- **Medium Volume**: Mistral (20 RPM), Together AI (10-30 RPM)
- **Low Volume**: Cohere (10 RPM), OpenRouter (varies)