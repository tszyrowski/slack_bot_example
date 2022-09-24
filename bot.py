from cgitb import text
import imp
import os
from pathlib import Path

from dotenv import load_dotenv
import slack

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

# client.chat_postMessage(channel="#test", text="Hello from slack chat bot")

if __name__ == "__main__":
    client.chat_postMessage(channel="#test", text="Script worked")

