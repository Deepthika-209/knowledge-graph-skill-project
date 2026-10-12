from database import get_connection


def check_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    print("\nDatabase tables:")
    print("-" * 30)

    for table in tables:
        print(table["name"])

    connection.close()


if __name__ == "__main__":
    check_database()