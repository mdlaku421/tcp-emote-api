from flask import Flask, request, jsonify
import os

app = Flask(__name__)

emotes = []

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    if not data or "emote" not in data:
        return jsonify({"status":"error"})
    emotes.append(data["emote"])
    return jsonify({"status":"queued"})

@app.route("/get")
def get():
    if len(emotes)==0:
        return jsonify({"emote":""})
    return jsonify({"emote": emotes.pop(0)})

app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)))
