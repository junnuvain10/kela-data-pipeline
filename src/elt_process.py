from database_connection import get_connection
from logger import get_logger

logger = get_logger(__name__)


def run_elt_process():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            logger.info("Starting ELT transformation (OLTP -> OLAP)...")
            
            # Read pure SQL commands from a separate file
            with open("sql/03_elt_process.sql", "r", encoding="utf-8") as file:
                sql_script = file.read()
            
            cur.execute(sql_script)
            conn.commit()
            logger.info("ELT transformation completed successfully.")
            
    except Exception as e:
        conn.rollback() # Automatically roll back changes in case of an error
        logger.error(f"ELT process failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    run_elt_process()