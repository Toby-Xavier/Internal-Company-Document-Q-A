import os
import numpy as np
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import AzureOpenAI
from prompts import SYSTEM_PROMPT, build_user_prompt


# Environment setup

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")


# Chunking utility

def chunk_text(text, chunk_size=600, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# Load & chunk documents

def load_documents(folder="documents"):
    all_chunks = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        # TXT files
        if filename.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                all_chunks.extend(chunk_text(text))

        # PDF files
        elif filename.lower().endswith(".pdf"):
            try:
                reader = PdfReader(path)

                if reader.is_encrypted:
                    reader.decrypt("")

                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                all_chunks.extend(chunk_text(text))

            except Exception as e:
                print(f"Skipping {filename}: {e}")

    return all_chunks


# Embeddings

def get_embeddings(texts, max_chars=2000):
    valid_texts = []
    embeddings = []

    for text in texts:
        if len(text) > max_chars:
            continue

        response = client.embeddings.create(
            model=EMBEDDING_DEPLOYMENT,
            input=text
        )

        valid_texts.append(text)
        embeddings.append(response.data[0].embedding)

    return valid_texts, embeddings


# Similarity search

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_context(question_embedding, doc_embeddings, docs, top_k=3):
    scores = [cosine_similarity(question_embedding, emb) for emb in doc_embeddings]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return "\n\n".join(docs[i] for i in top_indices)


# Ask the knowledge bot

def ask_bot(question, docs, embeddings):
    question_embedding = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=question
    ).data[0].embedding

    context = retrieve_context(question_embedding, embeddings, docs)
    user_prompt = build_user_prompt(question, context)

    response = client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# CLI Application

if __name__ == "__main__":
    print("Internal Company Knowledge Base Bot")
    print("Type 'exit' to quit\n")

    print("Loading documents and creating chunks...")
    documents = load_documents()
    print(f"Created {len(documents)} document chunks.")

    print("Generating embeddings...")
    documents, embeddings = get_embeddings(documents)
    print("Embeddings ready.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye! Let me know if you need anything else.")
            break

        answer = ask_bot(user_input, documents, embeddings)
        print(f"\nBot: {answer}\n")
