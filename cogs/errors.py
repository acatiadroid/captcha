from discord.ext import commands
import discord
import sys
import traceback

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ You are on cooldown. Please wait **`{round(error.retry_after)}`** seconds before using this command again.", delete_after=10)
        
        if isinstance(error, commands.MissingRequiredArgument):
            e = discord.Embed(
                title='You are missing a required argument!', color=0x5865F2)
            e.description = f"""
            You are missing an argument that is required.
            Message: `{error}`
            
            **Command usage:**```yaml
{ctx.command.qualified_name} {ctx.command.signature}```
            NOTE: Arguments with `< >` around them are required, `[ ]` aren\'t required."""

            await ctx.send(embed=e, delete_after=10)


        if isinstance(error, commands.BadArgument):
            e = discord.Embed(title='Invalid argument!', color=0x5865F2)
            e.description = f"""
                    You have provided an argument that is invalid.
                    Message: `{error}`
                    
                    **Command usage:**```yaml
        {ctx.command.qualified_name} {ctx.command.signature}```
                    NOTE: Arguments with `< >` around them are required, `[ ]` aren\'t required."""

            await ctx.send(embed=e, delete_after=10)
        
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'I am missing the required permissions to do this. Please check that my role is above the users role and I have the necessary permissions.')


        else:
            e = discord.Embed(title='An unknown error occured', color=0x5865F2)
            e.description = f"Please report the following to our [support server](https://discord.gg/p5bURjs):\n\n{type(error)}: {error.__traceback__}"
            await ctx.send(embed=e, delete_after=10)
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)
