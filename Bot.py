import discord
from discord.ext import commands
from datetime import timedelta

# ------------------
# CONFIG
# ------------------
TOKEN = "MTQ2MzU2MjgzMjU2OTMwMzI0Ng.GZhtg4.FhbqXj8xNtiehXBVHump0Q60pqo1EifB9YvS58"
ROLE_NAME = "🌿Los lugares de Ana"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

timeout_minutes = 10

# ------------------
# FUNCIONES
# ------------------

def has_mod_role(member):
    return any(role.name == ROLE_NAME for role in member.roles)

# ------------------
# EVENTOS
# ------------------

@bot.event
async def on_ready():
    print(f"🟢 Bot listo como {bot.user}")

# ------------------
# CHECK GLOBAL DE ROL
# ------------------

@bot.check
async def global_role_check(ctx):
    if ctx.author.guild_permissions.administrator:
        return True

    if has_mod_role(ctx.author):
        return True

    await ctx.send("❌ No tienes el rol **🌿Los lugares de Ana**.")
    return False

# ------------------
# COMANDOS
# ------------------

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason="Sin razón"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} expulsado.\n📄 {reason}")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="Sin razón"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} baneado.\n📄 {reason}")

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 {amount} mensajes borrados.")
    await msg.delete(delay=3)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason="Sin razón"):
    duration = timedelta(minutes=timeout_minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 {member.mention} silenciado por {timeout_minutes} min.\n📄 {reason}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} ya puede hablar.")

@bot.command()
async def setmute(ctx, minutes: int):
    global timeout_minutes

    if minutes < 1 or minutes > 10080:
        await ctx.send("❌ Entre 1 y 10080 minutos.")
        return

    timeout_minutes = minutes
    await ctx.send(f"⏱️ Tiempo de mute cambiado a {minutes} minutos.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Falta un argumento.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Usuario no encontrado.")
    else:
        raise error

bot.run(TOKEN)
