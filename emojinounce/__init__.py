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
    @app.route("/", methods=["GET"])
    @app.route("/health", methods=["GET"])
    def default():
      return "ok", 200

    @slack_events_adapter.on("emoji_changed")
    def handle_emoji(event_wrapper):
        event = event_wrapper.get("event")
        if event.get("subtype") == "add":
            if event.get('value').startswith("alias:"):
                alias = event.get('value')[6:]
                blocks = f"""{
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Alias Added\n*Original Emoji:* `:{event['name']}:`\n*New Alias:* `:{alias}:`"
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "{event['value']}",
                                "alt_text": "{alias}"
                            }
                        }
                    ]
                }"""
                slack_client.chat_postMessage(channel=announce_channel_id, blocks=blocks)
                
            else:
                blocks = f"""{
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Emoji Added\n*Name:* `:{event['name']}:`"
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "{event['value']}",
                                "alt_text": "{event['name']}"
                            }
                        }
                    ]
                }"""
                slack_client.chat_postMessage(channel=announce_channel_id, blocks=blocks)
        elif event.get("subtype") == "remove":
            
            for name in event['names']:
                blocks = f"""{
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Emoji Removed\n*Name:* `:{name}:`"
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "https://a.slack-edge.com/production-standard-emoji-assets/13.0/apple-medium/1f6ab.png",
                                "alt_text": "{name}"
                            }
                        }
                    ]
                }"""
                slack_client.chat_postMessage(channel=announce_channel_id, blocks=blocks)
            
    # Error events
    @slack_events_adapter.on("error")
    def error_handler(err):
        print("ERROR: " + str(err))

    return app
