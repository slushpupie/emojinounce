# Copyright 2019, Jay Kline
# Apache 2.0 License (https://www.apache.org/licenses/LICENSE-2.0.txt)

from slackeventsapi import SlackEventAdapter
import slack
import os
from flask import Flask


def create_app(config_filename, mapping={}):
    """Generate the Flask app"""

    announce_channel_id = os.environ["SLACK_ANNOUNCE_CHANNEL_ID"]
    slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
    endpoint = os.environ.get("SLACK_EVENTS_ENDPOINT", "/slack_events")

    # Create a SlackClient for your bot to use for Web API requests
    slack_client = slack.WebClient(slack_bot_token)

    app = Flask(__name__)
    slack_events_adapter = SlackEventAdapter(slack_signing_secret, endpoint, app)

    @slack_events_adapter.on("emoji_changed")
    def handle_emoji(event_wrapper):
        event = event_wrapper.get("event")
        if event.get("subtype") == "add":
            if event.get('value').startswith("alias:"):
                alias = event.get('value')[6:]
                text = f":{event['name']}: (new alias for `:{alias}:`)"
                slack_client.chat_postMessage(channel=announce_channel_id, text=text)
            else:
                text = f":{event['name']}:"
                slack_client.chat_postMessage(channel=announce_channel_id, text=text)
        elif event.get("subtype") == "remove":
            for name in event['names']:
                text = f"`:{name}:` has been removed"
                slack_client.chat_postMessage(channel=announce_channel_id, text=text)

    # Error events
    @slack_events_adapter.on("error")
    def error_handler(err):
        print("ERROR: " + str(err))

    return app
