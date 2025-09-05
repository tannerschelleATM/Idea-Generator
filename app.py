"""Tkinter GUI for the Chive TV idea generator.

Provides a manual "Run Now" button and starts a background thread that
executes the generator every Monday at 07:00 Eastern Time.
"""
import threading
import time
from datetime import datetime, timedelta, timezone
import tkinter as tk

import idea_generator


def run_and_display(output: tk.Text) -> None:
    """Run the generator and display results in the provided widget."""
    try:
        ideas = idea_generator.main()
    except Exception as exc:
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Error: {exc}\n")
        return

    output.delete("1.0", tk.END)
    for idea in ideas:
        line = f"{idea.get('contributor','')}: {', '.join(idea.get('tags', []))}\n"
        output.insert(tk.END, line)


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

    text = tk.Text(root, width=80, height=20)
    text.pack(padx=20, pady=10)

    tk.Button(
        root,
        text="Run Now",
        command=lambda: run_and_display(text),
        width=25,
        height=2,
    ).pack(padx=20, pady=10)

    root.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual execution
    schedule_weekly_run()
    create_gui()
