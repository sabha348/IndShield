"""
Test script for config_loader module.

This script tests the config loader's ability to:
1. Load valid configuration files
2. Handle missing configuration files
3. Validate configuration values
4. Provide default values
5. Work correctly with detection classes
"""

import os
import sys
import tempfile
import json
from models.config_loader import load_config


def test_valid_config():
    """Test loading a valid configuration file."""
    print("Test 1: Load with valid config file")
    config = load_config()
    assert config is not None, "Config should not be None"
    assert 'fire_model' in config, "Config should contain fire_model"
    assert 'fire_confidence' in config, "Config should contain fire_confidence"
    assert 'gear_model' in config, "Config should contain gear_model"
    assert 'gear_confidence' in config, "Config should contain gear_confidence"
    print("✓ Valid config loaded successfully")
    print(f"  Fire model: {config['fire_model']}")
    print(f"  Fire confidence: {config['fire_confidence']}")
    return True


def test_missing_config():
    """Test handling of missing configuration file."""
    print("\nTest 2: Load with non-existent config file")
    config = load_config('/tmp/nonexistent_config_file.yaml')
    assert config is not None, "Config should return defaults when file missing"
    assert 'fire_model' in config, "Default config should contain fire_model"
    print("✓ Missing config handled correctly with defaults")
    return True


def test_invalid_confidence_values():
    """Test validation of confidence threshold values."""
    print("\nTest 3: Validate confidence threshold values")
    
    # Create a config file with invalid confidence values
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
fire_model: models/fire.pt
fire_confidence: 1.5
gear_model: models/gear.pt
gear_confidence: -0.1
people_model: models/yolov8n.pt
people_confidence: 0.45
""")
        temp_config = f.name
    
    try:
        config = load_config(temp_config)
        # Invalid values should be replaced with defaults
        assert 0.0 <= config['fire_confidence'] <= 1.0, "Fire confidence should be valid"
        assert 0.0 <= config['gear_confidence'] <= 1.0, "Gear confidence should be valid"
        print("✓ Invalid confidence values handled correctly")
        print(f"  Fire confidence corrected to: {config['fire_confidence']}")
        print(f"  Gear confidence corrected to: {config['gear_confidence']}")
        return True
    finally:
        os.unlink(temp_config)


def test_detection_classes_integration():
    """Test that detection classes work with config loader."""
    print("\nTest 4: Integration with detection classes")
    
    from models.fire_detection import fire_detection
    from models.gear_detection import gear_detection
    from models.r_zone import people_detection
    
    # Test fire detection
    fd = fire_detection()
    assert hasattr(fd, 'confidence'), "Fire detection should have confidence attribute"
    print(f"✓ Fire detection initialized with confidence: {fd.confidence}")
    
    # Test gear detection
    gd = gear_detection()
    assert hasattr(gd, 'confidence'), "Gear detection should have confidence attribute"
    assert hasattr(gd, 'class_ids'), "Gear detection should have class_ids attribute"
    print(f"✓ Gear detection initialized with confidence: {gd.confidence}")
    print(f"  Class IDs: {gd.class_ids}")
    
    # Test people detection
    pd = people_detection()
    assert hasattr(pd, 'conf'), "People detection should have conf attribute"
    print(f"✓ People detection initialized with confidence: {pd.conf}")
    
    return True


def test_empty_config():
    """Test handling of empty configuration file."""
    print("\nTest 5: Handle empty config file")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")  # Empty file
        temp_config = f.name
    
    try:
        config = load_config(temp_config)
        assert config is not None, "Config should return defaults for empty file"
        assert 'fire_model' in config, "Default config should be returned"
        print("✓ Empty config file handled correctly with defaults")
        return True
    finally:
        os.unlink(temp_config)


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running Config Loader Tests")
    print("=" * 60)
    
    tests = [
        test_valid_config,
        test_missing_config,
        test_invalid_confidence_values,
        test_detection_classes_integration,
        test_empty_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
