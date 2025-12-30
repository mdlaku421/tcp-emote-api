from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Store emotes in memory
emotes = []

@app.route("/")
def home():
    return "TCP Emote API is Running"

# Send emote
@app.route("/emote", methods=["GET"])
def send_emote():
    tc = request.args.get("tc")
    uid = request.args.get("uid")
    emote = request.args.get("emote")

    if not tc or not uid or not emote:
        return jsonify({"status":"error","msg":"Missing parameters"})

    emotes.append({
        "tc": tc,
        "uid": uid,
        "emote": emote
    })

    return jsonify({"status":"queued"})

# Bot will call this
@app.route("/get")
def get_emote():
    if len(emotes) == 0:
        return jsonify({"status":"empty"})

    data = emotes.pop(0)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
