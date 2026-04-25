"""Verify that Python is installed correctly and ready for Phase 0."""
import sys


def check_version():
    major, minor = sys.version_info.major, sys.version_info.minor
    version_str = f"{major}.{minor}.{sys.version_info.micro}"
    if major < 3 or (major == 3 and minor < 11):
        print(f"✗ Python {version_str} detected. This lab requires Python 3.11 or higher.")
        print("  Download from: https://python.org/downloads")
        sys.exit(1)
    print(f"✓ Python version: {version_str}")


def check_stdlib():
    modules = ["pathlib", "csv", "json", "datetime", "collections", "itertools"]
    for mod in modules:
        try:
            __import__(mod)
        except ImportError:
            print(f"✗ Standard library module '{mod}' not available.")
            sys.exit(1)
    print("✓ Standard library available")


if __name__ == "__main__":
    check_version()
    check_stdlib()
    print("✓ Ready for Phase 0")
