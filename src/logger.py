import logging
import os
from datetime import datetime

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# 1. Try to get the timestamp from the environment variable (set by the pipeline), if it exists.
# 2. If the environment variable doesn't exist, use the current timestamp.

timestamp = os.environ.get("RUN_TIMESTAMP", datetime.now().strftime("%d-%m-%Y_%H%M%S"))
log_filename = f"logs/pipeline_run_{timestamp}.log"

# Configure the logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Function to get a logger instance
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)