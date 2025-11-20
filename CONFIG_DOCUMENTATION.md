# Configuration File Documentation

## Overview

The `config.yaml` file contains configuration settings for the IndShield detection models. This file allows you to customize model paths, confidence thresholds, and class mappings without modifying the source code.

## File Location

The configuration file should be placed at the root of the project:
```
IndShield/
├── config.yaml          # Configuration file
├── models/
│   ├── config_loader.py # Config loader module
│   ├── fire_detection.py
│   ├── gear_detection.py
│   └── r_zone.py
└── ...
```

## Configuration Schema

### Fire Detection Settings

```yaml
fire_model: models/fire.pt        # Path to fire detection model file
fire_confidence: 0.80              # Confidence threshold (0.0 - 1.0)
```

- **fire_model**: Path to the YOLO model file for fire detection
- **fire_confidence**: Minimum confidence score (0.0 to 1.0) required to consider a detection valid
  - Default: 0.85
  - Lower values detect more objects but may have more false positives
  - Higher values are more strict but may miss some detections

### Gear Detection Settings

```yaml
gear_model: models/gear.pt        # Path to gear detection model file
gear_confidence: 0.85              # Confidence threshold (0.0 - 1.0)
gear_classes:                      # Class ID mappings
  helmet: 2                        # Helmet class ID
  vest: 3                          # Safety vest class ID
  boots: 4                         # Safety boots class ID
```

- **gear_model**: Path to the YOLO model file for safety gear detection
- **gear_confidence**: Minimum confidence score required for gear detection
  - Default: 0.85
- **gear_classes**: Dictionary mapping gear item names to their class IDs in the model
  - Each value must be an integer representing the class ID
  - You can add or remove gear types as needed

### People Detection Settings

```yaml
people_model: models/yolov8n.pt   # Path to people detection model file
people_confidence: 0.45            # Confidence threshold (0.0 - 1.0)
people_region: null                # Optional restricted region coordinates
```

- **people_model**: Path to the YOLO model file for people detection
- **people_confidence**: Minimum confidence score for people detection
  - Default: 0.45
- **people_region**: Optional list of coordinates defining a restricted region
  - Format: `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]`
  - Set to `null` to disable region restriction

## Example Configuration

```yaml
# Fire Detection Configuration
fire_model: models/fire.pt
fire_confidence: 0.80

# Gear Detection Configuration
gear_model: models/gear.pt
gear_confidence: 0.85
gear_classes:
  helmet: 2
  vest: 3
  boots: 4

# People Detection Configuration
people_model: models/yolov8n.pt
people_confidence: 0.45
people_region: null
```

## Validation and Error Handling

The configuration loader includes automatic validation:

1. **Missing File**: If the config file is not found, default values are used
2. **Invalid Confidence**: Values outside 0.0-1.0 range are replaced with defaults
3. **Invalid YAML**: Syntax errors result in using default configuration
4. **Invalid Class IDs**: Non-integer class IDs trigger a warning
5. **Empty File**: Empty config files are handled gracefully with defaults

## Default Values

If any configuration value is missing or invalid, these defaults are used:

```python
DEFAULT_CONFIG = {
    'fire_model': 'models/fire.pt',
    'fire_confidence': 0.85,
    'gear_model': 'models/gear.pt',
    'gear_confidence': 0.85,
    'gear_classes': {
        'helmet': 2,
        'vest': 3,
        'boots': 4
    },
    'people_model': 'models/yolov8n.pt',
    'people_confidence': 0.45,
    'people_region': None
}
```

## Usage in Code

The configuration is automatically loaded by the detection classes:

```python
from models.fire_detection import fire_detection
from models.gear_detection import gear_detection
from models.r_zone import people_detection

# All classes automatically load config.yaml
fire_det = fire_detection()
gear_det = gear_detection()
people_det = people_detection()
```

You can also load the configuration manually:

```python
from models.config_loader import load_config

# Load default config
config = load_config()

# Load from custom path
config = load_config('/path/to/custom/config.yaml')
```

## Troubleshooting

### Configuration Not Loading

If the configuration is not being applied:

1. Verify the file is named exactly `config.yaml`
2. Check the file is in the root directory of the project
3. Ensure the YAML syntax is valid (use a YAML validator)
4. Check the application logs for configuration warnings

### Invalid Confidence Values

If you see warnings about invalid confidence values:

- Ensure all confidence values are between 0.0 and 1.0
- Use decimal notation (e.g., `0.85` not `85%`)

### Model Not Found

If model files cannot be loaded:

- Verify the model file paths in the config are correct
- Ensure model files exist at the specified locations
- Use relative paths from the project root

## Best Practices

1. **Version Control**: Commit `config.yaml` with reasonable defaults
2. **Environment-Specific Configs**: Consider using different config files for different environments
3. **Confidence Tuning**: Start with default values and adjust based on performance
4. **Model Paths**: Use relative paths for better portability
5. **Documentation**: Document any custom class IDs or non-standard settings

## Security Considerations

- Do not store sensitive information in `config.yaml`
- Ensure model files are from trusted sources
- Validate model file integrity before deployment
- Restrict write access to the config file in production
