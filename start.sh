#!/usr/bin/env bash

# Activate environment
source .venv/bin/activate

# Install dependencies if missing
pip install -r requirements.txt > /dev/null 2>&1

# Run your project
python src/main.py