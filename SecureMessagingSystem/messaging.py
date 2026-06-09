import uuid
from datetime import datetime

from database import connect_db
from crypto_utils import (
    encrypt_message,
    decrypt_message,
    create_hmac,
    verify_hmac
)

from logger_util import log_event

def send_message(
        sender,
        receiver,
        message
):

    encrypted = encrypt_message(
        message
    )

    hmac_value = create_hmac(
        message
    )

    timestamp = str(
        datetime.now()
    )

    conn = connect_db()

    cursor = conn.cursor()

    message_id = str(uuid.uuid4())
   
    cursor.execute(
    """
    INSERT INTO messages(
    message_id,
    sender,
    receiver,
    encrypted_message,
    hmac_value,
    timestamp
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        message_id,
        sender,
        receiver,
        encrypted,
        hmac_value,
        timestamp
    )
)

    conn.commit()
    conn.close()

    log_event(
        f"MESSAGE SENT {sender}->{receiver}"
    )

def read_messages(user):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender,
               encrypted_message,
               hmac_value,
               timestamp
        FROM messages
        WHERE receiver=?
        """,
        (user,)
    )

    rows = cursor.fetchall()

    conn.close()

    messages = []

    for sender, encrypted, hmac_val, timestamp in rows:

        plain = decrypt_message(
            encrypted
        )

        status = verify_hmac(
            plain,
            hmac_val
        )

        messages.append(
            (
                sender,
                plain,
                status,
                timestamp
            )
        )

    return messages

def check_replay_attack(message_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM messages
        WHERE message_id=?
        """,
        (message_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count > 1