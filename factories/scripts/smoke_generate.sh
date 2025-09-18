#!/usr/bin/env bash
set -e
python orchestrator.py --dry-run --count=5
python orchestrator.py --count=3
echo "OK smoke."
