"""
Configuration Loader for Disk Forensic Analyzer
Handles loading, validation, and management of configuration settings
"""

import json
import yaml
from pathlib import Path
import logging
from typing import Any, Dict, Optional

class ConfigLoader:
    def __init__(self, config_path: str = 'config/config.json'):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file with defaults"""
        default_config = self._get_default_config()
        
        try:
            if self.config_path.exists():
                # Determine file type
                if self.config_path.suffix.lower() in ['.json']:
                    with open(self.config_path, 'r') as f:
                        user_config = json.load(f)
                elif self.config_path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    with open(self.config_path, 'r') as f:
                        user_config = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {self.config_path.suffix}")
                
                # Merge user config with defaults
                self.config = self._deep_merge(default_config, user_config)
                self.logger.info(f"Loaded configuration from {self.config_path}")
                
                # Save merged config for reference
                self._save_reference_config()
                
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                self.config = default_config
                
                # Create directory and save default config
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                self.logger.info(f"Created default config file: {self.config_path}")
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON config: {e}")
            self.config = default_config
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML config: {e}")
            self.config = default_config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.config = default_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return comprehensive default configuration"""
        return {
            "system": {
                "project_name": "Disk Forensic Analyzer",
                "version": "2.0",
                "timezone": "UTC",
                "date_format": "%Y-%m-%d %H:%M:%S",
                "log_level": "INFO"
            },
            
            "data_collection": {
                "max_entries": 100000,
                "preserve_timestamps": True,
                "collect_prefetch": True,
                "collect_event_logs": True,
                "collect_registry": True,
                "collect_browser_history": True,
                "collect_system_info": True,
                "artifact_sources": {
                    "prefetch_path": "C:/Windows/Prefetch",
                    "event_logs_path": "C:/Windows/System32/winevt/Logs",
                    "registry_hives": ["SAM", "SYSTEM", "SOFTWARE", "SECURITY", "NTUSER.DAT"]
                }
            },
            
            "analysis": {
                "include_synthetic_anomalies": True,
                "timeline_reconstruction": {
                    "merge_strategy": "chronological",
                    "deduplicate": True,
                    "normalize_timestamps": True
                },
                "max_timeline_entries": 50000
            },
            
            "anomaly_detection": {
                "enabled": True,
                "mode": "hybrid",
                
                "rule_based": {
                    "enabled": True,
                    "temporal_detection": {
                        "night_hours": [22, 23, 0, 1, 2, 3, 4, 5],
                        "weekend_detection": True,
                        "burst_detection": True,
                        "burst_threshold": 2.0
                    },
                    "pattern_detection": {
                        "suspicious_keywords": [
                            "suspicious", "malware", "exploit", "keylogger",
                            "backdoor", "trojan", "ransomware", "worm"
                        ],
                        "risky_extensions": [".exe", ".dll", ".bat", ".ps1", ".vbs", ".js"],
                        "suspicious_locations": ["temp", "tmp", "downloads"]
                    },
                    "behavioral_detection": {
                        "rare_user_threshold": 5,
                        "high_activity_threshold": 2.0
                    }
                },
                
                "ml_models": {
                    "isolation_forest": {
                        "enabled": True,
                        "contamination": 0.1,
                        "n_estimators": 100,
                        "random_state": 42
                    },
                    "random_forest": {
                        "enabled": False,
                        "n_estimators": 50,
                        "requires_labeled_data": True
                    }
                },
                
                "hybrid": {
                    "voting_threshold": 0.7,
                    "ensemble_weights": {
                        "rule_based": 0.3,
                        "ml": 0.7
                    },
                    "fusion_strategy": "weighted_average",
                    "enable_adaptive_learning": True,
                    "confidence_thresholds": {
                        "high": 0.8,
                        "medium": 0.5,
                        "low": 0.3
                    }
                }
            },
            
            "visualization": {
                "generate_html": True,
                "generate_pdf": False,
                "interactive_plots": True,
                "save_csv": True,
                "save_json": True,
                "plots": {
                    "timeline_plot": True,
                    "activity_heatmap": True,
                    "artifact_distribution": True,
                    "anomaly_analysis": True,
                    "hybrid_detection_flow": True
                },
                "dpi": 300
            },
            
            "output": {
                "directory": "./output",
                "subdirectories": {
                    "reports": "reports",
                    "plots": "plots",
                    "data": "data",
                    "models": "models"
                },
                "timestamp_format": "%Y%m%d_%H%M%S",
                "compress_output": False
            },
            
            "logging": {
                "log_file": "logs/forensic_analyzer.log",
                "log_level": "INFO",
                "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "max_log_size": 10485760,
                "backup_count": 5
            }
        }
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Recursively merge two dictionaries"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _save_reference_config(self) -> None:
        """Save current config as reference"""
        ref_path = Path("config/active_config.json")
        ref_path.parent.mkdir(exist_ok=True)
        
        with open(ref_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Dot-separated key (e.g., "anomaly_detection.mode")
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys:
            if isinstance(config, dict) and k in config:
                config = config[k]
            else:
                return default
        
        return config
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        
        Args:
            key: Dot-separated key
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            elif not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def validate(self) -> bool:
        """Validate configuration values"""
        errors = []
        
        # Validate anomaly detection mode
        valid_modes = ["rule_only", "ml_only", "hybrid"]
        mode = self.get("anomaly_detection.mode")
        if mode not in valid_modes:
            errors.append(f"Invalid anomaly detection mode: {mode}. Must be one of: {valid_modes}")
        
        # Validate thresholds
        burst_threshold = self.get("anomaly_detection.rule_based.temporal_detection.burst_threshold")
        if burst_threshold is not None and burst_threshold < 0:
            errors.append(f"Burst threshold must be >= 0, got {burst_threshold}")
        
        # Validate night hours
        night_hours = self.get("anomaly_detection.rule_based.temporal_detection.night_hours")
        if night_hours and not all(0 <= hour <= 23 for hour in night_hours):
            errors.append("Night hours must be between 0 and 23")
        
        # Validate confidence thresholds
        confidence_thresholds = self.get("anomaly_detection.hybrid.confidence_thresholds", {})
        if confidence_thresholds:
            if not (0 <= confidence_thresholds.get('low', 0) <= 
                    confidence_thresholds.get('medium', 0.5) <= 
                    confidence_thresholds.get('high', 1) <= 1):
                errors.append("Confidence thresholds must be 0 <= low <= medium <= high <= 1")
        
        if errors:
            for error in errors:
                self.logger.error(f"Config validation error: {error}")
            return False
        
        return True
    
    def save(self, path: Optional[str] = None) -> None:
        """
        Save current configuration to file
        
        Args:
            path: Path to save config (defaults to original path)
        """
        save_path = Path(path) if path else self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        self.logger.info(f"Configuration saved to {save_path}")
    
    def print_summary(self) -> None:
        """Print configuration summary to console"""
        summary = f"""
        {'='*60}
        DISK FORENSIC ANALYZER CONFIGURATION SUMMARY
        {'='*60}
        
        System:
          Project: {self.get('system.project_name')} v{self.get('system.version')}
          Timezone: {self.get('system.timezone')}
          Log Level: {self.get('system.log_level')}
        
        Data Collection:
          Max Entries: {self.get('data_collection.max_entries'):,}
          Prefetch: {'✓' if self.get('data_collection.collect_prefetch') else '✗'}
          Event Logs: {'✓' if self.get('data_collection.collect_event_logs') else '✗'}
          Registry: {'✓' if self.get('data_collection.collect_registry') else '✗'}
          Browser History: {'✓' if self.get('data_collection.collect_browser_history') else '✗'}
        
        Anomaly Detection:
          Mode: {self.get('anomaly_detection.mode').upper()}
          Rule-Based: {'✓' if self.get('anomaly_detection.rule_based.enabled') else '✗'}
          ML Models: {', '.join([
              name for name, model in self.get('anomaly_detection.ml_models', {}).items() 
              if model.get('enabled', False)
          ]) or 'None'}
          Hybrid Fusion: {self.get('anomaly_detection.hybrid.fusion_strategy')}
        
        Visualization:
          HTML Reports: {'✓' if self.get('visualization.generate_html') else '✗'}
          Interactive Plots: {'✓' if self.get('visualization.interactive_plots') else '✗'}
          CSV Export: {'✓' if self.get('visualization.save_csv') else '✗'}
          JSON Export: {'✓' if self.get('visualization.save_json') else '✗'}
        
        Output:
          Directory: {self.get('output.directory')}
          Timestamp Format: {self.get('output.timestamp_format')}
        
        {'='*60}
        """
        
        print(summary)

# Convenience function for quick access
def load_config(config_path: str = 'config/config.json') -> ConfigLoader:
    """Load configuration and return ConfigLoader instance"""
    return ConfigLoader(config_path)