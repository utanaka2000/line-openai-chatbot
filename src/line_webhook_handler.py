import os

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
)
from linebot.v3.webhooks import ImageMessageContent, MessageEvent, TextMessageContent

from src.usecase import process_image_message, process_text_message

configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


def handle_line_event(body, signature):
    handler.handle(body, signature)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    print(event)
    with ApiClient(configuration) as api_client:
        process_text_message(event, api_client)


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event: MessageEvent):
    print(event)
    with ApiClient(configuration) as api_client:
        process_image_message(event, api_client)
