import tkinter as tk
from tkinter import filedialog, messagebox

from key_generator import generate_keys
from signer import sign_file
from verifier import verify_file

selected_file = None


def browse_file():
    global selected_file
    selected_file = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
    )

    if selected_file:
        file_label.config(text=selected_file)


def generate():
    generate_keys()
    messagebox.showinfo("Success", "Keys Generated Successfully")


def sign():
    if not selected_file:
        messagebox.showwarning("Warning", "Select a file first")
        return

    sig_path = sign_file(selected_file)
    messagebox.showinfo("Signed", f"Signature saved:\n{sig_path}")


def verify():
    if not selected_file:
        messagebox.showwarning("Warning", "Select a file first")
        return

    valid = verify_file(selected_file)

    if valid:
        result_label.config(text="✓ VALID SIGNATURE", fg="green")
    else:
        result_label.config(text="✗ INVALID SIGNATURE", fg="red")


root = tk.Tk()
root.title("Digital Signature System")
root.geometry("600x400")

title = tk.Label(
    root,
    text="Digital Signature Verification System",
    font=("Arial", 16, "bold")
)
title.pack(pady=20)

tk.Button(root, text="Generate Keys", command=generate).pack(pady=5)
tk.Button(root, text="Select File", command=browse_file).pack(pady=5)
tk.Button(root, text="Sign File", command=sign).pack(pady=5)
tk.Button(root, text="Verify Signature", command=verify).pack(pady=5)

file_label = tk.Label(root, text="No File Selected")
file_label.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=20)

root.mainloop()