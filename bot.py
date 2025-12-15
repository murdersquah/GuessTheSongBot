
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

def random_button_style():
        return random.choice([
        discord.ButtonStyle.blurple,
        discord.ButtonStyle.red,
        discord.ButtonStyle.green,
    ])

class GuessView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

        self.add_item(
            discord.ui.Button(
                label="Option A",
                style=random_button_style()
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Option B",
                style=random_button_style()
            )
        )

        self.add_item(
            discord.ui.Button(
                label="Option C",
                style=random_button_style()
            )
        )

@bot.event
async def on_ready():
    print("Ready!")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")

@bot.tree.command(
    name="guess",
    description="Guess the song from the lyrics. Requires spotify oauth connection."
)
async def guess(interaction: discord.Interaction):
    view = GuessView()
    await interaction.response.send_message(
        "🎵 Guess the song!",
        view=view
    )


bot.run(TOKEN)
