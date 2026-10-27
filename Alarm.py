
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import winsound


class DigitalAlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Alarm Clock")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#101820")

        self.alarm_time = None
        self.alarm_enabled = False
        self.ringing = False
        self.snooze_until = None
        self.last_triggered = None

        self.bg = "#101820"
        self.panel = "#1B2838"
        self.accent = "#00D9FF"
        self.white = "#FFFFFF"
        self.muted = "#AABAC3"
        self.green = "#39D98A"
        self.red = "#FF5C70"

        # Title
        tk.Label(
            root,
            text="DIGITAL ALARM CLOCK",
            font=("Segoe UI", 19, "bold"),
            fg=self.accent,
            bg=self.bg
        ).pack(pady=(20, 10))

        # Current time
        self.time_label = tk.Label(
            root,
            text="00:00:00",
            font=("Consolas", 42, "bold"),
            fg=self.white,
            bg=self.bg
        )
        self.time_label.pack(pady=5)

        self.date_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 12),
            fg=self.muted,
            bg=self.bg
        )
        self.date_label.pack(pady=(0, 20))

        # Alarm settings panel
        panel = tk.Frame(root, bg=self.panel, padx=20, pady=15)
        panel.pack(fill="x", padx=25)

        tk.Label(
            panel,
            text="SET ALARM TIME",
            font=("Segoe UI", 12, "bold"),
            fg=self.white,
            bg=self.panel
        ).grid(row=0, column=0, columnspan=3, pady=(0, 12))

        self.hour_var = tk.StringVar(value="07")
        self.minute_var = tk.StringVar(value="00")

        self.hour_entry = tk.Entry(
            panel,
            textvariable=self.hour_var,
            font=("Consolas", 23),
            width=4,
            justify="center"
        )
        self.hour_entry.grid(row=1, column=0, padx=5)

        tk.Label(
            panel,
            text=":",
            font=("Consolas", 23, "bold"),
            fg=self.white,
            bg=self.panel
        ).grid(row=1, column=1)

        self.minute_entry = tk.Entry(
            panel,
            textvariable=self.minute_var,
            font=("Consolas", 23),
            width=4,
            justify="center"
        )
        self.minute_entry.grid(row=1, column=2, padx=5)

        tk.Label(
            panel,
            text="24-hour format (HH:MM)",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.panel
        ).grid(row=2, column=0, columnspan=3, pady=(8, 0))

        # Buttons
        buttons = tk.Frame(root, bg=self.bg)
        buttons.pack(pady=20)

        self.set_button = tk.Button(
            buttons,
            text="Set Alarm",
            command=self.set_alarm,
            font=("Segoe UI", 11, "bold"),
            bg=self.green,
            fg="#101820",
            width=12,
            relief="flat",
            cursor="hand2"
        )
        self.set_button.grid(row=0, column=0, padx=5, pady=5)

        self.cancel_button = tk.Button(
            buttons,
            text="Cancel Alarm",
            command=self.cancel_alarm,
            font=("Segoe UI", 11, "bold"),
            bg=self.red,
            fg=self.white,
            width=12,
            relief="flat",
            cursor="hand2"
        )
        self.cancel_button.grid(row=0, column=1, padx=5, pady=5)

        self.snooze_button = tk.Button(
            buttons,
            text="Snooze 5 Min",
            command=self.snooze_alarm,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent,
            fg="#101820",
            width=12,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.snooze_button.grid(row=1, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(
            buttons,
            text="Stop Sound",
            command=self.stop_alarm,
            font=("Segoe UI", 11, "bold"),
            bg="#536477",
            fg=self.white,
            width=12,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.grid(row=1, column=1, padx=5, pady=5)

        # Status
        self.status_label = tk.Label(
            root,
            text="No alarm set",
            font=("Segoe UI", 11),
            fg=self.muted,
            bg=self.bg
        )
        self.status_label.pack(pady=5)

        self.update_clock()

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())

            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Time",
                "Enter a valid time.\nHour: 00-23, Minute: 00-59"
            )
            return

        self.alarm_time = f"{hour:02d}:{minute:02d}"
        self.alarm_enabled = True
        self.snooze_until = None
        self.last_triggered = None

        self.status_label.config(
            text=f"Alarm set for {self.alarm_time}",
            fg=self.green
        )

    def cancel_alarm(self):
        self.alarm_enabled = False
        self.alarm_time = None
        self.snooze_until = None

        if self.ringing:
            self.stop_alarm()

        self.status_label.config(
            text="Alarm cancelled",
            fg=self.muted
        )

    def trigger_alarm(self):
        if self.ringing:
            return

        self.ringing = True
        self.status_label.config(
            text="ALARM RINGING! Wake up!",
            fg=self.red
        )

        self.stop_button.config(state="normal")
        self.snooze_button.config(state="normal")

        self.ring_sound()

    def ring_sound(self):
        if not self.ringing:
            return

        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except RuntimeError:
            self.root.bell()

        self.root.after(1200, self.ring_sound)

    def stop_alarm(self):
        self.ringing = False
        self.stop_button.config(state="disabled")
        self.snooze_button.config(state="disabled")

        if self.alarm_enabled:
            self.status_label.config(
                text=f"Alarm stopped. Next alarm: {self.alarm_time}",
                fg=self.green
            )
        else:
            self.status_label.config(
                text="Alarm stopped",
                fg=self.muted
            )

    def snooze_alarm(self):
        if not self.ringing:
            return

        self.stop_alarm()
        self.snooze_until = datetime.now() + timedelta(minutes=5)

        self.status_label.config(
            text="Snoozed for 5 minutes",
            fg=self.accent
        )

    def update_clock(self):
        now = datetime.now()

        self.time_label.config(
            text=now.strftime("%H:%M:%S")
        )
        self.date_label.config(
            text=now.strftime("%A, %d %B %Y")
        )

        # Check snooze first
        if (
            self.snooze_until is not None
            and now >= self.snooze_until
        ):
            self.snooze_until = None
            self.trigger_alarm()

        # Check the regular alarm
        elif (
            self.alarm_enabled
            and not self.ringing
            and self.snooze_until is None
            and now.strftime("%H:%M") == self.alarm_time
        ):
            trigger_key = now.strftime("%Y-%m-%d %H:%M")

            if self.last_triggered != trigger_key:
                self.last_triggered = trigger_key
                self.trigger_alarm()

        self.root.after(250, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalAlarmClock(root)
    root.mainloop()
