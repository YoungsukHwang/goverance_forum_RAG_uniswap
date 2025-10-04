import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from .utils import get_secret

class GovernanceRAG:
    def __init__(self, st=None):
        api_key = get_secret("OPENAI_API_KEY", st=st)
        self.client = OpenAI(api_key=api_key)
        self.chroma = chromadb.PersistentClient(path="index")
        self.collection = self.chroma.get_collection(
            "uniswap_gov",
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key, model_name="text-embedding-3-small"
            ),
        )

    def query(self, question: str, k: int = 5) -> str:
        results = self.collection.query(query_texts=[question], n_results=k)
        docs = [m["title"] for m in results["metadatas"][0]]
        context = "\n".join(docs)

        prompt = f"""
You are an assistant summarizing Uniswap Governance Forum.
Question: {question}
Context:
{context}
Answer clearly in 3–5 bullet points.
"""
        resp = self.client.responses.create(model="gpt-4o-mini", input=prompt)
        return resp.output_text
