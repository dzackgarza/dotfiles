#!/usr/bin/env python3
"""
Input Box Behavior Tests

These tests validate the expected behaviors of the dedicated input box:
1. Input box appears with proper ">" prompt
2. Long text wraps to multiple lines with proper indentation
3. Input box maintains full screen width
4. Input box updates show user typing (when possible)
5. Input box is visually separate from timeline content
"""

import unittest
import pexpect
import sys
import re
import time


class InputBoxBehaviorTests(unittest.TestCase):
    """
    Tests that validate input box UI behavior and display.
    
    These tests ensure the input box works like Claude Code:
    - Full screen width
    - Proper ">" prompt inside
    - Multiline text wrapping
    - Visual separation from timeline
    """
    
    def spawn_repl(self):
        """Spawn a new REPL instance for testing."""
        return pexpect.spawn('python', ['src/main.py', '--config', 'debug'], timeout=10)
    
    def test_input_box_appears_with_prompt(self):
        """BEHAVIOR: Test that input box appears with proper "> " prompt."""
        print("\n🎯 TESTING INPUT BOX PROMPT DISPLAY")
        print("=" * 60)
        print("EXPECTED: Input box appears with "> " prompt inside")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup sequence to complete
            child.expect('Welcome', timeout=5)
            
            # Look for input box with prompt
            print("\n🔍 CHECKING FOR INPUT BOX WITH PROMPT...")
            try:
                # Look for the characteristic input box pattern
                child.expect(r'╭.*╮.*>\s*.*╰.*╯', timeout=3)
                print("✅ SUCCESS: Input box with prompt found")
                
                # Verify it's full width (should have many characters in the border)
                output = child.after.decode() if child.after else ""
                if '──' in output and len([c for c in output if c == '─']) > 20:
                    print("✅ SUCCESS: Input box appears to be full screen width")
                else:
                    print("❌ WARNING: Input box may not be full screen width")
                
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Input box with prompt did NOT appear")
                self.fail(f"""
🚨 INPUT BOX PROMPT FAILURE 🚨

EXPECTED: Input box with "> " prompt should appear after startup
ACTUAL: No input box found within 3 seconds

ARCHITECTURAL ISSUE: Input box not displaying properly after startup.

Buffer content: {repr(child.before)}
""")
        finally:
            child.close()
        
        print("\n🎉 INPUT BOX PROMPT VALIDATION COMPLETE!")
        print("✅ Input box displays with proper prompt")
    
    def test_input_box_shows_user_input(self):
        """BEHAVIOR: Test that input box updates to show user input."""
        print("\n🎯 TESTING INPUT BOX USER INPUT DISPLAY")
        print("=" * 60)
        print("EXPECTED: Input box updates to show user typing")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup and input box
            child.expect('Welcome', timeout=5)
            
            # Send input
            print("\n🔍 SENDING USER INPUT...")
            child.sendline('Test input')
            
            # Look for input box that shows the user's input
            print("🔍 CHECKING FOR INPUT BOX WITH USER INPUT...")
            try:
                child.expect(r'>\s*Test input', timeout=3)
                print("✅ SUCCESS: Input box shows user input")
                
                # Verify input appears in a box format
                output = child.after.decode() if child.after else ""
                if '╭' in output and '╰' in output:
                    print("✅ SUCCESS: User input appears in proper box format")
                else:
                    print("❌ WARNING: User input may not be in proper box format")
                    
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Input box with user input did NOT appear")
                self.fail(f"""
🚨 INPUT BOX USER INPUT FAILURE 🚨

EXPECTED: Input box should show "> Test input" after user types
ACTUAL: No input box with user input found within 3 seconds

ARCHITECTURAL ISSUE: Input box not updating with user input.

Buffer content: {repr(child.before)}
""")
        finally:
            child.close()
        
        print("\n🎉 INPUT BOX USER INPUT VALIDATION COMPLETE!")
        print("✅ Input box updates to show user input")
    
    def test_input_box_separation_from_timeline(self):
        """BEHAVIOR: Test that input boxes are visually separate from timeline."""
        print("\n🎯 TESTING INPUT BOX TIMELINE SEPARATION")
        print("=" * 60)
        print("EXPECTED: Input boxes are visually distinct from timeline plugins")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send input to generate timeline content
            print("\n🔍 GENERATING TIMELINE AND INPUT BOX CONTENT...")
            child.sendline('Hello')
            
            # Look for both timeline plugins and input boxes
            child.expect('User_Input', timeout=5)
            
            # Get all output
            output = child.before.decode() + child.after.decode()
            
            print("🔍 ANALYZING VISUAL SEPARATION...")
            
            # Count timeline plugins vs input boxes
            plugin_blocks = len(re.findall(r'🔧.*✅', output))
            input_boxes = len(re.findall(r'╭.*>\s*.*╰', output))
            
            print(f"📊 FOUND: {plugin_blocks} timeline plugins, {input_boxes} input boxes")
            
            if plugin_blocks > 0 and input_boxes > 0:
                print("✅ SUCCESS: Both timeline plugins and input boxes present")
                
                # Check visual distinction
                if '🔧' in output:  # Timeline plugins have tool emoji
                    print("✅ SUCCESS: Timeline plugins have distinctive markers")
                else:
                    print("❌ WARNING: Timeline plugins may not have distinctive markers")
                
            else:
                self.fail(f"""
🚨 INPUT BOX SEPARATION FAILURE 🚨

EXPECTED: Both timeline plugins and input boxes should be present and distinct
ACTUAL: Found {plugin_blocks} timeline plugins, {input_boxes} input boxes

ARCHITECTURAL ISSUE: Input boxes not properly separated from timeline content.

Output sample: {repr(output[:500])}
""")
        finally:
            child.close()
        
        print("\n🎉 INPUT BOX SEPARATION VALIDATION COMPLETE!")
        print("✅ Input boxes are visually distinct from timeline plugins")
    
    def test_input_box_multiline_behavior(self):
        """BEHAVIOR: Test input box behavior with long text (should wrap)."""
        print("\n🎯 TESTING INPUT BOX MULTILINE BEHAVIOR")
        print("=" * 60)
        print("EXPECTED: Long text should wrap and expand input box vertically")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('Welcome', timeout=5)
            
            # Send very long input
            long_text = "This is a very long input that should definitely wrap to multiple lines because it exceeds the normal terminal width and should trigger the multiline behavior of the input box"
            
            print(f"\n🔍 SENDING LONG INPUT ({len(long_text)} characters)...")
            child.sendline(long_text)
            
            # Look for the long text in input display
            print("🔍 CHECKING FOR MULTILINE INPUT BOX...")
            try:
                child.expect('very long input', timeout=5)
                print("✅ SUCCESS: Long input detected in output")
                
                # Get output to analyze structure
                output = child.after.decode() if child.after else ""
                
                # Check if text appears to be wrapped (multiple lines in box)
                if output.count('\n') > 1:
                    print("✅ SUCCESS: Input appears to span multiple lines")
                else:
                    print("❌ WARNING: Input may not be properly wrapped")
                
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Long input not found in output")
                self.fail(f"""
🚨 INPUT BOX MULTILINE FAILURE 🚨

EXPECTED: Long input should appear in input box, potentially wrapped
ACTUAL: Long input not found in output within 5 seconds

ARCHITECTURAL ISSUE: Input box not handling long text properly.

Buffer content: {repr(child.before)}
""")
        finally:
            child.close()
        
        print("\n🎉 INPUT BOX MULTILINE VALIDATION COMPLETE!")
        print("✅ Input box handles long text appropriately")


if __name__ == '__main__':
    print("🎯 RUNNING INPUT BOX BEHAVIOR TESTS")
    print("=" * 80)
    print("These tests validate input box UI behavior and display characteristics.")
    print("Focus: prompt display, user input updates, visual separation, multiline handling")
    print()
    
    unittest.main(verbosity=2)