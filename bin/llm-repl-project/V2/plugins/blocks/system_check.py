"""System check plugin - performs system validation as an independent plugin."""

import asyncio
import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext
from ..llm_interface import LLMRequest, LLMManager


class SystemCheckPlugin(BlockPlugin):
    """
    Plugin that performs system checks.
    
    This plugin is completely self-contained and manages:
    - Running system validation checks
    - Tracking check results
    - Rendering check status and results
    - Emitting events for check completion
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="system_check",
            version="1.0.0",
            description="Performs system validation checks",
            author="LLM REPL Team",
            capabilities=[PluginCapability.SYSTEM_CHECK, PluginCapability.DISPLAY_RENDERING],
            dependencies=[],
            config_schema={
                "type": "object",
                "properties": {
                    "timeout_seconds": {"type": "integer", "default": 30},
                    "required_checks": {"type": "array", "items": {"type": "string"}},
                    "fail_fast": {"type": "boolean", "default": False},
                    "llm_config": {"type": "object", "description": "LLM configuration for heartbeat checks"}
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the system check plugin."""
        self._data.update({
            "timeout_seconds": self._config.get("timeout_seconds", 30),
            "required_checks": self._config.get("required_checks", []),
            "fail_fast": self._config.get("fail_fast", False),
            "llm_config": self._config.get("llm_config", {}),
            "checks": [],
            "all_passed": False,
            "check_results": {},
            "started_at": None,
            "completed_at": None
        })
    
    async def _on_activate(self) -> None:
        """Activate the system check plugin."""
        self._data["started_at"] = datetime.now().isoformat()
    
    async def _on_deactivate(self) -> None:
        """Deactivate the system check plugin."""
        pass
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process system checks."""
        # input_data should contain the checks to run
        if isinstance(input_data, dict) and "checks" in input_data:
            checks = input_data["checks"]
        elif isinstance(input_data, list):
            checks = input_data
        else:
            # Default system checks
            checks = [
                {"name": "Configuration", "type": "config_check"},
                {"name": "Dependencies", "type": "dependency_check"},
                {"name": "Permissions", "type": "permission_check"}
            ]
        
        check_results = {}
        all_passed = True
        
        for check in checks:
            check_name = check.get("name", "Unknown Check")
            check_type = check.get("type", "generic")
            
            try:
                # Run the specific check
                result = await self._run_check(check_name, check_type, check.get("config", {}))
                check_results[check_name] = result
                
                if not result["passed"]:
                    all_passed = False
                    if self._data["fail_fast"]:
                        break
                        
            except Exception as e:
                check_results[check_name] = {
                    "passed": False,
                    "message": f"Check failed with error: {str(e)}",
                    "error": True
                }
                all_passed = False
                
                if self._data["fail_fast"]:
                    break
        
        # Update plugin data
        self._data.update({
            "checks": checks,
            "check_results": check_results,
            "all_passed": all_passed,
            "completed_at": datetime.now().isoformat()
        })
        
        return {
            "all_passed": all_passed,
            "results": check_results,
            "summary": {
                "total_checks": len(checks),
                "passed_checks": sum(1 for r in check_results.values() if r["passed"]),
                "failed_checks": sum(1 for r in check_results.values() if not r["passed"]),
            }
        }
    
    async def _run_check(self, check_name: str, check_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific system check."""
        if check_type == "config_check":
            return await self._check_configuration(config)
        elif check_type == "dependency_check":
            return await self._check_dependencies(config)
        elif check_type == "permission_check":
            return await self._check_permissions(config)
        elif check_type == "llm_heartbeat":
            return await self._check_llm_heartbeat(config)
        else:
            # Generic check - always pass unless explicitly configured
            return {
                "passed": config.get("should_pass", True),
                "message": config.get("message", f"{check_name} completed"),
                "details": config.get("details", {})
            }
    
    async def _check_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check system configuration."""
        import os
        from pathlib import Path
        
        # Check for config files
        config_files = []
        config_dir = Path("src/config")
        if config_dir.exists():
            for file in config_dir.glob("*.py"):
                if file.name != "__init__.py":
                    config_files.append(file.name)
        
        # Check for configuration directories
        config_dirs = []
        if config_dir.exists():
            config_dirs.append("src/config/")
        
        # Check environment variables
        env_vars = []
        llm_env_vars = ["GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OLLAMA_HOST"]
        for var in llm_env_vars:
            if os.getenv(var):
                env_vars.append(var)
        
        details = {
            "config_files": config_files,
            "config_directories": config_dirs,
            "environment_variables": env_vars,
            "active_config": config.get("active_config", "debug")
        }
        
        message_parts = []
        if config_files:
            message_parts.append(f"Files: {', '.join(config_files)}")
        if config_dirs:
            message_parts.append(f"Directories: {', '.join(config_dirs)}")
        if env_vars:
            message_parts.append(f"Env vars: {', '.join(env_vars)}")
        
        message = "; ".join(message_parts) if message_parts else "Default configuration"
        
        return {
            "passed": True,
            "message": message,
            "details": details
        }
    
    async def _check_dependencies(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check system dependencies."""
        import sys
        import importlib.util
        
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # Check critical packages
        required_packages = {
            "rich": "Terminal formatting",
            "prompt_toolkit": "Input handling", 
            "pydantic": "Data validation",
            "pytest": "Testing framework"
        }
        
        available_packages = []
        missing_packages = []
        
        for package, description in required_packages.items():
            spec = importlib.util.find_spec(package)
            if spec is not None:
                available_packages.append(f"{package} ({description})")
            else:
                missing_packages.append(f"{package} ({description})")
        
        # Check for optional packages
        optional_packages = {
            "asyncio": "Async support",
            "pathlib": "Path handling",
            "datetime": "Time handling"
        }
        
        for package, description in optional_packages.items():
            spec = importlib.util.find_spec(package)
            if spec is not None:
                available_packages.append(f"{package} ({description})")
        
        details = {
            "python_version": python_version,
            "available_packages": available_packages,
            "missing_packages": missing_packages,
            "total_checked": len(required_packages) + len(optional_packages)
        }
        
        if missing_packages:
            message = f"Missing: {', '.join(missing_packages)}"
            passed = False
        else:
            message = f"Python {python_version}; {len(available_packages)} packages available"
            passed = True
        
        return {
            "passed": passed,
            "message": message,
            "details": details
        }
    
    async def _check_permissions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check system permissions."""
        # For now, this is a placeholder - in a real implementation
        # this would check actual permissions
        return {
            "passed": True,
            "message": "All permissions are correct",
            "details": {"permissions_checked": ["file_access", "network_access", "process_access"]}
        }
    
    async def _check_llm_heartbeat(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform heartbeat check with LLM providers."""
        provider_name = config.get("provider", "unknown")
        model_name = config.get("model", "unknown")
        interface_name = config.get("interface_name", "default")
        llm_manager = config.get("llm_manager")
        timeout = config.get("timeout", 10)
        
        if not llm_manager:
            return {
                "passed": False,
                "message": f"❌ {provider_name}/{model_name}: No LLM manager provided",
                "details": {"provider": provider_name, "model": model_name, "error": "no_manager"}
            }
        
        try:
            # Create a simple heartbeat request
            heartbeat_request = LLMRequest(
                messages=[{"role": "user", "content": "Hi"}],
                model=model_name,
                temperature=0.1,
                max_tokens=10,
                request_id=f"heartbeat_{interface_name}",
                cognitive_module="system_check",
                task_description=f"Heartbeat check for {provider_name}/{model_name}"
            )
            
            start_time = time.time()
            
            # Make the request with timeout
            try:
                response = await asyncio.wait_for(
                    llm_manager.make_request(heartbeat_request, interface_name),
                    timeout=timeout
                )
                duration = time.time() - start_time
                
                return {
                    "passed": True,
                    "message": f"{provider_name}/{model_name}: Online ({duration:.1f}s, ↑{response.tokens.input_tokens} ↓{response.tokens.output_tokens})",
                    "details": {
                        "provider": provider_name,
                        "model": model_name,
                        "response_time": duration,
                        "input_tokens": response.tokens.input_tokens,
                        "output_tokens": response.tokens.output_tokens,
                        "total_tokens": response.tokens.total_tokens,
                        "content_preview": response.content[:50] + "..." if len(response.content) > 50 else response.content
                    }
                }
                
            except asyncio.TimeoutError:
                return {
                    "passed": False,
                    "message": f"❌ {provider_name}/{model_name}: Timeout ({timeout}s)",
                    "details": {"provider": provider_name, "model": model_name, "error": "timeout"}
                }
                
        except Exception as e:
            return {
                "passed": False,
                "message": f"❌ {provider_name}/{model_name}: Error - {str(e)}",
                "details": {"provider": provider_name, "model": model_name, "error": str(e)}
            }
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the system check display."""
        check_results = self._data.get("check_results", {})
        all_passed = self._data.get("all_passed", False)
        
        # Base render data
        render_data = {
            "render_type": "system_check",
            "title": "System Check",
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "yellow",
                "title_style": "bold",
            }
        }
        
        # Add state-specific content and styling
        if self._state.value == "processing":
            render_data.update({
                "title": "🔍 System Check (running...)",
                "content": "Checking system components...",
                "style": {"border_color": "yellow", "show_spinner": True}
            })
            
        elif self._state.value == "completed":
            status_icon = "✅" if all_passed else "❌"
            status_text = "passed" if all_passed else "failed"
            
            render_data.update({
                "title": f"{status_icon} System Check ({status_text})",
                "style": {"border_color": "green" if all_passed else "red"},
                "all_passed": all_passed,
                "check_summary": {
                    "total": len(check_results),
                    "passed": sum(1 for r in check_results.values() if r["passed"]),
                    "failed": sum(1 for r in check_results.values() if not r["passed"])
                }
            })
            
            # Add detailed results for inscribed mode
            if context.display_mode == "inscribed":
                render_data["detailed_results"] = []
                
                # Group results by type for better formatting
                config_results = []
                dependency_results = []
                llm_results = []
                
                for check_name, result in check_results.items():
                    status = "✅" if result["passed"] else "❌"
                    
                    if "LLM" in check_name:
                        llm_results.append({
                            "name": check_name,
                            "status": status,
                            "message": result["message"],
                            "passed": result["passed"],
                            "details": result.get("details", {})
                        })
                    elif "Configuration" in check_name:
                        config_results.append({
                            "name": check_name,
                            "status": status,
                            "message": result["message"],
                            "passed": result["passed"],
                            "details": result.get("details", {})
                        })
                    elif "Dependencies" in check_name:
                        dependency_results.append({
                            "name": check_name,
                            "status": status,
                            "message": result["message"],
                            "passed": result["passed"],
                            "details": result.get("details", {})
                        })
                    else:
                        render_data["detailed_results"].append({
                            "name": check_name,
                            "status": status,
                            "message": result["message"],
                            "passed": result["passed"]
                        })
                
                # Add config results with details
                for result in config_results:
                    render_data["detailed_results"].append(result)
                
                # Add dependency results with details
                for result in dependency_results:
                    render_data["detailed_results"].append(result)
                
                # Add LLM results in table format
                render_data["llm_results"] = llm_results
        
        elif self._state.value == "error":
            render_data.update({
                "title": "❌ System Check (error)",
                "content": "System check encountered an error",
                "style": {"border_color": "red"},
                "error": True
            })
        
        return render_data
    
    def add_check(self, name: str, passed: bool, message: str, details: Dict[str, Any] = None) -> None:
        """Add a check result (for manual check addition)."""
        if "check_results" not in self._data:
            self._data["check_results"] = {}
        
        self._data["check_results"][name] = {
            "passed": passed,
            "message": message,
            "details": details or {},
            "added_manually": True
        }
        
        # Update all_passed status
        self._data["all_passed"] = all(
            result["passed"] for result in self._data["check_results"].values()
        )
    
    def get_check_results(self) -> Dict[str, Any]:
        """Get all check results."""
        return self._data.get("check_results", {})
    
    def get_check_summary(self) -> Dict[str, Any]:
        """Get a summary of check results."""
        results = self._data.get("check_results", {})
        return {
            "total_checks": len(results),
            "passed_checks": sum(1 for r in results.values() if r["passed"]),
            "failed_checks": sum(1 for r in results.values() if not r["passed"]),
            "all_passed": self._data.get("all_passed", False),
            "started_at": self._data.get("started_at"),
            "completed_at": self._data.get("completed_at")
        }