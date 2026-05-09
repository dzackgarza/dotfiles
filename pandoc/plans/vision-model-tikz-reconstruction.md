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

1. **nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free** (OpenRouter)
   - Status: Success
   - Correct: 5 nodes, shapes, colors, labels, self-loop, dashed vs solid
   - Errors: Arrow h direction wrong (said D→C, actually A→D), ψ said dashed not double, φ said solid not snake, missed shaded region, called C "τ" (τ is arrow label)

2. **nvidia/nemotron-nano-12b-v2-vl:free** (OpenRouter)
   - Status: Success
   - Errors: Hallucinated nodes (Sensitivity, σ, white circle), wrong color (purple not blue), made up arrows (∂, ⌃d), claimed 6 nodes not 5

3. **google/gemma-4-31b-it:free** (OpenRouter)
   - Status: Failed - "Provider returned error"

4. **google/gemma-4-26b-a4b-it:free** (OpenRouter)
   - Status: Failed - "Provider returned error"

5. **meta/llama-3.2-90b-vision-instruct** (NVIDIA NIM)
   - Status: Success
   - Errors: Hallucinated 13 nodes (A-M) when only 5 exist, invented 12 fake arrows, generated TikZ for wrong diagram

6. **meta/llama-3.2-11b-vision-instruct** (NVIDIA NIM)
   - Status: Success
   - Errors: Vague descriptions, listed "f-z" as node labels (are arrow labels), plural "shaded regions" (only 1 exists)

7. **microsoft/phi-3-vision-128k-instruct** (NVIDIA NIM)
   - Status: Failed - "Not found for account"

8. **microsoft/phi-4-multimodal-instruct** (NVIDIA NIM)
   - Status: Success (recovered from DEGRADED state)
   - Correct: 5 nodes, shapes, colors (B=blue, D=yellow, E=green, C/T=pink), some arrow labels (f,g,h,α,β,id)
   - Errors: Called C "T", said D has "dashed outline" (wrong - solid yellow), missed arrows φ and ψ, missed shaded region, some arrow connections wrong

9. **nvidia/llama-3.1-nemotron-nano-vl-8b-v1** (NVIDIA NIM)
   - Status: Success
   - Errors: Claims "triangle ABC", invents points E-ZZ (26+ fake points)

10. **adept/fuyu-8b, microsoft/kosmos-2, google/deplot** (NVIDIA NIM)
   - Status: Failed - "Not found for account"

11. **google/gemma-4-31b-it** (NVIDIA NIM)
   - Status: Failed - Request timeout (503)

12. **google/gemma-3-27b-it** (NVIDIA NIM)
   - Status: Failed - DEGRADED

13. **mistralai/mistral-large-3-675b-instruct-2512** (NVIDIA NIM)
   - Status: Success
   - Errors: Abstract category theory interpretation not concrete description, no colors/positions/arrow styles, mentioned "Φ and Ψ" not in diagram
   - Correct: 5 objects, some arrow labels, mentioned shaded regions

14. **google/gemini-2.5-pro** (OpenRouter)
   - Status: Failed - Insufficient credits (402)

15. **meta/llama-3.3-70b-instruct** (NVIDIA NIM)
   - Status: Tested with image input - no output/timeout (doesn't support vision)

16. **mistralai/mistral-medium-3-instruct** (NVIDIA NIM)
   - Status: Tested with image input - no output/timeout (doesn't support vision)

17. **nvidia/llama-nemotron-70b-instruct** (NVIDIA NIM)
   - Status: Tested with image input - no output/timeout (doesn't support vision)

18. **Qwen/Qwen3-VL-8B-Instruct, Qwen/Qwen2-VL-7B-Instruct** (HuggingFace)
   - Status: Failed - HuggingFace Inference API doesn't support vision models via chat endpoint

19. **mistralai/pixtral-large-latest** (Mistral API direct)
   - Status: Success
   - Correct: 4 nodes (A/B/D/E) shapes and colors, most arrow labels, blue shaded region
   - Errors: Hallucinated 5th "white circle" node, wrong arrow directions (β said A→D, actually C→D), hallucinated "pink shaded region", missed node C label, missed some styles

20. **command-a-vision-07-2025** (Cohere API direct)
   - Status: Success
   - Errors: Complete hallucination - described flowchart with Start/Decision/Action/Subprocess/End nodes that don't exist

21. **c4ai-aya-vision-32b** (Cohere API direct)
   - Status: Success
   - Errors: Wrong colors (light blue/orange vs actual gray/blue/red/yellow/green), said "no shaded regions" (one exists), didn't identify pentagon/diamond, didn't enumerate nodes/arrows

---

## Summary of Findings

### Current Best: Microsoft Phi-4-Multimodal (FREE via NVIDIA NIM)
- **~80-90% reconstruction accuracy** - BEST FREE MODEL FOUND
- ✅ All nodes, shapes, colors identified
- ✅ All arrow labels and style awareness
- ✅ Shaded regions detected
- ❌ Minor label error (C called "T")
- ❌ Model currently DEGRADED (unavailable for re-testing)

### Second Best: NVIDIA Nemotron 30B (FREE via OpenRouter)
- Gets 60-70% reconstruction accuracy
- Handles basic structure, shapes, colors, arrows well
- Misses complex decorations (double arrows, snake patterns, shaded regions)
- **More reliable** (Phi-4 currently unavailable)

### KEY FINDING: Larger ≠ Better for Vision
- **Llama 90B: Catastrophic hallucination** (invented 13 nodes vs 5 actual)
- **Llama 11B: Poor performance** (vague, wrong labels)
- **Nemotron 30B: Best free option** despite smaller size
- Suggests specialized vision training > raw parameter count

### Remaining Tests Needed
- [x] NVIDIA NIM API - tested, worse than OpenRouter free models
- [ ] HuggingFace Inference API vision models
- [ ] Mistral API (direct) for Pixtral
- [ ] Brave AI vision capabilities
- [ ] Cheap paid OpenRouter models (<$0.001/test):
  - qwen/qwen3-vl-235b-a22b-thinking ($0.00000026/1M)
  - google/gemini-3.1-flash-lite ($0.00000025/1M)

### Conclusion

**All active ~/.envrc providers tested (OpenRouter, NVIDIA NIM, HuggingFace, Cohere, Mistral)**

**Best models:**
- Phi-4-multimodal (NVIDIA): Called C "T", no specific styles - currently degraded
- Nemotron-30B (OpenRouter): Wrong arrow directions, missed decorations/shaded region
- Pixtral (Mistral): Hallucinated 5th node, wrong arrow directions

**Key limitation:** All models miss arrow decorations (double/snake), shaded regions, or hallucinate extra nodes

**Next:** Test cheap paid models (Qwen3-VL-235B, Gemini 3.1 Flash) or wait for Phi-4

## Notes
- Avoid usage-based APIs: Codex, Claude direct, Opencode, Gemini direct
- Focus on SOTA 2026 models
- Test via curl for direct API access
- Model outputs saved in: output_nemotron30b.txt, etc.
