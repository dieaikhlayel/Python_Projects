import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            'database': {
                'path': 'passwords.db',
                'backup_path': 'backups/'
            },
            'security': {
                'key_derivation_iterations': 100000,
                'min_password_length': 8,
                'require_special_chars': True
            },
            'cloud': {
                'enable_sync': False,
                'sync_service': 'google_drive',
                'sync_interval': 3600
            },
            'gui': {
                'theme': 'dark',
                'auto_lock_minutes': 15
            }
        }
        
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                # Deep merge with default config
                return self._deep_merge(default_config, user_config)
        
        # Create default config file
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return default_config
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in update.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        
        # Save to file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)