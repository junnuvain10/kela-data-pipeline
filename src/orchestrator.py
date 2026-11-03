import subprocess
import sys
import time
from logger import get_logger

logger = get_logger(__name__)

def run_script(script_path: str):
    logger.info(f"Starting: {script_path}")
    
    # Run the script and capture its output
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Failed: {script_path}\nError details:\n{result.stderr}")
        # Stop the entire pipeline if a single step fails
        sys.exit(1) 
    
    logger.info(f"Completed: {script_path}\n{result.stdout}")

def main():
    logger.info("--- Kela Data Pipeline: Started ---")
    start_time = time.time()  # Start the clock
    
    # Execute pipeline steps in strict order
    run_script("src/setup_database.py")
    run_script("src/generate_data.py")
    run_script("src/elt_process.py")
    run_script("tests/test_data_quality.py")
    
    end_time = time.time()  # Stop the clock
    duration = end_time - start_time
    
    logger.info("--- Kela Data Pipeline: Completed Successfully ---")
    logger.info(f"Total execution time: {duration:.2f} seconds")

if __name__ == "__main__":
    main()