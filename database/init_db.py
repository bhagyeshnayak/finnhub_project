"""Database initialization script - creates database and tables if they don't exist"""
import mysql.connector
import os

def init_database():
    """Create the finnhub database if it doesn't exist"""
    try:
        # Connect without specifying a database
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root")
        )
        cursor = conn.cursor()
        
        db_name = os.getenv("DB_NAME", "finnhub")
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✓ Database '{db_name}' is ready")
        
        cursor.close()
        conn.close()
        
        # Now create tables
        from database.models import create_table
        create_table()
        print("✓ Tables created successfully")
        
    except mysql.connector.Error as e:
        if e.errno == 2003:
            print("✗ Error: Cannot connect to MySQL server. Make sure MySQL is running.")
        else:
            print(f"✗ Database Error: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        raise


if __name__ == "__main__":
    init_database()
