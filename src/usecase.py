import base64

from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent

from src.openai_chat import generate_image_comment, generate_response


def is_mentioned(text, bot_name) -> bool:
    return f"@{bot_name}" in text


def reply_message(reply: str, api_client, event):
    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token, messages=[TextMessage(text=reply)]
        )
    )


def process_text_message(event: MessageEvent, api_client: ApiClient) -> None:
    line_bot_api = MessagingApi(api_client)
    if event.source.type != "user" and not is_mentioned(
        event.message.text, line_bot_api.get_bot_info().display_name
    ):
        return

    reply_text = generate_response(event.source.text)
    print(reply_text)
    reply_message(reply_text, api_client, event)


def process_image_message(event: MessageEvent, api_client: ApiClient) -> None:
    if event.source.type != "user":
        return
    line_blob_api = MessagingApiBlob(api_client)
    content = line_blob_api.get_message_content(event.message.id)
    base64_image = base64.b64encode(content).decode("utf-8")

    reply_text = generate_image_comment(base64_image)
    print(reply_text)
    reply_message(reply_text, api_client, event)
