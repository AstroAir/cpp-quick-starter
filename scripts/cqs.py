#!/usr/bin/env python3
"""
cpp-quick-starter CLI - Convenience wrapper script.

Usage:
    python cqs.py init          Initialize a new project
    python cqs.py add module    Add a new module
    python cqs.py add dep       Add a dependency
    python cqs.py info          Show project information
    python cqs.py doctor        Check development environment

Or install and use directly:
    pip install -e .
    cqs init
"""

import sys
import os

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.main import main

if __name__ == "__main__":
    sys.exit(main())
