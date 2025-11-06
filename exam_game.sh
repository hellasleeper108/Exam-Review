#!/bin/bash
# Exam Review Game - Shell wrapper
# This script runs the Python exam review application

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Run the Python application
python3 "$SCRIPT_DIR/review.py" "$@"
