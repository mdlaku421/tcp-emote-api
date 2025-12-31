from flask import Flask, request, jsonify
import socket
import os

VPS_IP = "34.142.230.235"
TCP_PORT = 9000   # যেটাতে তোমার game bot listen করছে

app = Flask(__name__)

def send_to_game(emote):
    try:
        s = socket.socket()
        s.connect((VPS_IP, TCP_PORT))
        s.send(emote.encode())
        s.close()
        return True
    except Exception as e:
        print("TCP ERROR:", e)
        return False

@app.route("/", methods=["GET"])
def home():
    return "TCP Emote API is running"

@app.route("/emote", methods=["GET"])
def emote():
    tc = request.args.get("tc")
    uid = request.args.get("uid")
    emote_id = request.args.get("emote")

    if not emote_id:
        return jsonify({"error": "Missing emote"}), 400

    msg = f"{tc}|{uid}|{emote_id}"
    ok = send_to_game(msg)

    if ok:
        return jsonify({"status": "sent", "data": msg})
    else:
        return jsonify({"status": "failed", "reason": "tcp offline"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
