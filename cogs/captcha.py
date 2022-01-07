import discord
from discord.ext import commands

from utils import images

class RegenCaptcha(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 45
        self.ctx = None
    
    @discord.ui.button(style=discord.ButtonStyle.green, label="Don't know? Regenerate image")
    async def btnRegen(self, button: discord.ui.Button, interaction: discord.Interaction):
        # TODO

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


def setup(bot):
    bot.add_cog(Captcha(bot))