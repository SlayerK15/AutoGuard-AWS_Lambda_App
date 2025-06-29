import requests
from autoguard.config import SLACK_WEBHOOK_URL

def notify_slack(message):
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})
