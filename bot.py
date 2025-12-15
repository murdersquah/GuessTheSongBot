import json
import random
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
    embed = discord.Embed(
        title="🎵 Guess The Song",
        description="Choose a category to start the game (coming soon):",
        color=discord.Color.blurple(),
    )

    embed.add_field(name=" Artist", value="Guess songs by an artist", inline=False)
    embed.add_field(name="Album", value="Guess songs from an album ", inline=False)
    embed.add_field(name="Liked Songs", value="Guess your liked songs", inline=False)
    embed.add_field(name="Playlist", value="Guess playlist", inline=False)
    embed.add_field(name="Trending Songs", value="Guess trending songs", inline=False)


    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
