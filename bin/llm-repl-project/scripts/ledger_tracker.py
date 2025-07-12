#!/usr/bin/env python3
"""
Ledger Development Tracker

Automates the process of working through V3.1 ledgers:
- Tracks current ledger status
- Creates TodoWrite tasks for phases
- Manages testing and completion workflow
- Archives completed ledgers
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class LedgerTracker:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.ledger_dir = self.project_root / ".ai" / "ledgers" / "v3.1"
        self.status_file = self.ledger_dir / ".ledger_status.json"
        self.load_status()
    
    def load_status(self):
        """Load current ledger status."""
        if self.status_file.exists():
            with open(self.status_file) as f:
                self.status = json.load(f)
        else:
            self.status = {
                "current_ledger": None,
                "completed_ledgers": [],
                "ledger_states": {},
                "last_updated": None
            }
    
    def save_status(self):
        """Save current ledger status."""
        self.status["last_updated"] = datetime.now().isoformat()
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)
    
    def start_ledger(self, ledger_name: str):
        """Start working on a ledger with test-first development."""
        ledger_path = self.ledger_dir / f"{ledger_name}.md"
        
        if not ledger_path.exists():
            print(f"❌ Ledger not found: {ledger_path}")
            return False
        
        # Parse ledger to extract phases and features
        phases = self.extract_phases_from_ledger(ledger_path)
        features = self.extract_features_from_ledger(ledger_path)
        
        # Create TodoWrite tasks with test-first approach
        todos = []
        
        # First, add test creation tasks for all features
        print(f"\n🧪 Creating test-first tasks for {len(features)} features...")
        for j, feature in enumerate(features, 1):
            test_task = {
                "content": f"{ledger_name}: Write failing test for '{feature['name']}'",
                "status": "pending",
                "priority": "high",
                "id": f"{ledger_name}_test_{j}"
            }
            todos.append(test_task)
            
            # Implementation task is blocked until test exists
            impl_task = {
                "content": f"{ledger_name}: Implement '{feature['name']}' to pass test",
                "status": "pending",
                "priority": "high",
                "id": f"{ledger_name}_impl_{j}",
                "depends_on": f"{ledger_name}_test_{j}"
            }
            todos.append(impl_task)
        
        # Then add phase-based coordination tasks
        for i, phase in enumerate(phases, 1):
            todos.append({
                "content": f"{ledger_name}: {phase['name']} - {phase['description']}",
                "status": "pending",
                "priority": "medium",
                "id": f"{ledger_name}_phase_{i}"
            })
        
        # Update status
        self.status["current_ledger"] = ledger_name
        self.status["ledger_states"][ledger_name] = {
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "phases": phases,
            "current_phase": 1
        }
        
        self.save_status()
        
        # Output todos for Claude Code to pick up
        print(f"\n✅ Started ledger: {ledger_name}")
        print(f"📋 Created {len(todos)} tasks ({len(features)*2} test+impl, {len(phases)} phases)")
        print(f"🧪 Test-First Development: Write tests before implementation!")
        print(f"🎯 First task: Write failing tests for features")
        
        # Write todos to a file that can be imported
        todos_file = self.project_root / f".todos_{ledger_name}.json"
        with open(todos_file, 'w') as f:
            json.dump(todos, f, indent=2)
        
        print(f"💾 Todo tasks written to: {todos_file}")
        return True
    
    def extract_phases_from_ledger(self, ledger_path: Path) -> List[Dict[str, str]]:
        """Extract implementation phases from ledger markdown."""
        with open(ledger_path) as f:
            content = f.read()
        
        phases = []
        in_implementation_plan = False
        current_phase = None
        
        for line in content.split('\n'):
            if "### Implementation Plan" in line or "## Implementation Plan" in line:
                in_implementation_plan = True
                continue
            
            if in_implementation_plan:
                if line.startswith('## ') and "Phase" not in line:
                    break  # End of implementation section
                
                if re.match(r'\d+\. \*\*Phase ', line):
                    # Extract phase info
                    phase_line = line.strip()
                    if '**' in phase_line:
                        phase_name = phase_line.split('**')[1].replace('Phase ', 'Phase ')
                        phases.append({
                            "name": phase_name,
                            "description": "",
                            "tasks": []
                        })
                        current_phase = len(phases) - 1
                
                elif line.startswith('   - ') and current_phase is not None:
                    # Extract task
                    task = line.strip()[2:]  # Remove "- "
                    phases[current_phase]["tasks"].append(task)
                
                elif line.strip() and current_phase is not None and not line.startswith('#'):
                    # Extract description
                    if not phases[current_phase]["description"]:
                        phases[current_phase]["description"] = line.strip()
        
        # Fallback phases if none found
        if not phases:
            phases = [
                {"name": "Test Planning", "description": "Write failing acceptance tests", "tasks": []},
                {"name": "Implementation", "description": "Make tests pass", "tasks": []},
                {"name": "Testing", "description": "Verify all tests green", "tasks": []},
                {"name": "UX Polish", "description": "Final polish with test coverage", "tasks": []},
                {"name": "Integration", "description": "Integrate with passing tests", "tasks": []}
            ]
        
        return phases
    
    def extract_features_from_ledger(self, ledger_path: Path) -> List[Dict[str, str]]:
        """Extract testable features from ledger markdown."""
        with open(ledger_path) as f:
            content = f.read()
        
        features = []
        
        # Look for user-visible behaviors or features
        for line in content.split('\n'):
            # Match patterns like "- User can...", "- Display...", "- Show..."
            if re.match(r'^\s*[-*]\s+(User|Users|Display|Show|Enable|Allow|Support)', line, re.IGNORECASE):
                feature_text = line.strip().lstrip('-*').strip()
                features.append({
                    "name": feature_text[:50],  # Truncate for readability
                    "description": feature_text
                })
            # Also match numbered items describing features
            elif re.match(r'^\s*\d+\.\s+(User|Users|Display|Show|Enable|Allow|Support)', line, re.IGNORECASE):
                feature_text = re.sub(r'^\s*\d+\.\s*', '', line).strip()
                features.append({
                    "name": feature_text[:50],
                    "description": feature_text
                })
        
        # If no specific features found, create generic ones based on ledger name
        if not features:
            base_name = ledger_path.stem.replace('-', ' ').title()
            features = [
                {"name": f"{base_name} basic functionality", "description": f"Core {base_name} features work"},
                {"name": f"{base_name} user interaction", "description": f"Users can interact with {base_name}"},
                {"name": f"{base_name} error handling", "description": f"{base_name} handles errors gracefully"}
            ]
        
        return features[:10]  # Limit to avoid too many tasks
    
    def next_phase(self, ledger_name: str):
        """Move to next phase of current ledger."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not started: {ledger_name}")
            return False
        
        state = self.status["ledger_states"][ledger_name]
        current_phase = state["current_phase"]
        total_phases = len(state["phases"])
        
        if current_phase >= total_phases:
            print(f"✅ All phases complete for {ledger_name}")
            return self.complete_ledger(ledger_name)
        
        # Move to next phase
        state["current_phase"] = current_phase + 1
        next_phase_info = state["phases"][current_phase]  # 0-indexed
        
        self.save_status()
        
        print(f"➡️ Moving to next phase: {next_phase_info['name']}")
        print(f"📝 Description: {next_phase_info['description']}")
        return True
    
    def test_ledger(self, ledger_name: str):
        """Run tests for current ledger."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not started: {ledger_name}")
            return False
        
        print(f"🧪 Testing ledger: {ledger_name}")
        print(f"📋 Checking test-first compliance...")
        
        # First verify all source files have tests
        missing_tests = self.check_test_coverage(ledger_name)
        if missing_tests:
            print(f"\n⚠️  Warning: {len(missing_tests)} source files lack tests:")
            for file in missing_tests:
                print(f"  ❌ {file}")
            print(f"\n💡 Create tests with: just create-test <feature>")
        
        # Run relevant tests based on ledger type
        test_commands = {
            "live-inscribed-block-system": ["pytest tests/test_live_blocks.py -v"],
            "mock-cognition-pipeline": ["pytest tests/test_cognition_sub_blocks.py -v"],
            "timeline-ui-widget": ["pytest tests/test_timeline.py -v"],
            "rich-content-display": ["pytest tests/test_rich_display.py -v"]
        }
        
        commands = test_commands.get(ledger_name, ["pytest tests/ -v"])
        
        for cmd in commands:
            print(f"  Running: {cmd}")
            os.system(cmd)
        
        # Mark testing phase as complete
        state = self.status["ledger_states"][ledger_name]
        if state["current_phase"] < len(state["phases"]):
            current_phase = state["phases"][state["current_phase"] - 1]
            if "test" in current_phase["name"].lower():
                return self.next_phase(ledger_name)
        
        return True
    
    def check_test_coverage(self, ledger_name: str) -> List[str]:
        """Check which source files lack tests."""
        src_dir = self.project_root / "V3-minimal" / "src"
        test_dir = self.project_root / "V3-minimal" / "tests"
        
        missing_tests = []
        
        # Check all Python files in src/
        for src_file in src_dir.rglob("*.py"):
            if src_file.name == "__init__.py":
                continue
                
            # Derive expected test file
            test_name = f"test_{src_file.stem}.py"
            test_file = test_dir / test_name
            
            if not test_file.exists():
                missing_tests.append(str(src_file.relative_to(src_dir)))
        
        return missing_tests
    
    def complete_ledger(self, ledger_name: str):
        """Complete a ledger and archive it."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not started: {ledger_name}")
            return False
        
        # Mark as completed
        self.status["completed_ledgers"].append({
            "name": ledger_name,
            "completed_at": datetime.now().isoformat()
        })
        
        self.status["ledger_states"][ledger_name]["status"] = "completed"
        self.status["ledger_states"][ledger_name]["completed_at"] = datetime.now().isoformat()
        
        # Clear current ledger if this was it
        if self.status["current_ledger"] == ledger_name:
            self.status["current_ledger"] = None
        
        self.save_status()
        
        # Archive the ledger
        ledger_file = self.ledger_dir / f"{ledger_name}.md"
        archive_dir = self.ledger_dir / "completed"
        archive_dir.mkdir(exist_ok=True)
        
        # Move to archive with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"{ledger_name}_{timestamp}.md"
        
        if ledger_file.exists():
            ledger_file.rename(archive_file)
            print(f"📁 Archived ledger to: {archive_file}")
        
        # Clean up todo files
        todos_file = self.project_root / f".todos_{ledger_name}.json"
        if todos_file.exists():
            todos_file.unlink()
        
        print(f"✅ Completed ledger: {ledger_name}")
        
        # Suggest next ledger
        self.suggest_next_ledger()
        return True
    
    def request_review(self, ledger_name: str):
        """Request human review for ledger completion."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not started: {ledger_name}")
            return False
        
        # Mark as pending review
        self.status["ledger_states"][ledger_name]["status"] = "pending_review"
        self.status["ledger_states"][ledger_name]["review_requested_at"] = datetime.now().isoformat()
        
        # Extract promised behaviors from ledger
        ledger_file = self.ledger_dir / f"{ledger_name}.md"
        behaviors = self.extract_user_behaviors(ledger_file)
        
        self.status["ledger_states"][ledger_name]["promised_behaviors"] = behaviors
        self.save_status()
        
        print(f"📋 Review requested for: {ledger_name}")
        print(f"🎯 Promised user-visible behaviors:")
        for i, behavior in enumerate(behaviors, 1):
            print(f"  {i}. {behavior}")
        
        print(f"\n🔍 Human reviewer must verify these behaviors work in the UI")
        print(f"✅ To approve: python scripts/ledger_tracker.py approve-review {ledger_name}")
        print(f"❌ To reject: python scripts/ledger_tracker.py reject-review {ledger_name} 'feedback'")
        return True
    
    def approve_review(self, ledger_name: str):
        """Approve ledger completion after human verification."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not found: {ledger_name}")
            return False
        
        state = self.status["ledger_states"][ledger_name]
        if state.get("status") != "pending_review":
            print(f"❌ Ledger not pending review: {ledger_name}")
            return False
        
        print(f"✅ Human approved: {ledger_name}")
        return self.complete_ledger(ledger_name)
    
    def reject_review(self, ledger_name: str, feedback: str):
        """Reject ledger completion with feedback."""
        if ledger_name not in self.status["ledger_states"]:
            print(f"❌ Ledger not found: {ledger_name}")
            return False
        
        state = self.status["ledger_states"][ledger_name]
        state["status"] = "needs_rework"
        state["rejection_feedback"] = feedback
        state["rejected_at"] = datetime.now().isoformat()
        
        self.save_status()
        
        print(f"❌ Ledger rejected: {ledger_name}")
        print(f"📝 Feedback: {feedback}")
        print(f"🔄 Status changed to: needs_rework")
        return True
    
    def extract_user_behaviors(self, ledger_file: Path) -> List[str]:
        """Extract user-visible behaviors from ledger markdown."""
        if not ledger_file.exists():
            return []
        
        with open(ledger_file) as f:
            content = f.read()
        
        behaviors = []
        in_behaviors_section = False
        
        for line in content.split('\n'):
            if "user-visible behaviors" in line.lower() or "observable behaviors" in line.lower():
                in_behaviors_section = True
                continue
            
            if in_behaviors_section:
                if line.startswith('##') and 'behavior' not in line.lower():
                    break  # End of behaviors section
                
                # Extract numbered or bulleted behaviors
                if re.match(r'\d+\.\s+', line.strip()) or line.strip().startswith('- '):
                    behavior = re.sub(r'^\d+\.\s*|\-\s*', '', line.strip())
                    if behavior:
                        behaviors.append(behavior)
        
        # Fallback: extract from any section mentioning "user sees" or "user can"
        if not behaviors:
            for line in content.split('\n'):
                if ('user sees' in line.lower() or 'user can' in line.lower() or 
                    'users see' in line.lower() or 'displays' in line.lower()):
                    clean_line = line.strip('- ').strip()
                    if clean_line and len(clean_line) > 20:  # Reasonable behavior description
                        behaviors.append(clean_line)
        
        return behaviors[:10]  # Limit to most important behaviors

    def suggest_next_ledger(self):
        """Suggest the next ledger to work on."""
        v3_1_priority = [
            "live-inscribed-block-system",
            "mock-cognition-pipeline", 
            "rich-content-display-engine",
            "timeline-ui-widget",
            "mock-data-framework",
            "event-driven-ui-updates",
            "mock-plugin-system",
            "input-and-command-system"
        ]
        
        completed_names = [l["name"] for l in self.status["completed_ledgers"]]
        
        for ledger in v3_1_priority:
            if ledger not in completed_names:
                ledger_file = self.ledger_dir / f"{ledger}.md"
                if ledger_file.exists():
                    print(f"💡 Suggested next ledger: {ledger}")
                    return ledger
        
        print("🎉 All V3.1 ledgers completed!")
        return None
    
    def status_report(self):
        """Generate status report."""
        print("\n📊 Ledger Development Status")
        print("=" * 40)
        
        if self.status["current_ledger"]:
            current = self.status["current_ledger"]
            state = self.status["ledger_states"][current]
            current_phase = state["current_phase"]
            total_phases = len(state["phases"])
            
            print(f"🎯 Current Ledger: {current}")
            print(f"📈 Progress: Phase {current_phase}/{total_phases}")
            
            if current_phase <= len(state["phases"]):
                phase_info = state["phases"][current_phase - 1]
                print(f"🔄 Current Phase: {phase_info['name']}")
                print(f"📝 Description: {phase_info['description']}")
        else:
            print("🔄 No active ledger")
        
        print(f"\n✅ Completed: {len(self.status['completed_ledgers'])}")
        for ledger in self.status["completed_ledgers"]:
            print(f"  - {ledger['name']}")
        
        next_ledger = self.suggest_next_ledger()
        if next_ledger:
            print(f"\n💡 Next suggested: {next_ledger}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python ledger_tracker.py <command> [ledger_name] [feedback]")
        print("Commands: start, next, test, complete, status, request-review, approve-review, reject-review")
        return
    
    tracker = LedgerTracker()
    command = sys.argv[1]
    
    if command == "start" and len(sys.argv) > 2:
        tracker.start_ledger(sys.argv[2])
    elif command == "next" and len(sys.argv) > 2:
        tracker.next_phase(sys.argv[2])
    elif command == "test" and len(sys.argv) > 2:
        tracker.test_ledger(sys.argv[2])
    elif command == "complete" and len(sys.argv) > 2:
        if os.geteuid() != 0:
            print("❌ Error: The 'complete' command requires sudo privileges for human sign-off.")
            print("Run as: sudo python scripts/ledger_tracker.py complete <ledger-name>")
            return
        tracker.complete_ledger(sys.argv[2])
    elif command == "request-review" and len(sys.argv) > 2:
        tracker.request_review(sys.argv[2])
    elif command == "approve-review" and len(sys.argv) > 2:
        tracker.approve_review(sys.argv[2])
    elif command == "reject-review" and len(sys.argv) > 3:
        tracker.reject_review(sys.argv[2], sys.argv[3])
    elif command == "status":
        tracker.status_report()
    else:
        print("Invalid command or missing ledger name")

if __name__ == "__main__":
    main()
