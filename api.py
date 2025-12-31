from flask import Flask, request, jsonify
import socket

VPS_IP = "34.142.230.235"
TCP_PORT = 9000

app = Flask(__name__)

def send_to_game(data):
    try:
        s = socket.socket()
        s.connect((VPS_IP, TCP_PORT))
        s.send(data.encode())
        s.close()
        return True
    except Exception as e:
        print("TCP error:", e)
        return False

@app.route("/")
def home():
    return "TCP Emote API Online"

@app.route("/emote")
def emote():
    tc = request.args.get("tc")
    uid = request.args.get("uid")
    emote = request.args.get("emote")

    if not tc or not uid or not emote:
        return jsonify({"error": "missing params"}), 400

    data = f"{tc}|{uid}|{emote}"
    ok = send_to_game(data)

    if ok:
        return jsonify({"status": "sent", "data": data})
    else:
        return jsonify({"status": "tcp_offline"}), 500

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500
