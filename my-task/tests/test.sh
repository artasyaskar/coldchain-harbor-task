#!/bin/bash
set -e

mkdir -p /logs/verifier
python3 /tests/run_tests.py
