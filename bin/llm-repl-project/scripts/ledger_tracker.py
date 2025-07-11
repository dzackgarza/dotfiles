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
        """Start working on a ledger."""
        ledger_path = self.ledger_dir / f"{ledger_name}.md"
        
        if not ledger_path.exists():
            print(f"❌ Ledger not found: {ledger_path}")
            return False
        
        # Parse ledger to extract phases
        phases = self.extract_phases_from_ledger(ledger_path)
        
        # Create TodoWrite tasks for each phase
        todos = []
        for i, phase in enumerate(phases, 1):
            todos.append({
                "content": f"{ledger_name}: {phase['name']} - {phase['description']}",
                "status": "pending",
                "priority": "high" if i <= 2 else "medium",
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
        print(f"✅ Started ledger: {ledger_name}")
        print(f"📋 Created {len(todos)} phase tasks")
        print(f"🎯 Current phase: {phases[0]['name']}")
        
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
                {"name": "Planning", "description": "Review and plan implementation", "tasks": []},
                {"name": "Implementation", "description": "Core development work", "tasks": []},
                {"name": "Testing", "description": "Testing and validation", "tasks": []},
                {"name": "UX Polish", "description": "Final polish and user experience improvements", "tasks": []},
                {"name": "Integration", "description": "Integrate ledger into the main system", "tasks": []},
                {"name": "System Integration", "description": "Integrate ledger into the main system", "tasks": []}
            ]
        
        return phases
    
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
        print("Usage: python ledger_tracker.py <command> [ledger_name]")
        print("Commands: start, next, test, complete, status")
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
        tracker.complete_ledger(sys.argv[2])
    elif command == "status":
        tracker.status_report()
    else:
        print("Invalid command or missing ledger name")

if __name__ == "__main__":
    main()
