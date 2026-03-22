'''
Config Parser

This module provides utilities for loading, validating, and merging configuration
files in JSON and YAML formats. It also includes preprocessing logic to convert
numeric range lists into tuples for easier downstream data handling.

Information
-----------
@author: Christian G. Garcia
@github: github.com/christiangarcia/django-model-seeder
'''


import json
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigParser:
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return ConfigParser._convert_to_tuples(data)

    @staticmethod
    def load_yaml(filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def _convert_to_tuples(config: Dict[str, Any]) -> Dict[str, Any]:
        for model_name, model_config in config.items():
            if isinstance(model_config, dict) and 'mapping' in model_config:
                mapping = model_config['mapping']
                for field_name, value in mapping.items():
                    if isinstance(value, list) and len(value) >= 2:
                        if all(isinstance(v, (int, float)) or v == 'float' for v in value):
                            mapping[field_name] = tuple(value)
        return config

    @staticmethod
    def load_config(filepath: str) -> Dict[str, Any]:
        path = Path(filepath)
        
        if path.suffix == '.json':
            return ConfigParser.load_json(filepath)
        elif path.suffix in ['.yaml', '.yml']:
            return ConfigParser.load_yaml(filepath)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        if not isinstance(config, dict):
            return False
        
        for model_name, model_config in config.items():
            if not isinstance(model_config, dict):
                return False
            if 'rows' not in model_config or 'mapping' not in model_config:
                return False
            if not isinstance(model_config['mapping'], dict):
                return False
        
        return True

    @staticmethod
    def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        merged = base_config.copy()
        
        for model_name, model_config in override_config.items():
            if model_name in merged:
                merged[model_name].update(model_config)
            else:
                merged[model_name] = model_config
        
        return merged