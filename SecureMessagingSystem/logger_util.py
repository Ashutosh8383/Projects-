from datetime import datetime

LOG_FILE = "data/logs.txt"

def log_event(event):

    with open(LOG_FILE, "a") as file:
        file.write(
            f"[{datetime.now()}] {event}\n"
        )