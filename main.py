import os
from time import time as Time

import requests
from dhooks import File, Webhook
from flask import Flask, request

app = Flask(__name__)
env = os.environ


@app.route("/", methods=["POST"])
def webhook():
    content = request.json["content"]
    username = request.json["username"]
    avatar_url = request.json["avatar_url"]
    try:
        media = request.json["media"].split(",")
    except:
        pass
    
    webhook_url = (
        "https://discord.com/api/webhooks/"
        + env.get("webhook_id")
        + "/"
        + env.get("webhook_token")
    )
    hook = Webhook(webhook_url)

    release_date = 1642694400
    now = Time()
    time = "> " + str(round((release_date - now) / 86400)) + " day until release"
    time.sleep(1)

    hook.send(content=time, username=username, avatar_url=avatar_url)
    hook.send(content=content, username=username, avatar_url=avatar_url)
    try:
        for url in media:
            r = requests.get(url)
            open("file", "wb").write(r.content)
            f = File("file", "image.jpg")
            hook.send(file=f, username=username, avatar_url=avatar_url)
    except:
        pass
    
    return "200 ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
