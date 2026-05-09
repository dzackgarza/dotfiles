# Vision Model Testing: TikZ Diagram Reconstruction

## Objective
Find SOTA 2026 vision model that can accurately describe mathematical diagrams for precise TikZ reconstruction.

## Test Methodology
1. Generate reference TikZ diagram (mathematical)
2. Render to PNG/SVG
3. Send to vision models with prompt: "Describe this mathematical diagram in precise detail, including all labels, arrows, positions, and mathematical notation. The description should be detailed enough to reconstruct this diagram in TikZ."
4. Attempt to reconstruct from description
5. Compare reconstruction quality

## Available API Providers (from ~/.envrc)
- [x] OPENROUTER_API_KEY - OpenRouter (aggregator, many SOTA models)
- [ ] NVIDIA_API_KEY / NVIDIA_NIM_API_KEY - NVIDIA NIM
- [ ] BRAVE_FREE_AI_API_KEY - Brave AI
- [ ] HF_TOKEN - HuggingFace Inference API
- [ ] CO_API_KEY - Cohere
- [ ] MISTRAL_API_KEY - Mistral
- [ ] GOOGLE_GENERATIVE_AI_API_KEY - Google AI (but avoid usage-based)

## Models to Test

### OpenRouter (Primary Testing)
- [ ] GPT-4o (OpenAI) - strong vision
- [ ] GPT-4o-mini (OpenAI) - cheaper alternative
- [ ] Gemini 2.0 Flash Thinking (Google) - SOTA 2026
- [ ] Gemini 1.5 Pro (Google) - strong vision
- [ ] Claude 3.5 Sonnet (Anthropic) - excellent vision
- [ ] Claude 3 Opus (Anthropic) - previous SOTA
- [ ] Llama 3.2 Vision (Meta) - open source
- [ ] Qwen2-VL (Alibaba) - strong open model
- [ ] Pixtral (Mistral) - multimodal

### NVIDIA NIM
- [ ] Check available vision models

### Other Providers
- [ ] Brave AI vision capabilities
- [ ] HuggingFace vision models
- [ ] Cohere vision (if available)

## Test Results

### Reference Diagram
- Location: TBD
- Description: TBD

### Model Test Results
(Format: Model | API Key Status | Description Quality | Reconstruction Accuracy | Notes)

---

## Notes
- Avoid usage-based APIs: Codex, Claude direct, Opencode, Gemini direct
- Focus on SOTA 2026 models
- Test via curl for direct API access
