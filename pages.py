"""
DEPRECATED ENTRY POINT
This script is kept for backward compatibility only.
Please run `python3 main.py` instead.

When invoked, this file will forward execution to the new main application.
"""

import sys

print("[DEPRECATED] pages.py is deprecated. Forwarding to main.py...")

try:
    from main import main as _main
except Exception as e:
    print(f"Failed to import main.py: {e}")
    sys.exit(1)

if __name__ == "__main__":
    _main()
else:
    # If imported by mistake, expose a callable for compatibility
    def run():
        _main()
