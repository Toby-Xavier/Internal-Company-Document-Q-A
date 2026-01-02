# Internal Company Knowledge Base/Q&A Bot

This project is an AI-powered internal knowledge base assistant designed for company staff. It allows employees to ask questions and receive accurate, detailed answers strictly based on the company's internal documents, including PDFs and text files. The bot uses Azure OpenAI for embeddings and chat completions, enabling Retrieval-Augmented Generation (RAG) to ensure responses are grounded in actual company content.

Features:
- Supports TXT and PDF documents, including encrypted PDFs.
- Document chunking for large files to improve retrieval accuracy.
- Uses Azure OpenAI embeddings to convert document chunks into vector representations.
- Retrieves the top-k most relevant chunks for each question.
- Uses Azure OpenAI Chat Completions to generate professional, full-paragraph answers.
- Implements token-safe embedding generation to prevent request errors.
- CLI interface for easy interaction.
- Includes automatic follow-up prompts after every answer to improve staff engagement.
- Fully configurable via .env file, including embedding and chat model deployment names.

Setup Instructions:
1. Clone the repository:
   git clone <your-repo-url>
   cd document-qa-bot
2. Install dependencies:
   pip install -r requirements.txt
   pip install pycryptodome  # required for AES-encrypted PDFs
3. Create and configure .env file with your Azure OpenAI details:
   AZURE_OPENAI_KEY=<your-azure-openai-key>
   AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT=<your-chat-deployment-name>
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your-embedding-deployment-name>
4. Add your company documents to the documents/ folder (TXT or PDF).
5. Run the bot:
   python app.py
   Type questions at the prompt. Type 'exit' to quit.

How It Works:
1. Load and Chunk Document: All TXT and PDF documents in the documents/folder are loaded and split into smaller chunks to improve retrieval accuracy.
2. Generate Embedding: Each chunk is converted into a vector using Azure OpenAI embeddings.
3. Process Questions: User questions are converted into embeddings and compared with document chunks using cosine similarity.
4. Retreieve Context: The top-k most relevant chunks are selected and sent to the Azure OpenAI chat model.
5. Generate Answers: The chat model generates a professional, document-grounded response and includes a polite follow-up prompt.

Technologies Used:
- Python 3.13+
- PyPDF2
- NumPy
- python-dotenv
- Azure OpenAI API
- PyCryptodome (for encrypted PDFs)
