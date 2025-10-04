# Init Chroma
INDEX_DIR = Path("index")
INDEX_DIR.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(INDEX_DIR))

# Drop existing collection if it exists
try:
    client.delete_collection("uniswap_gov")
except Exception:
    pass

collection = client.create_collection(
    "uniswap_gov",
    embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_KEY, model_name="text-embedding-3-small"
    )
)

# Add docs
for t in topics:
    text = f"{t['title']} ({t['created_at']})"
    collection.add(
        ids=[str(t["id"])],
        documents=[text],
        metadatas=[{"title": t["title"], "created_at": t["created_at"]}],
    )

print(f"✅ Indexed {len(topics)} topics into ChromaDB at {INDEX_DIR}")
