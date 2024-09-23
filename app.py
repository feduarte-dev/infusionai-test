import flask
from flask import Flask, request, render_template, jsonify
from message_helper import get_text_message_input, send_message
import os
from openai import OpenAI

app = Flask(__name__)

RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")


@app.route("/")
def index():
    return render_template("index.html", name=__name__)


@app.route("/send", methods=["POST"])
async def send():
    data = get_text_message_input(RECIPIENT_WAID)
    await send_message(data)
    return flask.redirect(flask.url_for("index"))


# Solved the multiple response for the same request but sometimes the message gets out of order in the queue
processed_messages = set()


@app.route("/process-message", methods=["POST"])
def process_message():
    data = request.json
    sender = data.get("sender")
    message = data.get("message")
    message_id = data.get("message_id")

    if message_id in processed_messages:
        return jsonify({"status": "message already processed"}), 200

    processed_messages.add(message_id)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a nice friend"},
            {"role": "user", "content": message},
        ],
    )

    print(f"Mensagem recebida de {sender}: {message}")
    print(completion.choices[0].message.content)

    # Send the response content back to user when I learn how to send custom messages
    return jsonify({"status": "message received"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
