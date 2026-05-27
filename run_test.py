#!/usr/bin/env python
"""Test script to run main and capture errors."""

import sys
import subprocess
from pathlib import Path

script_dir = Path(__file__).parent
src_dir = script_dir / "src"

# Run main.py and capture output
result = subprocess.run(
    [sys.executable, str(src_dir / "main.py")],
    cwd=script_dir,
    capture_output=True,
    text=True,
    timeout=30
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")

# Save to file
with open(script_dir / "run_output.txt", "w") as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\n\nSTDERR:\n")
    f.write(result.stderr)
    f.write(f"\n\nReturn code: {result.returncode}\n")
