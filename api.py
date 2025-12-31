from flask import Flask, request, jsonify
import socket
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 9000   # bot will listen here

app = Flask(__name__)

def send_to_game(data):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((TCP_IP, TCP_PORT))
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
    region = request.args.get("region")
    tc = request.args.get("tc")
    uid = request.args.get("uid")
    emote = request.args.get("emote")

    if not region or not tc or not uid or not emote:
        return jsonify({"error":"missing params"}), 400

    data = f"{region}|{tc}|{uid}|{emote}"

    if send_to_game(data):
        return jsonify({"status":"sent","data":data})
    else:
        return jsonify({"status":"tcp_offline"}), 500
