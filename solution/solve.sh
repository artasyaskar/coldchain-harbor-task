#!/bin/bash
set -e

mkdir -p /workspace/output output
python3 /workspace/solution/solution.py || python solution/solution.py
