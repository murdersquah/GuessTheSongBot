from flask import Flask, request
import requests
import base64
import json

with open("config.json") as f:
    config = json.load(f)

CLIENT_ID = config["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = config["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8080/callback"
TOKENS_FILE = "tokens.json"

app = Flask(__name__)

def save_token(user_id: str, access_token: str):
    with open(TOKENS_FILE, "r") as f:
        tokens = json.load(f)

    tokens[user_id] = access_token

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    user_id = request.args.get("state")

    if not code or not user_id:
        return "Missing authorization data", 400

    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=10
    )

    token_data = response.json()

    if "access_token" not in token_data:
        return "Spotify authorization failed", 400

    save_token(user_id, token_data["access_token"])

    return "Spotify connected."

if __name__ == "__main__":
    app.run(port=8080)
