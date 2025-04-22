from unittest.mock import MagicMock, patch

from linebot.v3.webhook import MessageEvent

from src.usecase import process_text_message


class TestProcessTextMessage:
    @patch("src.usecase.reply_message")
    @patch("src.usecase.generate_response", return_value="Hello!")
    def test_source_type_is_user(self, mock_generate_response, mock_reply_message):
        # borrow from https://developers.line.biz/ja/reference/messaging-api/#message-event
        test_event = MessageEvent.from_json(
            """
            {
            "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
            "type": "message",
            "mode": "active",
            "timestamp": 1462629479859,
            "source": {
                "type": "user",
                "userId": "U4af4980629..."
            },
            "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
            "deliveryContext": {
                "isRedelivery": false
            },
            "message": {
                "id": "444573844083572737",
                "type": "text",
                "quoteToken": "q3Plxr4AgKd...",
                "text": "test message"
            }
            }
            """
        )

        mock_api_client = MagicMock()

        process_text_message(test_event, mock_api_client)

        mock_generate_response.assert_called_once_with("test message")
        mock_reply_message.assert_called_once_with(
            "Hello!", mock_api_client, test_event
        )

    @patch("src.usecase.reply_message")
    @patch("src.usecase.generate_response", return_value="Hello!")
    def test_source_type_is_group_without_bot_name(
        self, mock_generate_response, mock_reply_message
    ):
        test_event = MessageEvent.from_json(
            """
            {
            "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
            "type": "message",
            "mode": "active",
            "timestamp": 1462629479859,
            "source": {
                "type": "group",
                "groupId": "Ca56f94637c...",
                "userId": "U4af4980629..."
            },
            "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
            "deliveryContext": {
                "isRedelivery": false
            },
            "message": {
                "id": "444573844083572737",
                "type": "text",
                "quoteToken": "q3Plxr4AgKd...",
                "text": "@All @example Good Morning!! (love)",
                "emojis": [
                {
                    "index": 29,
                    "length": 6,
                    "productId": "5ac1bfd5040ab15980c9b435",
                    "emojiId": "001"
                }
                ],
                "mention": {
                "mentionees": [
                    {
                    "index": 0,
                    "length": 4,
                    "type": "all"
                    },
                    {
                    "index": 5,
                    "length": 8,
                    "userId": "U49585cd0d5...",
                    "type": "user",
                    "isSelf": false
                    }
                ]
                }
            }
            }
            """
        )

        mock_api_client = MagicMock()

        process_text_message(test_event, mock_api_client)

        mock_generate_response.assert_not_called()
        mock_reply_message.assert_not_called()

    @patch("src.usecase.reply_message")
    @patch("src.usecase.generate_response", return_value="Hello!")
    def test_source_type_is_group_with_bot_name(
        self, mock_generate_response, mock_reply_message
    ):
        test_event = MessageEvent.from_json(
            """
            {
                "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
                "type": "message",
                "mode": "active",
                "timestamp": 1462629479859,
                "source": {
                    "type": "group",
                    "groupId": "Ca56f94637c...",
                    "userId": "U4af4980629..."
                },
                "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                "deliveryContext": {
                    "isRedelivery": false
                },
                "message": {
                    "id": "444573844083572737",
                    "type": "text",
                    "quoteToken": "q3Plxr4AgKd...",
                    "text": "@All @example @bot_name Good Morning!! (love)",
                    "emojis": [
                    {
                        "index": 29,
                        "length": 6,
                        "productId": "5ac1bfd5040ab15980c9b435",
                        "emojiId": "001"
                    }
                    ],
                    "mention": {
                    "mentionees": [
                        {
                        "index": 0,
                        "length": 4,
                        "type": "all"
                        },
                        {
                        "index": 5,
                        "length": 8,
                        "userId": "U49585cd0d5...",
                        "type": "user",
                        "isSelf": false
                        }
                    ]
                    }
                }
                }
            """
        )

        with patch(
            "src.usecase.MessagingApi.get_bot_info",
            return_value=MagicMock(display_name="bot_name"),
        ):
            mock_api_client = MagicMock()

            process_text_message(test_event, mock_api_client)

            mock_generate_response.assert_called_once_with(
                "@All @example @bot_name Good Morning!! (love)"
            )
            mock_reply_message.assert_called_once_with(
                "Hello!", mock_api_client, test_event
            )
