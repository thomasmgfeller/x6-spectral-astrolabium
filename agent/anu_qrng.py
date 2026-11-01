"""Acquire one AQN trial block per UTC week and publish it to the data-only branch."""
import hashlib
import http.client
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HOST = "api.quantumnumbers.anu.edu.au"
QUERY = "/?length=1024&type=uint8"
SOURCE = "https://" + HOST + QUERY
FAQ = "https://quantumnumbers.anu.edu.au/faq"
DATA_REF = "HEAD:refs/heads/anu-qrng-data"
SIZE = 1024


def parse_block(payload):
    if not isinstance(payload, dict):
        raise ValueError("Unexpected AQN envelope")
    values = payload.get("data")
    length = payload.get("length", SIZE)
    if (payload.get("success", True) is not True or payload.get("type", "uint8") != "uint8"
            or type(length) is not int or length != SIZE or not isinstance(values, list)
            or len(values) != SIZE or any(type(v) is not int or not 0 <= v <= 255 for v in values)):
        raise ValueError("Invalid AQN uint8 block")
    return bytes(values)


def download(key):
    # HTTPSConnection sends one GET. It neither follows redirects nor retries.
    conn = http.client.HTTPSConnection(HOST, timeout=20)
    try:
        conn.request("GET", QUERY, headers={"x-api-key": key, "Accept": "application/json"})
        reply = conn.getresponse()
        if reply.status != 200:
            raise ValueError(f"AQN HTTP {reply.status}; slot consumed")
        body = reply.read(16385)
        if len(body) > 16384:
            raise ValueError("AQN response exceeds limit")
        return parse_block(json.loads(body))
    finally:
        conn.close()


def publish(directory, names, message):
    for args in (["add", "--", *names], ["commit", "-m", message], ["push", "origin", DATA_REF]):
        subprocess.run(["git", "-C", directory, *args], check=True)


def collect(directory, key, reviewed, *, clock=lambda: datetime.now(timezone.utc), fetch=download):
    now = clock()
    if not key or not reviewed:
        raise ValueError("Set a dedicated free Trial key and its terms review date")
    age = (now.date() - date.fromisoformat(reviewed)).days
    if not 0 <= age < 90:
        raise ValueError("Review current trial pricing and terms before further requests")
    last = directory / "last-attempt.json"
    if last.exists():
        previous = datetime.fromisoformat(json.loads(last.read_text())["reserved_at"])
        if previous > now:
            raise ValueError("Archive reservation is in the future")
        if previous.isocalendar()[:2] == now.isocalendar()[:2] or now - previous < timedelta(minutes=1):
            return False
    # Push first. A non-fast-forward, a timeout or a failed request never buys a retry.
    last.write_text(json.dumps({"reserved_at": now.isoformat()}) + "\n")
    publish(directory, [last.name], "Reserve AQN trial request " + now.date().isoformat())
    values = fetch(key)
    received = clock().isoformat()
    record = {
        "schema": "x6.anu-qrng/1", "source": SOURCE, "provider": "Australian National University",
        "usage_terms": FAQ, "trial_terms_reviewed_on": reviewed, "retrieved_at": received,
        "type": "uint8", "length": SIZE, "data_hex": values.hex(),
        "sha256": hashlib.sha256(values).hexdigest(),
    }
    encoded = json.dumps(record, indent=2) + "\n"
    name = now.date().isoformat() + ".json"
    with (directory / name).open("x") as f:
        f.write(encoded)
    (directory / "latest.json").write_text(encoded)
    publish(directory, [name, "latest.json"], "Archive AQN trial block " + now.date().isoformat())
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m agent.anu_qrng <archive-git-worktree>")
    try:
        acquired = collect(Path(sys.argv[1]), os.environ.get("ANU_TRIAL_API_KEY"),
                           os.environ.get("ANU_TRIAL_REVIEWED_ON"))
        print("Archived one AQN block." if acquired else "Slot already reserved. No request.")
    except (ValueError, OSError, http.client.HTTPException, subprocess.CalledProcessError) as exc:
        # Responses and credentials must never enter CI logs.
        if isinstance(exc, ValueError) and str(exc).startswith("AQN HTTP "):
            print(str(exc), file=sys.stderr)
        sys.exit("AQN acquisition stopped (" + type(exc).__name__ + "). Check settings and archive.")
