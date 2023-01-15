import discord
import pytz
from datetime import datetime
from discord.ext import commands

timezone = pytz.timezone("Asia/Taipei")

lastMessages = {}

class Sniper(commands.Cog, name="Sniper"):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()     
  async def on_raw_message_delete(self, message):
    if message.cached_message.author == self.bot.user:
      return
    channel_id = str(message.channel_id)
    guild_id = str(message.guild_id)

    if lastMessages.get(guild_id):
      lastMessages.get(guild_id).update({channel_id:{
        "author":message.cached_message.author,
        "content":message.cached_message.content,
        "time":datetime.now(timezone)
      }})
    else:
      lastMessages.update({guild_id: {channel_id:{
        "author":message.cached_message.author,
        "content":message.cached_message.content,
        "time":datetime.now(timezone),
      }}})

  @commands.command()
  async def snipe(self, ctx):
    selectedMessage = None
    channel_id = str(ctx.channel.id)
    guild_id = str(ctx.guild.id)
    if guild_id in lastMessages:
      guild = lastMessages.get(guild_id)
      if channel_id in guild:
        selectedMessage = guild.get(channel_id)
    if selectedMessage:
      author = selectedMessage["author"]
      content = selectedMessage["content"]
      time = selectedMessage["time"]
      year = str(time.year).zfill(2)
      month = str(time.month).zfill(2)
      day = str(time.day).zfill(2)
      hour = str(time.hour).zfill(2)
      minute = str(time.minute).zfill(2)
      embedMessage = discord.Embed(title=content, color=0xffbde1)
      embedMessage.set_author(name=author, icon_url=author.avatar.url)
      embedMessage.set_footer(text=f"{year}/{month}/{day} {hour}:{minute}")
      await ctx.send(embed=embedMessage)
    else:
      await ctx.send("No message to be sniped! o(〒﹏〒)o")
    
async def setup(bot):
  await bot.add_cog(Sniper(bot))
