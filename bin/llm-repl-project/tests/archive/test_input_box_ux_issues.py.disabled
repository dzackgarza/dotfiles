#!/usr/bin/env python3
"""
Input Box UX Issue Detection Tests

These tests specifically catch the UX problems we're seeing:
1. Visible escape sequences in output
2. Excessive redrawing/flashing 
3. Poor cursor management
4. Raw terminal control codes appearing

These tests MUST FAIL when UX issues are present.
"""

import unittest
import pexpect
import sys
import re
import time


class InputBoxUXIssueTests(unittest.TestCase):
    """
    Tests that specifically catch UX issues in input box implementation.
    
    These tests are designed to FAIL when we have:
    - Visible escape sequences
    - Excessive redrawing
    - Poor cursor management
    - Raw terminal codes in output
    """
    
    def spawn_repl(self):
        """Spawn a new REPL instance for testing."""
        return pexpect.spawn('python', ['src/main.py', '--config', 'debug'], timeout=10)
    
    def test_no_visible_escape_sequences(self):
        """UX ISSUE: Test that no escape sequences are visible in output."""
        print("\n🚨 TESTING FOR VISIBLE ESCAPE SEQUENCES")
        print("=" * 60)
        print("EXPECTED: No escape sequences like [3A, [K should be visible")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send input to trigger input box updates
            print("\n🔍 SENDING INPUT TO TRIGGER ESCAPE SEQUENCES...")
            child.sendline('Test')
            
            # Wait for processing
            child.expect('User_Input', timeout=5)
            
            # Get all output
            output = child.before.decode() + child.after.decode()
            
            print("🔍 SCANNING FOR VISIBLE ESCAPE SEQUENCES...")
            
            # Look for common escape sequences that shouldn't be visible
            escape_patterns = [
                r'\[3A',     # Move cursor up 3 lines
                r'\[K',      # Clear line
                r'\[2A',     # Move cursor up 2 lines
                r'\[1A',     # Move cursor up 1 line
                r'\[0m',     # Reset formatting (sometimes visible)
                r'\033\[',   # Raw escape sequences
                r'\x1b\[',   # Hex escape sequences
            ]
            
            violations = []
            for pattern in escape_patterns:
                matches = re.findall(pattern, output)
                if matches:
                    violations.append(f"Found {len(matches)} instances of '{pattern}'")
            
            if violations:
                print("❌ ESCAPE SEQUENCE VIOLATIONS FOUND:")
                for violation in violations:
                    print(f"   • {violation}")
                
                # Show context around violations
                for pattern in escape_patterns:
                    for match in re.finditer(pattern, output):
                        start = max(0, match.start() - 20)
                        end = min(len(output), match.end() + 20)
                        context = output[start:end]
                        print(f"   Context: {repr(context)}")
                
                self.fail(f"""
🚨 VISIBLE ESCAPE SEQUENCES DETECTED 🚨

EXPECTED: Escape sequences should be hidden from user
ACTUAL: Found visible escape sequences in output

VIOLATIONS:
{chr(10).join(f'  • {v}' for v in violations)}

UX ISSUE: Escape sequences are appearing in user-visible output.
This creates a poor user experience with visible cursor control codes.

Sample output: {repr(output[:300])}
""")
            else:
                print("✅ SUCCESS: No visible escape sequences detected")
                
        finally:
            child.close()
        
        print("\n🎉 ESCAPE SEQUENCE VALIDATION COMPLETE!")
        print("✅ No visible escape sequences in output")
    
    def test_no_excessive_redrawing(self):
        """UX ISSUE: Test that input box doesn't redraw excessively."""
        print("\n🚨 TESTING FOR EXCESSIVE REDRAWING")
        print("=" * 60)
        print("EXPECTED: Input box should not redraw for every character")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send a short input
            print("\n🔍 SENDING SHORT INPUT...")
            child.sendline('Hello')
            
            # Wait for processing
            child.expect('User_Input', timeout=5)
            
            # Get all output
            output = child.before.decode() + child.after.decode()
            
            print("🔍 COUNTING INPUT BOX REDRAWS...")
            
            # Count how many times input boxes are drawn
            # Each box has distinctive border patterns
            box_patterns = [
                r'╭─+╮',  # Top border
                r'╰─+╯',  # Bottom border
                r'│.*>',  # Left border with prompt
            ]
            
            redraw_counts = {}
            for pattern in box_patterns:
                matches = re.findall(pattern, output)
                redraw_counts[pattern] = len(matches)
            
            # For a 5-character input, we should see:
            # 1. Initial empty box
            # 2. Final box with complete input
            # NOT: 5+ boxes (one per character)
            
            total_redraws = sum(redraw_counts.values())
            expected_max = 10  # Reasonable upper bound
            
            print(f"📊 BOX REDRAW ANALYSIS:")
            for pattern, count in redraw_counts.items():
                print(f"   {pattern}: {count} instances")
            print(f"   Total redraws: {total_redraws}")
            
            if total_redraws > expected_max:
                print(f"❌ EXCESSIVE REDRAWING DETECTED: {total_redraws} > {expected_max}")
                
                self.fail(f"""
🚨 EXCESSIVE REDRAWING DETECTED 🚨

EXPECTED: Input box should redraw minimally (≤{expected_max} times)
ACTUAL: Found {total_redraws} box redraws for 5-character input

UX ISSUE: Input box is redrawing too frequently.
This creates a poor user experience with flashing/flickering.

REDRAW BREAKDOWN:
{chr(10).join(f'  {pattern}: {count}' for pattern, count in redraw_counts.items())}

Sample output: {repr(output[:400])}
""")
            else:
                print(f"✅ SUCCESS: Reasonable redraw count ({total_redraws} ≤ {expected_max})")
                
        finally:
            child.close()
        
        print("\n🎉 REDRAW VALIDATION COMPLETE!")
        print("✅ Input box redrawing is reasonable")
    
    def test_clean_cursor_management(self):
        """UX ISSUE: Test that cursor management is clean and invisible."""
        print("\n🚨 TESTING FOR CLEAN CURSOR MANAGEMENT")
        print("=" * 60)
        print("EXPECTED: Cursor movements should be invisible to user")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send input
            print("\n🔍 SENDING INPUT TO TEST CURSOR MANAGEMENT...")
            child.sendline('Test')
            
            # Wait for processing
            child.expect('User_Input', timeout=5)
            
            # Get all output
            output = child.before.decode() + child.after.decode()
            
            print("🔍 ANALYZING CURSOR MANAGEMENT...")
            
            # Look for signs of poor cursor management
            cursor_issues = []
            
            # Check for raw cursor commands
            if '\033[' in output:
                cursor_issues.append("Raw escape sequences found")
            
            # Check for visible cursor positioning
            if '[A' in output or '[B' in output or '[C' in output or '[D' in output:
                cursor_issues.append("Visible cursor positioning commands")
            
            # Check for multiple consecutive identical boxes (sign of redraw issues)
            box_content = re.findall(r'│.*>.*│', output)
            if len(box_content) > len(set(box_content)) * 2:
                cursor_issues.append("Multiple identical boxes (redraw issue)")
            
            # Check for mixed formatting (sign of cursor position issues)
            if output.count('│') != output.count('╭') or output.count('╭') != output.count('╰'):
                cursor_issues.append("Mismatched box formatting (cursor position issue)")
            
            if cursor_issues:
                print("❌ CURSOR MANAGEMENT ISSUES FOUND:")
                for issue in cursor_issues:
                    print(f"   • {issue}")
                
                self.fail(f"""
🚨 CURSOR MANAGEMENT ISSUES DETECTED 🚨

EXPECTED: Clean, invisible cursor management
ACTUAL: Found cursor management issues

ISSUES:
{chr(10).join(f'  • {issue}' for issue in cursor_issues)}

UX ISSUE: Poor cursor management creates visible artifacts.
This degrades the user experience with visible cursor commands.

Sample output: {repr(output[:400])}
""")
            else:
                print("✅ SUCCESS: Clean cursor management detected")
                
        finally:
            child.close()
        
        print("\n🎉 CURSOR MANAGEMENT VALIDATION COMPLETE!")
        print("✅ Cursor management is clean and invisible")
    
    def test_no_terminal_control_pollution(self):
        """UX ISSUE: Test that no terminal control codes pollute the output."""
        print("\n🚨 TESTING FOR TERMINAL CONTROL POLLUTION")
        print("=" * 60)
        print("EXPECTED: No raw terminal control codes in user-visible output")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send input
            print("\n🔍 SENDING INPUT TO CHECK FOR CONTROL POLLUTION...")
            child.sendline('Hello')
            
            # Wait for processing
            child.expect('User_Input', timeout=5)
            
            # Get all output
            output = child.before.decode() + child.after.decode()
            
            print("🔍 SCANNING FOR TERMINAL CONTROL POLLUTION...")
            
            # Look for various forms of terminal control pollution
            control_patterns = [
                (r'\x1b\[[0-9;]*[mK]', 'ANSI escape sequences'),
                (r'\033\[[0-9;]*[mK]', 'Octal escape sequences'),
                (r'\[0m', 'Reset formatting codes'),
                (r'\[1m', 'Bold formatting codes'),
                (r'\[3[0-9]m', 'Color codes'),
                (r'\r\n', 'Windows line endings'),
                (r'\\033', 'Escaped escape sequences'),
                (r'\\x1b', 'Escaped hex sequences'),
            ]
            
            violations = []
            for pattern, description in control_patterns:
                matches = re.findall(pattern, output)
                if matches:
                    violations.append(f"{description}: {len(matches)} instances")
            
            if violations:
                print("❌ TERMINAL CONTROL POLLUTION FOUND:")
                for violation in violations:
                    print(f"   • {violation}")
                
                self.fail(f"""
🚨 TERMINAL CONTROL POLLUTION DETECTED 🚨

EXPECTED: Clean output without terminal control codes
ACTUAL: Found terminal control codes in output

VIOLATIONS:
{chr(10).join(f'  • {v}' for v in violations)}

UX ISSUE: Terminal control codes are polluting user-visible output.
This creates a poor user experience with visible control characters.

Sample output: {repr(output[:400])}
""")
            else:
                print("✅ SUCCESS: No terminal control pollution detected")
                
        finally:
            child.close()
        
        print("\n🎉 TERMINAL CONTROL VALIDATION COMPLETE!")
        print("✅ No terminal control pollution in output")


if __name__ == '__main__':
    print("🚨 RUNNING INPUT BOX UX ISSUE DETECTION TESTS")
    print("=" * 80)
    print("These tests specifically catch UX problems that degrade user experience.")
    print("Focus: visible escape sequences, excessive redrawing, poor cursor management")
    print("NOTE: These tests MUST FAIL when UX issues are present!")
    print()
    
    unittest.main(verbosity=2)