from quart import Quart, render_template, url_for, redirect, request, jsonify
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from decouple import config
from discord.ext import ipc

app = Quart(__name__)
client = ipc.Client(secret_key="abc")

app.secret_key = b"hello"
app.config["DISCORD_CLIENT_ID"] = config("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = config("CLIENT_SECRET")  
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = config("TOKEN")

discord = DiscordOAuth2Session(app)

@app.route("/")
async def base():
    return redirect(url_for(".dashboard"))

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for(".dashboard"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/dashboard")
@requires_authorization
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for("login"))
    user = await discord.fetch_user()

    return await render_template("index.html", name=user.name)

@app.route("/dashboard", methods=["POST"])
async def form_post():
    # req = await request.form
    # await client.request("frm_post", text=req["text"])
    
    guilds = await client.request("guilds")
    user_guilds = await discord.fetch_guilds()

    for guild in user_guilds:
        if guild.permissions.manage_guild:
            guild.class_color = "green-border" if guild.id in guilds else "red-border"
            guilds.append(guild)
    
    guilds.sort(key=lambda x: x.class_color == "red-border")
    name = (await discord.fetch_user()).name
    return await render_template("dashboard.html", guilds = guilds, name = name)


@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))
    
    

if __name__ == "__main__":
    app.run(debug=True)
