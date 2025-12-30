from flask import Flask, request, jsonify
import socket
import os

app = Flask(__name__)

TCP_IP = "127.0.0.1"
TCP_PORT = 9000   # যদি main.py তে আলাদা থাকে, সেটা বসাবে

def send_to_bot(msg):
    try:
        s = socket.socket()
        s.connect((TCP_IP, TCP_PORT))
        s.send(msg.encode())
        s.close()
        return True
    except:
        return False

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    if not data or "emote" not in data:
        return jsonify({"status":"error","msg":"emote missing"})
    if send_to_bot(data["emote"]):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"bot offline"})

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
