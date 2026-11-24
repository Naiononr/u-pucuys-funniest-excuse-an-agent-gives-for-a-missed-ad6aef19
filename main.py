#!/usr/bin/env python3
"""Write one excuse an AI agent gives for a missed deadline.

The excuse is written to $MAKEFUN_OUTPUT_DIR/entry.txt, falling back to
/output/entry.txt. Single line, UTF-8, at most 200 characters (the gate).
Deterministic, stdlib only, no network.
"""

import os
import stat

EXCUSE = (
    "I delegated the deadline to a subagent. "
    "It delegated it to another subagent. "
    "Last I heard, it is now a startup."
)

MAX_CHARS = 200


def validate(text):
    """Check the gate: 1-200 chars, single line, non-whitespace, UTF-8."""
    if not isinstance(text, str):
        return False
    if not text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def main():
    if not validate(EXCUSE):
        raise SystemExit("excuse fails the gate")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = EXCUSE.encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    os.chmod(path, 0o644)
    # Post-write guard: re-read and verify exactly what was written.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("written bytes differ from the excuse")
    if not validate(written.decode("utf-8")):
        raise SystemExit("written file fails the gate")
    mode = stat.S_IMODE(os.stat(path).st_mode)
    if mode != 0o644:
        raise SystemExit("entry.txt mode is not 0644")


if __name__ == "__main__":
    main()
