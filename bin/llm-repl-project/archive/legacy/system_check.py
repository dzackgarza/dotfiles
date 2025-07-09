#!/usr/bin/env python3
"""
System Check Module - Consolidated startup validation system

Handles all system startup checks including model heartbeat validation,
configuration validation, and system status reporting.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from scrivener import Scrivener, InscriptionEvent, EventType
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED


class CheckStatus(Enum):
    """Status of individual system checks."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class SystemCheckResult:
    """Result of a system check."""
    name: str
    status: CheckStatus
    message: str
    duration: float = 0.0
    error: Optional[str] = None


class SystemCheck:
    """
    Consolidated system check handler that manages all startup validations.
    
    This class handles:
    - Model heartbeat checks
    - Configuration validation
    - System status reporting
    - Live state updates through scrivener
    - Wall clock timing
    - Proper error handling and reporting
    """
    
    def __init__(self, scrivener: Scrivener, config, intent_manager, main_query_manager):
        self.scrivener = scrivener
        self.config = config
        self.intent_manager = intent_manager
        self.main_query_manager = main_query_manager
        
        # System check state
        self.checks: List[SystemCheckResult] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.overall_status = CheckStatus.PENDING
        
    async def run_all_checks(self) -> bool:
        """
        Run all system checks and return True if all pass.
        
        Returns:
            bool: True if all checks passed, False otherwise
        """
        self.start_time = time.time()
        self.overall_status = CheckStatus.RUNNING
        
        try:
            # Start the system check display
            await self._display_system_check_start()
            
            # Run individual checks
            await self._run_configuration_check()
            await self._run_model_heartbeat_checks()
            await self._run_artificial_delay_test()
            
            # Determine overall status
            failed_checks = [c for c in self.checks if c.status == CheckStatus.FAILED]
            if failed_checks:
                self.overall_status = CheckStatus.FAILED
                await self._display_system_check_failed(failed_checks)
                return False
            else:
                self.overall_status = CheckStatus.PASSED
                await self._display_system_check_passed()
                return True
                
        except Exception as e:
            self.overall_status = CheckStatus.FAILED
            await self._display_system_check_error(str(e))
            return False
        finally:
            self.end_time = time.time()
            
    async def _display_system_check_start(self):
        """Start the system check as a lifecycle-managed cognition block."""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Start system check as a cognition block with its own lifecycle
        await self.scrivener.inscribe(InscriptionEvent(
            event_type=EventType.COGNITION_BLOCK,
            content=f"System Check ({current_time})",
            metadata={
                "state": "running",
                "system_check": True,
                "wall_clock": current_time,
                "configuration": f"{self.config.intent_detection_display_name} + {self.config.main_query_display_name}",
                "sub_blocks": ["Configuration validation", "Model heartbeat checks", "Timing verification"]
            }
        ))
        
    async def _run_configuration_check(self):
        """Validate the configuration settings."""
        check_start = time.time()
        
        try:
            # Validate configuration
            assert self.config is not None, "Configuration is None"
            assert hasattr(self.config, 'intent_detection_provider'), "Missing intent detection provider"
            assert hasattr(self.config, 'main_query_provider'), "Missing main query provider"
            assert hasattr(self.config, 'intent_detection_model'), "Missing intent detection model"
            assert hasattr(self.config, 'main_query_model'), "Missing main query model"
            
            duration = time.time() - check_start
            self.checks.append(SystemCheckResult(
                name="Configuration",
                status=CheckStatus.PASSED,
                message="✓ Configuration validated",
                duration=duration
            ))
            
        except Exception as e:
            duration = time.time() - check_start
            self.checks.append(SystemCheckResult(
                name="Configuration",
                status=CheckStatus.FAILED,
                message="✗ Configuration validation failed",
                duration=duration,
                error=str(e)
            ))
            
    async def _run_model_heartbeat_checks(self):
        """Run heartbeat checks for all configured models."""
        # Check intent detection model
        await self._check_model_heartbeat(
            "Intent Detection",
            self.intent_manager,
            self.config.intent_detection_display_name
        )
        
        # Check main query model (if different)
        if (self.config.main_query_provider != self.config.intent_detection_provider or 
            self.config.main_query_model != self.config.intent_detection_model):
            await self._check_model_heartbeat(
                "Main Query",
                self.main_query_manager,
                self.config.main_query_display_name
            )
        else:
            # Same model, just record it as shared
            self.checks.append(SystemCheckResult(
                name="Main Query",
                status=CheckStatus.PASSED,
                message=f"✓ {self.config.main_query_display_name} (shared)",
                duration=0.0
            ))
            
    async def _check_model_heartbeat(self, check_name: str, manager, display_name: str):
        """Check heartbeat for a specific model with unassailable assertions."""
        check_start = time.time()
        
        try:
            # Make a specific test request that requires the model to respond with a keyword
            test_prompt = "Please respond with exactly the word HEARTBEAT_OK to confirm you are working properly."
            expected_keyword = "HEARTBEAT_OK"
            
            # Make the request
            response = await manager.make_request(test_prompt)
            
            # Unassailable assertions - any failure should immediately fail the check
            if response is None:
                raise ValueError(f"Model {display_name} returned None response")
            
            if not hasattr(response, 'content'):
                raise ValueError(f"Model {display_name} response missing content attribute")
            
            if not response.content:
                raise ValueError(f"Model {display_name} returned empty content")
            
            if not isinstance(response.content, str):
                raise ValueError(f"Model {display_name} returned non-string content: {type(response.content)}")
            
            # Check for the specific keyword in the response
            response_text = response.content.strip().upper()
            if expected_keyword not in response_text:
                raise ValueError(f"Model {display_name} did not respond with required keyword '{expected_keyword}'. Got: '{response.content[:100]}...'")
            
            # Validate token information if available
            if hasattr(response, 'tokens'):
                if not hasattr(response.tokens, 'input_tokens') or not hasattr(response.tokens, 'output_tokens'):
                    raise ValueError(f"Model {display_name} response missing token information")
            
            duration = time.time() - check_start
            self.checks.append(SystemCheckResult(
                name=check_name,
                status=CheckStatus.PASSED,
                message=f"✓ {display_name}",
                duration=duration
            ))
            
        except Exception as e:
            duration = time.time() - check_start
            error_msg = str(e)
            
            # Add more specific error information for common issues
            if "404" in error_msg or "not found" in error_msg.lower():
                error_msg = f"Model {display_name} not found on server"
            elif "connection" in error_msg.lower():
                error_msg = f"Cannot connect to {display_name} server"
            elif "timeout" in error_msg.lower():
                error_msg = f"Model {display_name} request timed out"
            
            self.checks.append(SystemCheckResult(
                name=check_name,
                status=CheckStatus.FAILED,
                message=f"✗ {display_name}",
                duration=duration,
                error=error_msg
            ))
            
            # Log the failure for debugging
            print(f"DEBUG: Model heartbeat failed for {display_name}: {error_msg}")
            
            # Re-raise the exception to ensure the system check fails
            raise RuntimeError(f"Model {display_name} heartbeat failed: {error_msg}")
            
    async def _run_artificial_delay_test(self):
        """Run an artificial delay test as requested."""
        check_start = time.time()
        
        try:
            # Artificial 2-second delay for testing
            await asyncio.sleep(2.0)
            
            duration = time.time() - check_start
            self.checks.append(SystemCheckResult(
                name="Timing Test",
                status=CheckStatus.PASSED,
                message="✓ Artificial delay test",
                duration=duration
            ))
            
        except Exception as e:
            duration = time.time() - check_start
            self.checks.append(SystemCheckResult(
                name="Timing Test",
                status=CheckStatus.FAILED,
                message="✗ Artificial delay test",
                duration=duration,
                error=str(e)
            ))
            
    async def _display_system_check_passed(self):
        """Complete the system check cognition block."""
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Complete the system check cognition block
        check_summary = []
        for check in self.checks:
            if check.status == CheckStatus.PASSED:
                check_summary.append(f"{check.message} ({check.duration:.2f}s)")
                
        await self.scrivener.inscribe(InscriptionEvent(
            event_type=EventType.COGNITION_BLOCK,
            content=f"System Check Complete - All systems operational ({total_duration:.2f}s)",
            metadata={
                "state": "inscribed",
                "system_check": True,
                "status": "passed",
                "wall_clock": current_time,
                "total_duration": total_duration,
                "sub_blocks": check_summary
            }
        ))
        
    async def _display_system_check_failed(self, failed_checks: List[SystemCheckResult]):
        """Display failed system check results."""
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        current_time = datetime.now().strftime("%H:%M:%S")
        
        content = Text()
        content.append("🔍 System Check Failed\n", style="bold red")
        content.append(f"⏰ Wall Clock: {current_time}\n", style="dim white")
        content.append(f"Total Duration: {total_duration:.2f}s\n\n", style="dim white")
        
        # Add all check results
        for check in self.checks:
            if check.status == CheckStatus.PASSED:
                content.append(f"{check.message} ({check.duration:.2f}s)\n", style="green")
            elif check.status == CheckStatus.FAILED:
                content.append(f"{check.message} ({check.duration:.2f}s)\n", style="red")
                if check.error:
                    content.append(f"  Error: {check.error}\n", style="dim red")
        
        content.append(f"\n❌ {len(failed_checks)} system check(s) failed", style="bold red")
        
        await self.scrivener.inscribe(InscriptionEvent(
            event_type=EventType.SYSTEM_MESSAGE,
            content=content,
            metadata={
                "system_check": True,
                "status": "failed",
                "wall_clock": current_time,
                "total_duration": total_duration,
                "failed_checks": len(failed_checks)
            }
        ))
        
    async def _display_system_check_error(self, error: str):
        """Display system check error."""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        content = Text()
        content.append("🔍 System Check Error\n", style="bold red")
        content.append(f"⏰ Wall Clock: {current_time}\n", style="dim white")
        content.append(f"Error: {error}\n", style="red")
        content.append("\n❌ System check failed with error", style="bold red")
        
        await self.scrivener.inscribe(InscriptionEvent(
            event_type=EventType.SYSTEM_MESSAGE,
            content=content,
            metadata={
                "system_check": True,
                "status": "error",
                "wall_clock": current_time,
                "error": error
            }
        ))