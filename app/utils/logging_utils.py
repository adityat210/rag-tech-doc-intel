import json
from datetime import datetime
from pathlib import Path
#should try to create structured local logs
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "query_logs.jsonl"

def log_query_event(event: dict):
    #adding query event as JSON line to log files
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event_with_timestamp = {
        "timestamp": datetime.utcnow().isoformat(), 
        **event
    }

    with LOG_FILE.open("a", encoding="utf-8") as f:
        #each requuest becomes JSON object one per line
        f.write(json.dumps(event_with_timestamp))
        print()