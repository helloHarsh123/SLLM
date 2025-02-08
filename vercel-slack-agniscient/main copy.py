from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from agniscient import Config, SecureLLMClient
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.context.say import Say
from threading import Thread
import uvicorn

fast_app = FastAPI()

class CompletionRequest(BaseModel):
    prompt: str

class CompletionResponse(BaseModel):
    response: str

def initialize_client(openai_key: str, our_key: str, db_connection_string: Optional[str] = None):
    """Initialize the global client instance"""
    global _client
    load_dotenv()
    open_ai_key = os.getenv('OPEN_AI_KEY')
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
    config = Config(
        openai_key=open_ai_key,
        our_key="hg12345"
    )
    _client = SecureLLMClient(config)

load_dotenv()  
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
app = App(token=SLACK_BOT_TOKEN)

@app
def secureOpenAi(ack, say, command):
    # Acknowledge the command right away
    ack()
    # Extract the user's message
    text = command['text']
    response = _client.generate_response(
        text
    )
    say(f"*User's message:* {text}\n*AI's response:* {response}\n----------------")

if __name__ == "__main__":
    # Initialize the client
    initialize_client()
    # Run the server
    uvicorn.run(fast_app, host="0.0.0.0", port=3333)