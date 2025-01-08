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


# Streamlit Styling
st.markdown(
    """
    <style>
        body {
            font-family: 'Poppins', Arial, sans-serif;
            background-color: #030027;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            max-width: 700px;
            max-height: 90vh;
            margin: auto;
            margin-top: 5%;
            background: #151E3F;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            padding: 15px;
        }
        .header {
            color: yellow;
            text-align: center;
            font-size: 25px;
            font-weight: 500;
            margin-bottom: 15px;
        }
        .chat-window {
            height: 400px;
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .chat-bubble {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.5;
            max-width: 80%;
        }
        .user-bubble {
            background-color: #151E3F;
            color: white;
            align-self: flex-end;
        }
        .ai-bubble {
            background-color: #e5e5ea;
            color: black;
            align-self: flex-start;
        }
        .input-area {
            margin-top: 15px;
            display: flex;
            gap: 15px;
        }
        textarea {
            flex-grow: 1;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            resize: none;
            font-family: 'Poppins', Arial, sans-serif;
        }
        button {
            padding: 10px;
            background-color: yellow;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Container
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="header">Hackonauts Chatbot</div>', unsafe_allow_html=True)

# Chat Window
if "messages" not in st.session_state:
    st.session_state["messages"] = []

chat_window = st.empty()

# Display messages
with chat_window.container():
    for message in st.session_state["messages"]:
        if message["type"] == "user":
            st.markdown(f'<div class="chat-bubble user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Input Area
st.markdown('<div class="input-area">', unsafe_allow_html=True)
user_message = st.text_area("Type your message...", key="message", label_visibility="collapsed")
if st.button("Send", use_container_width=False):
    if user_message.strip():
        st.session_state["messages"].append({"type": "user", "content": user_message})

        # Call API
        try:
            response = run_flow(user_message)
            ai_message = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get(
                "message", {}).get("text", "No response.")
        except Exception as e:
            ai_message = f"An error occurred: {e}"

        st.session_state["messages"].append({"type": "ai", "content": ai_message})
        st.experimental_rerun()
    else:
        st.error("Please enter a valid message.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
