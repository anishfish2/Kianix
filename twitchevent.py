from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
WEBHOOK_SECRET = "your_webhook_secret"
WEBHOOK_URL = "your_webhook_url"

# Route to handle incoming EventSub notifications
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    payload = request.json
    # Handle the incoming EventSub notification here
    print("Received EventSub notification:", payload)
    return "OK"

# Route to verify the Webhook subscription
@app.route("/webhook", methods=["GET"])
def webhook_verification():
    challenge = request.args.get("hub.challenge")
    return challenge

# Subscribe to the "channel.online" event
def subscribe_to_eventsub():
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {CLIENT_SECRET}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "channel.online",
        "version": "1",
        "condition": {
            "broadcaster_user_id": "your_channel_id"
        },
        "transport": {
            "method": "webhook",
            "callback": WEBHOOK_URL,
            "secret": WEBHOOK_SECRET
        }
    }
    response = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, json=data)
    print("Subscription response:", response.text)

if __name__ == "__main__":
    app.run(debug=True)
    subscribe_to_eventsub()