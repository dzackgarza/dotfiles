#!/usr/bin/env python3
"""
Timeline Purity Validation Tests

These tests ensure that ONLY plugin blocks appear on the timeline.
Any raw text outside blocks is a structural violation.
"""

import unittest
import pexpect
import sys
import re


class TimelinePurityTests(unittest.TestCase):
    """
    Tests that validate timeline purity - only plugin blocks allowed.
    
    These tests catch violations where raw text appears outside blocks.
    """
    
    def test_no_raw_text_pollution(self):
        """PURITY: Test that no raw text appears outside plugin blocks."""
        print("\n🎯 TESTING TIMELINE PURITY")
        print("=" * 60)
        print("EXPECTED: Only plugin blocks, no raw text")
        
        # Launch program
        child = pexpect.spawn('python', ['src/main.py', '--config', 'debug'])
        child.logfile_read = sys.stdout.buffer
        
        try:
            # Wait for welcome to complete
            child.expect('Welcome', timeout=5)
            
            # Send input
            print("\n🔍 SENDING USER INPUT...")
            child.sendline('Hello')
            
            # Wait for User_Input block to appear
            child.expect('User_Input', timeout=5)
            
            # Get all output up to this point
            output = child.before.decode() + child.after.decode()
            
            print("\n🔍 ANALYZING TIMELINE PURITY...")
            
            # Check for timeline violations
            violations = self._find_timeline_violations(output)
            
            if violations:
                print("❌ TIMELINE PURITY VIOLATIONS FOUND:")
                for violation in violations:
                    print(f"   • {violation}")
                
                self.fail(f"""
🚨 TIMELINE PURITY VIOLATION 🚨

EXPECTED: Only plugin blocks on timeline
ACTUAL: Found raw text outside blocks

VIOLATIONS:
{chr(10).join(f'  • {v}' for v in violations)}

ARCHITECTURAL ISSUE: Raw text is bypassing the secure timeline system.
All content must appear within plugin blocks with proper metadata.

Raw output for analysis:
{repr(output)}
""")
            else:
                print("✅ SUCCESS: Timeline is pure - only plugin blocks found")
            
        finally:
            child.close()
        
        print("\n🎉 TIMELINE PURITY VALIDATION COMPLETE!")
        print("✅ No raw text pollution detected")
    
    def _find_timeline_violations(self, output: str) -> list:
        """
        Find timeline violations - raw text outside plugin blocks.
        
        Returns list of violation descriptions.
        """
        violations = []
        lines = output.split('\n')
        
        in_block = False
        for i, line in enumerate(lines):
            # Check if we're entering a block
            if '╭' in line and '🔧' in line:
                in_block = True
                continue
            
            # Check if we're exiting a block
            if '╰' in line and in_block:
                in_block = False
                continue
            
            # Skip empty lines and pure whitespace
            if not line.strip():
                continue
            
            # Skip control sequences and expected interface elements
            if any(skip in line for skip in ['\x1b', '\r', 'python', 'src/main.py']):
                continue
            
            # If we have content outside a block, it's a violation
            if not in_block and line.strip():
                # Check for specific violation patterns
                stripped = line.strip()
                
                # Raw prompt violation
                if stripped.startswith('>') and not ('╭' in line or '│' in line):
                    violations.append(f"Raw prompt on line {i+1}: '{stripped}'")
                
                # Raw user input echo violation
                elif stripped and not any(c in stripped for c in ['╭', '╰', '│', '┬', '┴']):
                    # This is likely raw text that should be in a block
                    violations.append(f"Raw text on line {i+1}: '{stripped}'")
        
        return violations


if __name__ == '__main__':
    print("🎯 RUNNING TIMELINE PURITY VALIDATION TESTS")
    print("=" * 80)
    print("These tests ensure only plugin blocks appear on the timeline.")
    print("Raw text pollution violates the secure timeline architecture.")
    print()
    
    unittest.main(verbosity=2)