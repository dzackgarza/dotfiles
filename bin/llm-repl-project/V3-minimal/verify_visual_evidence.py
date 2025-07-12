#!/usr/bin/env python3
"""Verify visual evidence from screenshots"""

from pathlib import Path
import re

def extract_messages_from_screenshot(screenshot_path):
    """Extract MESSAGE numbers from screenshot"""
    if not screenshot_path.exists():
        return []
    
    content = screenshot_path.read_text()
    text_pattern = r'<text[^>]*>([^<]+)</text>'
    all_text = re.findall(text_pattern, content)
    
    messages = []
    for text in all_text:
        decoded = text.replace('&#160;', ' ').strip()
        if 'MESSAGE' in decoded:
            match = re.search(r'MESSAGE (\d+)', decoded)
            if match:
                messages.append(int(match.group(1)))
    
    return sorted(messages)

def main():
    print("📸 VISUAL EVIDENCE VERIFICATION")
    print("=" * 50)
    
    screenshot_dir = Path("debug_screenshots")
    
    top_path = screenshot_dir / "current_state_top.svg"
    bottom_path = screenshot_dir / "current_state_bottom.svg"
    
    print(f"\n🔍 CHECKING SCREENSHOTS:")
    print(f"   Top screenshot: {'✅ EXISTS' if top_path.exists() else '❌ MISSING'}")
    print(f"   Bottom screenshot: {'✅ EXISTS' if bottom_path.exists() else '❌ MISSING'}")
    
    if top_path.exists() and bottom_path.exists():
        top_messages = extract_messages_from_screenshot(top_path)
        bottom_messages = extract_messages_from_screenshot(bottom_path)
        
        print(f"\n📊 MESSAGE VISIBILITY:")
        print(f"   Top position: {top_messages}")
        print(f"   Bottom position: {bottom_messages}")
        
        print(f"\n🎯 SCROLLING VERIFICATION:")
        if top_messages != bottom_messages:
            print(f"   ✅ SCROLLING WORKS: Different messages visible at different positions")
            print(f"   ✅ Users can access different content by scrolling")
            
            all_visible = set(top_messages + bottom_messages)
            print(f"   📈 Total accessible messages: {len(all_visible)}")
            
        else:
            print(f"   ❌ SCROLLING BROKEN: Same messages at both positions")
            print(f"   ❌ Users cannot access different content")
            
        print(f"\n🏆 FINAL VERDICT:")
        if top_messages != bottom_messages and len(top_messages) > 0:
            print(f"   ✅ FIX SUCCESSFUL: Mouse wheel scrolling enables content access")
            print(f"   ✅ Problem solved - users can now scroll timeline")
        else:
            print(f"   ❌ FIX INCOMPLETE: Scrolling still not working properly")
            
    else:
        print(f"\n❌ Cannot verify - screenshots missing")

if __name__ == "__main__":
    main()