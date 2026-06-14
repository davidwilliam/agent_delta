#!/usr/bin/env python
"""Build the Docker sandbox image for a fixture.

Usage:
    python scripts/build_sandbox.py [fixture_name]   # default: python_package
"""

import sys

from agent_delta.sandbox_build import build_image

if __name__ == "__main__":
    build_image(sys.argv[1] if len(sys.argv) > 1 else "python_package")
