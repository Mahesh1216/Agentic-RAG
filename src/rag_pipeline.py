import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langdetect import detect
from deep_translator import GoogleTranslator
from serpapi import GoogleSearch

load_dotenv()

# Set up the Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=gemini_api_key)
client = genai.GenerativeModel('gemini-2.5-pro')

# Set up the SerpAPI client
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

def create_retriever():
    """
    Loads data, creates embeddings, and builds a FAISS vector store retriever.
    """
    # 1. Load data
    data_dir = r"C:\RAG Chatbot\data"
    courses_df = pd.read_csv(os.path.join(data_dir, "courses.csv"), encoding='utf-8-sig')
    lang_map_df = pd.read_csv(os.path.join(data_dir, "lang_map.csv"))
    
    # 2. Map language codes to names for better context
    lang_map_dict = dict(zip(lang_map_df['Code'], lang_map_df['Language']))
    courses_df['Released Languages'] = courses_df['Released Languages'].apply(
        lambda x: ', '.join([lang_map_dict.get(int(code.strip()), 'Unknown') for code in str(x).split(',')]) if pd.notna(x) else ''
    )
    
    # 3. Create a combined text field for comprehensive context
    courses_df['combined_text'] = courses_df.apply(lambda row: f"Course Title: {row['Course Title']}. About Course: {row['Course Description']}. Languages: {row['Released Languages']}. Audience: {row['Who This Course is For']}.", axis=1)
    
    # 4. Load data into LangChain documents
    loader = DataFrameLoader(courses_df, page_content_column='combined_text')
    documents = loader.load()

    # 5. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 6. Create embeddings
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # 7. Create FAISS vector store and retriever
    vectorstore = FAISS.from_documents(texts, embeddings)
    retriever = vectorstore.as_retriever()
    
    return retriever

def translate_text(text, dest_lang):
    return GoogleTranslator(source='auto', target=dest_lang).translate(text)

def get_rag_response(retriever, query: str) -> str:
    """
    Performs the full RAG process: retrieves context, then generates a Gemini response.
    """
    try:
        # 1. Retrieve relevant documents based on the user's query
        docs = retriever.get_relevant_documents(query)
        
        # 2. Combine the retrieved documents into a single context string
        context = " ".join([doc.page_content for doc in docs])
        
        # 3. Get the final answer from Gemini using the query and context
        prompt = f"You are a helpful assistant for Boss Wallah courses. Use the provided context to answer questions about courses. If the information isn\'t in the context, state that you can only answer based on the provided data.\n\nContext: {context}\n\nQuestion: {query}"
        completion = client.generate_content(prompt)
        return completion.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"
    
    
def get_llm_response(query):
    """
    Performs the full RAG process: retrieves context, then generates a Gemini response.
    """
    try:
        # Detect language of the query
        lang = detect(query)

        prompt = f"You are a helpful Ai assistant made by Boss Wallah .\n\nQuestion: {query}"
        completion = client.generate_content(prompt)
        
        # Translate the response back to the original language
        translated_response = translate_text(completion.text, lang)
        return translated_response
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"

def agentic_search(retriever, query: str) -> str:
    """
    First, tries to answer the query using the RAG pipeline.
    If the RAG response indicates that the information is not in the dataset,
    it performs a web search to find the answer.
    """
    rag_response = get_rag_response(retriever, query)

    if "I can only answer based on the provided data" in rag_response or "not in the context" in rag_response:
        if not serpapi_api_key:
            return "I can only answer based on the provided data. To search the web, please provide a SerpAPI key."
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi_api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "organic_results" in results and results["organic_results"]:
            return results["organic_results"][0]["snippet"]
        else:
            return "I could not find any information on the web for your query."
    else:
        return rag_response