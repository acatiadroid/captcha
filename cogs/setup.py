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
            ctx.guild.id,
            {
                "msg_channel": channel.id,
                "msg_id": msg.id
            },
            append=False
        )
        
        await ctx.send(f"Success! The message has been sent into {channel.mention}.")

    @commands.command(name="verifiedrole", aliases=["vrole", "verified_role"])
    @checks.guild_manager()
    async def verifiedrole(self, ctx, role: discord.Role):
        """
        Sets the role that will be given to users that complete the captcha successfully.

        Required permission:
        Manage Guild

        Arguments:
            role — the role to give to users that pass verification.
        """
        botrole = ctx.me.top_role
        if role.position >= botrole.position:
            return await ctx.send(f'{role} (position: {role.position})is above or equal to my highest role {botrole} (position: {botrole.position}). This means I can\'t give that role.')

        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            return await ctx.send("That role is above or equal to your highest role, therefore you cannot set it.")
        
        insert_config(
            ctx.guild.id,
            append=True,
            key="verified_role",
            value=role.id
        )

        await ctx.send(f"Success! Verified role has been set to **{role}**")



def setup(bot):
    bot.add_cog(Configuration(bot))
