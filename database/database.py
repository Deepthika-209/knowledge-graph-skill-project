import sqlite3
from pathlib import Path


# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = (
    DATABASE_DIR / "academic_skill_graph.db"
)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'student',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------
    # MIGRATION FOR EXISTING DATABASE
    # --------------------------------------------------
    # If the database was created before the role
    # column existed, add the column now.
    # --------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    if "role" not in columns:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN role TEXT
            NOT NULL DEFAULT 'student'
        """)

    # --------------------------------------------------
    # STUDENT PROFILES
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            student_id TEXT UNIQUE,

            name TEXT NOT NULL,

            college TEXT,

            branch TEXT,

            graduation_year INTEGER,

            target_domain TEXT,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    # --------------------------------------------------
    # STUDENT SKILLS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_skills (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            skill_name TEXT NOT NULL,

            proficiency INTEGER DEFAULT 1,

            FOREIGN KEY (user_id)
                REFERENCES users(id),

            UNIQUE(user_id, skill_name)
        )
    """)

    # --------------------------------------------------
    # STUDENT INTERESTS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_interests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            domain_name TEXT NOT NULL,

            FOREIGN KEY (user_id)
                REFERENCES users(id),

            UNIQUE(user_id, domain_name)
        )
    """)

    # --------------------------------------------------
    # STUDENT PROJECTS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            project_name TEXT NOT NULL,

            description TEXT,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    # --------------------------------------------------
    # SAVED RECOMMENDATIONS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_recommendations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            recommendation_type TEXT NOT NULL,

            recommendation_name TEXT NOT NULL,

            saved_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    initialize_database()

    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)

    print(
        "\nDatabase initialized successfully!"
    )

    print(
        f"Database location:\n{DATABASE_FILE}"
    )

    print("\nUsers table columns:")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = cursor.fetchall()

    for column in columns:

        print(
            f"  {column['name']}"
        )

    connection.close()

    print("\n" + "=" * 60)