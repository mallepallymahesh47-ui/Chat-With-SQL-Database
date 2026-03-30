# Chat with SQL Databases 🐬

> Ask questions about your database in plain English — powered by Groq · LangChain · SQLite / MySQL

---

Querying a database traditionally requires knowledge of SQL — making data inaccessible to non-technical users. Even for developers, writing queries for quick lookups is tedious and slow.

A conversational AI interface that lets anyone ask natural language questions about their database and receive accurate, human-readable answers — no SQL knowledge required. Supports both SQLite file uploads and live MySQL connections.

---

## Features

- **Natural Language to SQL**: Automatically converts your question into a SQL query using Groq's Llama 3.1
- **SQLite Support**: Upload any `.db` file and start chatting instantly
- **MySQL Support**: Connect to a live MySQL database with credentials
- **Conversational Memory**: Maintains chat history for follow-up questions
- **Schema Viewer**: Inspect your database schema directly from the sidebar
- **LangSmith Tracing**: Built-in LangChain tracing for observability

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| LLM | Groq (Llama 3.1 8B Instant) |
| AI Framework | LangChain |
| Database (local) | SQLite |
| Database (remote) | MySQL |
| Observability | LangSmith |
| Package Manager | uv |

---

## Project Structure

```
chat-with-sql-database/
├── main.py           # Streamlit app — UI, chat logic, LLM chains
├── connections.py    # SQLite & MySQL connection helpers
├── sql.py            # Script to create and seed sample SQLite DB
├── mystudents.db     # Sample SQLite database (students data)
├── pyproject.toml    # Project dependencies
├── .env              # Environment variables (not committed)
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Groq API key
- LangChain API key (for tracing)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chat-with-sql-database
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # or
   pip install langchain langchain-community langchain-groq streamlit python-dotenv sqlalchemy mysql-connector-python
   ```

3. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGCHAIN_API_KEY=your_langchain_api_key_here
   LANGCHAIN_PROJECT=your_project_name
   ```

4. **(Optional) Generate sample database**
   ```bash
   python sql.py
   ```
   This creates `mystudents.db` with 7 student records for testing.

---

## Usage

### Start the App
```bash
streamlit run main.py
```
Navigate to `http://localhost:8501`

### Chat with SQLite
1. Select **"Chat with SQLite File"** from the sidebar
2. Upload your `.db` file
3. Start asking questions in the chat input

### Chat with MySQL
1. Select **"Chat with MySQL"** from the sidebar
2. Enter your credentials (host, port, username, password, database)
3. Click **Connect**, then start chatting

---

## How It Works

```
User Question
     │
     ▼
┌─────────────────────┐
│  SQL Chain (Groq)   │  ← Reads schema, writes SQL query
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Database Executor  │  ← Runs query on SQLite / MySQL
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Answer Chain (Groq)│  ← Converts SQL result to natural language
└─────────────────────┘
     │
     ▼
  AI Response
```

1. The LLM reads your database schema and generates a SQL query from your question
2. The query is executed against your actual database
3. The result is passed back to the LLM, which returns a clean, friendly answer

---

## API Keys

| Key | Where to get it |
|-----|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `LANGCHAIN_API_KEY` | [smith.langchain.com](https://smith.langchain.com) |
