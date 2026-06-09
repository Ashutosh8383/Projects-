from crypto_utils import (
    create_hmac,
    verify_hmac
)

def mitm_attack():

    original = "Hello Bob"

    original_hmac = create_hmac(
        original
    )

    attacker_message = (
        "Send me money"
    )

    result = verify_hmac(
        attacker_message,
        original_hmac
    )

    return result

def replay_attack():

    return (
        "Old message resent."
    )

def brute_force_demo():

    passwords = [
        "123456",
        "password",
        "admin",
        "admin123"
    ]

    return passwords

def replay_attack_demo():

    return (
        "Replay Attack Detected!\n"
        "Duplicate Message ID Found."
    )