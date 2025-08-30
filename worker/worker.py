import json
import time
import redis
from backend.utils.vectorstore import add_text
import os 
STREAM = "ingest"
GROUP = "workers"
CONSUMER = "worker_1"


REDIS_URL = os.getenv("REDIS_URL")
r = redis.from_url(REDIS_URL)

# Setup group
try:
    r.xgroup_create(STREAM, GROUP, id="$", mkstream=True)
except redis.ResponseError:
    pass

print("Worker started, waiting for messages...")

while True:
    msgs = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=5000)
    if not msgs:
        continue
    for stream, entries in msgs:
        for msg_id, payload in entries:
            try:
                body = {k.decode(): v.decode() for k, v in payload.items()}
                texts = json.loads(body.get("texts", "[]"))
                if texts:
                    add_text(texts)
                r.xack(STREAM, GROUP, msg_id)
            except Exception as e:
                print(f"Error processing message {msg_id}: {e}")
    time.sleep(0.2)
