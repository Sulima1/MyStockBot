import os, discord, pandas
from dotenv import load_dotenv
from discord.ext import commands
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt



load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AV_TOKEN = os.getenv('AV_TOKEN')

client = discord.Client()
ts = TimeSeries(key = str(AV_TOKEN), output_format = 'pandas')

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name = GUILD)
    print("connected")


@client.event
async def on_message(message):    
    if message.author == client.user:
        return
    cleaned = message.content.split()
    if (len(cleaned) == 1):
        await message.channel.send("Hi I'm MyStockBot! In order to use me, please ping me and the name of the stock you would like to look up.")
    else:
       data, meta_data = ts.get_intraday(symbol=cleaned[1],interval='1min', outputsize='full')
       data['4. close'].plot()
       plt.title("Intraday Times Series for the " + cleaned[1] + " stock (1 min)")
       plt.show()


client.run(DISCORD_TOKEN)