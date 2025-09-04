"""Tkinter GUI for the Chive TV idea generator.

Provides a manual "Run Now" button and starts a background thread that
executes the generator every Monday at 07:00 Eastern Time.
"""
import threading
import time
from datetime import datetime, timedelta, timezone
import tkinter as tk
from tkinter import messagebox

import idea_generator


def run_and_notify() -> None:
    """Run the generator and show a message box with the result."""
    try:
        ideas = idea_generator.main()
        messagebox.showinfo("Idea Generator", f"Generated {len(ideas)} ideas")
    except Exception as exc:
        messagebox.showerror("Idea Generator", str(exc))


def _seconds_until_next_monday_7am_et(now: datetime) -> float:
    """Return seconds until next Monday 07:00 US/Eastern."""
    # Compute next Monday in US/Eastern. EST is UTC-5, EDT is UTC-4; we assume -5.
    et_offset = -5
    next_monday = (now + timedelta(days=(7 - now.weekday()))).replace(
        hour=7 - et_offset, minute=0, second=0, microsecond=0
    )
    return (next_monday - now).total_seconds()


def schedule_weekly_run() -> None:
    """Schedule the generator to run weekly before Monday 7AM ET."""
    def worker() -> None:
        while True:
            now = datetime.now(timezone.utc)
            time.sleep(max(0, _seconds_until_next_monday_7am_et(now)))
            try:
                idea_generator.main()
            except Exception:
                pass
            time.sleep(1)

    threading.Thread(target=worker, daemon=True).start()


def create_gui() -> None:
    root = tk.Tk()
    root.title("Chive TV Idea Generator")
    tk.Button(root, text="Run Now", command=run_and_notify, width=25, height=2).pack(
        padx=20, pady=20
    )
    root.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual execution
    schedule_weekly_run()
    create_gui()
