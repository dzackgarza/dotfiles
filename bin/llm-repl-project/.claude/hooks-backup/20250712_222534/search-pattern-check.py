#!/usr/bin/env python3
"""
Search Pattern Check - Questions the need for extensive searching

When Claude uses search tools extensively, this hook occasionally asks whether
the difficulty in finding things indicates a structural or design problem.
"""

import json
import sys
import random
from hook_logger import log_hook_execution

def main():
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get('tool_name', '')
    
    # Only trigger on search-related tools
    if tool_name not in ['Grep', 'Glob', 'Task', 'Read']:
        log_hook_execution("search-pattern-check", tool_name, "approve", "Not a search tool")
        sys.exit(0)  # Approve - exit code 0
    
    # Different frequencies for different tools
    if tool_name == 'Read':
        trigger_chance = 5  # 1 in 5 for Read
    else:
        trigger_chance = 4  # 1 in 4 for search tools
    
    if random.randint(1, trigger_chance) != 1:
        log_hook_execution("search-pattern-check", tool_name, "approve", f"Random check not triggered (1/{trigger_chance})")
        sys.exit(0)  # Approve - exit code 0
    
    # Different messages for different search patterns
    search_questions = [
        "🤔 You've been searching everywhere for this - if it's not in the intuitive place, isn't that a design problem?",
        "🏗️ When code is hard to find, that's often a structural issue. Should this be reorganized?",
        "📍 If you can't find it where you'd expect it, maybe it's in the wrong place?",
        "🗺️ Extensive searching suggests poor organization. Is the codebase structure fighting you?",
        "🎯 The best code is discoverable. If you're hunting for it, should it be moved somewhere obvious?",
        "🔍 All this searching... maybe the real problem is that things aren't where they should be?",
        "📂 Good architecture makes things easy to find. Is this a code organization problem?",
        "🧩 If the logical place doesn't have it, perhaps the logic needs rethinking?",
        "🚪 When the front door isn't where you expect it, maybe the house needs redesigning?",
        "💡 Searching this hard suggests the code structure doesn't match mental models. Time to refactor?",
        "🎪 If finding code feels like a treasure hunt, the treasure might be buried too deep.",
        "🏛️ Architecture should guide you to the right place. Is this architecture misleading you?",
        "🧭 Lost in the codebase? Maybe the map (structure) needs redrawing, not more searching.",
        "🎨 If intuition fails to find it, the design might be counter-intuitive. Consider restructuring?",
        "🔄 Circular searching often means circular dependencies. Is the architecture too tangled?",
        "⏰ You've been working on this for a while - isn't that a code complexity issue?",
        "📚 If it takes this long to understand, maybe the code needs better documentation?",
        "🕐 Time spent searching is time not spent building. Is this a documentation problem?",
        "🤷 When simple tasks take forever, the code might be too complex. Time to simplify?",
        "📖 You've been reading for a while - shouldn't good code be self-explanatory?",
        "⏳ All this time investigating... is the code lacking clear documentation?",
        "🔬 Deep diving this much suggests the code isn't transparent. Add clarifying comments?",
        "⌛ If understanding takes this long, imagine onboarding a new developer. Document better?",
        "🎯 You've been at this for a while - is the complexity justified or just accidental?",
        "🚧 Long investigation times often indicate missing architectural documentation."
    ]
    
    # Context-specific additions based on search type
    if tool_name == 'Grep':
        grep_specific = [
            "🎣 Grep fishing expeditions suggest the code isn't self-documenting. Add better names?",
            "📝 If you need grep to understand the code flow, the code might need clearer organization.",
            "🔤 Searching for string patterns? Maybe the code needs better naming conventions."
        ]
        search_questions.extend(grep_specific)
    elif tool_name == 'Glob':
        glob_specific = [
            "📁 Glob patterns suggest you don't know where files live. Time for a better folder structure?",
            "🗂️ If file locations aren't predictable, maybe follow a standard project layout?",
            "🏷️ Wildcarding through directories? Consider more descriptive file organization."
        ]
        search_questions.extend(glob_specific)
    
    message = random.choice(search_questions)
    
    # Sometimes add a follow-up thought
    if random.randint(1, 3) == 1:
        follow_ups = [
            "\n\n💭 Before more searching, consider: would refactoring make this unnecessary?",
            "\n\n🤷 Maybe the answer isn't finding it, but questioning why it's hidden.",
            "\n\n🎯 Sometimes the best search is reorganizing so searching isn't needed.",
            "\n\n🏗️ If V3 doesn't have this search problem, what did they do differently?"
        ]
        message += random.choice(follow_ups)
    
    log_hook_execution("search-pattern-check", tool_name, "block", f"Triggered question: {message}")
    
    # Use stderr + exit code 2 to show message to Claude
    print(message, file=sys.stderr)
    sys.exit(2)  # Show message to Claude, then continue

if __name__ == "__main__":
    main()