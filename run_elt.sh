#!/bin/bash

# Set the timestamp for the run
export RUN_TIMESTAMP=$(date +"%d-%m-%Y_%H%M%S")

echo "Starting Kela data pipeline..."

# Run the orchestrator using uv (Python's logger handles the log files automatically)
uv run python src/orchestrator.py

# Check execution success from the Linux exit code ($?)
if [ $? -eq 0 ]; then
    echo "✅ Data pipeline run successful! Check the logs folder for details."
else
    echo "❌ Data pipeline run failed! Check the logs folder for errors."
fi