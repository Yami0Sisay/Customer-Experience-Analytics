import psycopg2

def get_connection():
    """
    Helper to create a PostgreSQL connection.
    Adjust user/password if you changed them during installation.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="bank_reviews",
        user="bank_user",      
        password="bank_user_123"  
    )
    return conn


def main():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM banks;")
        count = cur.fetchone()[0]
        print(f"Connected successfully. banks table has {count} rows.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error while connecting/querying PostgreSQL:")
        print(e)


if __name__ == "__main__":
    main()
