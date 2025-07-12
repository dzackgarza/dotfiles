#!/usr/bin/env python3
"""
Test YAML config loading functionality
"""

from src.config import AnimationConfig, ConfigLoader

def test_yaml_config():
    """Test YAML configuration loading"""
    
    print("Testing YAML Config Loading...")
    print()
    
    # Test config file discovery
    config_file = ConfigLoader.find_config_file()
    print(f"Config file found: {config_file}")
    
    # Test config loading
    config = ConfigLoader.load_config()
    print(f"Loaded config: {config}")
    print()
    
    # Test animation speeds
    speeds = AnimationConfig.get_current_speeds()
    print("Current animation speeds:")
    for key, value in speeds.items():
        print(f"  {key}: {value} chars/sec")
    print()
    
    # Test expected values from config.yaml
    expected_speeds = {
        'initial': 1500,
        'progress': 2000,
        'completion': 2500,
        'summary': 1800
    }
    
    print("Validation:")
    for key, expected in expected_speeds.items():
        actual = speeds.get(key)
        if actual == expected:
            print(f"✅ {key}: {actual} chars/sec (matches config)")
        else:
            print(f"❌ {key}: {actual} chars/sec (expected {expected})")

if __name__ == "__main__":
    test_yaml_config()