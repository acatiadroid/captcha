from discord import AllowedMentions, Intents
from discord.ext import commands, ipc

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
                command_prefix=["c.", "C."],
                case_insensitive=True,
                help_command=commands.MinimalHelpCommand(),
                allowed_mentions=AllowedMentions(
                    users=True,
                    everyone=False,
                    roles=False,
                    replied_user=False
                ),
                intents=Intents.all(),
                owner_id=600056626749112322
            )
        self.ipc = ipc.Server(self, secret_key="abc")
    
    async def on_ready(self):
        print("yo")