import json

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
class GuessView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.guesses = 0        

        self.add_item(GuessButton("Artist"))
        self.add_item(GuessButton("Album"))
        self.add_item(GuessButton("Playlist"))


class GuessButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.guesses += 1

        await interaction.response.send_message(
            f"Guess attempt #{self.view.guesses}",
            ephemeral=True
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
 
    view = GuessView()            

    await interaction.response.send_message(
        "Choose a category to start guessing:",
        view=view                
    )


bot.run(TOKEN)
