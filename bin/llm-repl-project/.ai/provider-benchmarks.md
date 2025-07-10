# LLM Provider Performance Benchmarks

**Last Updated:** 2025-07-10

This document contains comprehensive performance data for language model providers across different categories and task types.

## Task Performance Rubrics

### Scoring Scale (0-10)
- **8-10**: Excellent performance, frontier-level capability
- **4-7**: Good performance, handles most cases
- **0-3**: Poor performance, frequent failures

### Task Categories

#### Instruction Processing
- **Instruction Routing**: Maps user requests to internal actions/functions
- **Instruction Rewriting**: Converts vague instructions into clear, actionable steps
- **Capability-Based Routing**: Assigns tasks to optimal model/tool
- **Prompt Amplification**: Adds relevant, context-aware instructions
- **Query Expansion**: Expands queries with relevant synonyms, clarifications
- **Instruction Decomposition**: Breaks complex tasks into actionable steps

#### Validation and Quality Control
- **Tool Use Formatting Validation**: Detects and flags format errors
- **Response Structure Assessment**: Checks for presence/order of required sections
- **Format Correction**: Corrects formatting issues
- **Query-Result Alignment**: Checks if output addresses original query
- **Intent-Result Consistency**: Detects intent drift
- **Redundancy/Contradiction Detection**: Flags redundancy/contradiction

#### Cognitive Operations
- **Rationale Generation**: Provides clear, logical explanations
- **Task Triage**: Filters out-of-scope/inappropriate tasks
- **Simple Classification**: Sentiment/intent/spam classification
- **Summarization**: Creates concise, accurate summaries
- **Error/Quality Scoring**: Assigns meaningful confidence/quality scores
- **Parameter Extraction**: Extracts structured data from text
- **User Feedback Integration**: Incorporates corrections effectively

## Model Performance Matrix

### Local Models (Quantized)

| Task Type | Best Local Model | Performance Score |
|-----------|------------------|-------------------|
| Instruction Routing | Nous Hermes 2 Mistral 7B Q | 7/10 |
| Instruction Rewriting | OpenHermes 2.5 Mistral 7B Q | 7/10 |
| Capability-Based Routing | MythoMax L2 13B Q | 7/10 |
| Prompt Amplification | LM Studio 7B (Quantized) | 7/10 |
| Query Expansion | Neural Chat 7B Q | 7/10 |
| Rationale Generation | Grok 1.5 (Quantized) | 8/10 |
| Tool Use Formatting | Llama 3 8B (Quantized) | 8/10 |
| Structure Assessment | Mistral 7B (Quantized) | 7/10 |
| Format Correction | Faraday 7B (Quantized) | 7/10 |
| Query-Result Alignment | Falcon 7B (Quantized) | 7/10 |
| Intent-Result Consistency | OpenChat 3.5 Q | 7/10 |
| Contradiction Detection | OobaGPT 7B (Quantized) | 7/10 |
| Task Triage | Command R+ (Quantized) | 8/10 |
| Classification | Starling-LM 7B Alpha Q | 8/10 |
| Summarization | Falcon 7B (Quantized) | 8/10 |
| Error/Quality Scoring | Command R+ (Quantized) | 8/10 |
| Parameter Extraction | Mistral 7B (Quantized) | 8/10 |
| Instruction Decomposition | Phi-4 Mini (Quantized) | 8/10 |
| Feedback Integration | LM Studio 7B (Quantized) | 8/10 |
| Todo Planning | Phi-3.5 Mini (Quantized) | 8/10 |

### Free-Tier Endpoints

| Task Type | Best Free Model | Performance Score | RPM Limit |
|-----------|-----------------|-------------------|-----------|
| Instruction Routing | Gemini 1.5 Flash | 8/10 | 60 |
| Instruction Rewriting | Claude 3 Haiku | 8/10 | 20 |
| Capability-Based Routing | GPT-3.5 Turbo | 8/10 | 20 |
| Prompt Amplification | Gemini 1.5 Flash | 8/10 | 60 |
| Query Expansion | GPT-3.5 Turbo | 8/10 | 20 |
| Rationale Generation | Claude 3 Haiku | 8/10 | 20 |
| Tool Use Formatting | GPT-3.5 Turbo | 8/10 | 20 |
| Structure Assessment | Gemini 1.5 Flash | 8/10 | 60 |
| Format Correction | Gemini 1.5 Flash | 8/10 | 60 |
| Query-Result Alignment | GPT-3.5 Turbo | 8/10 | 20 |
| Intent-Result Consistency | Gemini 1.5 Flash | 8/10 | 60 |
| Contradiction Detection | Claude 3 Haiku | 8/10 | 20 |
| Task Triage | Gemini 1.5 Flash | 8/10 | 60 |
| Classification | Gemini 1.5 Flash | 8/10 | 60 |
| Summarization | GPT-3.5 Turbo | 8/10 | 20 |
| Error/Quality Scoring | Claude 3 Haiku | 8/10 | 20 |
| Parameter Extraction | Gemini 1.5 Flash | 8/10 | 60 |
| Instruction Decomposition | GPT-3.5 Turbo | 8/10 | 20 |
| Feedback Integration | Claude 3 Haiku | 8/10 | 20 |
| Todo Planning | Gemini 1.5 Flash | 8/10 | 60 |

### Paid Endpoints

| Task Type | Best Paid Model | Performance Score |
|-----------|-----------------|-------------------|
| Instruction Routing | Gemini 2.5 Pro | 9/10 |
| Instruction Rewriting | Claude 4 Opus | 9/10 |
| Capability-Based Routing | GPT-4o | 9/10 |
| Prompt Amplification | Gemini 2.5 Flash | 8/10 |
| Query Expansion | GPT-4o | 8/10 |
| Rationale Generation | Claude 4 Opus | 9/10 |
| Tool Use Formatting | GPT-4o | 9/10 |
| Structure Assessment | Gemini 2.5 Flash | 9/10 |
| Format Correction | Gemini 2.5 Pro | 9/10 |
| Query-Result Alignment | GPT-4o | 9/10 |
| Intent-Result Consistency | Gemini 2.5 Pro | 9/10 |
| Contradiction Detection | Claude 4 Opus | 9/10 |
| Task Triage | Gemini 2.5 Flash | 9/10 |
| Classification | Gemini 2.5 Flash | 9/10 |
| Summarization | GPT-4o | 9/10 |
| Error/Quality Scoring | Claude 4 Sonnet | 8/10 |
| Parameter Extraction | Gemini 2.5 Flash | 9/10 |
| Instruction Decomposition | GPT-4o | 9/10 |
| Feedback Integration | Claude 4 Sonnet | 8/10 |
| Todo Planning | Gemini 2.5 Pro | 9/10 |

## Available Provider Endpoints

### Our API Keys Available

✅ **Google Gemini** (GEMINI_API_KEY): 60 RPM, Gemini 2.5 Pro/Flash, 60k tokens/min
✅ **Groq** (GROQ_API_KEY): 30-60 RPM, Llama 3.3 70B, DeepSeek R1, 10M tokens/month  
✅ **Mistral AI** (MISTRAL_API_KEY): 20 RPM, Magistral Medium, Mistral Medium-3, 10k tokens/day
✅ **Hugging Face** (HUGGING_FACE_API_KEY): 30-60 RPM, Llama 4, Mistral Small 3.2, 250k tokens/month
✅ **Together AI** (TOGETHER_AI_API_KEY): 10-30 RPM, Llama 3.3 Turbo, DeepSeek R1, 100k tokens/day
✅ **OpenRouter** (OPENROUTER_API_KEY): 10-30 RPM, Claude 4 Opus, GPT-4.5, 100k tokens/month
✅ **DeepSeek** (DEEPSEEK_API_KEY): 10-20 RPM, DeepSeek R1-0528, V3-0324, 100k tokens/day
✅ **Cohere** (COHERE_API_KEY): 10 RPM, Command R+, 1M tokens/month

### Additional Tools Available
✅ **Brave Search** (BRAVE_API_KEY): Web search capabilities
✅ **Tavily** (TAVILY_API_KEY): Research and web data
✅ **Firecrawl** (FIRECRAWL_API_KEY): Web scraping
✅ **Serper** (SERPER_API_KEY): Google search API
✅ **GitHub** (GITHUB_API_TOKEN): Repository access

### Paid Endpoints

| Provider | Models | Key Strengths | Notes |
|----------|--------|---------------|--------|
| Anthropic | Claude 4 Opus/Sonnet | Complex reasoning, safety | No free tier |
| OpenAI | GPT-4o, GPT-4 Turbo | Tool use, general intelligence | Limited free credits |
| Google | Gemini 2.5 Pro/Flash | Speed, multimodal | Generous free tier |

## Speed Performance

### Tokens Per Minute (Normalized)

- **Fastest Local**: Mistral 7B (Quantized) - 8/10
- **Fastest Free**: Gemini 1.5 Flash - 10/10
- **Fastest Paid**: Gemini 2.5 Flash - 10/10

## Recommendations by Use Case

### High-Volume, Low-Latency Tasks
1. **Local**: Mistral 7B (Quantized)
2. **Free**: Gemini 1.5 Flash
3. **Paid**: Gemini 2.5 Flash

### Complex Reasoning Tasks
1. **Local**: Grok 1.5 (Quantized)
2. **Free**: Claude 3 Haiku
3. **Paid**: Claude 4 Opus

### Tool Use and Formatting
1. **Local**: Llama 3 8B (Quantized)
2. **Free**: GPT-3.5 Turbo
3. **Paid**: GPT-4o

### Cost-Sensitive Applications
1. **Free Options**: Gemini 1.5 Flash (60 RPM), Groq (30-60 RPM)
2. **Local Fallback**: Mistral 7B for basic tasks
3. **Paid for Critical**: Claude 4 Opus for complex reasoning

## Implementation Notes

- **Rate Limits**: Always implement proper rate limiting and retries
- **Fallback Strategy**: Have local models as fallbacks for free-tier limits
- **Cost Monitoring**: Track token usage across providers
- **Performance Monitoring**: Log response quality and latency
- **Model Updates**: Benchmark new model releases regularly