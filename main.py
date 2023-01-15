import os
import discord
import asyncio

from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ.get("PREFIX"), intents=intents, help_command=None)
  
@bot.event
async def on_ready():
  print("Running")
    
async def load_extensions():
    for folder in os.listdir("modules"):
      if os.path.exists(os.path.join("modules", folder, "cog.py")):
        await bot.load_extension(f"modules.{folder}.cog")
        
async def main():
  await load_extensions()
  keep_alive()
  token = os.environ.get("DISCORD_KEY")
  await bot.start(token) 

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except:
    os.system("kill 1")
