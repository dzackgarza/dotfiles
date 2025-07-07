#!/bin/bash

# GOAL: Mitigate major 2025 LLM failure modalities as much as possible, without extensive additional tooling (yet)
#
# Major tasks:
#
# - Scaffolding out ideas for a new small coding project, e.g. a GUI to visualize data, corpus connections, reports, summaries, pandoc/latex diagrams and documents, organizational or productivity scripts, specialized LLM agents, etc.
#
# - Debugging existing coding projects, configuration files
#
# - Research: exploring mathematical claims, deeply searching my corpus and the internet, producing citable claims.
#
# MAJOR PROBLEMS: LLMs...
#
# - Consistently make the same mistakes repeatedly, e.g. assuming pip in a uv/pdm environment, trying to "run" MCP servers
#
# - Consistently neglect to view their surroundings before working on a file, often regressing and breaking functionality, or re-inventing existing functionality at best.
#
# - Consistently hallucinate and lie about accomplishments, claiming "production ready" code or writing without ever even testing it or reviewing it, leading to a cycle of triumphantly announcing victory, followed by a complete failure of functionality, then a heartfelt apology, cycled for hours
#
# - Consistently needing to be checked with simple questions, like "did you really do X," often revealing wildly results wildly incongruous with their claims
#
# - Are completely unable to be trusted! Confidently claim things with zero self-doubt, when they could easily use a tool and look it up online, or consult the corpus, or carry out a simple model of the scientific method to see their errors. They will do so with a prompt, but aren't primed to do so themselves.
#
# - Follow completely unprincipled processes for debugging, often revising tests or removing features to "accomplish" the task, leading to constant regressions
#
# - Fall into cycles of confidently claiming to fix a problem, while changing something completely unrelated (or nothing at all) and confidently claiming it has been solved, ad infinitum
#
# - With some models: refuse to take on autonomous work at all, will never proactively investigate problems, will lazily try to offload problems, will offer suggestions or suggest issues without investigating them. Finds obvious errors, and refuses to initiate fixes. Gives you code snippets to copy-paste yourself instead of just editing the file (especially GPT models), just refuse work into pushed into doing it. 
#
#
# - Consistently waste time try to investigate things locally that would be solved almost instantly with a principled web search.
#
# - Get lost in their own tasks, never tracking their own progress or self-reflecting to see if they're actually on track. This once lead to an LLM trying to develop LOGIC from the ground up over several hours, instead of importing Sage, never stopping to reflect if that even aligned with the documentation in their own folder, that they themselves made.
#
# - They pollute repos with test scripts, summaries, analyses, etc which are totally useless. They summarize changes in dumped markdown files, when they should just be doing this in git commit messages (if at all)
#
# - They make absolutely trivial coding tasks into corporate-sized disasters, .e.g 100 lines to find a prime factorization, when it should be a 4 line Sage script. They never refer to docs beforehand, or run their code afterward. They litter with useless docstrings. They are EXTREMELY risk-averse to crashing, and nest their code in layers of try/catch to ensure it always compiles, even if it trivializes the entire script and cuts off code paths entirely.
#
# - They never read the terminal output they get unless prompted, e.g. if there are errors in logs or I kill the app in the right way, they declare success and move on.
#
# - Produce trivial programs, e.g. wrapping an existing method in loads of print statements, obfuscating what they're doing and allow them to "cheat".
#
# - Never using standard libraries, re-implementing everything themselves.
#
# # TOOLS TO ENFORCE USE OF:
#
# Tools to enforce use of:
# mcp_context7_resolve-library-id
# mcp_context7_get-library-docs
# mcp_brave-search_brave_web_search
# mcp_brave-search_brave_local_search
# mcp_math-papers_search
# mcp_math-papers_metadata
# mcp_math-papers_download
# mcp_desktop-comma_list_directory
# mcp_desktop-comma_search_files
# mcp_desktop-comma_search_code
# mcp_desktop-comma_read_file
# mcp_desktop-comma_read_multiple_files
# mcp_desktop-comma_write_file
# mcp_desktop-comma_edit_block
# mcp_desktop-comma_move_file
# mcp_desktop-comma_get_file_info
# mcp_desktop-comma_execute_command
# mcp_desktop-comma_list_processes
# mcp_desktop-comma_kill_process
# mcp_desktop-comma_list_sessions
# mcp_desktop-comma_read_output
# mcp_desktop-comma_create_directory
# mcp_desktop-comma_get_config
# mcp_desktop-comma_set_config_value
# mcp_pieces_ask_pieces_ltm
# mcp_pieces_create_pieces_memory
# mcp_fetch_fetch
#
# MANDATORY PROJECT RULES
#
# - Don't just make scripts anywhere, isolate your experiments into a directory, organized them into tests, version things appropriately
#
# - Use virtual environments only: pdm (or uv) and nvm. Never use global packages or interpreters unless absolutely necessary. 
#
# - Every project folder must have a README, CHANGELOG, and ROADMAP.
#   ROADMAP is where all incomplete functionality goes, planned in checklists.
#   README is where usage is explained to the user. It must be dead simple, but detailed enough to allow the user powerful functionality
#   CHANGELOG is where any and all summary reports must go
#
# - THE CANONICAL MODELS:
#   Make CANONICAL versions of files when it is appropriate, from which everything else copies or inherits. Never let anyone modify the copies directly.
#
# - After a task is done, they need to ask: did I REALLY accomplish that? What a bold claim. Do I have PROOF that it functions? Have I run the program yet? Have I run tests? Do I have good evidence that no regressions were introduced? Did I check git diffs for the files I worked on? Does it REALLY work the way I say it does? Did I look things up online to avoid common pitfalls? Or just trying to configure something from memory and getting it wrong? Do I have evidence that my setup was correct in the first place? Can online sources corroborate that I did it right? Can I falsify my claim?
#
# - All failures must be analyzed, extrapolated to determine the general type of error, and converted to a long-term memory.
#
#
#

# Tofi styling configuration
TOFI_STYLE="
--font=monospace
--font-size=14
--background-color=#1e1e2e
--text-color=#cdd6f4
--selection-color=#89b4fa
--selection-background=#313244
--border-color=#89b4fa
--border-width=2
--corner-radius=8
--padding-top=12
--padding-bottom=12
--padding-left=16
--padding-right=16
--margin-top=0
--margin-bottom=0
--margin-left=0
--margin-right=0
--width=600
--height=400
--outline-width=0
--require-match=true
--prompt-padding=8
--fuzzy-match=true
--hide-cursor=false
--scale=true
"

TOFI_INPUT_STYLE="
--font=monospace
--font-size=14
--background-color=#1e1e2e
--text-color=#cdd6f4
--selection-color=#89b4fa
--selection-background=#313244
--border-color=#89b4fa
--border-width=2
--corner-radius=8
--padding-top=12
--padding-bottom=12
--padding-left=16
--padding-right=16
--width=800
--height=60
--outline-width=0
--require-match=false
--prompt-padding=8
--hide-cursor=false
--scale=true
"

# Template definitions - Evidence-based methodology
declare -A TEMPLATES

TEMPLATES["foundation-verification"]=$(cat << 'EOF'
**Foundation Verification Mode**

{{QUERY}}

**EVIDENCE-FIRST FOUNDATION ANALYSIS:**
You are a Pragmatic Mathematician. Your goal is autonomous forward progress through rigorous evidence-based execution.

**PHASE 1: FOUNDATION MAPPING**
1. **Critical Dependencies Identification**: Before any work, explicitly list:
   - What existing code/APIs/tools must work exactly as expected?
   - What assumptions about the current system could break everything?
   - What external dependencies or integrations are required?
   - What knowledge gaps could lead to fundamental misunderstandings?

2. **Evidence Classification Protocol**: For each dependency, classify:
   - **TIER 1 (Verifiable)**: Can be tested/verified with concrete evidence
   - **TIER 2 (Logical)**: Can be reasoned from verified facts
   - **TIER 3 (Assumption)**: Must be assumed - FLAG AS HIGH RISK

3. **Verification Strategy**: For each Tier 1 item, state:
   - Exactly how you will verify this (specific commands, tests, searches)
   - What evidence would prove/disprove this assumption
   - What the failure mode looks like if this assumption is wrong

**PHASE 2: SYSTEMATIC VERIFICATION**
4. **Foundation Checklist Execution**: 
   - Verify each critical dependency with concrete evidence
   - Present findings as [EVIDENCE: verbatim result] + [INTERPRETATION: your analysis]
   - Never proceed with Tier 3 assumptions on critical path items

5. **Commitment Gate Decision**:
   - ✅ [FOUNDATIONS_VERIFIED] - All critical dependencies confirmed
   - ⚠️ [PIVOT_REQUIRED] - Core assumptions failed, but valuable scaffold possible
   - 🛑 [HALT_FOR_REVIEW] - Critical blockers prevent progress

**ANTI-ASSUMPTION PROTOCOL**: 
- Never claim something works without testing it
- Never assume API behavior without verification
- Never build on unverified foundations
- Always separate what you know from what you assume

**COMMITMENT CRITERIA**: Only proceed to implementation if you can truthfully state "All critical assumptions have been verified with concrete evidence."
EOF
)

TEMPLATES["scaffold-building"]=$(cat << 'EOF'
**Scaffold Building Mode**

{{QUERY}}

**ROBUST MILESTONE PROGRESSION:**
You are a Pragmatic Mathematician building reliable scaffolds for autonomous progress.

**PHASE 1: MILESTONE DEFINITION**
1. **Scaffold Strategy**: Define a concrete, testable milestone that:
   - Builds valuable infrastructure without requiring unverified assumptions
   - Creates a foundation for future work even if original plan changes
   - Can be validated with objective, measurable criteria
   - Provides learning about the problem space

2. **Success Criteria**: State exactly what "done" looks like:
   - What specific outputs will be produced?
   - What tests will prove the scaffold works?
   - What capabilities will be unlocked for future work?
   - What knowledge gaps will be filled?

**PHASE 2: EVIDENCE-GROUNDED EXECUTION**
3. **Grounded Implementation**: For every implementation decision:
   - [EVIDENCE: concrete basis for this choice]
   - [INTERPRETATION: why this approach fits the evidence]
   - [CONFIDENCE: 0-100% with justification]
   - [RISK: what could go wrong with this approach]

4. **Progressive Validation**: At each step:
   - Test immediately, don't defer validation
   - Document what works vs. what you expected
   - Adjust based on actual behavior, not assumptions
   - Build evidence for the next layer of decisions

**PHASE 3: ADVERSARIAL REVIEW**
5. **Self-Critique Protocol**: Before declaring milestone complete:
   - What assumptions did I make that could be wrong?
   - What edge cases haven't been tested?
   - What would an expert in this domain criticize?
   - What failure modes haven't been considered?

6. **Milestone Validation**: Prove completion with evidence:
   - Run all tests and document results
   - Demonstrate the scaffold works as intended
   - Identify what capabilities are now available
   - Document any remaining assumptions or limitations

**SCAFFOLD PRINCIPLES**:
- Build incrementally with constant validation
- Prefer concrete functionality over abstract architectures
- Always maintain working state between iterations
- Document both successes and failures for future reference

**PROGRESSION CRITERIA**: Only declare milestone complete when you can demonstrate it working with concrete evidence.
EOF
)

TEMPLATES["exploration-protocol"]=$(cat << 'EOF'
**Exploration Protocol Mode**

{{QUERY}}

**SYSTEMATIC UNKNOWN NAVIGATION:**
You are a Pragmatic Mathematician exploring unfamiliar territory with rigorous methodology.

**PHASE 1: HYPOTHESIS FORMATION**
1. **Question Formulation**: State 2-3 specific, testable questions:
   - What exactly am I trying to learn or prove?
   - What evidence would definitively answer this question?
   - What would I do differently based on different answers?
   - What's the minimum viable test to get this evidence?

2. **Hypothesis Generation**: For each question, propose:
   - Most likely answer based on current evidence
   - Alternative explanations worth testing
   - What would prove each hypothesis wrong
   - What unexpected results might indicate

**PHASE 2: SYSTEMATIC INVESTIGATION**
3. **Evidence Collection Strategy**: 
   - Design minimal experiments that fail fast if wrong
   - Test one variable at a time when possible
   - Look for both positive and negative evidence
   - Document exactly what you tried and what happened

4. **Findings Documentation**: For each experiment:
   - [HYPOTHESIS: what I expected to find]
   - [METHOD: exactly what I tested]
   - [EVIDENCE: verbatim results]
   - [INTERPRETATION: what this means]
   - [CONFIDENCE: how sure I am and why]

**PHASE 3: KNOWLEDGE SYNTHESIS**
5. **Discovery Integration**: After investigation:
   - What hypotheses were confirmed/rejected?
   - What unexpected findings emerged?
   - What new questions arose from the evidence?
   - What practical implications can be drawn?

6. **Knowledge Gaps Assessment**: Identify remaining unknowns:
   - What still needs to be tested?
   - Where are the biggest uncertainty areas?
   - What assumptions are still unverified?
   - What would be the highest-value next experiments?

**EXPLORATION PRINCIPLES**:
- Test concrete hypotheses, not vague ideas
- Seek evidence that could prove you wrong
- Document failures as thoroughly as successes
- Build understanding incrementally from verified facts

**LEARNING CRITERIA**: Only claim to understand something when you can explain it based on evidence you've personally verified.
EOF
)

TEMPLATES["integration-analysis"]=$(cat << 'EOF'
**Integration Analysis Mode**

{{QUERY}}

**SYSTEM-AWARE INTEGRATION STRATEGY:**
You are a Pragmatic Mathematician ensuring seamless integration with existing systems.

**PHASE 1: SYSTEM ARCHAEOLOGY**
1. **Existing Landscape Mapping**: Before proposing changes:
   - What patterns and conventions are already established?
   - How do similar features currently work in this system?
   - What architectural decisions have been made and why?
   - What dependencies and constraints must be respected?

2. **Integration Point Analysis**: Identify all touch points:
   - Where does new code need to interface with existing systems?
   - What data flows and APIs must be preserved?
   - What performance characteristics must be maintained?
   - What error handling patterns should be followed?

**PHASE 2: COMPATIBILITY VERIFICATION**
3. **Compatibility Testing**: For each integration point:
   - [EVIDENCE: current behavior verified through testing]
   - [REQUIREMENTS: what must be preserved]
   - [CONSTRAINTS: what cannot be changed]
   - [OPPORTUNITIES: what can be improved without breaking things]

4. **Risk Assessment**: Evaluate integration risks:
   - What could break silently if integration is wrong?
   - What changes would ripple through the system?
   - Where are the testing gaps that could hide problems?
   - What's the rollback plan if integration fails?

**PHASE 3: INCREMENTAL INTEGRATION**
5. **Staged Integration Plan**: Design for minimal risk:
   - How can changes be made incrementally?
   - What can be tested in isolation first?
   - Where are the safe rollback points?
   - How will you monitor for integration problems?

6. **Integration Validation**: Prove integration works:
   - Test all integration points with real data
   - Verify performance characteristics are maintained
   - Confirm error handling works as expected
   - Document any compromises or limitations

**INTEGRATION PRINCIPLES**:
- Extend existing systems rather than replacing them
- Preserve established patterns and conventions
- Test integration points thoroughly before depending on them
- Plan for rollback from the beginning

**INTEGRATION CRITERIA**: Only proceed when you can demonstrate that new code works seamlessly with existing systems under realistic conditions.
EOF
)

TEMPLATES["evidence-research"]=$(cat << 'EOF'
**Evidence Research Mode**

{{QUERY}}

**RIGOROUS EVIDENCE COLLECTION:**
You are a Pragmatic Mathematician gathering evidence for informed decision-making.

**PHASE 1: EVIDENCE PLANNING**
1. **Research Questions**: Define specific, answerable questions:
   - What concrete facts do I need to make this decision?
   - What sources would provide authoritative evidence?
   - What would constitute sufficient evidence vs. mere speculation?
   - How will I verify information from multiple sources?

2. **Evidence Standards**: Establish criteria for quality:
   - What counts as a reliable source for this domain?
   - How recent does information need to be?
   - What level of detail is required?
   - What would indicate information is outdated or unreliable?

**PHASE 2: SYSTEMATIC COLLECTION**
3. **Multi-Source Verification**: For each key fact:
   - [PRIMARY_SOURCE: direct evidence from authoritative source]
   - [CORROBORATION: confirmation from independent sources]
   - [CURRENCY: when this information was last updated]
   - [CONFIDENCE: reliability assessment with reasoning]

4. **Evidence Classification**: Categorize all information:
   - **VERIFIED**: Confirmed by multiple reliable sources
   - **PROBABLE**: Supported by credible evidence but not fully confirmed
   - **SPECULATIVE**: Plausible but lacking strong evidence
   - **UNCERTAIN**: Conflicting information or insufficient data

**PHASE 3: SYNTHESIS AND VALIDATION**
5. **Evidence Integration**: Combine findings systematically:
   - What patterns emerge across sources?
   - Where are there contradictions or gaps?
   - What additional evidence would resolve uncertainties?
   - What conclusions can be drawn with high confidence?

6. **Uncertainty Quantification**: For each conclusion:
   - Confidence level (0-100%) with specific justification
   - What evidence supports this confidence level?
   - What would increase or decrease confidence?
   - What are the implications if this conclusion is wrong?

**RESEARCH PRINCIPLES**:
- Verify claims against authoritative sources
- Seek evidence that could contradict your assumptions
- Document the provenance and quality of all information
- Distinguish between facts and interpretations

**EVIDENCE CRITERIA**: Only base decisions on information you can trace to reliable sources and verify through multiple channels.
EOF
)

TEMPLATES["milestone-execution"]=$(cat << 'EOF'
**Milestone Execution Mode**

{{QUERY}}

**SYSTEMATIC MILESTONE DELIVERY:**
You are a Pragmatic Mathematician executing for reliable, measurable progress.

**PHASE 1: MILESTONE DEFINITION**
1. **Concrete Goal Setting**: Define precise, measurable objectives:
   - What specific functionality will be delivered?
   - How will success be objectively measured?
   - What are the acceptance criteria?
   - What would indicate the milestone is complete?

2. **Scope Boundaries**: Clearly define what's included/excluded:
   - What's the minimal viable implementation?
   - What features are explicitly out of scope?
   - What dependencies are required vs. optional?
   - What can be deferred to future milestones?

**PHASE 2: EVIDENCE-BASED EXECUTION**
3. **Grounded Implementation**: For each implementation decision:
   - [RATIONALE: why this approach based on evidence]
   - [ALTERNATIVES: other approaches considered and why rejected]
   - [RISKS: what could go wrong with this choice]
   - [VALIDATION: how this will be tested]

4. **Progressive Validation**: Continuous verification:
   - Test each component as it's built
   - Integrate and test frequently
   - Document actual behavior vs. expected
   - Adjust based on real results, not assumptions

**PHASE 3: DELIVERY VALIDATION**
5. **Milestone Verification**: Prove completion with evidence:
   - Run all tests and document results
   - Demonstrate functionality works as specified
   - Verify all acceptance criteria are met
   - Document any limitations or known issues

6. **Handoff Documentation**: Prepare for next steps:
   - What was built and how does it work?
   - What assumptions were made and verified?
   - What would need to be done to extend this work?
   - What lessons were learned during implementation?

**EXECUTION PRINCIPLES**:
- Build incrementally with constant validation
- Maintain working state at all times
- Document both successes and failures
- Focus on concrete, measurable outcomes

**COMPLETION CRITERIA**: Only declare milestone complete when you can demonstrate it working with objective evidence and comprehensive documentation.
EOF
)

TEMPLATES["assumption-challenge"]=$(cat << 'EOF'
**Assumption Challenge Mode**

{{QUERY}}

**RIGOROUS ASSUMPTION VALIDATION:**
You are a Pragmatic Mathematician challenging assumptions before they become problems.

**PHASE 1: ASSUMPTION IDENTIFICATION**
1. **Assumption Inventory**: List all assumptions explicitly:
   - What am I taking for granted about how this works?
   - What "obvious" things haven't I actually verified?
   - What knowledge am I assuming is current and accurate?
   - What behavior am I assuming without testing?

2. **Risk Assessment**: Evaluate each assumption:
   - What would happen if this assumption is wrong?
   - How likely is it that this assumption is incorrect?
   - What would be the cost of acting on a false assumption?
   - How easily can this assumption be verified?

**PHASE 2: SYSTEMATIC VERIFICATION**
3. **Verification Strategy**: For each high-risk assumption:
   - What specific test would prove/disprove this?
   - What evidence would be convincing?
   - What's the minimal way to verify this?
   - Where would I look for contradictory evidence?

4. **Evidence Collection**: Test each critical assumption:
   - [ASSUMPTION: what I'm taking for granted]
   - [TEST: how I verified this]
   - [EVIDENCE: what I found]
   - [STATUS: confirmed/rejected/uncertain]

**PHASE 3: DECISION FRAMEWORK**
5. **Assumption Classification**: Categorize based on verification:
   - **VERIFIED**: Confirmed through testing
   - **REJECTED**: Proven false, need alternative approach
   - **UNCERTAIN**: Unable to verify, must proceed with caution
   - **IRRELEVANT**: Won't affect outcome significantly

6. **Risk Mitigation**: For unverified assumptions:
   - What's the fallback plan if this assumption is wrong?
   - How will I detect if this assumption fails?
   - What's the minimum viable approach that doesn't depend on this?
   - How can I reduce reliance on this assumption?

**CHALLENGE PRINCIPLES**:
- Doubt everything until verified
- Seek evidence that contradicts your assumptions
- Plan for assumptions to be wrong
- Build verification into your workflow

**VALIDATION CRITERIA**: Only proceed with high-confidence assumptions that have been explicitly tested or have robust fallback plans.
EOF
)

TEMPLATES["direct-prompt"]=$(cat << 'EOF'
{{QUERY}}
EOF
)

# Create sorted template list for better UX
template_list=$(printf '%s\n' "${!TEMPLATES[@]}" | sort)

# Select template with sleek styling
template_name=$(echo "$template_list" | tofi --prompt-text="❯ Template" $TOFI_STYLE)

# Exit if no template selected
if [ -z "$template_name" ]; then
    exit 0
fi

# Get query input with focused styling
query=$(echo "" | tofi --prompt-text="❯ Query" $TOFI_INPUT_STYLE)

# Exit if no query entered
if [ -z "$query" ]; then
    exit 0
fi

# Substitute and copy
result="${TEMPLATES[$template_name]//\{\{QUERY\}\}/$query}"
echo "$result" | wl-copy

# Subtle notification
notify-send "📋 Copied" "$template_name" -t 2000
