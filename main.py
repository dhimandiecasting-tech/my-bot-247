import discord
from discord.ext import commands

# 1. Setup the bot connection with proper permissions
intents = discord.Intents.default()
intents.members = True          # Required for welcoming and kicking/banning members
intents.message_content = True  # Required for reading the prefix commands (!kick, !ban)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🎉 Success! {bot.user.name} is online with Welcome, Kick, and Ban features!")


# 2. AUTOMATIC WELCOME GREET
@bot.event
async def on_member_join(member):
    # The bot looks for a text channel named 'general'
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"👋 Welcome to the server, {member.mention}! Glad to have you here! 🎉")


# 3. KICK COMMAND (Type: !kick @username)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🚨 Kicked {member.mention} for: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I cannot kick this user! Make sure my Bot Role is dragged **higher** than their role in Server Settings.")


# 4. BAN COMMAND (Type: !ban @username)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.guild.ban(member, reason=reason)
        await ctx.send(f"🔨 Banned {member.mention} for: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I cannot ban this user! Make sure my Bot Role is dragged **higher** than their role in Server Settings.")


# 5. Fallback Error Handler (If you don't have personal permissions to use it)
@kick.error
@ban.error
async def moderation_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You do not have permission to use this moderation command.")


# 6. Secure cloud environment configuration for 24/7 hosting
import os
bot.run(os.environ.get("DISCORD_TOKEN"))
