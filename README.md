# Boss Wallah Chatbot API

This is a FastAPI-based chatbot API for Boss Wallah courses. It supports:

* **RAG (Retriever + Gemini LLM)**: Uses course data to provide answers.
* **LLM-only mode**: Directly queries Gemini LLM without using retriever.
* **Agentic Search**: For queries outside the dataset, it can search the web.

---

## 🛠 Setup

### 1. Clone the repository

```bash
git clone https://github.com/SachinYadav666/Boss-Wallah-Chatbot.git
cd boss-wallah-chatbot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory with your Gemini and SerpAPI keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

### 5. Prepare the data

Ensure the following CSV files exist in the `data/` folder:

* `courses.csv` – course details
* `lang_map.csv` – language code mapping

---

## 🚀 Running the API

Start the FastAPI server:

```bash
python -m src.main
```

Default URL:

```
http://127.0.0.1:8000
```

Interactive Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 📦 API Endpoints

### **POST /chat**

Single endpoint to handle both RAG and LLM queries.

**Request Body (JSON):**

```json
{
  "query": "Your question here",
  "type": "rag"  // optional, default is "rag"; use "llm" for LLM-only
}
```

**Example 1: RAG query (default)**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "Tell me about Python courses"}'
```

**Example 2: LLM-only query**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "Tell me about Python courses", "type": "llm"}'
```

### **POST /agent-chat**

This endpoint uses an agentic approach. It first tries to answer from the dataset, and if it can't, it searches the web.

**Request Body (JSON):**

```json
{
  "query": "Your question here"
}
```

**Example:**

```bash
curl -X POST "http://127.0.0.1:8000/agent-chat" \
-H "Content-Type: application/json" \
-d '{"query": "Are there any stores near Whitefield, Bangalore where I can buy seeds for papaya farming?"}'
```


---

## ⚡ Notes

* The RAG pipeline is **initialized once** at startup for faster responses.
* Ensure your `GEMINI_API_KEY` and `SERPAPI_API_KEY` are valid to avoid API errors.
* Use the `type` field in the `/chat` endpoint to switch between **RAG** and **LLM-only** modes.