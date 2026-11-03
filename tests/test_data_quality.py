import os
import sys
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from database_connection import get_connection
from logger import get_logger

logger = get_logger(__name__)

# Function to build SQL queries based on the test type
def build_sql_query(test):
    t_type = test["type"]
    table = test["table"]
    col = test["column"]

# Each test type has a different SQL query structure. We will build the query based on the test type.
    if t_type == "uniqueness":
        return f"SELECT COUNT(*) FROM (SELECT {col} FROM {table} GROUP BY {col} HAVING COUNT(*) > 1) AS duplicates;"
    elif t_type == "not_null":
        return f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL;"
    elif t_type == "referential_integrity":
        ref_table = test["ref_table"]
        ref_col = test["ref_column"]
        return f"""
            SELECT COUNT(*) FROM {table} f
            LEFT JOIN {ref_table} d ON f.{col} = d.{ref_col}
            WHERE d.{ref_col} IS NULL;
        """
    else:
        raise ValueError(f"Unknown test type: {t_type}")

def main():
    logger.info("--- Running Dynamic Data Quality Checks ---")

    # Load the data quality tests from the JSON configuration file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'data_quality_tests.json')

    # Check if the configuration file exists
    with open(config_path, 'r') as f:
        tests = json.load(f)

    conn = get_connection()
    all_passed = True

# Execute each test and log the results
    with conn.cursor() as cur:
        for test in tests:
            query = build_sql_query(test)
            try:
                cur.execute(query)
                result = cur.fetchone()[0]
                
                if result == 0:
                    logger.info(f"[PASS] {test['name']}")
                else:
                    logger.error(f"[FAIL] {test['name']} (Failed: {result} violation(s) found)")
                    all_passed = False
            except Exception as e:
                logger.error(f"[ERROR] {test['name']}: {e}")
                all_passed = False

    conn.close()
    
    if all_passed:
        logger.info("All Data Quality checks passed successfully!")
        sys.exit(0)
    else:
        logger.error("Data Quality checks failed. Pipeline stopped.")
        sys.exit(1)

if __name__ == "__main__":
    main()