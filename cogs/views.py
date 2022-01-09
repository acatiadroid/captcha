import discord
from discord.ext.commands import CommandError

from utils import images

def key(interaction):
    return interaction.user

class ButtonOnCooldown(CommandError):
    def __init__(self, retry_after):
        self.retry_after = round(retry_after)

class RegenCaptcha(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 45

    async def interaction_check(self, interaction: discord.Interaction):
        retry_after = self.cooldown.update_rate_limit(interaction)
        if retry_after:
            raise ButtonOnCooldown(retry_after)

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction):
        if isinstance(error, ButtonOnCooldown):
            time = f"{error.retry_after} second" if error.retry_after == 1 else f"{error.retry_after} seconds"
            return await interaction.response.send_message(f"You're on cooldown. Please wait {time}.")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Don't know? Regenerate image")
    async def btnRegen(self, button: discord.ui.Button, interaction: discord.Interaction):
        captcha = images.generate_captcha()
        await interaction.response.send_message(
            content="Complete this new captcha to gain access to the server:",
            captcha=captcha["file_src"]
        ) 


class YesNo(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 25
        self.value = False
    
    @discord.ui.button(style=discord.ButtonStyle.Green, label="Yes")
    async def btnYes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()
    
    @discord.ui.button(style=discord.ButtonStyle.red, label="No")
    async def btnNo(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.stop()


class Skip(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 30
        self.value = False
    
    @discord.ui.View(style=discord.ButtonStyle.blurple, label="Skip")
    async def btnSkip(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()