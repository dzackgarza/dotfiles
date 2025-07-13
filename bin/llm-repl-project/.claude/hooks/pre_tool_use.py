#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
PreToolUse Hook - Security Validation and Access Control

CLAUDE COMMUNICATION METHODS:
================================================================================
This hook can directly communicate with Claude using these methods:

1. EXIT CODE 2 + stderr:
   - Blocks tool execution completely
   - stderr content is automatically fed to Claude as an error message
   - Claude receives the error and must respond accordingly
   - Example: sys.exit(2) with print("BLOCKED: reason", file=sys.stderr)

2. JSON OUTPUT + EXIT CODE 0:
   Advanced control via stdout JSON:
   
   a) Decision Control:
      {"decision": "block", "reason": "explanation"} 
      - Blocks tool, reason shown to Claude
      
      {"decision": "approve", "reason": "explanation"}
      - Bypasses permissions, reason shown to user (NOT Claude)
      
   b) Session Control:
      {"continue": false, "stopReason": "reason"}
      - Stops Claude entirely, reason shown to user (NOT Claude)

3. NO COMMUNICATION (Exit Code 0, no stderr):
   - Tool proceeds normally
   - Only logging occurs, no Claude interaction

CURRENT IMPLEMENTATION: Uses method #1 (Exit Code 2 + stderr) for security blocks
================================================================================
"""

import json
import sys
import re
from pathlib import Path

# ================================================================================
# EXTENSIBLE SECURITY VALIDATORS
# ================================================================================
# Add new validators here by creating functions that follow the pattern:
# def is_[type]_violation(tool_name, tool_input) -> tuple[bool, str]:
#     """Return (is_violation, reason) tuple"""

def is_dangerous_rm_command(tool_name, tool_input):
    """
    Comprehensive detection of dangerous rm commands.
    Matches various forms of rm -rf and similar destructive patterns.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    # Normalize command by removing extra spaces and converting to lowercase
    normalized = ' '.join(command.lower().split())
    
    # Pattern 1: Standard rm -rf variations
    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf, etc.
        r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
        r'\brm\s+--recursive\s+--force',  # rm --recursive --force
        r'\brm\s+--force\s+--recursive',  # rm --force --recursive
        r'\brm\s+-r\s+.*-f',  # rm -r ... -f
        r'\brm\s+-f\s+.*-r',  # rm -f ... -r
    ]
    
    # Check for dangerous patterns
    for pattern in patterns:
        if re.search(pattern, normalized):
            message = """Dangerous rm command blocked.

Before removing files, consider:
• Did you create a .bak backup first?
• Could you move to an archive/ directory instead?
• Is this truly meant to be permanently deleted?
• Have you confirmed this won't break dependencies?

Safer alternatives:
• mv file.txt file.txt.bak
• mkdir -p archive && mv files/ archive/
• Use git to track deletions if this is a repo"""
            return True, message
    
    # Pattern 2: Check for rm with recursive flag targeting dangerous paths
    dangerous_paths = [
        r'/',           # Root directory
        r'/\*',         # Root with wildcard
        r'~',           # Home directory
        r'~/',          # Home directory path
        r'\$HOME',      # Home environment variable
        r'\.\.',        # Parent directory references
        r'\*',          # Wildcards in general rm -rf context
        r'\.',          # Current directory
        r'\.\s*$',      # Current directory at end of command
    ]
    
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):  # If rm has recursive flag
        for path in dangerous_paths:
            if re.search(path, normalized):
                message = f"""Extremely dangerous rm command targeting {path} blocked.

This could destroy your entire system or important data!

Critical questions:
• Are you absolutely certain this is what you want?
• Have you backed up everything important?
• Is there a specific reason you need to delete rather than archive?
• Could you accomplish this goal more safely?

Much safer approach:
• Create timestamped archives: mkdir -p archive/$(date +%Y%m%d_%H%M%S) && mv target archive/
• Use git if this is a repository
• Consider using trash utilities instead of rm"""
                return True, message
    
    return False, ""

def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                message = """Access to .env files blocked for security.

.env files contain sensitive data like API keys and passwords.

Why is this blocked?
• Prevents accidental exposure of secrets
• Stops credentials from being logged or displayed
• Protects against unintentional commits to version control

Safe alternatives:
• Use .env.sample or .env.example for templates
• Check environment variables: echo $VARIABLE_NAME
• Use dedicated secret management tools
• Read documentation instead of the actual .env file"""
                return True, message
        
        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
            ]
            
            for pattern in env_patterns:
                if re.search(pattern, command):
                    message = """Environment file access via bash blocked.

This prevents exposure of sensitive credentials.

Questions to consider:
• Do you really need to access the .env file directly?
• Are you trying to debug environment variables?
• Is this for documentation or template creation?

Safer approaches:
• Use printenv or echo $VAR_NAME to check variables
• Create .env.sample files for templates
• Use source .env && echo $VAR (if you must)
• Check application logs instead of reading .env directly"""
                    return True, message
    
    return False, ""


def is_network_exposure(tool_name, tool_input):
    """
    Detect commands that might expose services to the network unsafely.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    normalized = ' '.join(command.lower().split())
    
    network_patterns = [
        r'\b(python|python3)\s+.*-m\s+http\.server.*0\.0\.0\.0',  # Python HTTP server on all interfaces
        r'\bnc\s+.*-l.*0\.0\.0\.0',                               # netcat listening on all interfaces
        r'\b(node|npm)\s+.*start.*0\.0\.0\.0',                    # Node server on all interfaces
    ]
    
    for pattern in network_patterns:
        if re.search(pattern, normalized):
            message = """Unsafe network exposure blocked.

Binding to 0.0.0.0 exposes services to ALL network interfaces.

Security concerns:
• Makes your service accessible from any connected network
• Exposes development servers to potential attackers
• Could leak sensitive data or development code
• May violate corporate security policies

Questions to ask:
• Do you really need external access to this service?
• Is this for local development or production?
• Have you considered security implications?

Safer alternatives:
• Bind to localhost/127.0.0.1 for local development only
• Use proper authentication and HTTPS for external access
• Set up a reverse proxy with security controls
• Use VPN or SSH tunneling for remote access"""
            return True, message
    
    return False, ""

def is_package_manager_usage(tool_name, tool_input):
    """
    Block system package manager usage and guide toward proper alternatives.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    normalized = ' '.join(command.lower().split())
    
    # System package managers that should be blocked
    package_manager_patterns = [
        r'\bpacman\s+',                    # Arch Linux pacman
        r'\byay\s+',                       # AUR helper yay
        r'\bparu\s+',                      # AUR helper paru
        r'\bapt-get\s+',                   # Debian/Ubuntu apt-get
        r'\bapt\s+install',                # Debian/Ubuntu apt
        r'\bdnf\s+',                       # Fedora dnf
        r'\byum\s+',                       # RHEL/CentOS yum
        r'\bzypper\s+',                    # openSUSE zypper
        r'\bbrew\s+install',               # macOS Homebrew
        r'\bsnap\s+install',               # Ubuntu Snap
        r'\bflatpak\s+install',            # Flatpak
        r'\bchoco\s+install',              # Windows Chocolatey
        r'\bwinget\s+install',             # Windows Package Manager
        r'\bpip\s+install\s+(?!.*--user)',  # pip without --user flag
        r'\bpip3\s+install\s+(?!.*--user)', # pip3 without --user flag
    ]
    
    for pattern in package_manager_patterns:
        if re.search(pattern, normalized):
            message = """System package manager usage blocked.

You should NOT install system packages. Here's why:

Problems with system package installation:
• Pollutes the global system environment
• Can break existing system functionality
• Requires elevated privileges (security risk)
• Creates dependency conflicts
• Makes environments non-reproducible

What you SHOULD do instead:
• Use virtual environments: python -m venv .venv && source .venv/bin/activate
• Use user-level installs: pip install --user package_name
• Use project-specific tools: npm install, pdm add, poetry add
• Use containerized environments: docker, podman

If a tool absolutely MUST be installed system-wide:
• Use notify-send to ask the user to install it manually
• DO NOT attempt fallbacks or workarounds
• DO NOT compromise on tool quality
• Example: notify-send "Please install: sudo pacman -S package-name"

The user maintains control over their system packages."""
            return True, message
    
    return False, ""

def is_sudo_command_usage(tool_name, tool_input):
    """
    Block ALL sudo command usage with educational messaging.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    normalized = ' '.join(command.lower().split())
    
    # Block ANY sudo usage
    if re.search(r'\bsudo\s+', normalized):
        message = """ALL sudo commands are blocked.

Sudo gives you system administrator privileges, which is dangerous.

Why sudo is blocked:
• Can cause irreversible system damage
• Security risk - elevated privileges
• Should not be needed for development tasks
• User should maintain control over their system

What to do instead:
• Use virtual environments for isolation
• Use user-level package managers (pip --user, npm install)
• Work within your user directory
• Use containerization for system-level needs

If you absolutely need system-level changes:
• Use notify-send to ask the user to run the command
• Example: notify-send "Please run: sudo systemctl enable service-name"
• DO NOT attempt to work around this restriction
• The user decides what gets elevated privileges

Remember: Good development practices shouldn't require root access."""
        return True, message
    
    return False, ""

def is_textual_gui_app_launch(tool_name, tool_input):
    """
    Block all possible ways of running the Textual GUI app in V3-minimal directory.
    Directs users to proper testing workflow with user stories and canonical Pilot tests.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    normalized = ' '.join(command.lower().split())
    
    # Patterns that would launch the GUI app
    gui_launch_patterns = [
        r'\bpdm\s+run\s+python\s+-m\s+src\.main',              # pdm run python -m src.main
        r'\bjust\s+run\b',                                      # just run
        r'\bpython\s+src/main\.py',                            # python src/main.py
        r'\bpython3\s+src/main\.py',                           # python3 src/main.py
        r'\bpython\s+-m\s+src\.main',                          # python -m src.main
        r'\bpython3\s+-m\s+src\.main',                         # python3 -m src.main
        r'\bpython\s+.*src.*main\.py',                         # variations with paths
        r'\bpython3\s+.*src.*main\.py',                        # variations with paths
        r'\b\.\/src\/main\.py',                                # ./src/main.py
        r'\bsrc\/main\.py',                                    # direct execution
    ]
    
    # Check if we're in V3-minimal directory context
    import os
    current_dir = os.getcwd()
    if 'V3-minimal' in current_dir or any(pattern_match for pattern_match in [
        re.search(pattern, normalized) for pattern in gui_launch_patterns
    ] if pattern_match):
        
        for pattern in gui_launch_patterns:
            if re.search(pattern, normalized):
                return True, ("GUI app launch blocked. ALL GUI tests must: 1) Set up a user story, "
                            "2) Integrate it into the canonical Pilot tests, 3) Set up and review the "
                            "screenshot grid instead of running the app directly.")
    
    return False, ""

def check_tdd_workflow_reminders(tool_name, tool_input):
    """
    Provide TDD workflow reminders based on tool usage patterns.
    These are educational reminders, not blocks.
    """
    # TDD reminders for code editing
    if tool_name in ['Edit', 'Write', 'MultiEdit']:
        file_path = tool_input.get('file_path', '')
        if file_path.endswith(('.py', '.js', '.ts')) and 'src/' in file_path:
            print("🧪 TDD REMINDER: Are you implementing a task with user story validation?", file=sys.stderr)
            print("   Run: task-master test-story --id=<task> to verify story passes", file=sys.stderr)
            
        # Sacred GUI specific reminders
        content = tool_input.get('new_string', '') or tool_input.get('content', '')
        if content and ('Sacred' in content or 'Timeline' in content):
            print("🏛️ SACRED GUI: Ensure story demonstrates 3-area layout", file=sys.stderr)
            print("   Required: Timeline/Workspace/Input visibility in temporal grid", file=sys.stderr)
    
    # Task Master command interception
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        
        # Block set-status=done, require complete-with-story
        if 'task-master set-status' in command and '--status=done' in command:
            message = """Task completion command blocked.

⚠️  STOP: Use 'task-master complete-with-story' instead of 'set-status=done'

Required for completion:
• Visual proof through temporal grid validation
• User story must pass before marking done
• Ensures TDD compliance

Correct command:
task-master complete-with-story --id=<task-id>

This enforces the requirement for visual validation."""
            return True, message
            
        # Git commit TDD check
        if command.startswith('git commit'):
            print("📋 TDD CHECK: All completed tasks have user story validation?", file=sys.stderr)
            print("   Verify: Pre-commit hook will validate this automatically", file=sys.stderr)
            
        # Task Master next command guidance
        if 'task-master next' in command:
            print("🎯 NEXT STEP: Generate user story BEFORE coding", file=sys.stderr)
            print("   Command: task-master generate-story --id=<task-id>", file=sys.stderr)
    
    return False, ""

# ================================================================================
# SECURITY VALIDATOR REGISTRY
# ================================================================================
# Add new validators to this list to automatically include them in security checks
SECURITY_VALIDATORS = [
    is_dangerous_rm_command,
    is_env_file_access,
    is_package_manager_usage,
    is_sudo_command_usage,
    is_network_exposure,
    is_textual_gui_app_launch,
    check_tdd_workflow_reminders,
]

def run_security_validation(tool_name, tool_input):
    """
    Run all registered security validators.
    Returns (is_blocked, reason) tuple.
    """
    for validator in SECURITY_VALIDATORS:
        is_violation, reason = validator(tool_name, tool_input)
        if is_violation:
            return True, reason
    return False, ""

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Run all security validators
        is_blocked, reason = run_security_validation(tool_name, tool_input)
        
        if is_blocked:
            print(f"BLOCKED: {reason}", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Simple logging like canonical hooks
        log_dir = Path.cwd() / '.claude' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()