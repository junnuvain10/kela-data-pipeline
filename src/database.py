import os
import logging
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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