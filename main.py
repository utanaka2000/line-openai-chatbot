from linebot.v3.exceptions import InvalidSignatureError

from src.line_webhook_handler import handle_line_event


def main(request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    try:
        handle_line_event(body, signature)
        return "OK", 200

    except InvalidSignatureError:
        return (
            "Invalid signature. Please check your channel access token/channel secret.",
            403,
        )
    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500
