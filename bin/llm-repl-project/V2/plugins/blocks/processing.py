"""Processing plugin - handles query processing as an independent plugin."""

from typing import Any, Dict, List, Optional
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext, PluginEvent


class ProcessingPlugin(BlockPlugin):
    """
    Plugin that handles query processing.
    
    This plugin is completely self-contained and manages:
    - Query processing pipeline
    - Sub-step execution (intent detection, main query, etc.)
    - Progress tracking and display
    - Inter-plugin communication for processing steps
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="processing",
            version="1.0.0",
            description="Handles query processing pipeline",
            author="LLM REPL Team",
            capabilities=[PluginCapability.QUERY_PROCESSING, PluginCapability.DISPLAY_RENDERING],
            dependencies=["intent_detector", "llm_manager"],
            config_schema={
                "type": "object",
                "properties": {
                    "timeout_seconds": {"type": "integer", "default": 60},
                    "max_retries": {"type": "integer", "default": 3},
                    "show_progress": {"type": "boolean", "default": True},
                    "processing_steps": {
                        "type": "array",
                        "default": ["intent_detection", "main_query"]
                    }
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the processing plugin."""
        self._data.update({
            "timeout_seconds": self._config.get("timeout_seconds", 60),
            "max_retries": self._config.get("max_retries", 3),
            "show_progress": self._config.get("show_progress", True),
            "processing_steps": self._config.get("processing_steps", ["intent_detection", "main_query"]),
            "current_step": None,
            "current_step_index": -1,
            "step_results": {},
            "step_timings": {},
            "total_tokens": {"input": 0, "output": 0},
            "processing_start_time": None,
            "processing_end_time": None,
            "query": "",
            "final_result": None
        })
    
    async def _on_activate(self) -> None:
        """Activate the processing plugin."""
        self._data["processing_start_time"] = datetime.now().isoformat()
    
    async def _on_deactivate(self) -> None:
        """Deactivate the processing plugin."""
        if not self._data.get("processing_end_time"):
            self._data["processing_end_time"] = datetime.now().isoformat()
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process a query through the processing pipeline."""
        # Extract query from input
        if isinstance(input_data, str):
            query = input_data
        elif isinstance(input_data, dict) and "query" in input_data:
            query = input_data["query"]
        else:
            raise ValueError("Processing plugin requires a query string or dict with 'query' key")
        
        self._data["query"] = query
        
        # Get required services from context
        intent_detector = context.get("intent_detector")
        llm_manager = context.get("llm_manager")
        
        if not intent_detector or not llm_manager:
            raise ValueError("Processing plugin requires intent_detector and llm_manager in context")
        
        # Execute processing steps
        step_results = {}
        step_timings = {}
        total_tokens = {"input": 0, "output": 0}
        
        for i, step_name in enumerate(self._data["processing_steps"]):
            self._data["current_step"] = step_name
            self._data["current_step_index"] = i
            
            step_start_time = datetime.now()
            
            try:
                if step_name == "intent_detection":
                    result = await self._process_intent_detection(query, intent_detector)
                elif step_name == "main_query":
                    result = await self._process_main_query(query, llm_manager, step_results)
                else:
                    # Custom step - emit event for other plugins to handle
                    event = PluginEvent(
                        event_type="processing_step",
                        source_plugin=self.plugin_id,
                        data={
                            "step_name": step_name,
                            "query": query,
                            "previous_results": step_results
                        }
                    )
                    # For now, just return a placeholder
                    result = {"step": step_name, "status": "completed", "message": "Custom step completed"}
                
                step_end_time = datetime.now()
                step_duration = (step_end_time - step_start_time).total_seconds()
                
                step_results[step_name] = result
                step_timings[step_name] = {
                    "start_time": step_start_time.isoformat(),
                    "end_time": step_end_time.isoformat(),
                    "duration_seconds": step_duration
                }
                
                # Update token counts
                if "tokens" in result:
                    tokens = result["tokens"]
                    input_tokens = tokens.get("input", 0)
                    output_tokens = tokens.get("output", 0)
                    total_tokens["input"] += input_tokens
                    total_tokens["output"] += output_tokens
                    
                    # Update plugin's token counter
                    self.add_input_tokens(input_tokens)
                    self.add_output_tokens(output_tokens)
                
            except Exception as e:
                step_results[step_name] = {
                    "status": "error",
                    "error": str(e),
                    "step": step_name
                }
                step_timings[step_name] = {
                    "start_time": step_start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "duration_seconds": (datetime.now() - step_start_time).total_seconds(),
                    "error": True
                }
        
        # Update plugin data
        self._data.update({
            "step_results": step_results,
            "step_timings": step_timings,
            "total_tokens": total_tokens,
            "processing_end_time": datetime.now().isoformat(),
            "current_step": None,
            "current_step_index": -1
        })
        
        # Determine final result
        if "main_query" in step_results:
            final_result = step_results["main_query"]
        else:
            final_result = {
                "status": "completed",
                "message": "Processing completed",
                "results": step_results
            }
        
        self._data["final_result"] = final_result
        
        return {
            "query": query,
            "final_result": final_result,
            "step_results": step_results,
            "step_timings": step_timings,
            "total_tokens": total_tokens,
            "processing_duration": self._get_total_duration()
        }
    
    async def _process_intent_detection(self, query: str, intent_detector: Any) -> Dict[str, Any]:
        """Process intent detection step."""
        try:
            intent = await intent_detector.detect_intent(query)
            return {
                "status": "completed",
                "intent": intent.value if hasattr(intent, 'value') else str(intent),
                "message": f"Intent detected: {intent}",
                "tokens": {"input": 15, "output": 5}  # Mock token counts
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": f"Intent detection failed: {str(e)}"
            }
    
    async def _process_main_query(self, query: str, llm_manager: Any, previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process main query step."""
        try:
            response = await llm_manager.make_request(query)
            
            return {
                "status": "completed",
                "response": response.content,
                "tokens": {
                    "input": response.tokens.input_tokens,
                    "output": response.tokens.output_tokens
                },
                "duration": response.duration_seconds,
                "message": "Query processed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": f"Main query failed: {str(e)}"
            }
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the processing display."""
        query = self._data.get("query", "")
        current_step = self._data.get("current_step")
        step_results = self._data.get("step_results", {})
        step_timings = self._data.get("step_timings", {})
        total_tokens = self._data.get("total_tokens", {"input": 0, "output": 0})
        
        # Base render data
        render_data = {
            "render_type": "processing",
            "query": query,
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "magenta",
                "title_style": "bold",
            }
        }
        
        # Note: Title will be set by standardized display formatter
        
        # Add state-specific content
        if self._state.value == "processing":
            render_data.update({
                "content": f"Processing query: {query}",
                "current_step": current_step,
                "progress": self._calculate_progress(),
            })
            
        elif self._state.value == "completed":
            duration = self._get_total_duration()
            render_data.update({
                "completed": True,
                "total_duration": duration,
                "total_tokens": total_tokens
            })
            
            # Add step summary
            step_summary = []
            for step_name in self._data["processing_steps"]:
                if step_name in step_results:
                    result = step_results[step_name]
                    timing = step_timings.get(step_name, {})
                    
                    status_icon = "✅" if result.get("status") == "completed" else "❌"
                    duration_str = f"({timing.get('duration_seconds', 0):.1f}s)" if timing else ""
                    
                    step_summary.append({
                        "name": step_name,
                        "status": status_icon,
                        "message": result.get("message", ""),
                        "duration": duration_str,
                        "tokens": result.get("tokens", {}),
                        "passed": result.get("status") == "completed"
                    })
            
            render_data["step_summary"] = step_summary
            
            # Add connections for inscribed mode
            if context.display_mode == "inscribed":
                render_data["show_connections"] = True
        
        elif self._state.value == "error":
            render_data.update({
                "content": "Processing encountered an error",
                "error": True
            })
        
        return render_data
    
    def _calculate_progress(self) -> float:
        """Calculate processing progress (0.0 to 1.0)."""
        if not self._data["processing_steps"]:
            return 0.0
        
        current_index = self._data.get("current_step_index", -1)
        if current_index < 0:
            return 0.0
        
        return (current_index + 1) / len(self._data["processing_steps"])
    
    def _get_total_duration(self) -> float:
        """Get total processing duration."""
        start_time = self._data.get("processing_start_time")
        end_time = self._data.get("processing_end_time")
        
        if not start_time or not end_time:
            return 0.0
        
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            return (end_dt - start_dt).total_seconds()
        except:
            return 0.0
    
    def get_processing_info(self) -> Dict[str, Any]:
        """Get comprehensive processing information."""
        return {
            "query": self._data.get("query", ""),
            "current_step": self._data.get("current_step"),
            "progress": self._calculate_progress(),
            "step_results": self._data.get("step_results", {}),
            "step_timings": self._data.get("step_timings", {}),
            "total_tokens": self._data.get("total_tokens", {"input": 0, "output": 0}),
            "total_duration": self._get_total_duration(),
            "final_result": self._data.get("final_result")
        }