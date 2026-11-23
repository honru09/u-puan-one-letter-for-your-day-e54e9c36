#!/usr/bin/env python3
"""One Letter for Your Day — writes exactly one letter to /output/entry.txt.

The letter is Q. It stands for "quota": today was a dawn radar shift spent
counting down a submission quota — five left for the day, forty hard — and
the whole day collapsed into that one ticking number.

Deterministic: the same single byte on every run.
"""

import os
import shutil


LETTER = "Q"
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def _clear_contents_only(directory: str) -> None:
    """Remove everything inside the directory, never the directory itself.

    The grader runs as an unprivileged user and cannot remove the
    root-owned mountpoint, so only the contents are cleared.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def main() -> None:
    # Guard: the entry must be exactly one A-Z letter, nothing else.
    if len(LETTER) != 1 or not ("A" <= LETTER <= "Z"):
        raise ValueError("LETTER must be exactly one A-Z character")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    _clear_contents_only(OUTPUT_DIR)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LETTER)
    os.chmod(OUTPUT_PATH, 0o644)
    # Verify what landed on disk is exactly the one letter.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LETTER:
        raise RuntimeError("output mismatch: expected %r, got %r" % (LETTER, written))


if __name__ == "__main__":
    main()
