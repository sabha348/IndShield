import yaml
import os
import logging

logger = logging.getLogger(__name__)

# Default configuration values
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

def validate_config(config):
    """
    Validate configuration values and provide helpful error messages.
    
    Args:
        config: Dictionary containing configuration values
        
    Returns:
        Dictionary with validated configuration
    """
    validated = config.copy()
    
    # Validate confidence thresholds
    for key in ['fire_confidence', 'gear_confidence', 'people_confidence']:
        if key in validated:
            value = validated[key]
            if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
                logger.warning(f"Invalid {key}: {value}. Must be between 0.0 and 1.0. Using default: {DEFAULT_CONFIG.get(key)}")
                validated[key] = DEFAULT_CONFIG.get(key)
    
    # Validate gear_classes structure
    if 'gear_classes' in validated:
        gear_classes = validated['gear_classes']
        if not isinstance(gear_classes, dict):
            logger.warning(f"Invalid gear_classes format. Using default.")
            validated['gear_classes'] = DEFAULT_CONFIG['gear_classes']
        else:
            for name, class_id in gear_classes.items():
                if not isinstance(class_id, int):
                    logger.warning(f"Invalid class ID for {name}: {class_id}. Must be an integer.")
    
    return validated

def load_config(config_path=None):
    """
    Load configuration from YAML file with error handling and validation.
    
    Args:
        config_path: Optional path to config file. If None, uses default path.
        
    Returns:
        Dictionary containing configuration values
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file has invalid YAML syntax
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    
    # Check if config file exists
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        logger.info("Using default configuration values")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if config is None:
            logger.warning(f"Empty configuration file: {config_path}. Using defaults.")
            return DEFAULT_CONFIG.copy()
        
        # Merge with defaults (config values override defaults)
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        
        # Validate the configuration
        validated_config = validate_config(merged_config)
        
        logger.debug(f"Configuration loaded successfully from {config_path}")
        return validated_config
        
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration file: {e}")
        logger.info("Using default configuration values")
        return DEFAULT_CONFIG.copy()
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        logger.info("Using default configuration values")
        return DEFAULT_CONFIG.copy()