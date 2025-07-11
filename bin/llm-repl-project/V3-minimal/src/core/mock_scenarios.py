"""
Mock Scenario Generator

Creates realistic mock scenarios for testing and demonstrating
the live block system with various conversation types and complexities.
"""

import asyncio
import random
from typing import List, Dict, Any, Optional

from .live_blocks import LiveBlock, LiveBlockManager


class MockScenarioGenerator:
    """Generates realistic mock scenarios for different conversation types."""

    def __init__(self, live_manager: LiveBlockManager):
        self.live_manager = live_manager
        self.scenario_catalog = self._build_scenario_catalog()

    def _build_scenario_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Build catalog of available scenarios."""
        return {
            "coding_session": {
                "description": "Complete coding session with multiple steps",
                "complexity": "high",
                "duration": "medium",
                "blocks": ["user", "cognition", "assistant", "tool", "assistant"],
            },
            "debugging_session": {
                "description": "Debugging workflow with error analysis",
                "complexity": "high",
                "duration": "long",
                "blocks": ["user", "cognition", "tool", "cognition", "assistant"],
            },
            "research_query": {
                "description": "Research and information gathering",
                "complexity": "medium",
                "duration": "medium",
                "blocks": ["user", "cognition", "tool", "assistant"],
            },
            "quick_question": {
                "description": "Simple question and answer",
                "complexity": "low",
                "duration": "short",
                "blocks": ["user", "cognition", "assistant"],
            },
            "complex_analysis": {
                "description": "Multi-step analysis with tools",
                "complexity": "very_high",
                "duration": "very_long",
                "blocks": [
                    "user",
                    "cognition",
                    "tool",
                    "cognition",
                    "tool",
                    "cognition",
                    "assistant",
                ],
            },
            "collaborative_coding": {
                "description": "Back-and-forth coding collaboration",
                "complexity": "high",
                "duration": "long",
                "blocks": [
                    "user",
                    "cognition",
                    "assistant",
                    "user",
                    "cognition",
                    "tool",
                    "assistant",
                ],
            },
        }

    async def generate_scenario(
        self, scenario_type: str, custom_params: Optional[Dict[str, Any]] = None
    ) -> List[LiveBlock]:
        """Generate a complete mock scenario."""
        if scenario_type not in self.scenario_catalog:
            raise ValueError(f"Unknown scenario type: {scenario_type}")

        scenario_config = self.scenario_catalog[scenario_type]
        params = custom_params or {}

        # Generate scenario based on type
        if scenario_type == "coding_session":
            return await self._generate_coding_session(params)
        elif scenario_type == "debugging_session":
            return await self._generate_debugging_session(params)
        elif scenario_type == "research_query":
            return await self._generate_research_query(params)
        elif scenario_type == "quick_question":
            return await self._generate_quick_question(params)
        elif scenario_type == "complex_analysis":
            return await self._generate_complex_analysis(params)
        elif scenario_type == "collaborative_coding":
            return await self._generate_collaborative_coding(params)
        else:
            return await self._generate_generic_scenario(scenario_config, params)

    async def _generate_coding_session(self, params: Dict[str, Any]) -> List[LiveBlock]:
        """Generate a realistic coding session scenario."""
        blocks = []

        # User request
        user_queries = [
            "Can you help me implement a binary search tree with insert, delete, and search operations?",
            "I need to create a REST API for a todo application using FastAPI",
            "Help me optimize this recursive function to use dynamic programming",
            "Write a Python script to process CSV files and generate reports",
        ]

        user_query = params.get("query", random.choice(user_queries))
        user_block = self.live_manager.create_live_block("user", user_query)
        blocks.append(user_block)

        await asyncio.sleep(0.2)

        # Cognition with detailed sub-modules
        cognition_block = self.live_manager.create_live_block(
            "cognition", "🧠 Analyzing coding request..."
        )

        # Route query sub-module
        route_sub = LiveBlock(
            "sub_module", "🎯 Parsing requirements and identifying approach"
        )
        route_sub.data.metadata.update(
            {
                "model": "code-analyzer-v2",
                "confidence": 0.92,
                "approach": "step-by-step implementation",
            }
        )
        await route_sub.start_mock_simulation("default")
        cognition_block.add_sub_block(route_sub)

        await asyncio.sleep(0.3)

        # Architecture planning sub-module
        arch_sub = LiveBlock(
            "sub_module", "📐 Designing code architecture and structure"
        )
        arch_sub.data.metadata.update(
            {
                "model": "architecture-planner-v1",
                "components": ["classes", "methods", "data_structures"],
                "complexity": "medium",
            }
        )
        await arch_sub.start_mock_simulation("default")
        cognition_block.add_sub_block(arch_sub)

        await asyncio.sleep(0.4)

        # Code generation sub-module
        code_sub = LiveBlock(
            "sub_module", "💻 Generating implementation with best practices"
        )
        code_sub.data.metadata.update(
            {
                "model": "code-generator-v3",
                "language": "python",
                "style_guide": "pep8",
                "test_coverage": True,
            }
        )
        await code_sub.start_mock_simulation("default")
        cognition_block.add_sub_block(code_sub)

        cognition_block.update_content("🧠 Code analysis and planning completed")
        cognition_block.update_progress(1.0)
        cognition_block.update_tokens(input_tokens=25, output_tokens=8)
        blocks.append(cognition_block)

        await asyncio.sleep(0.5)

        # Assistant response with code
        assistant_block = self.live_manager.create_live_block(
            "assistant", "💻 Implementing your request..."
        )

        code_responses = [
            "I'll help you implement a binary search tree. Here's a complete implementation:\n\n",
            "```python\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass BST:\n    def __init__(self):\n        self.root = None\n```\n\n",
            "The implementation includes insert, search, and delete operations with O(log n) complexity.\n\n",
            "Let me also add some test cases to verify the implementation:\n\n",
            "```python\n# Test the BST\nbst = BST()\nbst.insert(5)\nbst.insert(3)\nbst.insert(7)\nprint(bst.search(3))  # True\n```\n\n",
            "This implementation follows Python best practices and includes proper error handling.",
        ]

        for i, chunk in enumerate(code_responses):
            assistant_block.append_content(chunk)
            assistant_block.update_progress((i + 1) / len(code_responses))
            assistant_block.update_tokens(output_tokens=int(len(chunk.split()) * 1.3))
            await asyncio.sleep(0.4 + random.uniform(0.1, 0.3))

        blocks.append(assistant_block)

        # Optional tool execution for testing
        if params.get("include_testing", True):
            await asyncio.sleep(0.3)

            tool_block = self.live_manager.create_live_block(
                "tool", "🧪 Running code tests..."
            )

            test_stages = [
                "Setting up test environment...",
                "Running unit tests...",
                "Checking code coverage...",
                "All tests passed! ✅ Coverage: 95%",
            ]

            for i, stage in enumerate(test_stages):
                tool_block.update_content(f"🧪 {stage}")
                tool_block.update_progress((i + 1) / len(test_stages))
                await asyncio.sleep(0.6)

            tool_block.update_tokens(output_tokens=15)
            blocks.append(tool_block)

        return blocks

    async def _generate_debugging_session(
        self, params: Dict[str, Any]
    ) -> List[LiveBlock]:
        """Generate a realistic debugging session scenario."""
        blocks = []

        # User error report
        error_reports = [
            "I'm getting a 'KeyError' when trying to access a dictionary key. Here's the traceback:\n\nKeyError: 'user_id' at line 45 in process_user_data()",
            "My recursive function is causing a 'RecursionError: maximum recursion depth exceeded'. Can you help debug this?",
            "Getting 'AttributeError: NoneType object has no attribute split' in my string processing code",
            "My API is returning 500 errors intermittently. The logs show database connection issues.",
        ]

        user_error = params.get("error", random.choice(error_reports))
        user_block = self.live_manager.create_live_block("user", user_error)
        blocks.append(user_block)

        await asyncio.sleep(0.2)

        # Error analysis cognition
        analysis_block = self.live_manager.create_live_block(
            "cognition", "🔍 Analyzing error patterns..."
        )

        # Error parsing sub-module
        parse_sub = LiveBlock("sub_module", "📝 Parsing error message and stack trace")
        parse_sub.data.metadata.update(
            {
                "model": "error-parser-v2",
                "error_type": "KeyError",
                "confidence": 0.94,
                "line_number": 45,
            }
        )
        await parse_sub.start_mock_simulation("default")
        analysis_block.add_sub_block(parse_sub)

        await asyncio.sleep(0.4)

        # Root cause analysis sub-module
        cause_sub = LiveBlock(
            "sub_module", "🎯 Identifying root cause and potential fixes"
        )
        cause_sub.data.metadata.update(
            {
                "model": "cause-analyzer-v1",
                "likely_causes": ["missing key validation", "data structure mismatch"],
                "confidence": 0.87,
            }
        )
        await cause_sub.start_mock_simulation("default")
        analysis_block.add_sub_block(cause_sub)

        analysis_block.update_content(
            "🔍 Error analysis completed - root cause identified"
        )
        analysis_block.update_progress(1.0)
        analysis_block.update_tokens(input_tokens=30, output_tokens=12)
        blocks.append(analysis_block)

        await asyncio.sleep(0.3)

        # Code inspection tool
        inspection_block = self.live_manager.create_live_block(
            "tool", "🔎 Inspecting code structure..."
        )

        inspection_stages = [
            "Loading source code...",
            "Analyzing data flow...",
            "Checking variable assignments...",
            "Found issue: Missing key validation before dictionary access",
        ]

        for i, stage in enumerate(inspection_stages):
            inspection_block.update_content(f"🔎 {stage}")
            inspection_block.update_progress((i + 1) / len(inspection_stages))
            await asyncio.sleep(0.5)

        inspection_block.update_tokens(output_tokens=20)
        blocks.append(inspection_block)

        await asyncio.sleep(0.2)

        # Solution cognition
        solution_block = self.live_manager.create_live_block(
            "cognition", "💡 Formulating solution..."
        )

        # Solution planning sub-module
        plan_sub = LiveBlock("sub_module", "📋 Planning fix implementation")
        plan_sub.data.metadata.update(
            {
                "model": "solution-planner-v1",
                "fix_type": "defensive_programming",
                "estimated_effort": "low",
            }
        )
        await plan_sub.start_mock_simulation("default")
        solution_block.add_sub_block(plan_sub)

        solution_block.update_content("💡 Solution strategy finalized")
        solution_block.update_progress(1.0)
        solution_block.update_tokens(input_tokens=15, output_tokens=5)
        blocks.append(solution_block)

        await asyncio.sleep(0.3)

        # Assistant solution
        assistant_block = self.live_manager.create_live_block(
            "assistant", "🛠️ Here's how to fix the issue..."
        )

        solution_parts = [
            "I found the issue! The error occurs because the code tries to access a dictionary key that doesn't exist.\n\n",
            "Here's the problematic code and the fix:\n\n",
            "```python\n# Problematic code:\nuser_data = get_user_data()\nuser_id = user_data['user_id']  # KeyError if key doesn't exist\n\n# Fixed code:\nuser_data = get_user_data()\nuser_id = user_data.get('user_id', 'default_id')  # Safe access\n```\n\n",
            "Alternative approaches:\n1. Use try-except blocks\n2. Validate data structure before access\n3. Add input validation\n\n",
            "This defensive programming approach prevents the KeyError and makes your code more robust.",
        ]

        for i, part in enumerate(solution_parts):
            assistant_block.append_content(part)
            assistant_block.update_progress((i + 1) / len(solution_parts))
            assistant_block.update_tokens(output_tokens=int(len(part.split()) * 1.2))
            await asyncio.sleep(0.4 + random.uniform(0.1, 0.2))

        blocks.append(assistant_block)

        return blocks

    async def _generate_research_query(self, params: Dict[str, Any]) -> List[LiveBlock]:
        """Generate a research query scenario."""
        blocks = []

        research_queries = [
            "What are the key differences between REST and GraphQL APIs? Which should I use for my project?",
            "Can you explain the trade-offs between different machine learning algorithms for classification?",
            "What are the best practices for implementing microservices architecture?",
            "How do modern databases handle ACID properties in distributed systems?",
        ]

        query = params.get("query", random.choice(research_queries))
        user_block = self.live_manager.create_live_block("user", query)
        blocks.append(user_block)

        await asyncio.sleep(0.2)

        # Research cognition
        research_block = self.live_manager.create_live_block(
            "cognition", "🔬 Processing research query..."
        )

        # Query understanding sub-module
        understand_sub = LiveBlock(
            "sub_module", "📖 Understanding research scope and requirements"
        )
        understand_sub.data.metadata.update(
            {
                "model": "query-analyzer-v1",
                "topic_categories": ["architecture", "comparison", "best_practices"],
                "complexity": "medium",
            }
        )
        await understand_sub.start_mock_simulation("default")
        research_block.add_sub_block(understand_sub)

        await asyncio.sleep(0.3)

        # Knowledge retrieval sub-module
        retrieval_sub = LiveBlock(
            "sub_module", "🗃️ Retrieving relevant knowledge and sources"
        )
        retrieval_sub.data.metadata.update(
            {
                "model": "knowledge-retriever-v2",
                "sources_found": 15,
                "confidence": 0.91,
                "domains": ["software_engineering", "system_design"],
            }
        )
        await retrieval_sub.start_mock_simulation("default")
        research_block.add_sub_block(retrieval_sub)

        research_block.update_content("🔬 Research analysis completed")
        research_block.update_progress(1.0)
        research_block.update_tokens(input_tokens=20, output_tokens=8)
        blocks.append(research_block)

        await asyncio.sleep(0.4)

        # Knowledge synthesis tool (optional)
        if params.get("include_synthesis", True):
            synthesis_block = self.live_manager.create_live_block(
                "tool", "📊 Synthesizing research findings..."
            )

            synthesis_stages = [
                "Collecting relevant sources...",
                "Analyzing key concepts...",
                "Comparing different approaches...",
                "Synthesis complete - 12 key insights identified",
            ]

            for i, stage in enumerate(synthesis_stages):
                synthesis_block.update_content(f"📊 {stage}")
                synthesis_block.update_progress((i + 1) / len(synthesis_stages))
                await asyncio.sleep(0.5)

            synthesis_block.update_tokens(output_tokens=25)
            blocks.append(synthesis_block)

            await asyncio.sleep(0.3)

        # Assistant research response
        assistant_block = self.live_manager.create_live_block(
            "assistant", "📚 Here's a comprehensive analysis..."
        )

        research_parts = [
            "Great question! Let me break down the key differences between REST and GraphQL:\n\n",
            "## REST APIs\n- **Pros**: Simple, cacheable, stateless, well-established\n- **Cons**: Over-fetching, multiple requests, versioning challenges\n\n",
            "## GraphQL APIs\n- **Pros**: Single endpoint, precise data fetching, strong typing\n- **Cons**: Learning curve, caching complexity, query complexity\n\n",
            "## Recommendation\nFor your project, consider:\n- Use REST for simple CRUD operations\n- Use GraphQL for complex data relationships\n- Factor in team expertise and ecosystem\n\n",
            "Would you like me to dive deeper into any specific aspect?",
        ]

        for i, part in enumerate(research_parts):
            assistant_block.append_content(part)
            assistant_block.update_progress((i + 1) / len(research_parts))
            assistant_block.update_tokens(output_tokens=int(len(part.split()) * 1.4))
            await asyncio.sleep(0.5 + random.uniform(0.1, 0.3))

        blocks.append(assistant_block)

        return blocks

    async def _generate_quick_question(self, params: Dict[str, Any]) -> List[LiveBlock]:
        """Generate a simple question/answer scenario."""
        blocks = []

        quick_queries = [
            "What's the difference between == and === in JavaScript?",
            "How do I convert a string to uppercase in Python?",
            "What's the keyboard shortcut for commenting code in VS Code?",
            "How do I check if a file exists in Node.js?",
        ]

        query = params.get("query", random.choice(quick_queries))
        user_block = self.live_manager.create_live_block("user", query)
        blocks.append(user_block)

        await asyncio.sleep(0.1)

        # Quick cognition
        cognition_block = self.live_manager.create_live_block(
            "cognition", "⚡ Processing quick query..."
        )

        # Simple analysis sub-module
        analysis_sub = LiveBlock(
            "sub_module", "🎯 Analyzing query and retrieving answer"
        )
        analysis_sub.data.metadata.update(
            {"model": "quick-qa-v1", "query_type": "factual", "confidence": 0.96}
        )
        await analysis_sub.start_mock_simulation("default")
        cognition_block.add_sub_block(analysis_sub)

        cognition_block.update_content("⚡ Quick analysis completed")
        cognition_block.update_progress(1.0)
        cognition_block.update_tokens(input_tokens=10, output_tokens=3)
        blocks.append(cognition_block)

        await asyncio.sleep(0.2)

        # Quick assistant response
        assistant_block = self.live_manager.create_live_block(
            "assistant", "📝 Quick answer..."
        )

        quick_answers = [
            "In JavaScript:\n- `==` performs type coercion (loose equality)\n- `===` checks strict equality (no type conversion)\n\nExample: `'5' == 5` is true, but `'5' === 5` is false.",
            "In Python, use the `.upper()` method:\n```python\ntext = 'hello world'\nuppercase = text.upper()  # 'HELLO WORLD'\n```",
            "In VS Code:\n- **Windows/Linux**: Ctrl + /\n- **Mac**: Cmd + /\n\nThis toggles line comments for selected text.",
            "In Node.js, use the `fs` module:\n```javascript\nconst fs = require('fs');\nif (fs.existsSync('file.txt')) {\n    console.log('File exists!');\n}\n```",
        ]

        answer = random.choice(quick_answers)
        assistant_block.update_content(answer)
        assistant_block.update_progress(1.0)
        assistant_block.update_tokens(output_tokens=int(len(answer.split()) * 1.3))

        blocks.append(assistant_block)

        return blocks

    async def _generate_complex_analysis(
        self, params: Dict[str, Any]
    ) -> List[LiveBlock]:
        """Generate a complex multi-step analysis scenario."""
        blocks = []

        complex_queries = [
            "Analyze the performance bottlenecks in my distributed system and suggest optimization strategies",
            "Design a scalable architecture for a real-time chat application with 1M+ users",
            "Evaluate different data storage solutions for a machine learning pipeline with TB-scale data",
            "Create a comprehensive security audit plan for a financial services application",
        ]

        query = params.get("query", random.choice(complex_queries))
        user_block = self.live_manager.create_live_block("user", query)
        blocks.append(user_block)

        await asyncio.sleep(0.3)

        # Initial analysis cognition
        initial_analysis = self.live_manager.create_live_block(
            "cognition", "🧠 Breaking down complex problem..."
        )

        # Problem decomposition sub-module
        decomp_sub = LiveBlock(
            "sub_module", "🔄 Decomposing problem into analyzable components"
        )
        decomp_sub.data.metadata.update(
            {
                "model": "problem-decomposer-v1",
                "components_identified": 5,
                "analysis_depth": "deep",
            }
        )
        await decomp_sub.start_mock_simulation("default")
        initial_analysis.add_sub_block(decomp_sub)

        # Prioritization sub-module
        priority_sub = LiveBlock(
            "sub_module", "📊 Prioritizing analysis areas by impact"
        )
        priority_sub.data.metadata.update(
            {
                "model": "priority-analyzer-v1",
                "high_priority_areas": 3,
                "methodology": "impact_effort_matrix",
            }
        )
        await priority_sub.start_mock_simulation("default")
        initial_analysis.add_sub_block(priority_sub)

        initial_analysis.update_content(
            "🧠 Problem analysis and prioritization completed"
        )
        initial_analysis.update_progress(1.0)
        initial_analysis.update_tokens(input_tokens=35, output_tokens=15)
        blocks.append(initial_analysis)

        await asyncio.sleep(0.4)

        # First analysis tool
        tool1_block = self.live_manager.create_live_block(
            "tool", "📈 Running system performance analysis..."
        )

        tool1_stages = [
            "Collecting system metrics...",
            "Analyzing CPU and memory usage...",
            "Examining network latency patterns...",
            "Identifying performance bottlenecks...",
            "Analysis complete - 4 critical issues found",
        ]

        for i, stage in enumerate(tool1_stages):
            tool1_block.update_content(f"📈 {stage}")
            tool1_block.update_progress((i + 1) / len(tool1_stages))
            await asyncio.sleep(0.6)

        tool1_block.update_tokens(output_tokens=35)
        blocks.append(tool1_block)

        await asyncio.sleep(0.3)

        # Second analysis cognition
        second_analysis = self.live_manager.create_live_block(
            "cognition", "🔍 Deep-diving into findings..."
        )

        # Data correlation sub-module
        correlation_sub = LiveBlock(
            "sub_module", "🔗 Correlating performance data with system behavior"
        )
        correlation_sub.data.metadata.update(
            {
                "model": "correlation-analyzer-v2",
                "correlations_found": 12,
                "significance_threshold": 0.85,
            }
        )
        await correlation_sub.start_mock_simulation("default")
        second_analysis.add_sub_block(correlation_sub)

        # Impact assessment sub-module
        impact_sub = LiveBlock(
            "sub_module", "⚖️ Assessing business impact of identified issues"
        )
        impact_sub.data.metadata.update(
            {
                "model": "impact-assessor-v1",
                "critical_impacts": 2,
                "revenue_at_risk": "high",
            }
        )
        await impact_sub.start_mock_simulation("default")
        second_analysis.add_sub_block(impact_sub)

        second_analysis.update_content(
            "🔍 Deep analysis and impact assessment completed"
        )
        second_analysis.update_progress(1.0)
        second_analysis.update_tokens(input_tokens=28, output_tokens=18)
        blocks.append(second_analysis)

        await asyncio.sleep(0.4)

        # Second analysis tool
        tool2_block = self.live_manager.create_live_block(
            "tool", "🛠️ Generating optimization recommendations..."
        )

        tool2_stages = [
            "Modeling optimization scenarios...",
            "Calculating cost-benefit ratios...",
            "Validating recommendations against constraints...",
            "Generating implementation roadmap...",
            "Recommendations ready - 8 optimization strategies identified",
        ]

        for i, stage in enumerate(tool2_stages):
            tool2_block.update_content(f"🛠️ {stage}")
            tool2_block.update_progress((i + 1) / len(tool2_stages))
            await asyncio.sleep(0.7)

        tool2_block.update_tokens(output_tokens=42)
        blocks.append(tool2_block)

        await asyncio.sleep(0.3)

        # Final synthesis cognition
        synthesis = self.live_manager.create_live_block(
            "cognition", "🎯 Synthesizing comprehensive solution..."
        )

        # Solution integration sub-module
        integration_sub = LiveBlock(
            "sub_module", "🔄 Integrating analysis results into cohesive strategy"
        )
        integration_sub.data.metadata.update(
            {
                "model": "solution-synthesizer-v1",
                "strategies_integrated": 8,
                "coherence_score": 0.94,
            }
        )
        await integration_sub.start_mock_simulation("default")
        synthesis.add_sub_block(integration_sub)

        synthesis.update_content("🎯 Comprehensive solution synthesis completed")
        synthesis.update_progress(1.0)
        synthesis.update_tokens(input_tokens=45, output_tokens=25)
        blocks.append(synthesis)

        await asyncio.sleep(0.5)

        # Comprehensive assistant response
        assistant_block = self.live_manager.create_live_block(
            "assistant", "📋 Comprehensive Analysis Report..."
        )

        report_sections = [
            "# Performance Analysis Report\n\nBased on comprehensive analysis of your distributed system, here are my findings:\n\n",
            "## Critical Issues Identified\n1. **Database Connection Pooling**: Insufficient pool size causing bottlenecks\n2. **Cache Invalidation**: Inefficient cache strategy impacting response times\n3. **Load Balancing**: Uneven traffic distribution across nodes\n4. **Memory Leaks**: Gradual memory consumption in microservice A\n\n",
            "## Optimization Strategies\n\n### Short-term (1-2 weeks)\n- Increase database connection pool size\n- Implement Redis clustering for cache\n- Configure weighted load balancing\n\n",
            "### Medium-term (1-2 months)\n- Migrate to connection pooling middleware\n- Implement distributed caching strategy\n- Add circuit breakers for resilience\n\n",
            "### Long-term (3-6 months)\n- Consider database sharding\n- Implement event-driven architecture\n- Add comprehensive monitoring\n\n",
            "## Expected Impact\n- **Performance**: 40-60% improvement in response times\n- **Scalability**: Support for 3x current load\n- **Reliability**: 99.9% uptime target achievable\n\n",
            "Would you like me to elaborate on any specific optimization strategy?",
        ]

        for i, section in enumerate(report_sections):
            assistant_block.append_content(section)
            assistant_block.update_progress((i + 1) / len(report_sections))
            assistant_block.update_tokens(output_tokens=int(len(section.split()) * 1.5))
            await asyncio.sleep(0.6 + random.uniform(0.2, 0.4))

        blocks.append(assistant_block)

        return blocks

    async def _generate_collaborative_coding(
        self, params: Dict[str, Any]
    ) -> List[LiveBlock]:
        """Generate a collaborative coding session scenario."""
        blocks = []

        # This would implement back-and-forth interaction
        # For brevity, implementing a simplified version
        collaborative_queries = [
            "Let's work together to build a chat application. I want to start with the user authentication system.",
            "Can we pair program a solution for rate limiting in my API? I have some ideas but want your input.",
            "I'm working on a data pipeline and getting stuck on the error handling. Can you help me improve it?",
        ]

        query = params.get("query", random.choice(collaborative_queries))
        user_block = self.live_manager.create_live_block("user", query)
        blocks.append(user_block)

        # Simplified implementation - would be expanded for full collaboration
        # ... (similar pattern to other scenarios)

        return blocks

    async def _generate_generic_scenario(
        self, config: Dict[str, Any], params: Dict[str, Any]
    ) -> List[LiveBlock]:
        """Generate a generic scenario based on configuration."""
        blocks = []

        # Simple implementation for unknown scenarios
        user_block = self.live_manager.create_live_block(
            "user", "Generic query for testing..."
        )
        blocks.append(user_block)

        cognition_block = self.live_manager.create_live_block(
            "cognition", "Processing generic request..."
        )
        await cognition_block.start_mock_simulation("cognition")
        blocks.append(cognition_block)

        assistant_block = self.live_manager.create_live_block(
            "assistant", "Generic response..."
        )
        await assistant_block.start_mock_simulation("assistant_response")
        blocks.append(assistant_block)

        return blocks

    def get_available_scenarios(self) -> Dict[str, str]:
        """Get list of available scenarios with descriptions."""
        return {
            scenario: config["description"]
            for scenario, config in self.scenario_catalog.items()
        }

    def get_scenario_info(self, scenario_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific scenario."""
        if scenario_type not in self.scenario_catalog:
            raise ValueError(f"Unknown scenario type: {scenario_type}")

        return self.scenario_catalog[scenario_type].copy()
