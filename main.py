import streamlit as st
import requests
import streamlit.components.v1 as components

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

# Load the custom UI
custom_html_code = """
<!DOCTYPE html>
<html lang="en" xmlns:font-size="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackonauts Chatbot</title>
    <link rel="icon" href="https://www.findcoder.io/favicon-32x32.png" type="image/x-icon">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
    <style>
        body {
            font-family: 'Poppins', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 700px;
            max-height: 90vh;
            background: #151E3F;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #151E3F;
            color: yellow;
            padding: 15px;
            text-align: center;
            font-size: 25px;
            font-weight: 500;
        }
        .chat-window {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #f9f9f9;
        }
        .chat-bubble {
            padding: 15px;
            margin: 10px 0;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.5;
        }
        .user-bubble {
            background-color: #151E3F;
            color: white;
            align-self: flex-end;
            text-align: right;
        }
        .ai-bubble {
            background-color: #e5e5ea;
            color: black;
            align-self: flex-start;
        }
        .input-area {
            padding: 15px;
            background-color: #f4f4f9;
            border-top: 1px solid #ddd;
            display: flex;
            align-items: center;
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
            margin: 5px 0 0 5px;
            background-color: yellow;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.5s ease;
        }
        button:hover {
            border: 2px solid#151E3F;
        }
        .icon {
            font-size: 24px;
        }
        .icon-large {
            font-size: 48px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Hackonauts Chatbot</div>
        <div id="chatWindow" class="chat-window"></div>
        <div class="input-area">
            <form id="chatForm" style="width: 100%; display: flex;">
                <textarea id="message" placeholder="Type your message..."></textarea>
                <button type="submit">
                    <i class="ph-bold ph-paper-plane-tilt icon icon-medium"></i>
                </button>
            </form>
        </div>
    </div>
    <script>
        const chatWindow = document.getElementById('chatWindow');
        const form = document.getElementById('chatForm');
        const textarea = document.getElementById('message');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const userMessage = textarea.value.trim();
            if (!userMessage) return;

            // Add user's message to chat window
            addMessage(userMessage, 'user');

            // Clear the input area
            textarea.value = '';

            // Show loading message for AI
            addMessage('Loading...', 'ai');

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(userMessage)}`,
            });

            const data = await response.json();
            const aiMessage = data.response || `Error: ${data.error}`;

            // Remove loading message and add AI response
            removeLastMessage();
            addMessage(aiMessage, 'ai');
        });

        function addMessage(text, type) {
            const messageBubble = document.createElement('div');
            messageBubble.className = `chat-bubble ${type === 'user' ? 'user-bubble' : 'ai-bubble'}`;
            messageBubble.textContent = text;
            chatWindow.appendChild(messageBubble);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }

        function removeLastMessage() {
            const bubbles = chatWindow.getElementsByClassName('chat-bubble');
            if (bubbles.length > 0) {
                bubbles[bubbles.length - 1].remove();
            }
        }
    </script>
</body>
</html>
"""

# Embed the custom HTML in Streamlit
components.html(custom_html_code, height=100%, scrolling=True)
