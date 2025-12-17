#!/usr/bin/env python3
"""
API Configuration
Loads API key from environment with fallback warning.
"""

import os
import sys


def get_api_key() -> str:
    """
    Load API key from environment.
    Returns configured key or warns if not set.
    """
    api_key = os.environ.get("API_KEY")
    
    if not api_key:
        print(
            "[WARNING] API_KEY not set in environment. Using default 'test123' for development.",
            file=sys.stderr
        )
        return "test123"
    
    return api_key


# Load on module import
API_KEY = get_api_key()
