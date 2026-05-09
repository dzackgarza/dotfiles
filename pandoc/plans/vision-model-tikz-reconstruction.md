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

### Reference Diagrams

#### Test 1: Simple Commutative Diagram (TRIVIAL - OCR test only)
- Location: `/home/dzack/dotfiles/pandoc/plans/test-diagram.{tex,pdf,png}`
- Result: Too trivial, any OCR system passes

#### Test 2: Complex Graph Diagram (NONTRIVIAL)
- Location: `/home/dzack/dotfiles/pandoc/plans/complex-test-diagram.{tex,pdf,png}`
- Content:
  - 5 nodes with different shapes: circle (A, D), rectangle (B), diamond (C), pentagon (E)
  - Different fill colors: gray, blue, red, yellow, green
  - Various arrow styles: solid, dashed, double (ψ), curved (h from A→D), decorated/snake (φ)
  - Self-loop on D labeled "id"
  - Shaded background region (triangle A-B-D)
  - Multiple bend angles and curvatures

### API Status Check
- **OPENROUTER_API_KEY**: ❌ INSUFFICIENT CREDITS (Error 402)
  - Message: "Insufficient credits. Add more using https://openrouter.ai/settings/credits"
  - **ACTION NEEDED**: Add ~$1 credit to test FREE models (cost per test: <$0.001)

### Free/Cheap 2026 SOTA Vision Models on OpenRouter
1. qwen/qwen3-vl-235b-a22b-thinking - 235B with thinking ($0.00000026/1M)
2. qwen/qwen3-vl-235b-a22b-instruct - 235B base ($0.0000002/1M)
3. google/gemini-3.1-flash-lite - Gemini 3.x ($0.00000025/1M)
4. qwen/qwen3-vl-32b-instruct - 32B mid-size ($0.000000104/1M)
5. qwen/qwen3-vl-8b-instruct - 8B small ($0.00000008/1M)
6. meta-llama/llama-3.2-11b-vision-instruct - Meta ($0.000000245/1M)

### Model Test Results
(Format: Model | Description Quality | Reconstruction Accuracy | Notes)

1. **nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free** ✅
   - Quality: Excellent - captured 2x3 grid, all LaTeX labels, arrow directions, commutativity
   - Reconstruction: High confidence - very precise positioning and labeling
   - Response: Clean, structured, complete

2. **nvidia/nemotron-nano-12b-v2-vl:free** ✅
   - Quality: Good - captured all elements but verbose
   - Reconstruction: Medium-high - all info present but less structured
   - Response: Very detailed but harder to parse

3. **google/gemma-4-31b-it:free** ❌
   - Error: "Provider returned error" - model unavailable

4. **google/gemma-4-26b-a4b-it:free** ❌
   - Error: "Provider returned error" - model unavailable

---

## Notes
- Avoid usage-based APIs: Codex, Claude direct, Opencode, Gemini direct
- Focus on SOTA 2026 models
- Test via curl for direct API access
