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
    return response.json()


# Streamlit Interface
st.title("Chat with LangFlow")

# Input message from the user
user_message = st.text_input("Enter your message:")

if st.button("Send"):
    if not user_message.strip():
        st.error("Please enter a valid message.")
    else:
        try:
            response = run_flow(user_message)
            # Extract the result
            result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get(
                "text", "No response.")
            st.success("Response:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}"
