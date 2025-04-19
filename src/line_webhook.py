import base64
import os

from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import ImageMessageContent, MessageEvent, TextMessageContent

from src.openai_chat import generate_image_comment
from src.usecase import process_message

load_dotenv()
configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


def handle_line_event(body, signature):
    handler.handle(body, signature)


def is_mentioned(text, bot_name) -> bool:
    return f"@{bot_name}" in text


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print(event)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if event.source.type != "user" and not is_mentioned(
            event.message.text, line_bot_api.get_bot_info().display_name
        ):
            return
        reply_text = process_message(event)
        if reply_text is None:
            return
        print(reply_text)
        profile = line_bot_api.get_profile(event.source.user_id)
        print(profile.display_name)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=reply_text)]
            )
        )


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event: MessageEvent):
    print(event)
    if event.source.type != "user":
        return

    with ApiClient(configuration) as api_client:
        line_blob_api = MessagingApiBlob(api_client)
        content = line_blob_api.get_message_content(event.message.id)
        # image_data = b""
        # image_data = b"".join(content.iter_content())

        base64_image = base64.b64encode(content).decode("utf-8")
        reply_text = generate_image_comment(base64_image)
        print(reply_text)

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)],
                )
            )
