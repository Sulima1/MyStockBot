import os, discord, io
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AV_TOKEN = os.getenv('AV_TOKEN')

BACKGROUND = 0,0,0,0.9
LINE = 0,255,0,0.9

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
       with open(str(cleaned[1]) + '.png', "ab") as cleaned[1]:
        plt.savefig(cleaned[1], format='png', bbox_inches='tight', dpi=80, facecolor='k', edgecolor='g')
       file = discord.File('C:\VSCode_Projects\MyStockBot\GOOGL.png')
       embed = discord.Embed()
       embed.set_image(url='attachment://' + str(cleaned[1]) + '.png')
       await message.channel.send(embed=embed, file=file)



client.run(DISCORD_TOKEN)