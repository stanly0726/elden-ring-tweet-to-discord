import os
from flask import Flask, request
import requests
from dhooks import Webhook, File

app = Flask(__name__)
env = os.environ


@app.route("/", methods=["POST"])
def webhook():
    content = request.json["content"]
    username = request.json["username"]
    avatar_url = request.json["avatar_url"]
    media = request.json["media"].split(",")
    webhook_url = (
        "https://discord.com/api/webhooks/"
        + env.get("webhook_id")
        + "/"
        + env.get("webhook_token")
    )
    hook = Webhook(webhook_url)

    hook.send(content=content, username=username, avatar_url=avatar_url)

    for url in media:
        r = requests.get(url)
        open("file", "wb").write(r.content)
        f = File("file", "image.jpg")
        hook.send(file=f, username=username, avatar_url=avatar_url)

    return "200 ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
