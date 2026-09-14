import json
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")
client = OpenAI()

with open("index.json", "r", encoding="utf-8") as f:
    records = json.load(f)

question = "What is the latest working UAT start date and why did it change?"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

query_embedding = np.array(response.data[0].embedding)


def similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


results = []

for record in records:
    score = similarity(query_embedding, record["embedding"])
    results.append((score, record))

results.sort(key=lambda x: x[0], reverse=True)

print("\nQUESTION:")
print(question)

print("\nTOP MATCHES:\n")

for score, record in results[:5]:
    print(f"Source: {record['source']} | Chunk: {record['chunk']} | Score: {score:.3f}")
    print(record["text"][:700])
    print("\n" + "-" * 80 + "\n")
