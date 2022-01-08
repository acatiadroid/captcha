import discord
from discord.ext import commands

from utils import checks
from utils.json_wrapper import insert_config

from cogs.captcha import BeginVerification

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create")
    @checks.guild_manager()
    async def _create(self, ctx, channel: discord.TextChannel, *, message = None):
        """
        Creates a message containing a button which will initialize the verification process.

        Required permission:
        Manage Guild

        Arguments:
            channel — the channel you want the message to get sent in.
            message (OPTIONAL) — the message you want above the button. I.E "click below to verify"
        """
        e = discord.Embed(
            color=0xfc433a,
            title="Captcha",
            description=f":lock: {message}" if message else ":lock: Please click the button below to begin a captcha to verify that you're human!"
        )
        e.set_footer(text="This server is protected from raids by Captcha Bot")
        view = BeginVerification()
        msg = await channel.send(embed=e, view=view)
        insert_config(
            {
                "msg_channel": channel.id,
                "msg_id": msg.id
            },
            ctx
        )
        
        await ctx.send(f"Success! The message has been sent into {channel.mention}.")

    

def setup(bot):
    bot.add_cog(Configuration(bot))
