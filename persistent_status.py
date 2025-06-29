# persistent_status.py

import json, datetime, pathlib, os, itertools

BASE_DIR      = pathlib.Path(__file__).resolve().parent
LAST_FILE     = BASE_DIR / "last_status.json"
HISTORY_FILE  = BASE_DIR / "status-log.jsonl"
MAX_LINES     = 100_000

_line_counter = itertools.count(
    start=sum(1 for _ in HISTORY_FILE.open()) if HISTORY_FILE.exists() else 0
)

def _now() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

def _rotate_if_needed():
    if next(_line_counter) >= MAX_LINES:
        ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        HISTORY_FILE.rename(HISTORY_FILE.with_suffix(f".{ts}.bak"))
        # reset counter
        _line_counter.__init__()

def log_event(event: str, *, unit: str, ok: bool, error: str | None = None):
    rec = {
        "ts": _now(),
        "unit": unit,
        "event": event,
        "ok": ok,
        "error": error,
    }

    _rotate_if_needed()

    # --- append + flush + fsync so it's on-disk immediately ---
    with HISTORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
        fh.flush()
        os.fsync(fh.fileno())          # ← gjør linjen synlig med én gang

    LAST_FILE.write_text(json.dumps(rec, indent=2), encoding="utf-8")
