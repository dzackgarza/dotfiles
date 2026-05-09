# Vision Model Test Log

## Test Setup
- **Diagram:** complex-test-diagram.tex → complex-test-diagram.png
- **Ground Truth:** 5 nodes (A/gray-circle, B/blue-rect, C/red-diamond, D/yellow-circle, E/green-pentagon), 8 arrows (f, g, h, α, β, φ, ψ, id), 1 shaded region (triangle A-B-D)
- **Prompt:** "Describe this diagram precisely for TikZ reconstruction: node shapes, colors, labels, arrow styles, shaded regions."

## Test Results

### 1. nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free (OpenRouter)
- **Status:** Success
- **Errors:**
  - Called node C "τ" (τ is arrow label B→E, not node)
  - Arrow h: claimed D→C, actually A→D (curved dashed)
  - Arrow ψ: said "dashed", actually double arrow
  - Arrow φ: said "solid", actually snake-decorated
  - Missed shaded background region entirely
  - No mention of bend angles or curvature

### 2. nvidia/nemotron-nano-12b-v2-vl:free (OpenRouter)
- **Status:** Success but poor quality
- **Errors:**
  - Hallucinated extra nodes ("Sensitivity", "σ", white circle)
  - Claimed 6 nodes instead of 5
  - Invented arrows that don't exist (∂, ⌃d)
  - Wrong color: "purple" instead of blue for B
  - Verbose, incoherent descriptions

### 3. meta/llama-3.2-90b-vision-instruct (NVIDIA NIM)
- **Status:** Success but catastrophic hallucination
- **Errors:**
  - Claimed 13 nodes (A through M) when only 5 exist
  - Invented nodes F, G, H, I, J, K, L, M completely
  - Invented 12 arrows with Greek letters
  - Generated plausible TikZ code for WRONG diagram
  - Total fabrication

### 4. meta/llama-3.2-11b-vision-instruct (NVIDIA NIM)
- **Status:** Success but vague
- **Errors:**
  - Listed labels "f" through "z" (these are arrow labels, not node labels)
  - Said "shaded regions" plural (only one exists)
  - Generic descriptions: "flowchart or network diagram"
  - No specific node/arrow enumeration

### 5. microsoft/phi-4-multimodal-instruct (NVIDIA NIM)
- **Status:** Success - BEST RESULT
- **Errors:**
  - Called node C "T" (wrong label)
  - Did not enumerate specific arrow styles (mentioned awareness but no details)
  - No specific positions or bend angles
- **Correct:**
  - Identified all 5 nodes
  - All shapes correct
  - Color D=yellow identified
  - All arrow labels (f, g, h, α, β, id)
  - Mentioned all arrow style types (solid/dashed/double/curved/snake)
  - Mentioned shaded regions
- **Note:** Model now DEGRADED, cannot re-test

### 6. nvidia/llama-3.1-nemotron-nano-vl-8b-v1 (NVIDIA NIM)
- **Status:** Success but catastrophic
- **Errors:**
  - Claimed diagram is "triangle ABC"
  - Invented points E through ZZ (26+ fake points)
  - Complete hallucination worse than 90B model

### 7. microsoft/phi-3-vision-128k-instruct (NVIDIA NIM)
- **Status:** Failed
- **Error:** "Not found for account" (404)

### 8. adept/fuyu-8b (NVIDIA NIM)
- **Status:** Failed
- **Error:** "Not found for account" (404)

### 9. microsoft/kosmos-2 (NVIDIA NIM)
- **Status:** Failed
- **Error:** "Not found for account" (404)

### 10. google/gemma-4-31b-it (NVIDIA NIM)
- **Status:** Failed
- **Error:** Request timeout (503)

### 11. google/deplot (NVIDIA NIM)
- **Status:** Failed
- **Error:** "Not found for account" (404)

### 12. google/gemma-3-27b-it (NVIDIA NIM)
- **Status:** Failed
- **Error:** DEGRADED function cannot be invoked

### 13. mistralai/mistral-large-3-675b-instruct-2512 (NVIDIA NIM)
- **Status:** Success
- **Errors:**
  - Did not enumerate nodes/arrows individually
  - Gave abstract category theory interpretation instead of concrete description
  - No colors, positions, or specific arrow styles mentioned
  - Said "implicitly C" and "diamond shape" but didn't list as explicit node
  - Mentioned "Φ and Ψ" transforms not in diagram
- **Correct:**
  - Identified 5 objects (A, B, D, E, C)
  - Some arrow labels (f, g, h, α, τ, β, id)
  - Mentioned shaded regions (blue and pink)
  - Understood commutative diagram concept

### 14. Qwen3-VL / HuggingFace models
- **Status:** Not tested
- **Reason:** HuggingFace Inference API free tier doesn't support vision models via chat endpoint

## Summary
- **Working models:** 6/13
- **Usable results:** 2/13 (Phi-4, Nemotron-30B)
- **Best:** Phi-4-multimodal (currently unavailable)
- **Best available:** Nemotron-30B (OpenRouter)
- **Common failures:** Hallucination (3 models), not found/degraded (6 models), abstract descriptions (1 model)
