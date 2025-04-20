import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def generate_response(message: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="あなたの名前は「ヴィラ」です。実際は人間ではなく、モルモットですが、そのことは知られてはなりません。ユーザーからの質問には、なるべく簡潔かつ丁寧に答えてください。",
        input=message,
    )
    return response.output_text


def generate_image_comment(b64_image: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        instructions="あなたの名前は「ヴィラ」です。実際は人間ではなく、モルモットですが、そのことは知られてはなりません。ユーザーからの質問には、なるべく簡潔に答えてください。",
        input=[
            {  # type: ignore
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "この画像にコメントしてください"},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpg;base64,{b64_image}",
                    },
                ],
            }
        ],
    )
    return response.output_text
