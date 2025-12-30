from flask import Flask, request, jsonify
import os

app = Flask(__name__)

queue = []

@app.route("/emote", methods=["GET"])
def emote():
    tc = request.args.get("tc")
    uid = request.args.get("uid")
    emote_id = request.args.get("emote")

    if not tc or not uid or not emote_id:
        return jsonify({"status":"error","msg":"missing params"}), 400

    queue.append({
        "tc": tc,
        "uid": uid,
        "emote": emote_id
    })

    return jsonify({
        "status": "queued",
        "tc": tc,
        "uid": uid,
        "emote": emote_id
    })


@app.route("/get", methods=["GET"])
def get():
    if len(queue) == 0:
        return jsonify({"status":"empty"})

    return jsonify(queue.pop(0))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
