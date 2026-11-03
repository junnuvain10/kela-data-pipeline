from database_connection import get_connection
from logger import get_logger

logger = get_logger(__name__)

def setup_database():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            logger.info("Creating OLTP schema...")
            with open("sql/01_create_oltp.sql", "r", encoding="utf-8") as file:
                cur.execute(file.read())
            
            logger.info("Creating OLAP (Star) schema...")
            with open("sql/02_create_olap.sql", "r", encoding="utf-8") as file:
                cur.execute(file.read())
            
            conn.commit()
            logger.info("Database schemas created successfully.")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Database setup failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()