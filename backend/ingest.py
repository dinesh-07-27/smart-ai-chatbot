import chromadb
from chromadb.utils import embedding_functions
import os

client = chromadb.PersistentClient(path="./chroma_db")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection("faq", embedding_function=embed_fn)

faq_path = "faq.txt"
if not os.path.exists(faq_path):
    print("Create faq.txt in backend/ with lines 'Question:Answer'")
    raise SystemExit(1)

docs, ids, metas = [], [], []
with open(faq_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line: continue
        if ":" in line:
            q, a = line.split(":", 1)
            docs.append(a.strip())
            ids.append(str(i))
            metas.append({"question": q.strip()})
        else:
            docs.append(line)
            ids.append(str(i))
            metas.append({"question": ""})

if docs:
    collection.add(documents=docs, ids=ids, metadatas=metas)
    print("✅ FAQ ingested into ChromaDB")
else:
    print("No entries found in faq.txt")
