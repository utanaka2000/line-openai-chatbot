import os

from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from src.usecase import process_message

load_dotenv()
configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


def handle_line_event(body, signature):
    handler.handle(body, signature)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print(event)
    if event.source.type == "user":
        print("User ID:", event.source.user_id)
    elif event.source.type == "group":
        print("Group ID:", event.source.group_id)

    reply_text = process_message(event)
    if reply_text is None:
        return

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        profile = line_bot_api.get_profile(event.source.user_id)
        print(profile.display_name)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=reply_text)]
            )
        )
