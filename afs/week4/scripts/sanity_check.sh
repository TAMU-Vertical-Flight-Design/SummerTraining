#!/usr/bin/env bash
set -euo pipefail

python3 afs/week4/mission_planner.py
grep -RInE "ERROR|WARN" afs/week4/logs || true
