import os
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

def get_connection() -> connection:
    """
    Establishes and returns a connection to the PostgreSQL database.
    The caller is responsible for closing the connection.
    """
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

if __name__ == "__main__":
    # Test the database connection
    try:
        conn = get_connection()
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
  