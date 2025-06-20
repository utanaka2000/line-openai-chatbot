import base64
import os
import random
from dataclasses import dataclass

from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    PushMessageRequest,
    ReplyMessageRequest,
    StickerMessage,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent

from src.openai_chat import generate_image_comment, generate_response


def is_mentioned(text: str, bot_name: str) -> bool:
    return f"@{bot_name}" in text


def reply_message(reply: str, api_client: ApiClient, event: MessageEvent) -> None:
    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token, messages=[TextMessage(text=reply)]
        )
    )


def get_bot_name(api_client: ApiClient) -> str:
    line_bot_api = MessagingApi(api_client)
    bot_info = line_bot_api.get_bot_info()
    return bot_info.display_name


def get_user_name(event: MessageEvent, api_client: ApiClient) -> str | None:
    line_bot_api = MessagingApi(api_client)
    user_info = line_bot_api.get_user_profile(event.source.user_id)
    if user_info and user_info.display_name:
        return user_info.display_name
    else:
        return None


def process_text_message(event: MessageEvent, api_client: ApiClient) -> None:
    if event.source.type != "user" and not is_mentioned(
        event.message.text, get_bot_name(api_client)
    ):
        return

    reply_text = generate_response(event.message.text)
    print(reply_text)
    reply_message(reply_text, api_client, event)


def send_message(text: str, api_client: ApiClient, user_id: str) -> None:
    message = TextMessage(text=text)
    line_bot_api = MessagingApi(api_client)
    request = PushMessageRequest(to=user_id, messages=[message])
    line_bot_api.push_message(request)


def transfer_text_message(event: MessageEvent, api_client: ApiClient) -> None:
    if event.source.type != "user":
        return

    user_name = get_user_name(event, api_client)

    if user_name is None:
        user_name = "Unknown User"

    transfer_text = (
        f"{user_name}さんから「{event.message.text}」というメッセージが届きました。"
    )

    print(transfer_text)
    send_message(transfer_text, api_client, os.environ["LINE_TRANSFER_USER_ID"])


def process_image_message(event: MessageEvent, api_client: ApiClient) -> None:
    if event.source.type != "user":
        return
    line_blob_api = MessagingApiBlob(api_client)
    content = line_blob_api.get_message_content(event.message.id)
    base64_image = base64.b64encode(content).decode("utf-8")

    reply_text = generate_image_comment(base64_image)
    print(reply_text)
    reply_message(reply_text, api_client, event)


@dataclass
class Sticker:
    package_id: str
    sticker_id: str


def reply_sticker(sticker: Sticker, api_client: ApiClient, event: MessageEvent) -> None:
    line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                StickerMessage(
                    packageId=sticker.package_id, stickerId=sticker.sticker_id
                )
            ],
        )
    )


def process_sticker_message(event: MessageEvent, api_client: ApiClient) -> None:
    if event.source.type != "user":
        return

    stickers = [
        Sticker("6370", "11088035"),
        Sticker("789", "10866"),
        Sticker("789", "10876"),
        Sticker("6359", "11069858"),
    ]

    sticker = random.choice(stickers)
    print(sticker)
    reply_sticker(sticker, api_client, event)
