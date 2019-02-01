import os
from slackclient import SlackClient


slack_client = SlackClient(os.getenv('SLACK_BOT_TOKEN'))
starterbot_id = None

def send_message(message):
    starterbot_id = slack_client.api_call('auth.test')['user_id']
    slack_client.api_call(
        'chat.postMessage',
        channel=os.getenv('CHANNEL_ID'),
        text=message
    )
