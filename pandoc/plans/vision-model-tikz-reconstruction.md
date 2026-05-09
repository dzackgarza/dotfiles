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

### Model Test Results: Complex Diagram

1. **nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free** ✅ BEST FREE MODEL
   - **Correctly Identified:**
     - All 5 node shapes (circle, square, diamond, pentagon)
     - All node colors (gray, blue, red, yellow, green)
     - All node labels (A, B, C, D, E)
     - Self-loop on D with "id" label
     - Dashed vs solid arrow distinction (β, ψ dashed)
     - Most arrow directions and labels (f, g, φ, α, β, h, ψ, id)

   - **MISSED/INCORRECT:**
     - Curved arrow "h" (A→D with bend) - thought h was D→C
     - Double arrow styling on ψ (E→C)
     - Snake/decorated arrow on φ (A→E)
     - Shaded background region (triangle A-B-D)
     - Bend angles and specific curvatures
     - Label "τ" location (thought it was node label, not arrow label)

   - **Reconstruction Potential:** 60-70% - would get basic structure but miss decorations
   - **Response Quality:** Clean, structured, includes reasoning trace (1734 reasoning tokens)

2. **nvidia/nemotron-nano-12b-v2-vl:free** ❌ POOR
   - **Problems:**
     - Hallucinated nodes ("Sensitivity", "σ", white circle τ)
     - Wrong colors (purple instead of blue)
     - Made up arrows (∂, ⌃d) that don't exist
     - Confused about arrow count (listed 6 nodes instead of 5)
     - Incoherent arrow descriptions

   - **Reconstruction Potential:** <20% - too many errors
   - **Response Quality:** Verbose, confused, unreliable

3. **google/gemma-4-31b-it:free** ❌
   - Error: "Provider returned error" - model unavailable

4. **google/gemma-4-26b-a4b-it:free** ❌
   - Error: "Provider returned error" - model unavailable

---

## Summary of Findings

### Current Best: NVIDIA Nemotron 30B (FREE)
- Gets 60-70% reconstruction accuracy
- Handles basic structure, shapes, colors, arrows well
- Misses complex decorations (double arrows, snake patterns, shaded regions)
- Good enough for simple-to-moderate diagrams
- NOT good enough for complex TikZ with decorations

### Remaining Tests Needed
- [ ] Test cheap paid models on OpenRouter (<$0.001/test):
  - qwen/qwen3-vl-235b-a22b-thinking ($0.00000026/1M)
  - google/gemini-3.1-flash-lite ($0.00000025/1M)
  - qwen/qwen3-vl-32b-instruct ($0.000000104/1M)
- [ ] Test direct API providers:
  - NVIDIA NIM API (check available vision models)
  - HuggingFace vision models
  - Mistral Pixtral via direct API
- [ ] Create more test diagrams:
  - Spectral sequence with diagonal differentials
  - Dynkin diagram with edge multiplicities
  - Diagram with filled regions and patterns

### Conclusion So Far
Free models insufficient for precise TikZ reconstruction of complex diagrams.
Need to test cheap paid models or improve prompting strategy.

## Notes
- Avoid usage-based APIs: Codex, Claude direct, Opencode, Gemini direct
- Focus on SOTA 2026 models
- Test via curl for direct API access
- Model outputs saved in: output_nemotron30b.txt, etc.
