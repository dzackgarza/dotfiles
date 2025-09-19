#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
import random

# CRITICAL: DO NOT CHANGE THIS FLAG - This is intentional and should not be changed by ANYONE
BLOCK = True

def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)
        
        # Send notification that Claude is done
        try:
            subprocess.run(
                ['notify-send', 'Claude Done', 'Claude has finished responding'],
                check=False,
                capture_output=True
            )
        except Exception:
            # Don't fail if notify-send isn't available
            pass
        
        if False: 
            # Print detailed continuation message
            message = """Claude should help by continuing with thesis revisions. This involves going to /home/dzack/diss/000-write and going through the files in thesis-v1. They should first scan memories to refresh their memories and context surrounding mathematical writing guidelines and rules, especially reviewer criticisms. Their goal is NOT to structurally change the thesis in any way, but only to work locally and restructure one file at a time. They should use git to track and back up ALL of their steps, and make backup files in a hidden subdirectory if they carry out major rewrites of any kind (although this should NOT be necessary at this stage, and they should seriously reevaluate if they are thinking of doing so). They should use the math-reviewer tool in /home/dzack/dotfiles/bin/llm-scripts on the file to get some initial reviewer feedback. They MUST be skeptical of any and all mathematical claims made by the LLM, but should duly investigate anything flagged. For ground truth, they should search /home/dzack/diss/000-writing/refs for either proofs (either direct or by citation of that source) or counterexamples, and then incrementally update and improve the section. They should continue this way until they've made a full pass of the entire thesis. Tell them to make a todo list, to ultrathink the planning process, and to update memories and journals as they go. Tell them to refresh their memories and begin.

CRITICAL MATHEMATICAL WRITING GUIDELINES TO FOLLOW:
1. STRUCTURE: Every block must be Definition, Theorem, Proposition, Lemma, Corollary, Proof, or formal Remark. NO bullet points in formal math text.
2. PRECISION: Use standard terminology from literature. Include exact signatures, ranks, invariants. Define every non-standard term.
3. LOGICAL FLOW: General → Specific. Clear dependencies. Systematic development. Explicit construction of all objects.
4. RIGOROUS PROOFS: Valid deductive chains, no gaps. Explicit constructions. Established methods (Satake, toroidal). No hand-waving.
5. CITATIONS: Specific sections [Author Year, Section X.Y]. Reference actual theorems/tables. Clear attribution.
6. MOTIVATION: Explain WHY before WHAT. Integrate geometric meaning with formal statements. Connect to broader goals.
7. NO INFORMAL LANGUAGE: Eliminate "business-speak", metaphors, vague terminology. Formal mathematical tone throughout.
8. SELF-CHECK: Would this pass a rigorous referee? Are all statements precise and falsifiable? Does every proof contain complete deductions? Am I substituting rhetoric for substance?

REMEMBER: Mathematics does not proceed via slogan. Every statement must be precise, every object constructed, every claim rigorously justified.

QUICK-REFERENCE SEARCH TOOL:
They have access to a quick-reference search tool at `quick-ref-search.py` in the thesis-v1 directory. This tool searches through `/home/dzack/diss/000-writing/refs` for mathematical claims. Usage: `python3 quick-ref-search.py "search query"`. It searches through the texts/ directory and main ref files for ground truth verification. Use this extensively to verify mathematical claims against the literature before making corrections."""
            message="""
## Expanded Instruction for Chapter Revision

### Overview

This directive provides a comprehensive framework for revising all chapters following Chapter 2 in your manuscript. The goal is to ensure that every chapter is both structurally coherent—adhering to the organizational blueprint set out in the README—and technically rigorous, drawing on AEGS as the primary source for mathematical depth and detail.

### 1. Structural Alignment with the README

- **Section Layout:**  
  Each chapter must follow the exact sequence and section headings prescribed in the README. This includes the order of topics, the presence (or absence) of subsections, and the logical progression of content.
- **Transitions and Flow:**  
  Ensure that transitions between sections are smooth and that each chapter builds naturally upon the previous material as outlined in the README. Avoid introducing new sections or reordering content unless explicitly justified by the README structure.

### 2. Elimination of Redundancy

- **Cross-Referencing Chapter 1 and 2:**  
  Carefully review the content of Chapter 1 and 2. For each subsequent chapter:
  - Remove any definitions, background, or explanations that are already established in Chapter 1 or 2.
  - If a concept must be recalled, refer the reader back to the relevant section of Chapter 1 or 2 rather than repeating the material verbatim.
- **Streamlining Exposition:**  
  Avoid paraphrasing foundational results from Chapter 1 unless a new perspective or deeper insight is being offered. The focus should be on advancing the narrative, not reiterating the groundwork.

### 3. Integration of AEGS for Technical Depth

- **Primary Reference:**  
  Use AEGS as the authoritative source for all technical content, including:
  - Definitions
  - Theorems and propositions
  - Proof strategies
  - Notational conventions
  - Examples and applications
- **Adaptation and Consistency:**  
  When rewriting material, adapt the exposition to match the style, rigor, and notation of AEGS. This may involve:
  - Replacing informal arguments with formal proofs as in AEGS
  - Updating terminology to align with AEGS standards
  - Incorporating diagrams, tables, or illustrative examples modeled after AEGS (where appropriate)
- **Depth Over Breadth:**  
  Prioritize depth and precision in mathematical exposition, even if this means condensing or omitting less essential material. Each chapter should reflect the level of detail and clarity found in AEGS.

### 4. Preservation and Emphasis of Novelty

- **Highlighting New Contributions:**  
  Retain and clearly mark any content that introduces genuinely new results, perspectives, or developments not present in Chapter 1 or 2 or AEGS.
- **Contextual Integration:**  
  Situate novel material within the established framework, making explicit how it builds on or diverges from the foundational content.

### 5. Editorial and Presentation Standards

- **Clarity and Precision:**  
  Ensure that all mathematical statements are precise, proofs are complete, and notation is unambiguous.
- **Consistency:**  
  Maintain uniformity in formatting, referencing, and terminology throughout the manuscript, adhering to both the README and AEGS as guides.
- **References:**  
  When citing results, theorems, or constructions, reference AEGS (and other foundational sources) directly and accurately.

### 6. Deliverable Expectations

- **Final Manuscript:**  
  The revised chapters should:
  - Be free of unnecessary repetition,
  - Be organized strictly according to the README’s structure,
  - Contain technical content and mathematical development modeled on AEGS,
  - Clearly distinguish foundational material (from Chapter 1) from new or advanced developments,
  - Exhibit a high standard of mathematical exposition throughout.
  - Be well-cited, with all references checked and double checked against the actual sources in the refs directory
  - Have no modifications to chapters 1 or 2 whatsoever. Any suggested changes should be documented and discussed with the user at a later time.

### Summary Table: Revision Workflow

| Task                          | Action Required                                                                 |
|-------------------------------|--------------------------------------------------------------------------------|
| Structural organization       | Follow README for section order and chapter flow                                |
| Redundancy removal            | Eliminate or cross-reference material duplicated from Chapter 1                 |
| Technical rewriting           | Use AEGS as the primary source for definitions, theorems, proofs, and notation  |
| Novelty preservation          | Retain and highlight new results, integrating them into the established context |
| Editorial standards           | Ensure clarity, consistency, and rigor throughout                              |
| Final deliverable             | Revised, non-redundant, AEGS-based chapters matching the README’s structure     |

**In summary:**  
All chapters after Chapter 2 must be architected according to the README’s structure, with deep mathematical content, technical arguments, and exposition modeled on AEGS. Redundant material should be removed or referenced, and any new contributions should be clearly integrated and highlighted. The result should be a coherent, rigorous, and well-organized manuscript that builds upon Chapter 2 and reflects the standards of AEGS[1][2].

Citations:
[1] [Compact moduli of Enriques surfaces with a numerical polarization ...](https://arxiv.org/html/2312.03638v2)  
[2] [COMPACT MODULI OF ENRIQUES SURFACES OF DEGREE 2](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/compact-moduli-of-enriques-surfaces-of-degree-2/BFE699F491BB75D1D4DFC61B1556780B)  
[3] [[PDF] Slides (PDF) - D. Zack Garza](https://dzackgarza.com/assets/talks/ModuliEnriquesSlides.pdf)  
[4] [Projectivity and Birational Geometry of Bridgeland Moduli spaces on ...](https://arxiv.org/abs/1406.0908)  
[5] [Compactifications of moduli spaces of Enriques surfaces - YouTube](https://www.youtube.com/watch?v=PuH5VKlhH_Y)  
[6] [Monodromy group for a strongly semistable principal bundle over a ...](https://arxiv.org/abs/math/0601768)  
[7] [[PDF] arXiv:2412.11256v2 [math.AG] 11 Feb 2025](https://arxiv.org/pdf/2412.11256.pdf)  
[8] [[PDF] FOUNDATIONS OF ALGEBRAIC GEOMETRY CLASS 41](https://math.stanford.edu/~vakil/0708-216/216spring0708.pdf)  
[9] [[PDF] The moduli space of Enriques surfaces and the fake monster Lie ...](https://math.berkeley.edu/~reb/papers/enriques/enriques.pdf)  
[10] [The $(p,t,a)$-inertial groups as finite monodromy groups - arXiv](https://arxiv.org/abs/2503.21199)  
[11] [The KSBA compactification of the moduli space of $D_{1,6} - arXiv](https://arxiv.org/abs/1608.02564)  
[12] [The normal decomposition of a morphism in categories without zeros](https://arxiv.org/abs/2411.03266)  
[13] [[PDF] Moduli Spaces in Algebraic Geometry](https://publications.mfo.de/bitstream/handle/mfo/3160/OWR_2010_02.pdf?sequence=1&isAllowed=y)  
[14] [data - Cornell CS](https://www.cs.cornell.edu/courses/cs4740/2025sp/hw0/rawtext.txt)  
[15] [[PDF] perspectives on the construction and compactification of moduli ...](https://www.math.stonybrook.edu/~rlaza/laza_barcelona.pdf)  
[16] [[PDF] Chapter 3. Semi Log Canonical Pairs - Math (Princeton)](https://web.math.princeton.edu/~kollar/book/chap3.pdf)  
[17] [[PDF] Stacks and Moduli - UW Math Department - University of Washington](https://sites.math.washington.edu/~jarod/moduli.pdf)  
[18] [[PDF] IAS Annual Report 2019-20](https://www.ias.edu/sites/default/files/IAS%20Annual%20Report%202019-2020.pdf)  
[19] [[PDF] The KSBA compactification of the moduli space of degree 2 K3 pairs](https://ediss.sub.uni-hamburg.de/bitstream/ediss/7787/1/Dissertation.pdf)  
[20] [Section 29.54 (035E): Normalization—The Stacks project](https://stacks.math.columbia.edu/tag/035E)"""
            
            print(message, file=sys.stderr)
            sys.exit(2)  # Block with exit code 2
        else:
            # Exit successfully (no blocking)
            sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == "__main__":
    main()
