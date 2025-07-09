"""Cognition plugin - orchestrates cognitive modules in sequences."""

import asyncio
from typing import Any, Dict, List, Optional, Union, AsyncIterator
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext
from ..cognitive_modules import CognitiveModule, CognitiveModuleInput, CognitiveModuleOutput
from ..llm_interface import LLMManager, LLMInterface, MockLLMInterface


class CognitionPlugin(BlockPlugin):
    """
    Cognition plugin orchestrates cognitive modules in sequences.
    
    This plugin is essentially a pass-through that:
    - Manages sequences of cognitive modules
    - Provides LLM interfaces to modules
    - Coordinates data flow between modules
    - Maintains transparency logs
    - Supports both batch and streaming processing
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="cognition",
            version="1.0.0",
            description="Orchestrates cognitive modules for complex processing",
            author="LLM REPL Team",
            capabilities=[PluginCapability.QUERY_PROCESSING, PluginCapability.DISPLAY_RENDERING],
            dependencies=["llm_manager"],
            config_schema={
                "type": "object",
                "properties": {
                    "modules": {
                        "type": "array",
                        "description": "List of cognitive modules to execute in sequence",
                        "default": []
                    },
                    "llm_interface": {
                        "type": "string",
                        "description": "Name of LLM interface to use",
                        "default": "default"
                    },
                    "stream_processing": {
                        "type": "boolean",
                        "description": "Enable streaming processing",
                        "default": False
                    },
                    "fail_on_error": {
                        "type": "boolean",
                        "description": "Fail entire chain if one module fails",
                        "default": True
                    },
                    "max_retries": {
                        "type": "integer",
                        "description": "Maximum retries per module",
                        "default": 2
                    }
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the cognition plugin."""
        self._data.update({
            "modules": self._config.get("modules", []),
            "llm_interface": self._config.get("llm_interface", "default"),
            "stream_processing": self._config.get("stream_processing", False),
            "fail_on_error": self._config.get("fail_on_error", True),
            "max_retries": self._config.get("max_retries", 2),
            "module_instances": [],
            "module_outputs": [],
            "transparency_log": [],
            "current_module_index": -1,
            "total_modules": 0,
            "processing_start_time": None,
            "processing_end_time": None
        })
    
    async def _on_activate(self) -> None:
        """Activate the cognition plugin."""
        # Initialize cognitive modules
        modules = self._data["modules"]
        self._data["module_instances"] = []
        self._data["total_modules"] = len(modules)
        
        for module_config in modules:
            if isinstance(module_config, dict):
                module_class = module_config.get("class")
                module_params = module_config.get("params", {})
            else:
                # Assume it's a module class directly
                module_class = module_config
                module_params = {}
            
            if module_class:
                # Instantiate the module
                module_instance = module_class(**module_params)
                self._data["module_instances"].append(module_instance)
    
    async def _on_deactivate(self) -> None:
        """Deactivate the cognition plugin."""
        if not self._data.get("processing_end_time"):
            self._data["processing_end_time"] = datetime.now().isoformat()
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process input through the cognitive module chain."""
        # Get input text
        if isinstance(input_data, str):
            input_text = input_data
        elif isinstance(input_data, dict) and "content" in input_data:
            input_text = input_data["content"]
        else:
            raise ValueError("Cognition plugin requires string input or dict with 'content' key")
        
        # Get LLM manager from context
        llm_manager = context.get("llm_manager")
        if not llm_manager:
            # Create a mock LLM manager for testing
            llm_manager = LLMManager()
            llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        llm_interface = llm_manager.get_interface(self._data["llm_interface"])
        if not llm_interface:
            raise ValueError(f"LLM interface '{self._data['llm_interface']}' not found")
        
        self._data["processing_start_time"] = datetime.now().isoformat()
        
        # Process through module chain
        if self._data["stream_processing"]:
            return await self._process_streaming(input_text, llm_interface)
        else:
            return await self._process_batch(input_text, llm_interface)
    
    async def _process_batch(self, input_text: str, llm_interface: LLMInterface) -> Dict[str, Any]:
        """Process input through modules in batch mode."""
        module_instances = self._data["module_instances"]
        module_outputs = []
        transparency_log = []
        
        current_input = input_text
        
        for i, module in enumerate(module_instances):
            self._data["current_module_index"] = i
            
            try:
                # Create module input
                module_input = CognitiveModuleInput(
                    content=current_input,
                    context={"chain_position": i, "total_chain_length": len(module_instances)},
                    previous_outputs=module_outputs.copy()
                )
                
                # Process through module
                module_output = await module.process(module_input, llm_interface)
                
                # Store output and log
                module_outputs.append(module_output)
                transparency_log.append({
                    "module_name": module.metadata.name,
                    "module_index": i,
                    "input": current_input,
                    "output": module_output.to_dict(),
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update token counts
                if module_output.llm_response:
                    self.add_input_tokens(module_output.llm_response.tokens.input_tokens)
                    self.add_output_tokens(module_output.llm_response.tokens.output_tokens)
                
                # Use output as input for next module
                current_input = module_output.content
                
            except Exception as e:
                error_log = {
                    "module_name": module.metadata.name,
                    "module_index": i,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                transparency_log.append(error_log)
                
                if self._data["fail_on_error"]:
                    raise
                else:
                    # Continue with original input
                    pass
        
        self._data["module_outputs"] = module_outputs
        self._data["transparency_log"] = transparency_log
        self._data["processing_end_time"] = datetime.now().isoformat()
        self._data["current_module_index"] = -1
        
        return {
            "final_output": current_input,
            "module_outputs": [output.to_dict() for output in module_outputs],
            "transparency_log": transparency_log,
            "total_modules": len(module_instances),
            "processing_duration": self._get_processing_duration()
        }
    
    async def _process_streaming(self, input_text: str, llm_interface: LLMInterface) -> AsyncIterator[Dict[str, Any]]:
        """Process input through modules in streaming mode."""
        module_instances = self._data["module_instances"]
        module_outputs = []
        transparency_log = []
        
        current_input = input_text
        
        for i, module in enumerate(module_instances):
            self._data["current_module_index"] = i
            
            try:
                # Create module input
                module_input = CognitiveModuleInput(
                    content=current_input,
                    context={"chain_position": i, "total_chain_length": len(module_instances)},
                    previous_outputs=module_outputs.copy()
                )
                
                # Stream process through module
                accumulated_output = ""
                final_output = None
                
                async for chunk in module.stream_process(module_input, llm_interface):
                    if isinstance(chunk, str):
                        # Streaming content
                        accumulated_output += chunk
                        yield {
                            "type": "stream_chunk",
                            "module_name": module.metadata.name,
                            "module_index": i,
                            "content": chunk,
                            "accumulated_content": accumulated_output
                        }
                    elif isinstance(chunk, CognitiveModuleOutput):
                        # Final output
                        final_output = chunk
                        break
                
                if final_output:
                    # Store output and log
                    module_outputs.append(final_output)
                    transparency_log.append({
                        "module_name": module.metadata.name,
                        "module_index": i,
                        "input": current_input,
                        "output": final_output.to_dict(),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Update token counts
                    if final_output.llm_response:
                        self.add_input_tokens(final_output.llm_response.tokens.input_tokens)
                        self.add_output_tokens(final_output.llm_response.tokens.output_tokens)
                    
                    # Use output as input for next module
                    current_input = final_output.content
                    
                    yield {
                        "type": "module_complete",
                        "module_name": module.metadata.name,
                        "module_index": i,
                        "output": final_output.to_dict()
                    }
                
            except Exception as e:
                error_log = {
                    "module_name": module.metadata.name,
                    "module_index": i,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                transparency_log.append(error_log)
                
                yield {
                    "type": "module_error",
                    "module_name": module.metadata.name,
                    "module_index": i,
                    "error": str(e)
                }
                
                if self._data["fail_on_error"]:
                    raise
        
        self._data["module_outputs"] = module_outputs
        self._data["transparency_log"] = transparency_log
        self._data["processing_end_time"] = datetime.now().isoformat()
        self._data["current_module_index"] = -1
        
        yield {
            "type": "chain_complete",
            "final_output": current_input,
            "module_outputs": [output.to_dict() for output in module_outputs],
            "transparency_log": transparency_log,
            "total_modules": len(module_instances),
            "processing_duration": self._get_processing_duration()
        }
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the cognition plugin display."""
        current_module_index = self._data.get("current_module_index", -1)
        total_modules = self._data.get("total_modules", 0)
        module_outputs = self._data.get("module_outputs", [])
        transparency_log = self._data.get("transparency_log", [])
        
        # Base render data
        render_data = {
            "render_type": "cognition",
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "purple",
                "title_style": "bold",
            },
            "total_modules": total_modules,
            "current_module_index": current_module_index
        }
        
        # Add state-specific content
        if self._state.value == "processing":
            current_module_name = "Unknown"
            if current_module_index >= 0 and current_module_index < len(self._data.get("module_instances", [])):
                current_module = self._data["module_instances"][current_module_index]
                current_module_name = current_module.metadata.name
            
            render_data.update({
                "content": f"Processing through cognitive modules ({current_module_index + 1}/{total_modules})",
                "current_module": current_module_name,
                "progress": (current_module_index + 1) / total_modules if total_modules > 0 else 0
            })
            
        elif self._state.value == "completed":
            render_data.update({
                "content": f"Completed processing through {total_modules} cognitive modules",
                "completed": True,
                "processing_duration": self._get_processing_duration()
            })
            
            # Add module summary
            module_summary = []
            for i, output in enumerate(module_outputs):
                module_name = "Unknown"
                if i < len(self._data.get("module_instances", [])):
                    module_name = self._data["module_instances"][i].metadata.name
                
                module_summary.append({
                    "name": module_name,
                    "status": "✅" if output else "❌",
                    "tokens": output.llm_response.tokens.total_tokens if output.llm_response else 0,
                    "duration": output.llm_response.duration_seconds if output.llm_response else 0
                })
            
            render_data["module_summary"] = module_summary
            
            # Add transparency log for inscribed mode
            if context.display_mode == "inscribed":
                render_data["transparency_log"] = transparency_log
        
        elif self._state.value == "error":
            render_data.update({
                "content": "Error in cognitive processing",
                "error": True
            })
        
        return render_data
    
    def _get_processing_duration(self) -> float:
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
    
    def get_transparency_log(self) -> List[Dict[str, Any]]:
        """Get the complete transparency log."""
        return self._data.get("transparency_log", [])
    
    def get_module_outputs(self) -> List[Dict[str, Any]]:
        """Get outputs from all modules."""
        outputs = self._data.get("module_outputs", [])
        return [output.to_dict() for output in outputs]
    
    def add_cognitive_module(self, module: CognitiveModule) -> None:
        """Add a cognitive module to the chain."""
        if "module_instances" not in self._data:
            self._data["module_instances"] = []
        
        self._data["module_instances"].append(module)
        self._data["total_modules"] = len(self._data["module_instances"])
    
    def get_cognitive_modules(self) -> List[CognitiveModule]:
        """Get all cognitive modules in the chain."""
        return self._data.get("module_instances", [])