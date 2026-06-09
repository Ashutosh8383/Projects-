import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

from database import create_tables
from auth import register_user, login_user, user_exists
from messaging import send_message, read_messages
from attack_simulation import mitm_attack
from attack_simulation import (
    replay_attack_demo
)

create_tables()

current_user = None
current_theme = "light"

root = tk.Tk()
root.title("Secure Messaging System")
root.geometry("900x650")
root.resizable(False, False)

# Light Theme Colors
LIGHT_PRIMARY_COLOR = "#2E86AB"
LIGHT_SECONDARY_COLOR = "#A23B72"
LIGHT_SUCCESS_COLOR = "#06A77D"
LIGHT_DANGER_COLOR = "#D62828"
LIGHT_BG = "#F7F9FC"
LIGHT_TEXT = "#1F2937"
LIGHT_BORDER_COLOR = "#E5E7EB"
LIGHT_CARD_BG = "white"

# Dark Theme Colors
DARK_PRIMARY_COLOR = "#1A202C"
DARK_SECONDARY_COLOR = "#D97706"
DARK_SUCCESS_COLOR = "#059669"
DARK_DANGER_COLOR = "#EF4444"
DARK_BG = "#0F1419"
DARK_TEXT = "#F3F4F6"
DARK_BORDER_COLOR = "#374151"
DARK_CARD_BG = "#1F2937"

# Default to light theme
PRIMARY_COLOR = LIGHT_PRIMARY_COLOR
SECONDARY_COLOR = LIGHT_SECONDARY_COLOR
SUCCESS_COLOR = LIGHT_SUCCESS_COLOR
DANGER_COLOR = LIGHT_DANGER_COLOR
BG_COLOR = LIGHT_BG
TEXT_COLOR = LIGHT_TEXT
BORDER_COLOR = "#2E86AB"
CARD_BG = LIGHT_CARD_BG

# Configure style
style = ttk.Style()
style.theme_use('clam')

# Modern button style
style.configure('Accent.TButton',
    font=('Segoe UI', 10, 'bold'),
    padding=10
)

style.map('Accent.TButton',
    background=[('active', SECONDARY_COLOR)]
)

def toggle_theme():
    global current_theme, PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, DANGER_COLOR, BG_COLOR, TEXT_COLOR, BORDER_COLOR, CARD_BG

    if current_theme == "light":
        current_theme = "dark"
        PRIMARY_COLOR = DARK_PRIMARY_COLOR
        SECONDARY_COLOR = DARK_SECONDARY_COLOR
        SUCCESS_COLOR = DARK_SUCCESS_COLOR
        DANGER_COLOR = DARK_DANGER_COLOR
        BG_COLOR = DARK_BG
        TEXT_COLOR = DARK_TEXT
        BORDER_COLOR = DARK_PRIMARY_COLOR
        CARD_BG = DARK_CARD_BG
    else:
        current_theme = "light"
        PRIMARY_COLOR = LIGHT_PRIMARY_COLOR
        SECONDARY_COLOR = LIGHT_SECONDARY_COLOR
        SUCCESS_COLOR = LIGHT_SUCCESS_COLOR
        DANGER_COLOR = LIGHT_DANGER_COLOR
        BG_COLOR = LIGHT_BG
        TEXT_COLOR = LIGHT_TEXT
        BORDER_COLOR = "#2E86AB"
        CARD_BG = LIGHT_CARD_BG

    if current_user:
        show_dashboard()
    else:
        show_login()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def create_header(parent, title, subtitle=""):
    header_frame = tk.Frame(parent, bg=PRIMARY_COLOR, height=80)
    header_frame.pack(fill=tk.X)

    # Title section
    title_frame = tk.Frame(header_frame, bg=PRIMARY_COLOR)
    title_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    title_label = tk.Label(
        title_frame,
        text=title,
        font=("Segoe UI", 28, "bold"),
        bg=PRIMARY_COLOR,
        fg="white"
    )
    title_label.pack(side=tk.LEFT, pady=5)

    # Theme toggle button (right side)
    theme_emoji = "🌙" if current_theme == "light" else "☀️"
    theme_btn = tk.Button(
        title_frame,
        text=theme_emoji,
        command=toggle_theme,
        font=("Segoe UI", 14),
        bg=PRIMARY_COLOR,
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        relief=tk.FLAT
    )
    theme_btn.pack(side=tk.RIGHT)

    if subtitle:
        subtitle_label = tk.Label(
            header_frame,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=PRIMARY_COLOR,
            fg="#E0E7FF"
        )
        subtitle_label.pack()

def create_input_field(parent, label_text, show_char=None):
    frame = tk.Frame(parent, bg=CARD_BG)
    frame.pack(fill=tk.X, padx=20, pady=12)

    label = tk.Label(
        frame,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg=TEXT_COLOR
    )
    label.pack(anchor=tk.W, pady=(0, 5))

    entry = tk.Entry(
        frame,
        font=("Segoe UI", 11),
        show=show_char,
        bd=1,
        relief=tk.FLAT,
        bg=CARD_BG if current_theme == "dark" else "white",
        fg=TEXT_COLOR
    )
    entry.pack(fill=tk.X, ipady=8)

    return entry

def create_button(parent, text, command, bg_color=PRIMARY_COLOR, width=30):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 12, "bold"),
        bg=bg_color,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    button.pack(pady=10, fill=tk.X)
    return button

def show_replay_demo():
    messagebox.showwarning(
        "Replay Attack",
        replay_attack_demo()
    )

# ==========================
# LOGIN PAGE
# ==========================

def show_login():
    clear_window()

    # Set window background
    root.config(bg=BG_COLOR)

    # Main container
    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header
    create_header(main_frame, "🔐 Secure Messaging", "Secure Encrypted Communications")

    # Content frame
    content_frame = tk.Frame(main_frame, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # Card
    card_frame = tk.Frame(content_frame, bg=CARD_BG, relief=tk.FLAT, bd=1)
    card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    card_inner = tk.Frame(card_frame, bg=CARD_BG)
    card_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # Form title
    form_title = tk.Label(
        card_inner,
        text="Login to Your Account",
        font=("Segoe UI", 16, "bold"),
        bg=CARD_BG,
        fg=TEXT_COLOR
    )
    form_title.pack(pady=(0, 20))

    # Username field
    username_entry = create_input_field(card_inner, "👤 Username")

    # Password field
    password_entry = create_input_field(card_inner, "🔑 Password", show_char="•")

    def register():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror(
                "⚠️ Error",
                "Please fill all fields!"
            )
            return

        if register_user(username, password):
            messagebox.showinfo(
                "✅ Success",
                f"Registration successful!\nWelcome {username}!"
            )
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        else:
            messagebox.showerror(
                "❌ Error",
                "Username already exists!"
            )

    def login():
        global current_user

        username = username_entry.get()
        password = password_entry.get()

        success, message = login_user(
            username,
            password
        )

        if success:
            current_user = username
            messagebox.showinfo(
                "✅ Success",
                f"Welcome back, {username}! 🎉"
            )
            show_dashboard()
        else:
            messagebox.showerror(
                "❌ Login Failed",
                message
            )

    # Button frame - horizontal layout
    button_frame = tk.Frame(card_inner, bg=CARD_BG)
    button_frame.pack(fill=tk.X, pady=20)

    # Login button (left)
    login_btn_frame = tk.Frame(button_frame, bg=CARD_BG)
    login_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    login_btn = tk.Button(
        login_btn_frame,
        text="🚀 Login",
        command=login,
        font=("Segoe UI", 12, "bold"),
        bg=SUCCESS_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    login_btn.pack(fill=tk.BOTH, expand=True)

    # Register button (right)
    register_btn_frame = tk.Frame(button_frame, bg=CARD_BG)
    register_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

    register_btn = tk.Button(
        register_btn_frame,
        text="📝 Register",
        command=register,
        font=("Segoe UI", 12, "bold"),
        bg=PRIMARY_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    register_btn.pack(fill=tk.BOTH, expand=True)

# ==========================
# DASHBOARD
# ==========================

def show_dashboard():
    clear_window()
    root.config(bg=BG_COLOR)

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header
    create_header(main_frame, f"👋 Welcome, {current_user}!", "Dashboard")

    # Content
    content_frame = tk.Frame(main_frame, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # Cards container
    cards_frame = tk.Frame(content_frame, bg=BG_COLOR)
    cards_frame.pack(fill=tk.BOTH, expand=True)

    def create_dashboard_button(text, emoji, command):
        button = tk.Button(
            cards_frame,
            text=f"{emoji}\n{text}",
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR,
            bd=1,
            relief=tk.FLAT,
            padx=30,
            pady=20,
            cursor="hand2"
        )
        button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Hover effect
        def on_enter(e):
            button.config(bg=PRIMARY_COLOR, fg="white")
        def on_leave(e):
            button.config(bg=CARD_BG, fg=TEXT_COLOR)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    create_dashboard_button("Send Message", "✉️", show_send_message)
    create_dashboard_button("Inbox", "📬", show_inbox)
    create_dashboard_button("MITM Attack Demo", "⚔️", show_attack_demo)
    create_dashboard_button("Replay Attack Demo", "🔄", show_replay_demo)

    # Bottom section with back and logout buttons
    bottom_frame = tk.Frame(content_frame, bg=BG_COLOR)
    bottom_frame.pack(fill=tk.X, pady=20)

    # Button subframe for side-by-side layout
    button_subframe = tk.Frame(bottom_frame, bg=BG_COLOR)
    button_subframe.pack(fill=tk.X)

    # Back button
    back_btn_frame = tk.Frame(button_subframe, bg=BG_COLOR)
    back_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    back_btn = tk.Button(
        back_btn_frame,
        text="⬅️ Back to Login",
        command=logout,
        font=("Segoe UI", 12, "bold"),
        bg=PRIMARY_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    back_btn.pack(fill=tk.BOTH, expand=True)

    # Logout button
    logout_btn_frame = tk.Frame(button_subframe, bg=BG_COLOR)
    logout_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    logout_btn = tk.Button(
        logout_btn_frame,
        text="🚪 Logout",
        command=logout,
        font=("Segoe UI", 12, "bold"),
        bg=DANGER_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground="#991b1b",
        activeforeground="white",
        relief=tk.FLAT
    )
    logout_btn.pack(fill=tk.BOTH, expand=True)

# ==========================
# SEND MESSAGE
# ==========================

def show_send_message():
    clear_window()
    root.config(bg=BG_COLOR)

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_header(main_frame, "✉️ Send Secure Message", "Encrypt and send your message")

    content_frame = tk.Frame(main_frame, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # Card
    card_frame = tk.Frame(content_frame, bg=CARD_BG, relief=tk.FLAT, bd=1)
    card_frame.pack(fill=tk.BOTH, expand=True)

    card_inner = tk.Frame(card_frame, bg=CARD_BG)
    card_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # Receiver field
    receiver_entry = create_input_field(card_inner, "👤 Receiver Username")

    # Message label
    message_label = tk.Label(
        card_inner,
        text="💬 Message",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg=TEXT_COLOR
    )
    message_label.pack(anchor=tk.W, padx=20, pady=(12, 5))

    # Message box
    message_box = ScrolledText(
        card_inner,
        font=("Segoe UI", 10),
        width=70,
        height=12,
        bg=CARD_BG if current_theme == "dark" else "white",
        fg=TEXT_COLOR,
        bd=1,
        relief=tk.FLAT
    )
    message_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def send():
        receiver = receiver_entry.get()
        message = message_box.get("1.0", tk.END).strip()

        if not receiver or not message:
            messagebox.showerror(
                "⚠️ Error",
                "Please fill all fields!"
            )
            return

        if not user_exists(receiver):
            messagebox.showerror(
                "❌ Error",
                f"User '{receiver}' is not registered yet!\nPlease ask them to register first."
            )
            return

        send_message(
            current_user,
            receiver,
            message
        )

        messagebox.showinfo(
            "✅ Success",
            "Message encrypted and sent! 🔒"
        )

        message_box.delete("1.0", tk.END)
        receiver_entry.delete(0, tk.END)

    # Buttons
    button_frame = tk.Frame(card_inner, bg=CARD_BG)
    button_frame.pack(fill=tk.X)

    # Send button
    send_btn_frame = tk.Frame(button_frame, bg=CARD_BG)
    send_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    send_btn = tk.Button(
        send_btn_frame,
        text="📤 Send Message",
        command=send,
        font=("Segoe UI", 12, "bold"),
        bg=SUCCESS_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    send_btn.pack(fill=tk.BOTH, expand=True)

    # Back button
    back_btn_frame = tk.Frame(button_frame, bg=CARD_BG)
    back_btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    back_btn = tk.Button(
        back_btn_frame,
        text="⬅️ Back",
        command=show_dashboard,
        font=("Segoe UI", 12, "bold"),
        bg=PRIMARY_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    back_btn.pack(fill=tk.BOTH, expand=True)

# ==========================
# INBOX
# ==========================

def show_inbox():
    clear_window()
    root.config(bg=BG_COLOR)

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_header(main_frame, "📬 Your Inbox", "View received messages")

    content_frame = tk.Frame(main_frame, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # Card
    card_frame = tk.Frame(content_frame, bg=CARD_BG, relief=tk.FLAT, bd=1)
    card_frame.pack(fill=tk.BOTH, expand=True)

    card_inner = tk.Frame(card_frame, bg=CARD_BG)
    card_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    messages = read_messages(current_user)

    box = ScrolledText(
        card_inner,
        font=("Consolas", 9),
        width=100,
        height=20,
        bg=CARD_BG if current_theme == "dark" else "white",
        fg=TEXT_COLOR,
        bd=1,
        relief=tk.FLAT
    )
    box.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    if not messages:
        box.insert(
            tk.END,
            "📭 No messages found.\n"
        )
    else:
        for sender, message, integrity, timestamp in messages:
            status_icon = "✅" if integrity else "⚠️"
            box.insert(
                tk.END,
                f"\n{'─' * 70}\n"
            )
            box.insert(
                tk.END,
                f"📨 From: {sender}\n"
            )
            box.insert(
                tk.END,
                f"🕐 Time: {timestamp}\n"
            )
            box.insert(
                tk.END,
                f"💬 Message: {message}\n"
            )
            box.insert(
                tk.END,
                f"{status_icon} Integrity: {'Verified ✔️' if integrity else 'FAILED ❌'}\n"
            )

    box.config(state=tk.DISABLED)

    # Buttons
    button_frame = tk.Frame(card_inner, bg=CARD_BG)
    button_frame.pack(fill=tk.X)

    back_btn = tk.Button(
        button_frame,
        text="⬅️ Back",
        command=show_dashboard,
        font=("Segoe UI", 12, "bold"),
        bg=PRIMARY_COLOR,
        fg="white",
        bd=0,
        padx=30,
        pady=15,
        cursor="hand2",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        relief=tk.FLAT
    )
    back_btn.pack(fill=tk.X)

# ==========================
# ATTACK DEMO
# ==========================

def show_attack_demo():
    result = mitm_attack()

    if result:
        messagebox.showinfo(
            "⚔️ MITM Attack Result",
            "Attack Passed (Unexpected)\nIntegrity check was bypassed!"
        )
    else:
        messagebox.showwarning(
            "🛡️ MITM Attack Blocked",
            "Attack Detected!\n\n"
            "Integrity Check Failed.\n"
            "Your message is secure! ✅"
        )

# ==========================
# LOGOUT
# ==========================

def logout():
    global current_user

    current_user = None

    messagebox.showinfo(
        "👋 Logout",
        "You have been logged out successfully!"
    )

    show_login()

# ==========================
# START APP
# ==========================

show_login()

root.mainloop()