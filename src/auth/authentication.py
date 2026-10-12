import sys
from pathlib import Path

import bcrypt


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from database.database import get_connection


# ---------------------------------------------------------
# Password hashing
# ---------------------------------------------------------

def hash_password(password):
    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


# ---------------------------------------------------------
# Password verification
# ---------------------------------------------------------

def verify_password(password, hashed_password):
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_password_bytes
    )


# ---------------------------------------------------------
# Register user
# ---------------------------------------------------------

def register_user(email, password):

    email = email.strip().lower()

    if not email:
        return False, "Email is required."

    if not password:
        return False, "Password is required."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (email, password_hash)
        )

        connection.commit()

        return True, "Registration successful."

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):
            return False, "An account with this email already exists."

        return False, f"Registration failed: {error}"

    finally:
        connection.close()


# ---------------------------------------------------------
# Login user
# ---------------------------------------------------------

def login_user(email, password):

    email = email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, email, password_hash, role
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    if verify_password(
        password,
        user["password_hash"]
    ):

        return {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"]
        }

    return None


# ---------------------------------------------------------
# Test authentication
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Testing authentication system...")
    print("-" * 40)

    test_email = "test@example.com"
    test_password = "Test@123"

    success, message = register_user(
        test_email,
        test_password
    )

    print("Registration:", message)

    user = login_user(
        test_email,
        test_password
    )

    if user:

        print("Login: successful")
        print("User ID:", user["id"])
        print("Email:", user["email"])
        print("Role:", user["role"])

    else:

        print("Login: failed")