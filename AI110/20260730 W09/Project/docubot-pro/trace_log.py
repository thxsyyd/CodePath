"""
Trace logging for DocuBot Pro.

Every confidence-gated query produces a step-by-step trace of what the system
decided and why (RETRIEVE -> ASSESS -> DECIDE -> RESPOND). This makes the
agent's behavior auditable after the fact instead of a black box, and mirrors
the "read your traces" principle: trust the log, not the vibe.

Traces can be printed to the console and appended to a log file so a reviewer
can inspect decisions without re-running the system.
"""

import os
from datetime import datetime
from typing import List, Tuple


class TraceLogger:
    """Collects timestamped decision steps for a single query."""

    def __init__(self, query: str):
        self.query = query
        self.started_at = datetime.now()
        self.steps: List[Tuple[str, str]] = []

    def step(self, stage: str, detail: str) -> None:
        """Record one decision step, e.g. step('ASSESS', 'confidence=HIGH ...')."""
        self.steps.append((stage, detail))

    def render(self) -> str:
        """Return the trace as a readable multi-line string."""
        lines = [
            f"=== Trace for query: {self.query!r} ===",
            f"time: {self.started_at.isoformat(timespec='seconds')}",
        ]
        for stage, detail in self.steps:
            lines.append(f"  {stage:9s} | {detail}")
        return "\n".join(lines)

    def print_trace(self) -> None:
        """Print the trace to the console."""
        print(self.render())

    def append_to_file(self, path: str = "logs/trace.log") -> None:
        """
        Append this trace to a log file so decisions can be reviewed later.
        Creates the parent directory if needed.
        """
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(self.render())
            f.write("\n\n")
