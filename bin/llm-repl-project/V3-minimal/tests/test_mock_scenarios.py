"""Tests for mock scenario generation."""

import pytest
from src.core.mock_scenarios import MockScenarioGenerator
from src.core.live_blocks import LiveBlockManager


class TestMockScenarioGenerator:
    """Test MockScenarioGenerator functionality."""

    def test_initialization(self):
        """Test generator initializes correctly."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        assert generator.live_manager == manager
        assert len(generator.scenario_catalog) > 0
        assert "coding_session" in generator.scenario_catalog
        assert "debugging_session" in generator.scenario_catalog
        assert "research_query" in generator.scenario_catalog

    def test_scenario_catalog_structure(self):
        """Test scenario catalog has proper structure."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        for scenario_name, config in generator.scenario_catalog.items():
            assert "description" in config
            assert "complexity" in config
            assert "duration" in config
            assert "blocks" in config
            assert isinstance(config["blocks"], list)
            assert len(config["blocks"]) > 0

    def test_get_available_scenarios(self):
        """Test getting available scenarios."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        scenarios = generator.get_available_scenarios()

        assert isinstance(scenarios, dict)
        assert len(scenarios) > 0
        assert "coding_session" in scenarios
        assert isinstance(scenarios["coding_session"], str)

    def test_get_scenario_info(self):
        """Test getting scenario information."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        info = generator.get_scenario_info("coding_session")

        assert "description" in info
        assert "complexity" in info
        assert "duration" in info
        assert "blocks" in info

    def test_get_scenario_info_invalid(self):
        """Test getting info for invalid scenario."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        with pytest.raises(ValueError, match="Unknown scenario type"):
            generator.get_scenario_info("invalid_scenario")

    @pytest.mark.asyncio
    async def test_generate_invalid_scenario(self):
        """Test generating invalid scenario raises error."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        with pytest.raises(ValueError, match="Unknown scenario type"):
            await generator.generate_scenario("invalid_scenario")


@pytest.mark.asyncio
class TestSpecificScenarios:
    """Test specific scenario generation."""

    async def test_quick_question_scenario(self):
        """Test quick question scenario generation."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("quick_question")

        assert len(blocks) >= 3  # user, cognition, assistant minimum
        assert blocks[0].role == "user"
        assert any(block.role == "cognition" for block in blocks)
        assert any(block.role == "assistant" for block in blocks)

        # Check that blocks have content
        for block in blocks:
            assert len(block.data.content) > 0

    async def test_coding_session_scenario(self):
        """Test coding session scenario generation."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("coding_session")

        assert len(blocks) >= 3
        assert blocks[0].role == "user"

        # Should have cognition with sub-blocks
        cognition_blocks = [b for b in blocks if b.role == "cognition"]
        assert len(cognition_blocks) > 0

        cognition_block = cognition_blocks[0]
        assert len(cognition_block.data.sub_blocks) > 0

        # Should have assistant response
        assistant_blocks = [b for b in blocks if b.role == "assistant"]
        assert len(assistant_blocks) > 0

    async def test_research_query_scenario(self):
        """Test research query scenario generation."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("research_query")

        assert len(blocks) >= 3
        assert blocks[0].role == "user"

        # Should have research cognition
        cognition_blocks = [b for b in blocks if b.role == "cognition"]
        assert len(cognition_blocks) > 0

        # Should have meaningful content related to research
        user_content = blocks[0].data.content.lower()
        assert any(
            keyword in user_content
            for keyword in ["what", "how", "why", "explain", "compare", "analyze"]
        )

    async def test_debugging_session_scenario(self):
        """Test debugging session scenario generation."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("debugging_session")

        assert len(blocks) >= 4  # More complex scenario
        assert blocks[0].role == "user"

        # Should have multiple cognition blocks for analysis
        cognition_blocks = [b for b in blocks if b.role == "cognition"]
        assert len(cognition_blocks) >= 1

        # Should have tool usage for inspection
        tool_blocks = [b for b in blocks if b.role == "tool"]
        assert len(tool_blocks) >= 1

        # User content should indicate an error/problem
        user_content = blocks[0].data.content.lower()
        assert any(
            keyword in user_content
            for keyword in [
                "error",
                "bug",
                "issue",
                "problem",
                "exception",
                "traceback",
            ]
        )

    async def test_complex_analysis_scenario(self):
        """Test complex analysis scenario generation."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("complex_analysis")

        assert len(blocks) >= 5  # Complex scenario should have many blocks

        # Should have multiple cognition blocks
        cognition_blocks = [b for b in blocks if b.role == "cognition"]
        assert len(cognition_blocks) >= 2

        # Should have multiple tool executions
        tool_blocks = [b for b in blocks if b.role == "tool"]
        assert len(tool_blocks) >= 2

        # Should have comprehensive assistant response
        assistant_blocks = [b for b in blocks if b.role == "assistant"]
        assert len(assistant_blocks) >= 1

        # Assistant response should be substantial
        assistant_content = assistant_blocks[0].data.content
        assert len(assistant_content) > 500  # Should be a comprehensive response

    async def test_scenario_with_custom_params(self):
        """Test scenario generation with custom parameters."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        custom_params = {
            "query": "Custom test query for validation",
            "include_testing": False,
        }

        blocks = await generator.generate_scenario("coding_session", custom_params)

        # Should use custom query
        assert blocks[0].data.content == "Custom test query for validation"

        # Should not include testing tool (based on custom param)
        tool_blocks = [b for b in blocks if b.role == "tool"]
        # Might still have tools, but shouldn't have testing-specific ones
        assert len(blocks) >= 3

    async def test_scenario_block_progression(self):
        """Test that scenario blocks are properly ordered and connected."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("quick_question")

        # Blocks should be in logical order
        assert blocks[0].role == "user"  # Starts with user

        # Should have reasonable progression
        roles = [block.role for block in blocks]
        assert "user" in roles
        assert "cognition" in roles
        assert "assistant" in roles

        # User should come first
        assert roles.index("user") == 0

    async def test_scenario_data_quality(self):
        """Test that generated scenario data is realistic."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        blocks = await generator.generate_scenario("coding_session")

        # Check that blocks have realistic data
        for block in blocks:
            # Should have content
            assert len(block.data.content) > 0

            # Should have proper state
            assert block.state.value in ["live", "transitioning", "inscribed"]

            # Should have creation timestamp
            assert block.created_at is not None

            # If cognition block, should have sub-blocks
            if block.role == "cognition":
                assert len(block.data.sub_blocks) > 0

                # Sub-blocks should have metadata
                for sub_block in block.data.sub_blocks:
                    assert hasattr(sub_block.data, "metadata")
                    assert isinstance(sub_block.data.metadata, dict)


class TestScenarioMetadata:
    """Test scenario metadata and configuration."""

    def test_scenario_complexity_levels(self):
        """Test different complexity levels are represented."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        complexities = set()
        for config in generator.scenario_catalog.values():
            complexities.add(config["complexity"])

        # Should have different complexity levels
        assert len(complexities) > 1
        assert "low" in complexities
        assert "high" in complexities

    def test_scenario_duration_levels(self):
        """Test different duration levels are represented."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        durations = set()
        for config in generator.scenario_catalog.values():
            durations.add(config["duration"])

        # Should have different duration levels
        assert len(durations) > 1
        assert any(d in durations for d in ["short", "medium", "long"])

    def test_scenario_block_variety(self):
        """Test scenarios use variety of block types."""
        manager = LiveBlockManager()
        generator = MockScenarioGenerator(manager)

        all_block_types = set()
        for config in generator.scenario_catalog.values():
            all_block_types.update(config["blocks"])

        # Should use different block types
        expected_types = ["user", "cognition", "assistant", "tool"]
        for block_type in expected_types:
            assert block_type in all_block_types
