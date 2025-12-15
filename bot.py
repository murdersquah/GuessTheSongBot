-----------/import json
import urblib.parse
import discord
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["DISCORD_TOKEN"]
SPOTIFY_CLIENT_ID = config["SPOTIFY_CLIENT_ID"]

REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "user-read-private user-read-email playlist-read-private user-library-read"
TOKENS_FILE = "tokens.json"

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix=None,
    help_command=None,
    is_case_insensitive=True,
    intents=discord.Intents.all(),
)
def load_tokens():
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

def user_logged_in(user_id: int) -> bool:
    tokens = load_tokens()
    return str(user_id) in tokens

@bot.event
async def on_ready():
  await bot.tree.sync()
  print ("Bot online")

@bot.tree.command(name="login", description="Connect your Spotify account")
async def login(interaction: discord.Interaction):
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": str(interaction.user.id)
    }

    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode(params)
    )

    await interaction.response.send_message(
        f"Click to connect Spotify:\n{auth_url}",
        ephemeral=True
    )

@bot.tree.command(
    name="guess",
    description="Guess the song from the lyrics. Requires spotify oauth connection.",
)
async def guess(interaction: discord.Interaction):
    if not user_logged_in(interaction.user.id):
        await interaction.response.send_message(
            "❌ You must connect Spotify first using `/login`",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "Will implement later",
        ephemeral=True
    )
bot.run(TOKEN)
