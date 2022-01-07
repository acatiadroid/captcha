import discord
import asyncio
import os
from decouple import config
from discord.ext import commands

bot = commands.Bot(command_prefix="c.")

# @bot.command()
# async def captcha(ctx):
#     await ctx.author.send("Please solve the captcha below to gain access to the server:", file=file)
#     def check(message):
#         return message.author.id == ctx.author.id
#     try:
#         msg = await bot.wait_for("message", check=check, timeout=45)
#         print("ye")
#         if msg.content.lower() == text.lower():
#             await ctx.author.send('correct')
#         else:
#             await ctx.author.send('wrong')

#     except asyncio.TimeoutError:
#         await ctx.send("timeout")
    
#     os.remove(file_name + ".png")


if __name__ == "__main__":
    bot.run(config["TOKEN"])
