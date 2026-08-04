import hashlib
import hmac
import os
import sqlite3
import re
from datetime import date
from pathlib import Path
from typing import Dict, Optional, Tuple


DATABASE_FILE = Path(__file__).parent / "customers.db"
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def get_connection(database_file: Path = DATABASE_FILE) -> sqlite3.Connection:
    connection = sqlite3.connect(database_file)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database(database_file: Path = DATABASE_FILE) -> None:
    with get_connection(database_file) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                full_name TEXT NOT NULL,
                address TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                recovery_email TEXT,
                password_hash BLOB NOT NULL,
                password_salt BLOB NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(customers)")
        }
        if "recovery_email" not in columns:
            connection.execute("ALTER TABLE customers ADD COLUMN recovery_email TEXT")
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_customers_recovery_email
            ON customers(recovery_email COLLATE NOCASE)
            WHERE recovery_email IS NOT NULL
            """
        )


def _normalise_email(email: str) -> str:
    return email.strip().lower()


def _valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email))


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600_000)


def register_customer(
    username: str,
    full_name: str,
    address: str,
    date_of_birth: date,
    recovery_email: str,
    password: str,
    database_file: Path = DATABASE_FILE,
) -> Tuple[bool, str]:
    username = username.strip()
    full_name = full_name.strip()
    address = address.strip()
    recovery_email = _normalise_email(recovery_email)

    if not all((username, full_name, address, date_of_birth, recovery_email, password)):
        return False, "Please complete every registration field."
    if not _valid_email(recovery_email):
        return False, "Please enter a valid recovery email address."
    if len(username) < 4:
        return False, "Username must contain at least 4 characters."
    if len(password) < 8:
        return False, "Password must contain at least 8 characters."
    if date_of_birth > date.today():
        return False, "Date of birth cannot be in the future."

    initialise_database(database_file)
    salt = os.urandom(16)
    password_hash = _hash_password(password, salt)
    try:
        with get_connection(database_file) as connection:
            connection.execute(
                """
                INSERT INTO customers
                    (username, full_name, address, date_of_birth, recovery_email,
                     password_hash, password_salt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (username, full_name, address, date_of_birth.isoformat(), recovery_email,
                 password_hash, salt),
            )
    except sqlite3.IntegrityError:
        return False, "That username or recovery email is already registered."
    return True, "Registration successful. You can now log in."


def authenticate_customer(
    username: str, password: str, database_file: Path = DATABASE_FILE
) -> Optional[Dict]:
    initialise_database(database_file)
    with get_connection(database_file) as connection:
        customer = connection.execute(
            """
            SELECT id, username, full_name, recovery_email, password_hash, password_salt
            FROM customers WHERE username = ?
            """,
            (username.strip(),),
        ).fetchone()

    if customer is None:
        return None
    candidate_hash = _hash_password(password, customer["password_salt"])
    if not hmac.compare_digest(candidate_hash, customer["password_hash"]):
        return None
    return {
        "id": customer["id"],
        "username": customer["username"],
        "full_name": customer["full_name"],
        "recovery_email": customer["recovery_email"],
    }


def set_recovery_email(
    customer_id: int, recovery_email: str, database_file: Path = DATABASE_FILE
) -> Tuple[bool, str]:
    recovery_email = _normalise_email(recovery_email)
    if not _valid_email(recovery_email):
        return False, "Please enter a valid recovery email address."

    initialise_database(database_file)
    try:
        with get_connection(database_file) as connection:
            result = connection.execute(
                "UPDATE customers SET recovery_email = ? WHERE id = ?",
                (recovery_email, customer_id),
            )
            if result.rowcount == 0:
                return False, "Customer account was not found."
    except sqlite3.IntegrityError:
        return False, "That recovery email is already used by another account."
    return True, "Recovery email saved successfully."


def reset_customer_password(
    username: str,
    recovery_email: str,
    date_of_birth: date,
    new_password: str,
    database_file: Path = DATABASE_FILE,
) -> Tuple[bool, str]:
    """Reset a password after matching the customer's registered details."""
    username = username.strip()
    recovery_email = _normalise_email(recovery_email)

    if not all((username, recovery_email, date_of_birth, new_password)):
        return False, "Please complete every password reset field."
    if not _valid_email(recovery_email):
        return False, "Please enter a valid recovery email address."
    if len(new_password) < 8:
        return False, "New password must contain at least 8 characters."
    if date_of_birth > date.today():
        return False, "Date of birth cannot be in the future."

    initialise_database(database_file)
    with get_connection(database_file) as connection:
        customer = connection.execute(
            """
            SELECT id FROM customers
            WHERE username = ? COLLATE NOCASE
              AND recovery_email = ? COLLATE NOCASE
              AND date_of_birth = ?
            """,
            (username, recovery_email, date_of_birth.isoformat()),
        ).fetchone()

        if customer is None:
            return False, "The account details do not match our records."

        salt = os.urandom(16)
        password_hash = _hash_password(new_password, salt)
        connection.execute(
            """
            UPDATE customers
            SET password_hash = ?, password_salt = ?
            WHERE id = ?
            """,
            (password_hash, salt, customer["id"]),
        )

    return True, "Password changed successfully. You can now log in."
