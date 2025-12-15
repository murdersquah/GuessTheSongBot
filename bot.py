import json
import aiohttp
import urllib.parse
import discord
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["DISCORD_TOKEN"]
SPOTIFY_CLIENT_ID = config["SPOTIFY_CLIENT_ID"]
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "user-read-private user-read-email playlist-read-private user-library-read"

bot = commands.Bot(
    command_prefix=None,
    help_command=None,
    is_case_insensitive=True,
    intents=discord.Intents.all(),
)
spotify_tokens = {
}
    

@bot.event
async def on_ready():
    print("Ready!")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
@bot.tree.command(name="login", description="Connect your Spotify account")
async def login(interaction: discord.Interaction):
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": str(interaction.user.id),
    }

    url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode(params)
    )

    await interaction.response.send_message(
        f"Click to connect Spotify:\n{url}",
        ephemeral=True
    )


@bot.tree.command(
    name="guess",
   description="Guess the song from the lyrics.",
)
async def guess(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Guess feature coming soon 🎵"
    )





bot.run(TOKEN)
