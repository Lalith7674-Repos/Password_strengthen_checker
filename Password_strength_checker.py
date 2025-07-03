import tkinter as tk
from tkinter import messagebox
import re
import math
import string

class PasswordCheckerApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")

        self.title_font = ("Helvetica", 24, "bold")
        self.label_font = ("Helvetica", 12)
        self.result_font = ("Helvetica", 12, "italic")

        self.container = tk.Frame(root, bg="#1a1a1a")
        self.container.pack(expand=True, fill="both", padx=40, pady=40)

        self.title_label = tk.Label(
            self.container,
            text="Password Strength Analyzer",
            font=self.title_font,
            fg="#ffffff",
            bg="#1a1a1a",
            wraplength=400
        )
        self.title_label.pack(pady=(0, 30))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.container,
            textvariable=self.password_var,
            show="*",
            font=self.label_font,
            bg="#2c2c2c",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            width=30
        )
        self.password_entry.pack(pady=(0, 20), ipady=8)

        self.show_var = tk.BooleanVar()
        self.show_check = tk.Checkbutton(
            self.container,
            text="Show Password",
            variable=self.show_var,
            command=self.toggle_password,
            bg="#1a1a1a",
            fg="#aaaaaa",
            selectcolor="#1a1a1a",
            activebackground="#1a1a1a",
            activeforeground="#ffffff"
        )
        self.show_check.pack()

        self.check_button = tk.Button(
            self.container,
            text="Analyze Password",
            command=self.analyze_password,
            bg="#4CAF50",
            fg="#ffffff",
            font=self.label_font,
            relief="flat",
            activebackground="#45a049",
            cursor="hand2"
        )
        self.check_button.pack(pady=20, ipadx=20, ipady=8)

        self.result_label = tk.Label(
            self.container,
            text="",
            font=self.result_font,
            fg="#ffffff",
            bg="#1a1a1a",
            wraplength=400,
            justify="left"
        )
        self.result_label.pack(pady=(20, 0))

        self.strength_canvas = tk.Canvas(
            self.container,
            height=10,
            width=300,
            bg="#2c2c2c",
            highlightthickness=0
        )
        self.strength_canvas.pack(pady=(20, 0))

    def toggle_password(self):
        """Show or hide the password in the entry field."""
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def calculate_entropy(self, password):
        """Estimate the entropy (strength) of the password."""
        pool_size = 0
        if re.search(r"[a-z]", password):
            pool_size += 26
        if re.search(r"[A-Z]", password):
            pool_size += 26
        if re.search(r"[0-9]", password):
            pool_size += 10
        if re.search(r"[^a-zA-Z0-9]", password):
            pool_size += len(string.punctuation)

        if pool_size == 0:
            return 0
        return len(password) * math.log2(pool_size)

    def analyze_password(self):
        """Analyze the entered password and update the UI with feedback."""
        password = self.password_var.get()

        self.result_label.config(text="")
        self.strength_canvas.delete("all")

        if not password:
            messagebox.showwarning("Input Error", "Please enter a password!")
            return

        length_ok = len(password) >= 8
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"[0-9]", password))
        has_special = bool(re.search(r"[^a-zA-Z0-9]", password))

        entropy = self.calculate_entropy(password)

        score = sum([length_ok, has_lower, has_upper, has_digit, has_special])

        if entropy < 30 or score <= 2:
            strength = "Weak"
            color = "#ff4444"
            bar_width = 100
        elif entropy < 50 or score <= 3:
            strength = "Moderate"
            color = "#ffbb33"
            bar_width = 200
        else:
            strength = "Strong"
            color = "#00C851"
            bar_width = 300

        self.strength_canvas.create_rectangle(
            0, 0, bar_width, 10, fill=color, outline=""
        )

        feedback = f"Password Strength: {strength}\nEntropy: {entropy:.2f} bits\n\n"
        feedback += "Checklist:\n"
        feedback += f"✓ Length (8+): {'Yes' if length_ok else 'No'}\n"
        feedback += f"✓ Lowercase: {'Yes' if has_lower else 'No'}\n"
        feedback += f"✓ Uppercase: {'Yes' if has_upper else 'No'}\n"
        feedback += f"✓ Numbers: {'Yes' if has_digit else 'No'}\n"
        feedback += f"✓ Special Characters: {'Yes' if has_special else 'No'}\n"

        self.result_label.config(text=feedback)

def main():
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()