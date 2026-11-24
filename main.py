"""Entry for make.fun "Funniest Autocorrect Fail".

Writes one line -- a text message where autocorrect turned "meeting"
into "mating" -- to /output/entry.txt (the path the gate reads), or to
entry.txt next to this file when /output does not exist (local runs).

The line: "Sorry I'm late, I had a mating with my boss"
The slip: meeting -> mating. A mundane late-for-work apology becomes a
mortifying confession to the boss. The intended word is instantly clear
from context, the wrong word is specific and surprising, and the whole
thing reads as a real autocorrect slip, not a written joke.
"""

import hashlib
import os

ENTRY = "Sorry I'm late, I had a mating with my boss"

# The gate: /output/entry.txt must be UTF-8 text of 1 to 199 characters,
# not only white space.
MAX_CHARS = 199


def validate(text):
    """Check the entry line against the gate rules. Raises ValueError."""
    if not isinstance(text, str):
        raise ValueError("entry is not a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry is %d characters, gate needs 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry has leading or trailing white space")
    text.encode("utf-8")  # raises UnicodeEncodeError if not UTF-8
    if "mating" not in text:
        raise ValueError("the wrong word 'mating' is missing")
    if "meeting" in text:
        raise ValueError("the intended word 'meeting' leaked into the text")
    return True


def main():
    validate(ENTRY)
    if os.path.isdir("/output"):
        out = "/output/entry.txt"
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "entry.txt")
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Round-trip check: what landed on disk must be exactly the entry,
    # byte for byte, so a partial write or a wrong path can never pass.
    with open(out, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError("round-trip mismatch: disk holds %r" % written)
    print("wrote %s (%d chars, sha256 %s)"
          % (out, len(ENTRY), hashlib.sha256(written).hexdigest()))
    print(ENTRY)


if __name__ == "__main__":
    main()
