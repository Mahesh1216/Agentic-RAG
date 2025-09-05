import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="Boss Wallah Chatbot", page_icon=":robot:")
st.title("🤖 Boss Wallah Chatbot")

# User input
query = st.text_area("Enter your query:", "Tell me about honey bee farming course", height=100)

# Request type selection with default to RAG
response_type = st.radio("Response type:", ["Agentic AI"], index=0)

# Map the selected response type to the backend type
type_mapping = {
    "Agentic AI": "agent",
}

if st.button("Get Response", type="primary"):
    if query:
        try:
            endpoint = f"{FASTAPI_URL}/chat"
            payload = {"query": query, "type": type_mapping[response_type]}
            
            with st.spinner("Getting response..."):
                response = requests.post(endpoint, json=payload)
                response.raise_for_status()
                
                result = response.json()
                st.subheader("Response:")
                st.markdown(f"{result.get('response', 'No response received.')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend. Please ensure it is running at http://localhost:8000.")
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")

# Add some custom styling
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea>div>div>textarea {
        min-height: 100px;
    }
</style>
""", unsafe_allow_html=True)
