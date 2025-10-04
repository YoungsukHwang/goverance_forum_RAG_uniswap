import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY in .env")

# Load data
DATA_PATH = Path("data/topics.json")
with open(DATA_PATH, "r") as f:
    topics = json.load(f)

# Init Chroma
INDEX_DIR = Path("index")
INDEX_DIR.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(INDEX_DIR))
collection = client.get_or_create_collection(
    "uniswap_gov",
    embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_KEY, model_name="text-embedding-3-small"
    )
)

# Ingest
collection.delete(where={})  # clear old index
for t in topics:
    text = f"{t['title']} ({t['created_at']})"
    collection.add(
        ids=[str(t["id"])],
        documents=[text],
        metadatas=[{"title": t["title"], "created_at": t["created_at"]}],
    )

print(f"✅ Indexed {len(topics)} topics into ChromaDB at {INDEX_DIR}")
