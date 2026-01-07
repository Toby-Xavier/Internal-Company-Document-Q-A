# Internal Company Knowledge Base/Q&A Bot

An AI-powered internal knowledge base assistant designed for company staff. It allows employees to ask questions and receive accurate, detailed answers strictly based on the company's internal documents, including PDFs and text files. The bot uses Azure OpenAI for embeddings and chat completions, enabling Retrieval-Augmented Generation (RAG) to ensure responses are grounded in actual company content.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4.svg)
![RAG](https://img.shields.io/badge/RAG-Enabled-green.svg)

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Example Questions](#example-questions)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

## Features

- **Multi-format Support**: Works with TXT and PDF documents, including encrypted PDFs
- **Smart Document Chunking**: Splits large files into manageable chunks for improved retrieval accuracy
- **Vector Embeddings**: Uses Azure OpenAI embeddings to convert document chunks into vector representations
- **Intelligent Retrieval**: Retrieves top-k most relevant chunks for each question using cosine similarity
- **Professional Responses**: Generates full-paragraph answers using Azure OpenAI Chat Completions
- **Token-safe Processing**: Implements token-safe embedding generation to prevent request errors
- **Interactive CLI**: User-friendly command-line interface for easy interaction
- **Engagement Features**: Automatic follow-up prompts after every answer to improve staff engagement
- **Fully Configurable**: All settings managed via `.env` file, including model deployment names

## Tech Stack

### Core Technologies
- **Python 3.13+**: Core programming language
- **Azure OpenAI**: Enterprise AI platform for embeddings and chat
- **RAG (Retrieval-Augmented Generation)**: Document-grounded response generation

### Libraries & Tools
- **PyPDF2**: PDF document parsing and extraction
- **NumPy**: Vector operations and cosine similarity calculations
- **python-dotenv**: Environment variable management
- **Azure OpenAI API**: Embedding and chat completion endpoints
- **PyCryptodome**: AES-encrypted PDF decryption support

## How It Works

```
Documents → Chunking → Embeddings → Vector DB → Query → Similarity Search → Context → LLM → Answer
```

### Process Flow:

1. **Load and Chunk Documents**
   - All TXT and PDF documents in the `documents/` folder are loaded
   - Documents are split into smaller chunks to improve retrieval accuracy
   - Handles encrypted PDFs automatically

2. **Generate Embeddings**
   - Each chunk is converted into a vector using Azure OpenAI embeddings
   - Embeddings are stored in memory for fast retrieval

3. **Process Questions**
   - User questions are converted into embeddings
   - Compared with document chunks using cosine similarity

4. **Retrieve Context**
   - Top-k most relevant chunks are selected
   - Context is sent to the Azure OpenAI chat model

5. **Generate Answers**
   - Chat model generates a professional, document-grounded response
   - Includes a polite follow-up prompt for continued engagement

## Setup Instructions

### Prerequisites
- Python 3.13 or higher
- Azure OpenAI account with deployments for:
  - Chat completion (GPT-4o, GPT-4o-mini, etc.)
  - Text embeddings (text-embedding-ada-002, text-embedding-3-small, etc.)
- API key and endpoint

### Step 1: Clone the Repository
```bash
git clone <https://github.com/Toby-Xavier/Internal-Company-Document-Q-A>
cd document-qa-bot
```

### Step 2: Install Dependencies
```bash
pip3 install -r requirements.txt
pip3 install pycryptodome  # Required for AES-encrypted PDFs
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_KEY=<your-azure-openai-key>
AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=<your-chat-deployment-name>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your-embedding-deployment-name>
```

### Step 4: Add Company Documents

Add your internal documents to the `documents/` folder:
```
documents/
├── employee_handbook.pdf
├── company_policies.txt
├── hr_guidelines.pdf
└── technical_documentation.pdf
```

**Supported Formats:**
- `.txt` - Plain text files
- `.pdf` - PDF documents (including encrypted PDFs)

### Step 5: Run the Bot
```bash
python3 app.py
```

Type your questions at the prompt. Type `exit` to quit.

## Usage

### Starting the Bot
```bash
python3 app.py
```

### Example Interaction
```
🤖 Internal Knowledge Base Assistant
📚 Loaded 4 documents with 156 chunks
💬 Ask me anything about company documents (type 'exit' to quit)

You: What is the company's remote work policy?

Bot: According to our company policy documents, employees are allowed to work 
remotely up to 3 days per week after completing their probation period. Remote 
work requests must be approved by direct managers and require a stable internet 
connection and dedicated workspace. All remote workers must be available during 
core business hours (10 AM - 3 PM) and attend mandatory in-person meetings.

Would you like to know more about this topic or ask another question?

You: What are the core business hours?
...
```

### Commands
- **Ask any question**: Type your question and press Enter
- **Exit**: Type `exit` or `quit` to close the application
- **Follow-up**: Continue asking related questions for deeper insights

## Project Structure

```
document-qa-bot/
├── app.py                   # Main application file
├── documents/               # Folder for company documents (TXT, PDF)
│   ├── policy.pdf
│   └── handbook.txt
├── .env                     # Environment variables (not in repo)
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_ENDPOINT` | Your Azure resource endpoint | `https://myresource.openai.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT` | Chat model deployment name | `gpt-4o` |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model deployment name | `text-embedding-ada-002` |

### Recommended Models

**For Chat Completion:**
- `gpt-4o` - Most capable, best for complex queries
- `gpt-4o-mini` - Faster, cost-effective
- `gpt-4-turbo` - Balanced performance

**For Embeddings:**
- `text-embedding-3-small` - Latest, most efficient
- `text-embedding-3-large` - Higher accuracy
- `text-embedding-ada-002` - Reliable, widely used

### Tuning Parameters

You can adjust these in `app.py`:

```python
# Chunk size for document splitting
CHUNK_SIZE = 1000  # Characters per chunk

# Number of relevant chunks to retrieve
TOP_K = 3  # Increase for more context

# Temperature for response generation
TEMPERATURE = 0.3  # Lower = more focused, Higher = more creative
```

## Example Questions

### HR & Policies
```
- What is the company's leave policy?
- How do I request time off?
- What are the working hours?
- What is the dress code policy?
```

### IT & Technical
```
- How do I reset my password?
- What software tools does the company provide?
- How do I access the VPN?
- What are the data security guidelines?
```

### Benefits & Compensation
```
- What health insurance plans are available?
- How does the bonus structure work?
- What are the retirement benefits?
- When do performance reviews happen?
```

## Technical Details

### RAG Implementation

The bot uses a **Retrieval-Augmented Generation (RAG)** architecture:

1. **Document Processing**: Documents are split into chunks and converted to embeddings
2. **Semantic Search**: User queries are embedded and compared using cosine similarity
3. **Context Injection**: Top-k relevant chunks are injected into the LLM prompt
4. **Grounded Generation**: LLM generates answers based strictly on provided context

### Cosine Similarity Formula

```python
similarity = np.dot(query_embedding, chunk_embedding) / (
    np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
)
```

### Token Management

The bot implements token-safe embedding generation:
- Automatically truncates long chunks to fit model limits
- Handles batch processing efficiently
- Prevents API request failures due to token overflow

### Encryption Support

Supports password-protected PDFs using PyCryptodome:
- AES encryption/decryption
- Automatic password handling (configurable)
- Fallback to unencrypted processing

## Troubleshooting

### Common Issues

**Issue: "No documents found in documents/ folder"**
- **Solution**: Add `.txt` or `.pdf` files to the `documents/` folder

**Issue: "Authentication failed"**
- **Solution**: Check your `AZURE_OPENAI_KEY` in `.env` file
- Ensure your Azure subscription is active

**Issue: "Deployment not found"**
- **Solution**: Verify deployment names in Azure OpenAI Studio
- Ensure both chat and embedding deployments exist

**Issue: "Token limit exceeded"**
- **Solution**: Reduce `CHUNK_SIZE` or `TOP_K` in configuration
- Use a model with larger context window

**Issue: "PDF decryption failed"**
- **Solution**: Ensure `pycryptodome` is installed
- Check PDF encryption password if applicable

### Debug Mode

Enable verbose logging by adding to your `.env`:
```env
DEBUG=True
```

## Security Note

**Important**: This bot is designed for internal company use only. Ensure:
- Documents contain only internal, non-sensitive information
- API keys are kept secure and never committed to version control
- Access is restricted to authorized employees only
- Compliance with your company's data security policies

---
