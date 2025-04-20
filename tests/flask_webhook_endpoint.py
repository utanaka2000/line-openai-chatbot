from dotenv import load_dotenv
from flask import Flask, request

from main import main

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello_world():
    main(request)
    return "Hello, World!"


if __name__ == "__main__":
    # Use the following command:
    # PYTHONPATH=./ poetry run python tests/line/flask_webhook_endpoint.py
    app.run(debug=True)
