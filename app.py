import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="Boss Wallah Chatbot", page_icon=":robot:")
st.title("🤖 Boss Wallah Chatbot")

# User input
query = st.text_input("Enter your query:", "Tell me about honey bee farming course")

# Request type selection
response_type = st.radio("Choose response type:", ("rag", "llm", "agent"))

if st.button("Get Response"):
    if query:
        try:
            if response_type == "agent":
                endpoint = f"{FASTAPI_URL}/agent-chat"
            else:
                endpoint = f"{FASTAPI_URL}/chat"

            payload = {"query": query, "type": response_type}
            
            with st.spinner("Getting response..."):
                response = requests.post(endpoint, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                result = response.json()
                st.subheader("Response:")
                st.write(result.get("response", "No response received."))
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend. Please ensure it is running at http://localhost:8000.")
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")

st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
}
</style>
""", unsafe_allow_html=True)
