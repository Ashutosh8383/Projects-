import hashlib
import time
failed_attempts = {}
locked_accounts = {}

MAX_ATTEMPTS = 3
LOCK_TIME = 30

from database import connect_db
from logger_util import log_event

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def register_user(username, password):

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username,password_hash) VALUES (?,?)",
            (username, hash_password(password))
        )

        conn.commit()

        log_event(
            f"REGISTER SUCCESS : {username}"
        )

        return True

    except:

        return False

    finally:
        conn.close()

def user_exists(username):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None

def login_user(username, password):

    current_time = time.time()

    # Check if account is locked
    if username in locked_accounts:

        unlock_time = locked_accounts[username]

        if current_time < unlock_time:

            remaining = int(
                unlock_time - current_time
            )

            return (
                False,
                f"Account Locked. Try again in {remaining} seconds."
            )

        else:

            del locked_accounts[username]

            failed_attempts[username] = 0

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        if result[0] == hash_password(password):

            failed_attempts[username] = 0

            log_event(
                f"LOGIN SUCCESS : {username}"
            )

            return (
                True,
                "Login Successful"
            )
        else:
            failed_attempts[username] = (
                failed_attempts.get(username, 0) + 1
            )

            if failed_attempts[username] >= MAX_ATTEMPTS:

                locked_accounts[username] = (
                    current_time + LOCK_TIME
                )

                log_event(
                    f"ACCOUNT LOCKED : {username}"
                )

                return (
                    False,
                    "Too many failed attempts. Account locked for 30 seconds."
                )

            log_event(
                f"LOGIN FAILED : {username} - WRONG PASSWORD"
            )

            remaining = (
                MAX_ATTEMPTS -
                failed_attempts[username]
            )

            return (
                False,
                f"❌ Your password is wrong! Attempts left: {remaining}"
            )
    else:
        log_event(
            f"LOGIN FAILED : {username} - USER NOT FOUND"
        )

        return (
            False,
            f"❌ Username '{username}' does not exist. Please register first!"
        )