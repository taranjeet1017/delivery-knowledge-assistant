import re

import json
from datetime import datetime

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")
client = OpenAI()

with open("index.json", "r", encoding="utf-8") as f:
    records = json.load(f)

with open("eval_cases.json", "r", encoding="utf-8") as f:
    eval_cases = json.load(f)


def similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def normalize(text):
    text = text.lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def retrieve(question, top_k=5):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = response.data[0].embedding

    all_dates = [
        datetime.fromisoformat(record["source_date"])
        for record in records
    ]

    oldest_date = min(all_dates)
    newest_date = max(all_dates)
    date_range = max((newest_date - oldest_date).days, 1)

    chronology_terms = [
        "latest", "current", "now", "changed", "change",
        "status", "still", "prevent", "blocking", "blocker"
    ]

    chronology_sensitive = any(
        term in question.lower()
        for term in chronology_terms
    )

    results = []

    for record in records:

        semantic_score = similarity(
            query_embedding,
            record["embedding"]
        )

        adjusted_score = semantic_score

        if chronology_sensitive:
            record_date = datetime.fromisoformat(
                record["source_date"]
            )

            freshness = (
                (record_date - oldest_date).days
                / date_range
            )

            adjusted_score += 0.02 * freshness

        results.append(
            (adjusted_score, record)
        )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = []
    source_counts = {}

    for score, record in results:

        source = record["source"]

        if source_counts.get(source, 0) < 2:
            selected.append((score, record))
            source_counts[source] = source_counts.get(source, 0) + 1

        if len(selected) == top_k:
            break

    return selected


passed = 0

for case in eval_cases:

    matches = retrieve(case["question"])

    context = "\n\n---\n\n".join(
        f"""
SOURCE: {record['source']}
SOURCE DATE: {record['source_date']}

{record['text']}
"""
        for score, record in matches
    )

    prompt = f"""
Answer using ONLY the project information below.

Do not invent information.
Prefer newer evidence when project information changes.
If the requested fact is unsupported, say that it cannot be determined.

PROJECT INFORMATION:

{context}

QUESTION:

{case['question']}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    answer = response.output_text

    expected = case.get("expected_facts", [])

    if case.get("must_refuse_if_unsupported"):
        success = (
            "cannot be determined" in answer.lower()
            or "not stated" in answer.lower()
            or "not available" in answer.lower()
    )
    else:
        normalized_answer = normalize(answer)

        success = all(
            normalize(fact) in normalized_answer
            for fact in expected
    )
                   

    print("=" * 80)
    print(case["id"], "-", "PASS" if success else "FAIL")
    print("Question:", case["question"])
    print("Answer:", answer)

    if success:
        passed += 1

print("=" * 80)
print(f"RESULT: {passed}/{len(eval_cases)} evaluation cases passed")
