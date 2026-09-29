#!/usr/bin/env python3
import subprocess
import json
import sys

def get_battery_info():
    try:
        # Get battery path dynamically
        paths = subprocess.check_output(['upower', '-e'], text=True).strip().split('\n')
        bat_path = next((p for p in paths if 'battery' in p and 'DisplayDevice' not in p), None)
        
        if not bat_path:
            return None
            
        output = subprocess.check_output(['upower', '-i', bat_path], text=True)
        
        data = {}
        for line in output.split('\n'):
            line = line.strip()
            if ':' in line:
                key, val = line.split(':', 1)
                data[key.strip()] = val.strip()
                
        return data
    except Exception:
        return None

def main():
    info = get_battery_info()
    if not info:
        print(json.dumps({"text": "No Battery", "class": "error"}))
        return

    state = info.get('state', 'unknown')
    
    # Parse capacity
    percentage_str = info.get('percentage', '0%').replace('%', '')
    try:
        capacity = float(percentage_str)
    except ValueError:
        capacity = 0

    # Parse power draw
    energy_rate = info.get('energy-rate', '0 W').replace(' W', '')
    try:
        power = float(energy_rate)
    except ValueError:
        power = 0.0

    # Determine time string
    time_str = ""
    if state == 'charging' and 'time to full' in info:
        time_str = info['time to full']
    elif state == 'discharging' and 'time to empty' in info:
        time_str = info['time to empty']
        
    # Format time (e.g., "33.8 minutes" -> "33min", "2.5 hours" -> "2h 30min")
    formatted_time = ""
    if time_str:
        if 'minutes' in time_str:
            mins = float(time_str.split()[0])
            formatted_time = f"{int(mins)}min"
        elif 'hours' in time_str:
            hrs = float(time_str.split()[0])
            h = int(hrs)
            m = int((hrs - h) * 60)
            if m > 0:
                formatted_time = f"{h}h {m}min"
            else:
                formatted_time = f"{h}h"

    # Battery Icons mapping matching your config
    icons = ["󰂎", "󰁺", "󰁻", "󰁼", "󰁽", "󰁾", "󰁿", "󰂀", "󰂁", "󰂂", "󰁹"]
    icon_idx = min(int(capacity / 10), 10)
    icon = icons[icon_idx]

    if state == 'charging':
        icon = ""
    elif state == 'fully-charged' or (state == 'unknown' and capacity > 95):
        icon = "󱘖"

    # Format output text to match your current layout
    text_parts = [f"{icon} {int(capacity)}%"]
    if True:
        text_parts.append(f"{power:.2f}W")
    if formatted_time:
        text_parts.append(f"{formatted_time}")
        
    text = " ".join(text_parts)
    
    # CSS Classes for styling
    css_class = state
    if capacity <= 15:
        css_class += " critical"
    elif capacity <= 30:
        css_class += " warning"
    elif capacity >= 95:
        css_class += " good"

    # Tooltip
    tooltip = f"State: {state.capitalize()}"
    if formatted_time:
        tooltip += f"\nTime: {formatted_time}"
    if True:
        tooltip += f"\nPower: {power:.2f}W"

    # Output JSON for Waybar
    out = {
        "text": text,
        "tooltip": tooltip,
        "class": css_class,
        "percentage": int(capacity)
    }
    
    print(json.dumps(out))

if __name__ == "__main__":
    main()
