import requests, os

def send_webhook(message):
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"alert": message})
