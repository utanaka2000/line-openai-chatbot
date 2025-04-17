from linebot.v3.webhooks import MessageEvent


def process_message(event: MessageEvent) -> str | None:
    user_id = event.source.user_id
    message = event.message.text
    reply_text = message * 2
    return reply_text
