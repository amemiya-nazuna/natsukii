import random
import requests
import string
import re

commandCooldown = False
values = list(string.ascii_lowercase) + list(range(0, 10))
prefix = "https://streamable.com/"

from discord.ext import tasks, commands

class Streamable(commands.Cog, name="Random Streamable"):
  def __init__(self, bot):
    self.index = 0
    self.bot = bot

  @tasks.loop(seconds=1)
  async def findStreamable(self, ctx: commands.Context, startMessage):
    global commandCooldown
    self.index += 1
    link = prefix
    for index in range(random.randint(5, 6)):
      link += str(random.choice(values))
    request = requests.get(link)
    if not "Oops!" in request.text:
      views = 0
      getViews = re.search("(\w+)\s+views", request.text)
      if getViews:
        views = (int(getViews.groups(1)[0]))
      formattedViews = "{:,}".format(views)
      await startMessage.delete()
      await ctx.send(f"{link} **({formattedViews} views)** found after **{str(self.index)} attempts!**")
      commandCooldown = False
      self.findStreamable.stop()
    if self.index >= 50:
      await startMessage.delete()
      await ctx.send("Sorry! I couldn't find a valid Streamable link. o(〒﹏〒)o")
      commandCooldown = False
      self.findStreamable.stop()
    
  @commands.command()
  async def randomStreamable(self, ctx):
    global commandCooldown
    if commandCooldown == True:
      await ctx.send("Someone is already trying to find a Streamable link! (￣︿￣)")
      return
    commandCooldown = True
    self.index = 0
    startMessage = await ctx.send("Finding Streamable link... σ(￣、￣〃)")
    self.findStreamable.start(ctx, startMessage)
   
async def setup(bot):
  await bot.add_cog(Streamable(bot))
