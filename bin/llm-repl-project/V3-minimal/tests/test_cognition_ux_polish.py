"""
Tests for Cognition UX Polish

Validates polished user experience features including widgets,
animations, and interactive demonstrations.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from src.demos.simple_ux_polish_demo import SimpleUXPolishDemo
from src.widgets.cognition_pipeline_widget import (
    CognitionStepWidget,
    CognitionPipelineWidget,
    CognitionDashboardWidget
)
from src.core.mock_scenarios import MockCognitionPlugin, CognitionStep


class TestCognitionUXPolishDemo:
    """Test the UX polish demonstration features."""
    
    def test_demo_initialization(self):
        """Test UX demo initializes correctly."""
        demo = SimpleUXPolishDemo()
        assert demo.console is not None
        assert demo.scenario_generator is not None
    
    @pytest.mark.asyncio
    async def test_progressive_enhancement_demo(self):
        """Test progressive enhancement demo execution."""
        demo = CognitionUXPolishDemo()
        
        # Mock console to avoid output during tests
        demo.console = MagicMock()
        
        # Test the demo runs without errors
        try:
            await demo._demo_progressive_enhancement()
            # If we get here, the demo completed successfully
            assert True
        except Exception as e:
            pytest.fail(f"Progressive enhancement demo failed: {e}")
    
    @pytest.mark.asyncio
    async def test_realtime_dashboard_demo(self):
        """Test real-time dashboard demo execution."""
        demo = CognitionUXPolishDemo()
        demo.console = MagicMock()
        
        try:
            await demo._demo_realtime_dashboard()
            assert True
        except Exception as e:
            pytest.fail(f"Real-time dashboard demo failed: {e}")
    
    @pytest.mark.asyncio
    async def test_parallel_visualization_demo(self):
        """Test parallel visualization demo execution."""
        demo = CognitionUXPolishDemo()
        demo.console = MagicMock()
        
        try:
            await demo._demo_parallel_visualization()
            assert True
        except Exception as e:
            pytest.fail(f"Parallel visualization demo failed: {e}")
    
    @pytest.mark.asyncio
    async def test_interactive_control_demo(self):
        """Test interactive control demo execution."""
        demo = CognitionUXPolishDemo()
        demo.console = MagicMock()
        
        try:
            await demo._demo_interactive_control()
            assert True
        except Exception as e:
            pytest.fail(f"Interactive control demo failed: {e}")
    
    def test_enhanced_results_display(self):
        """Test enhanced results display formatting."""
        demo = CognitionUXPolishDemo()
        demo.console = MagicMock()
        
        # Mock result data
        result = {
            "scenario_type": "Test Scenario",
            "total_steps": 3,
            "total_tokens": 150,
            "total_duration": 5.2,
            "confidence": 0.85
        }
        
        # Test display doesn't crash
        try:
            demo._display_enhanced_results(result, "Test Demo")
            assert True
        except Exception as e:
            pytest.fail(f"Enhanced results display failed: {e}")


class TestCognitionWidgets:
    """Test cognition pipeline widgets."""
    
    def test_cognition_step_widget_creation(self):
        """Test cognition step widget can be created."""
        step = CognitionStep(
            name="Test Step",
            icon="🧪",
            model="test-model",
            description="Test description",
            estimated_tokens=10,
            estimated_duration=1.0
        )
        
        # Mock sub-module
        sub_module = MagicMock()
        sub_module.step = step
        sub_module.state = "pending"
        sub_module.progress = 0.0
        sub_module.result = None
        sub_module.add_update_callback = MagicMock()
        
        # Create widget
        widget = CognitionStepWidget(sub_module)
        
        assert widget.sub_module == sub_module
        assert widget.step_state == "pending"
        assert widget.step_progress == 0.0
    
    def test_cognition_step_widget_state_updates(self):
        """Test step widget updates when sub-module state changes."""
        step = CognitionStep(
            name="Test Step",
            icon="🧪",
            model="test-model",
            description="Test description",
            estimated_tokens=10,
            estimated_duration=1.0
        )
        
        sub_module = MagicMock()
        sub_module.step = step
        sub_module.state = "pending"
        sub_module.progress = 0.0
        sub_module.result = None
        sub_module.add_update_callback = MagicMock()
        
        widget = CognitionStepWidget(sub_module)
        
        # Simulate state change to running
        sub_module.state = "running"
        sub_module.progress = 0.5
        
        # Call the update callback manually
        widget._on_step_update(sub_module)
        
        assert widget.step_state == "running"
        assert widget.step_progress == 0.5
    
    def test_cognition_pipeline_widget_creation(self):
        """Test cognition pipeline widget creation."""
        plugin = EnhancedMockCognitionPlugin("simple_coding")
        
        # Mock plugin methods
        plugin.add_update_callback = MagicMock()
        plugin.get_current_status = MagicMock(return_value={
            "state": "pending",
            "progress": 0.0,
            "total_tokens": 0,
            "total_duration": 0.0,
            "completed_steps": []
        })
        
        widget = CognitionPipelineWidget(plugin)
        
        assert widget.cognition_plugin == plugin
        assert len(widget.step_widgets) >= 3  # Should have at least 3 sub-modules
        assert widget.pipeline_state == "pending"
    
    def test_cognition_dashboard_widget_creation(self):
        """Test cognition dashboard widget creation."""
        dashboard = CognitionDashboardWidget()
        
        assert dashboard.pipelines == []
        assert dashboard.active_pipeline is None
        assert dashboard.sidebar is not None
        assert dashboard.main_area is not None
    
    def test_dashboard_add_pipeline(self):
        """Test adding pipeline to dashboard."""
        dashboard = CognitionDashboardWidget()
        plugin = EnhancedMockCognitionPlugin("simple_coding")
        
        # Mock plugin methods
        plugin.add_update_callback = MagicMock()
        plugin.get_current_status = MagicMock(return_value={
            "state": "pending",
            "progress": 0.0,
            "total_tokens": 0,
            "total_duration": 0.0,
            "completed_steps": []
        })
        
        pipeline_widget = dashboard.add_pipeline(plugin, "Test Pipeline")
        
        assert len(dashboard.pipelines) == 1
        assert dashboard.active_pipeline == pipeline_widget
        assert pipeline_widget.cognition_plugin == plugin


class TestUXPolishIntegration:
    """Test UX polish integration features."""
    
    @pytest.mark.asyncio
    async def test_comprehensive_showcase_execution(self):
        """Test comprehensive showcase runs without errors."""
        demo = CognitionUXPolishDemo()
        
        # Mock console and disable clear/print to avoid output
        demo.console = MagicMock()
        demo.console.clear = MagicMock()
        demo.console.print = MagicMock()
        
        try:
            await demo.run_comprehensive_showcase()
            assert True
        except Exception as e:
            pytest.fail(f"Comprehensive showcase failed: {e}")
    
    def test_widget_css_classes(self):
        """Test that widgets have proper CSS classes defined."""
        # Test step widget CSS
        assert hasattr(CognitionStepWidget, "DEFAULT_CSS")
        assert "step-pending" in CognitionStepWidget.DEFAULT_CSS
        assert "step-running" in CognitionStepWidget.DEFAULT_CSS
        assert "step-completed" in CognitionStepWidget.DEFAULT_CSS
        
        # Test pipeline widget CSS
        assert hasattr(CognitionPipelineWidget, "DEFAULT_CSS")
        assert "pipeline-header" in CognitionPipelineWidget.DEFAULT_CSS
        assert "pipeline-metrics" in CognitionPipelineWidget.DEFAULT_CSS
        
        # Test dashboard widget CSS
        assert hasattr(CognitionDashboardWidget, "DEFAULT_CSS")
        assert "dashboard-sidebar" in CognitionDashboardWidget.DEFAULT_CSS
        assert "dashboard-main" in CognitionDashboardWidget.DEFAULT_CSS
    
    def test_widget_reactive_properties(self):
        """Test that widgets have proper reactive properties."""
        # Test step widget reactives
        step = CognitionStep(
            name="Test", icon="🧪", model="test", description="Test"
        )
        sub_module = MagicMock()
        sub_module.step = step
        sub_module.state = "pending"
        sub_module.progress = 0.0
        sub_module.result = None
        sub_module.add_update_callback = MagicMock()
        
        widget = CognitionStepWidget(sub_module)
        
        # Check reactive properties exist
        assert hasattr(widget, "step_state")
        assert hasattr(widget, "step_progress")
        assert hasattr(widget, "step_content")
    
    @pytest.mark.asyncio
    async def test_polished_features_demonstration(self):
        """Test that polished features are properly demonstrated."""
        demo = CognitionUXPolishDemo()
        demo.console = MagicMock()
        
        # Test each demo method exists and can be called
        assert hasattr(demo, "_demo_progressive_enhancement")
        assert hasattr(demo, "_demo_realtime_dashboard")
        assert hasattr(demo, "_demo_parallel_visualization")
        assert hasattr(demo, "_demo_interactive_control")
        
        # Test that these are async methods
        assert asyncio.iscoroutinefunction(demo._demo_progressive_enhancement)
        assert asyncio.iscoroutinefunction(demo._demo_realtime_dashboard)
        assert asyncio.iscoroutinefunction(demo._demo_parallel_visualization)
        assert asyncio.iscoroutinefunction(demo._demo_interactive_control)


if __name__ == "__main__":
    # Run basic tests manually
    async def run_basic_tests():
        print("🧪 Running UX Polish Tests")
        print("=" * 40)
        
        # Test demo creation
        demo = CognitionUXPolishDemo()
        print("✅ Demo creation successful")
        
        # Test widget creation
        step = CognitionStep(
            name="Test Step",
            icon="🧪", 
            model="test-model",
            description="Test description"
        )
        
        sub_module = MagicMock()
        sub_module.step = step
        sub_module.state = "pending"
        sub_module.progress = 0.0
        sub_module.result = None
        sub_module.add_update_callback = MagicMock()
        
        step_widget = CognitionStepWidget(sub_module)
        print("✅ Step widget creation successful")
        
        # Test dashboard
        dashboard = CognitionDashboardWidget()
        print("✅ Dashboard widget creation successful")
        
        print("\n🎉 All basic UX polish tests passed!")
    
    asyncio.run(run_basic_tests())