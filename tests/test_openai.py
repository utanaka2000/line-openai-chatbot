import base64

import pytest

from src.openai_chat import generate_image_comment, generate_response


@pytest.mark.api
def test_chat_with_gpt():
    # Test the chat_with_gpt function with a sample message
    message = "こんにちは"
    response = generate_response(message)
    print(response)

    # Check if the response is not empty
    assert response is not None, "Response should not be None"

    # Check if the response is a string
    assert isinstance(response, str), "Response should be a string"


@pytest.mark.api
def test_chat_with_image():
    # Test the chat_with_image function with a sample image URL
    with open("tests/data/image.jpg", "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    response = generate_image_comment(base64_image)
    print(response)

    # Check if the response is not empty
    assert response is not None, "Response should not be None"

    # Check if the response is a string
    assert isinstance(response, str), "Response should be a string"
