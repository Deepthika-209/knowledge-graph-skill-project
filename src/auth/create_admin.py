import sys
from pathlib import Path
import getpass

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database import get_connection
from src.auth.authentication import hash_password


# --------------------------------------------------
# CREATE ADMIN
# --------------------------------------------------

def create_admin():

    print("=" * 60)
    print("CREATE ADMIN ACCOUNT")
    print("=" * 60)

    email = input(
        "\nAdmin email: "
    ).strip().lower()

    if not email:

        print(
            "\nEmail cannot be empty."
        )

        return

    password = getpass.getpass(
        "Admin password: "
    )

    confirm_password = getpass.getpass(
        "Confirm password: "
    )

    if not password:

        print(
            "\nPassword cannot be empty."
        )

        return

    if len(password) < 6:

        print(
            "\nPassword must contain at least 6 characters."
        )

        return

    if password != confirm_password:

        print(
            "\nPasswords do not match."
        )

        return

    password_hash = hash_password(
        password
    )

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # --------------------------------------------------
        # CHECK EXISTING USER
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT id, email, role
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        # --------------------------------------------------
        # EXISTING USER
        # --------------------------------------------------

        if existing_user:

            cursor.execute(
                """
                UPDATE users
                SET password_hash = ?,
                    role = 'admin'
                WHERE id = ?
                """,
                (
                    password_hash,
                    existing_user["id"]
                )
            )

            connection.commit()

            print(
                "\nExisting account converted to ADMIN."
            )

        # --------------------------------------------------
        # NEW USER
        # --------------------------------------------------

        else:

            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    password_hash,
                    role
                )
                VALUES (?, ?, 'admin')
                """,
                (
                    email,
                    password_hash
                )
            )

            connection.commit()

            print(
                "\nAdmin account created successfully."
            )

        print(
            f"\nAdmin email: {email}"
        )

        print(
            "Role: admin"
        )

    except Exception as error:

        connection.rollback()

        print(
            f"\nFailed to create admin: {error}"
        )

    finally:

        connection.close()

    print(
        "\n" + "=" * 60
    )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    create_admin()