import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)



# Initialize the Slack client with bot token.
client = WebClient(token="TOKEN")
bot_user_id = client.auth_test()["user_id"]


@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Handle Slack URL verification
    if data.get("type") == "url_verification":
        challenge = data.get("challenge")
        return jsonify({"challenge": challenge})

    # Handle other Slack events 
    if 'event' in data:
        event = data['event']

        # Check if it's a message event 
        if event.get('type') == 'message' and 'subtype' not in event:
            channel_id = event['channel']
            user_message = event['text']
            user_id = event['user']
           

            # Ignore messages sent by the bot itself
            if user_id == bot_user_id:
                return jsonify({"status": "ok"}), 200

            

            # Echo the received message
            try:
                response = client.chat_postMessage(channel=channel_id, text=f"Echo: {user_message}")
            except SlackApiError as e:
                print(f"Error posting message: {e.response['error']}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=3000)
