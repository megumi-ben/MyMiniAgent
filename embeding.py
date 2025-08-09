import chunking
import chromadb
from google import genai

google_client = genai.Client(api_key="AIzaSyD18gzrSU2lDXblcOF1d-Tn7eWtI_FRuWQ")

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection("nameoftable")

def get_embedding(text: str, store: bool) -> list[float]:
    response = google_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": "RETRIEVAL_DOCUMENT" if store else "RETRIEVAL_QUERY"
        }
    )
    return response.embeddings[0].values

def create_db():
    for i,c in enumerate(chunking.get_chunks()):
        print(f"Processing chunk {i + 1}...\n{c}")
        print("---"*10)
        embedding = get_embedding(c, True)
        chromadb_collection.upsert(
            ids=str(i),
            documents=c,
            embeddings=embedding,
        )
def query_db(query: str) -> list[dict]:
    query_embedding = get_embedding(query, False)
    results = chromadb_collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    return results["documents"][0]

if __name__ == "__main__":
    # print(get_embedding(chunking.get_chunks()[0], True))
    # create_db()
    # print("Database created successfully.")
    results = query_db("西交")
    for doc in results:
        print(f"{doc}")
        print("---" * 10)