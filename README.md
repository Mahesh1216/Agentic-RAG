# 🤖 Boss Wallah Chatbot

An intelligent chatbot built with FastAPI and Streamlit that provides information about Boss Wallah courses using Agentic AI capabilities.

## ✨ Features

* **Agentic AI Integration**: Combines RAG (Retrieval Augmented Generation) with Gemini LLM for intelligent responses
* **Web Search Fallback**: Automatically searches the web for queries outside the training data
* **Multi-language Support**: Built-in language detection and translation capabilities
* **Modern Web Interface**: Clean, responsive UI built with Streamlit

## 🧠 Approach

### System Architecture

The chatbot follows a modular architecture with these key components:

1. **Frontend Layer**
   - Built with Streamlit for a clean, responsive interface
   - Handles user input and displays responses
   - Communicates with the backend via REST API

2. **Backend Layer**
   - FastAPI server handling HTTP requests
   - Implements RESTful endpoints for chat functionality
   - Manages session state and request routing

3. **Agentic AI Engine**
   - **RAG Pipeline**:
     - Uses FAISS for efficient similarity search
     - Embeds queries and documents using sentence-transformers
     - Retrieves most relevant context from the knowledge base
   
   - **LLM Integration**:
     - Google's Gemini model for natural language understanding
     - Processes retrieved context to generate human-like responses
     - Maintains conversation context when needed
   
   - **Agentic Capabilities**:
     - Decides when to use RAG vs. direct LLM responses
     - Can perform web searches for queries outside the knowledge base
     - Implements language detection and translation

### Data Flow

1. User submits a query through the Streamlit interface
2. Backend receives the query and processes it through the Agentic pipeline
3. The system determines the best approach (RAG, direct LLM, or web search)
4. For RAG:
   - Query is embedded and matched against the vector store
   - Most relevant documents are retrieved
   - Context is passed to the LLM for response generation
5. The response is formatted and returned to the user

### Key Technologies

- **Vector Database**: FAISS for efficient similarity search
- **Embeddings**: sentence-transformers for text embeddings
- **LLM**: Google's Gemini for natural language understanding
- **Web Framework**: FastAPI for backend, Streamlit for frontend
- **Language Processing**: Deep-translator for multi-language support

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- API Keys for Gemini and SerpAPI

### 1. Clone the Repository

```bash
git clone https://github.com/Mahesh1216/Agentic-RAG.git
cd Agentic-RAG
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root with your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

### 5. Run the Application

#### Start the Backend Server

```bash
python -m uvicorn src.main:app --reload
```

#### Start the Web Interface

In a new terminal:

```bash
streamlit run app.py
```

Access the application at: http://localhost:8501

## 🛠️ Project Structure

```
.
├── data/                   # Data files
│   ├── courses.csv         # Course information
│   └── lang_map.csv        # Language code mappings
├── src/
│   ├── main.py            # FastAPI application
│   └── rag_pipeline.py    # RAG and LLM logic
├── app.py                # Streamlit frontend
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🌐 API Documentation

Once the server is running, access the interactive API documentation at:

```
http://127.0.0.1:8000/docs
```

### Available Endpoints

#### POST /chat

Process user queries using Agentic AI.

**Request:**
```json
{
  "query": "Your question here",
  "type": "agent"
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Python courses"}'
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
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