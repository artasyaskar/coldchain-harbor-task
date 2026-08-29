#!/bin/bash
set -e

mkdir -p /logs/verifier
python3 /workspace/tests/run_tests.py || python /workspace/tests/run_tests.py || python tests/run_tests.py
