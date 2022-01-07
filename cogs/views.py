import discord
from discord.ext.commands import CooldownMapping, CommandError

def key(interaction):
    return interaction.user

class ButtonOnCooldown(CommandError):
    def __init__(self, retry_after):
        self.retry_after = round(retry_after)

class RegenCaptcha(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 45
        self.ctx = None

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Don't know? Regenerate image")
    async def btnRegen(self, button: discord.ui.Button, interaction: discord.Interaction):
        # TODO
        pass

class BeginVerification(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 45
        self.ctx = None
        self.cooldown = CooldownMapping.from_cooldown(1, 30, key)


    async def interaction_check(self, interaction: discord.Interaction):
        retry_after = self.cooldown.update_rate_limit(interaction)
        
        if retry_after:
            return await interaction.response.send_message("You're on cooldown")
    
    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction):
        if isinstance(error, ButtonOnCooldown):
            time = f"{error.retry_after} second" if error.retry_after == 1 else f"{error.retry_after} seconds"
            return await interaction.response.send_message(f"You're on cooldown. Please wait {time}.")

    @discord.ui.button(style=discord.ButtonStyle.green, label="Begin Verification")
    async def btnBegin(self, button: discord.ui.Button, interaction: discord.Interaction):
        # TODO
        pass
