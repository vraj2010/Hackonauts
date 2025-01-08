import streamlit as st
import requests
import streamlit.components.v1 as components

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "badb4656-66c0-45f4-b943-79abcbb3ec30"
APPLICATION_TOKEN = "AstraCS:saguMlpoQItPIzsXrFGOocRZ:fa56792c4868e61e6aca0341cfe84d0b3879fc21441620e5842ef793a1d6b5a9"
ENDPOINT = "8d3ea9fa-4330-4540-a09a-727bed8b447a?stream=false"

# Function to call API
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

# Full-Width Webpage Code
custom_html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackonauts Chatbot</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            background-color: #030027;
            color: white;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100vh;
            padding: 0 10%;
            box-sizing: border-box;
        }
        .header {
            text-align: center;
            font-size: 2.5em;
            color: yellow;
            margin-bottom: 20px;
        }
        .chat-window {
            width: 100%;
            max-width: 1200px;
            height: 70%;
            overflow-y: auto;
            background: #151E3F;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }
        .chat-bubble {
            margin: 10px 0;
            padding: 15px;
            border-radius: 15px;
            font-size: 1.2em;
        }
        .user-bubble {
            background-color: #4caf50;
            color: white;
            align-self: flex-end;
            text-align: right;
        }
        .ai-bubble {
            background-color: #f4f4f4;
            color: black;
            align-self: flex-start;
            text-align: left;
        }
        .input-area {
            width: 100%;
            max-width: 1200px;
            margin-top: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        textarea {
            width: 85%;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 1em;
            resize: none;
            font-family: 'Poppins', sans-serif;
        }
        button {
            width: 10%;
            margin-left: 10px;
            background-color: yellow;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2em;
            font-weight: bold;
        }
        button:hover {
            background-color: #e0c200;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Hackonauts Chatbot</div>
        <div id="chatWindow" class="chat-window"></div>
        <div class="input-area">
            <form id="chatForm" style="width: 100%; display: flex;">
                <textarea id="message" rows="1" placeholder="Type your message here..."></textarea>
                <button type="submit">Send</button>
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

            // Fetch response from the server
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

# Embed HTML in Streamlit
components.html(custom_html_code, height=800, scrolling=True)
