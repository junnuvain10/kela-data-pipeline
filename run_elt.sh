#!/bin/bash

# Define log directory and timestamped log file
LOG_DIR="logs"
TIMESTAMP=$(date +"%d-%m-%Y_%H%M%S")
LOG_FILE="${LOG_DIR}/pipeline_run_${TIMESTAMP}.log"

# Ensure the log directory exists (does not fail if it already exists)
mkdir -p "${LOG_DIR}"

echo "Starting Kela monthly data pipeline..."
echo "Orchestrator running, logs are being saved to: ${LOG_FILE}"

# Run the orchestrator using uv and redirect output (stdout and stderr) to the log file
uv run python src/orchestrator.py > "${LOG_FILE}" 2>&1

# Check execution success from the Linux exit code ($?)
if [ $? -eq 0 ]; then
    echo "✅ Data pipeline run successful! Check the log for details."
else
    echo "❌ Data pipeline run failed! Check the log for errors: ${LOG_FILE}"
fi