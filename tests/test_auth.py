from datetime import date

from auth import (
    authenticate_customer, register_customer, reset_customer_password,
    set_recovery_email,
)


def test_customer_registration_and_login(tmp_path):
    database = tmp_path / "customers.db"
    success, _ = register_customer(
        "testuser", "Test Customer", "1 Test Street", date(1990, 5, 10),
        "test@example.com", "SecurePass123", database,
    )
    assert success
    assert authenticate_customer("testuser", "SecurePass123", database)["full_name"] == "Test Customer"
    assert authenticate_customer("testuser", "wrong-password", database) is None


def test_duplicate_username_is_rejected(tmp_path):
    database = tmp_path / "customers.db"
    details = ("testuser", "Test Customer", "1 Test Street", date(1990, 5, 10), "test@example.com", "SecurePass123", database)
    assert register_customer(*details)[0]
    assert not register_customer(*details)[0]


def test_forgot_password_resets_login(tmp_path):
    database = tmp_path / "customers.db"
    birth_date = date(1990, 5, 10)
    assert register_customer(
        "testuser", "Test Customer", "1 Test Street", birth_date,
        "test@example.com", "SecurePass123", database,
    )[0]

    success, _ = reset_customer_password(
        "testuser", "test@example.com", birth_date, "NewSecurePass456", database
    )

    assert success
    assert authenticate_customer("testuser", "SecurePass123", database) is None
    assert authenticate_customer("testuser", "NewSecurePass456", database) is not None


def test_forgot_password_rejects_wrong_details(tmp_path):
    database = tmp_path / "customers.db"
    birth_date = date(1990, 5, 10)
    assert register_customer(
        "testuser", "Test Customer", "1 Test Street", birth_date,
        "test@example.com", "SecurePass123", database,
    )[0]

    success, _ = reset_customer_password(
        "testuser", "wrong@example.com", birth_date, "NewSecurePass456", database
    )

    assert not success
    assert authenticate_customer("testuser", "SecurePass123", database) is not None


def test_existing_customer_can_add_recovery_email(tmp_path):
    database = tmp_path / "customers.db"
    assert register_customer(
        "testuser", "Test Customer", "1 Test Street", date(1990, 5, 10),
        "first@example.com", "SecurePass123", database,
    )[0]
    customer = authenticate_customer("testuser", "SecurePass123", database)
    assert set_recovery_email(customer["id"], "new@example.com", database)[0]
    assert authenticate_customer("testuser", "SecurePass123", database)["recovery_email"] == "new@example.com"
