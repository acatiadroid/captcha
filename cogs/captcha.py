import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import CooldownMapping, CommandError

from cogs.views import RegenCaptcha
from utils import images
from utils.botinstance import Bot

def key(interaction):
    return interaction.user

class ButtonOnCooldown(CommandError):
    def __init__(self, retry_after):
        self.retry_after = round(retry_after)


class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global botobj
        botobj = self.bot
    
    @commands.command(name="test")
    @commands.is_owner()
    async def _test(self, ctx):
        await ctx.send('yo')

class BeginVerification(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.bot = botobj
        self.cooldown = CooldownMapping.from_cooldown(1, 30, key)

    # async def interaction_check(self, interaction: discord.Interaction):
    #     print('yes')
    #     retry_after = self.cooldown.update_rate_limit(interaction)

    #     if retry_after:
    #         raise ButtonOnCooldown(retry_after)


    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction):
        if isinstance(error, ButtonOnCooldown):
            time = f"{error.retry_after} second" if error.retry_after == 1 else f"{error.retry_after} seconds"
            return await interaction.response.send_message(f"You're on cooldown. Please wait {time}.", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Begin Verification", custom_id="btn")
    async def btnBegin(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            bot = Captcha(Bot())

            user = interaction.user
            captcha = images.generate_captcha()
            try:
                dm = await user.create_dm()
            except:
                return await interaction.response.send_message("Please enable your DMs!", ephemeral=True)

            e = discord.Embed(
                color=0xf43333,
                description="Please complete the captcha below by typing the letters you see in the image below and send it in this DM.",
                title="Are you a human? Let's find out!"
            )
            e.add_field(name="Don't know the letters?", value="That's fine! Use the button below to generate a new captcha.")
            e.set_footer(text="You have 45 seconds to respond.")
            e.set_image(url=f"attachment://captcha.png")
            await dm.send(embed=e, view=RegenCaptcha(), file=captcha["file_src"])

            await interaction.response.send_message(f":mailbox: You have mail! Check your DMs.", ephemeral=True)

            def check(message):
                return message.author.id == user.id

            try:
                msg = await bot.wait_for("message", check=check, timeout=45)
                print("1")
                if msg.content.lower() == captcha["text"]:
                    return await dm.send('correct')
                else:
                    return await dm.send('wrong')

            except asyncio.TimeoutError:
                return await interaction.response.send_message('Timeout')
        except Exception as e:
            print(e)    
    

def setup(bot):
    bot.add_cog(Captcha(bot))
