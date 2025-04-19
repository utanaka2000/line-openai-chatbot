from linebot.v3.webhooks import MessageEvent

from src.openai_chat import generate_response


def process_message(event: MessageEvent) -> str | None:
    # user_id = event.source.user_id
    message = event.message.text
    reply_text = generate_response(message)
    return reply_text
