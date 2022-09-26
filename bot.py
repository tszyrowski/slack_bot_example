import os
from pathlib import Path
import string

from dotenv import load_dotenv
from flask import Flask, request, Response
import slack
from slackeventsapi import SlackEventAdapter

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"],"/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

client.chat_postMessage(channel="#test", text="Slack bot created client")
BOT_ID = client.api_call("auth.test")["user_id"]

message_counts = {}

welcome_messages = {}

BAD_WORDS = ["hmm", "brum"]

class WelcomeMEssage:
    START_TEXT = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to this channel \n\n"
                "*Get started by completing the tasks*"
            )
        }
    }
    DIVIDER = {"type": "divider"}

    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.completed = False

    def get_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": "Welcome Robot!",
            "icon_emoji": self.icon_emoji,
            "text": "Fall back text, it is only if blocks failed",
            "blocks": [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }

    def _get_reaction_task(self):
        checkmark = ":white_check_mark:"
        if not self.completed:
            checkmark = ":white_large_square:"
        text = f"{checkmark} *React to this message*"

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


def send_welcome_message(channel, user):
    if channel not in welcome_messages:
        welcome_messages[channel] = {}
    if user in welcome_messages[channel]:
        return
    welcome = WelcomeMEssage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp = response["ts"]


    welcome_messages[channel][user] = welcome


def check_if_bad_words(message):
    msg = message.lower()
    msg.translate(str.maketrans("", "", string.punctuation))
    return any(word in msg for word in BAD_WORDS)


@slack_event_adapter.on("message")
def message(payload):
    print("--------------------- new message -------------------")
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if user_id != None and BOT_ID !=user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
        if text.lower() == "start":
            # Send message to the channel
            send_welcome_message(channel_id, user_id)
            # Send message directly to the user. Requires:
            # `im:write` and `reactions:read`
            send_welcome_message(f"@{user_id}", user_id)
        elif check_if_bad_words(text):
            ts = event.get("ts")
            client.chat_postMessage(
                channel=channel_id,
                thread_ts=ts,
                text="DON' LIKE IT"
            )
        # Send replicated message to the channel
        client.chat_postMessage(
            channel=channel_id,
            text=f"{text} send by {user_id}"
        )


@slack_event_adapter.on("reaction_added")
def reaction(payload):
    print("--------------------- new reaction -------------------")
    event = payload.get("event", {})
    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")

    if channel_id not in welcome_messages:
        return

    welcome = welcome_messages[channel_id][user_id]
    welcome.completed = True
    message = welcome.get_message()
    updated_message = client.chat_update(**message)
    welcome.timestamp = updated_message["ts"]


@app.route("/message-count", methods=["POST"])
def message_count():
    data = request.form
    print("-------------------- command message-count --------")
    print(data)
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(
        channel=channel_id,
        text=f"Message: {message_count}"
    )
    return Response(), 200

if __name__ == "__main__":
    
    app.run(debug=True)
    client.chat_postMessage(channel="#test", text="Script worked")

