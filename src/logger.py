import logging

# Default logging configuration for the entire project
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger(name: str) -> logging.Logger:
    """Returns a named logger for use across the project."""
    return logging.getLogger(name)