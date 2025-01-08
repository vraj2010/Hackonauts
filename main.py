import streamlit as st
import requests

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "badb4656-66c0-45f4-b943-79abcbb3ec30"
APPLICATION_TOKEN = "AstraCS:saguMlpoQItPIzsXrFGOocRZ:fa56792c4868e61e6aca0341cfe84d0b3879fc21441620e5842ef793a1d6b5a9"
ENDPOINT = "8d3ea9fa-4330-4540-a09a-727bed8b447a?stream=false"


def run_flow(message: str) -> dict:
    """
    Call the LangFlow API to process the message.
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# Streamlit Interface
st.set_page_config(page_title="Hackonauts Chatbot", layout="centered")

st.title("Chat with Hackonauts")
st.markdown("Get instant responses from LangFlow's AI engine.")

# Input container
with st.container():
    st.write("### Enter your message:")
    user_message = st.text_input("", placeholder="Type your message here...")

# Button and response container
if st.button("Send"):
    if not user_message.strip():
        st.error("⚠️ Please enter a valid message.")
    else:
        with st.spinner("Waiting for response..."):
            try:
                response = run_flow(user_message)
                # Extract the result
                result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get(
                    "results", {}).get("message", {}).get("text", "No response.")
                
                # Response container
                st.success("Response Received:")
                st.markdown(f"""
                    <div style="background-color:#f9f9f9; padding:10px; border-radius:5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                        <p style="color:#333; font-size:16px; font-family:Arial, sans-serif;">{result}</p>
                    </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ An error occurred: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
