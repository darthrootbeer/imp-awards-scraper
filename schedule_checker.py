#!/usr/bin/env python3
"""
Schedule checker for automation - determines if script should run based on config.yaml
"""

import os
import yaml
from datetime import datetime
from typing import Dict, Optional, Tuple

CONFIG_FILE = 'config.yaml'

def load_config() -> Dict:
    """Load unified configuration from config.yaml"""
    default_config = {
        'schedule': {
            'enabled': True,
            'days_of_week': {
                'monday': True,
                'tuesday': True,
                'wednesday': True,
                'thursday': True,
                'friday': True,
                'saturday': True,
                'sunday': True
            },
            'preferred_time': '08:00'
        }
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                # Merge with defaults
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in default_config:
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
        except Exception as e:
            print(f"Warning: Could not load {CONFIG_FILE}: {e}, using defaults")
    
    return default_config

def should_run_today() -> Tuple[bool, Optional[str]]:
    """
    Check if the script should run today based on config.yaml schedule settings.
    
    Returns:
        tuple: (should_run: bool, reason: str or None)
    """
    config = load_config()
    schedule = config.get('schedule', {})
    
    # Check if automation is enabled
    if not schedule.get('enabled', True):
        return False, "Automation is disabled in config.yaml (schedule.enabled: false)"
    
    # Get today's day name
    today = datetime.now().strftime('%A').lower()
    
    # Check if today is enabled
    days_of_week = schedule.get('days_of_week', {})
    if not days_of_week.get(today, True):
        return False, f"Today ({today}) is disabled in config.yaml"
    
    return True, None

if __name__ == "__main__":
    # CLI mode for testing
    should_run, reason = should_run_today()
    if should_run:
        print("✓ Script should run today")
        exit(0)
    else:
        print(f"✗ Script should NOT run: {reason}")
        exit(1)
