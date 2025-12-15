from flask import Flask, request
import requests
import base64
import json

from bot import spotify_tokens

app = Flask(__name__)

with open("config.json") as f:
    config = json.load(f)

CLIENT_ID = config["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = config["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8080/callback"


@app.route("/callback")
def callback():
    code = request.args.get("code")
    discord_user_id = request.args.get("state")

    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    token_data = response.json()
    spotify_tokens[int(discord_user_id)] = token_data["access_token"]

    return "Spotify connected successfully."


app.run(port=8080)
