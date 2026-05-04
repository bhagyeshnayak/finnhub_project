from database.db_connection import connect_db

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        ticker VARCHAR(50) UNIQUE,
        country VARCHAR(50),
        industry VARCHAR(100),
        market_cap DOUBLE
    )
    """)

    conn.commit()
    conn.close()