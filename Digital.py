"""A simple digital clock built with Python's Tkinter library."""

from datetime import datetime
import tkinter as tk


def update_clock() -> None:
    """Refresh the displayed local time and date once per second."""
    now = datetime.now()
    time_label.config(text=now.strftime("%I:%M:%S %p"))
    date_label.config(text=now.strftime("%A, %B %d, %Y"))
    root.after(1000, update_clock)


root = tk.Tk()
root.title("Digital Clock")
root.geometry("420x220")
root.resizable(False, False)
root.configure(bg="#101820")

heading_label = tk.Label(
    root,
    text="LOCAL TIME",
    font=("Segoe UI", 12, "bold"),
    fg="#00C2A8",
    bg="#101820",
)
heading_label.pack(pady=(28, 4))

time_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 36, "bold"),
    fg="#F2F4F8",
    bg="#101820",
)
time_label.pack()

date_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 12),
    fg="#AAB4C3",
    bg="#101820",
)
date_label.pack(pady=(4, 0))

update_clock()
root.mainloop()