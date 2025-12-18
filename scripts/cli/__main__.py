#!/usr/bin/env python3
"""
Allow running the CLI module directly: python -m cli
"""

from .main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
