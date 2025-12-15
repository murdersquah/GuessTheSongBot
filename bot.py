import json
import aiohttp

import discord
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["DISCORD_TOKEN"]
BOT_ID = config["DISCORD_BOT_ID"]

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


@bot.tree.command(
    name="guess",
    description="Guess the song from the lyrics. Requires spotify oauth connection.",
)
async def guess(interaction: discord.Interaction):
    user_id = interaction.user.id


    access_token = spotify_tokens.get(user_id)

    if not access_token:
        await interaction.response.send_message(
            "You have not connected your Spotify account."
        )
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"},
        ) as resp:

            if resp.status != 200:
                await interaction.response.send_message(
                    "Spotify authentication failed. Please reconnect your account."
                )
                return

            profile = await resp.json()

    display_name = profile.get("display_name", "Unknown")
    spotify_id = profile.get("id")

    await interaction.response.send_message(
        f"Spotify connected User: **{display_name}**\nID: `{spotify_id}`"
    )




bot.run(TOKEN)
