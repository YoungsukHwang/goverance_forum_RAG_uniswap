import requests, json
from datetime import datetime, timedelta
from pathlib import Path

BASE_URL = "https://gov.uniswap.org/latest.json"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def fetch_recent_topics(months=6, limit=100):
    cutoff = datetime.utcnow() - timedelta(days=30*months)
    resp = requests.get(BASE_URL)
    data = resp.json()

    topics = []
    for t in data.get("topic_list", {}).get("topics", []):
        created = datetime.fromisoformat(t["created_at"].replace("Z",""))
        if created > cutoff:
            topics.append(t)
    return topics[:limit]

if __name__ == "__main__":
    topics = fetch_recent_topics(months=6)
    out = DATA_DIR / "topics.json"
    with open(out, "w") as f:
        json.dump(topics, f, indent=2)
    print(f"✅ Saved {len(topics)} topics to {out}")
