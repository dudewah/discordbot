import discord
import coinmarketcap
import pickle
import random
import asyncio
import os
from discord.ext import commands


##############################################################
##############################################################

bot = commands.Bot(command_prefix="!")

market = coinmarketcap.Market()


##############################################################
##############################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("addquote"):
            if not os.path.isfile("SILquote_file.txt"):
                SILquote_list = []
            else:
                with open("SILquote_file.txt", "rb") as SILquote_file:
                     SILquote_list = pickle.load(SILquote_file)
            SILquote_list.append(message.content[9:])
            with open("SILquote_file.txt", "wb") as SILquote_file:
                pickle.dump(SILquote_list,SILquote_file)
        elif "SIL" in message.content:
            with open("SILquote_file.txt", "rb") as SILquote_file:
                SILquote_list = pickle.load(SILquote_file)
            await bot.send_message(message.channel, random.choice(SILquote_list))
        elif message.content.startswith("moon"):
            await bot.send_message(message.channel, ":full_moon:") 
        elif message.content.startswith("whale"):
            await bot.send_message(message.channel, ":whale:")
    await bot.process_commands(message)



@bot.command()
async def multiply(left : float, right : float):
    """multiplies two numbers together"""
    await bot.say(left * right)


@bot.command()
async def add(left : float, right : float):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def exponent(number : float, power : float):
    """raises the first number to the exponent of the second number"""
    exponentiate = number ** power
    await bot.say(exponentiate)

@bot.command()
async def divide(left : float, right: float):
    """divdes first number by second number"""
    await bot.say(left/right)


##############################################################
##############################################################


@bot.command()
async def price(currency):
    """pulls price info for currency"""
    crypto = market.ticker(currency)[0]
    crypto_price = float(crypto.get('price_usd'))
    await bot.say(currency + " " + "price: \n" + format(crypto_price,",f"))

@bot.command()
async def satoshis(currency):
    """pulls price in satoshis for a currency"""
    crypto = market.ticker(currency)[0]
    crypto_price = crypto.get('price_btc')
    await bot.say(currency + " " + "Satoshi Price: \n" + crypto_price)
    

@bot.command()
async def volume(currency):
    """pulls 24hr volume for currency"""
    crypto = market.ticker(currency)[0]
    crypto_vol = float(crypto.get('24h_volume_usd'))
    await bot.say(currency + " "  "24 Hour Volume: \n" + format(crypto_vol,",f"))

@bot.command()
async def marketcap(currency):
    """pulls market cap for currency"""
    crypto = market.ticker(currency)[0]
    crypto_marketcap = float(crypto.get('market_cap_usd'))
    await bot.say(currency + " "  "Market Cap: \n" + format(crypto_marketcap,",f"))

@bot.command()
async def availablesupply(currency):
    """pulls current available supply for currency"""
    crypto = market.ticker(currency)[0]
    crypto_availsupply = float(crypto.get('available_supply'))
    await bot.say(currency + " "  "Current Available Supply: \n" + format(crypto_availsupply,",f"))

@bot.command()
async def totalsupply(currency):
    """pulls current total supply for currency"""
    crypto = market.ticker(currency)[0]
    crypto_totalsupply = float(crypto.get('total_supply'))
    await bot.say(currency + " "  "Current Total Supply: \n" + format(crypto_totalsupply,",f"))

@bot.command()
async def onehourpercent(currency):
    """pulls 1hr percent change for currency"""
    crypto = market.ticker(currency)[0]
    crypto_hourpercent = float(crypto.get('percent_change_1h'))
    await bot.say(currency + " " + "1 Hour Percent Change: \n" + "%.2f%%" % crypto_hourpercent)

@bot.command()
async def dailypercent(currency):
    """pulls 24hr percent change for currency"""
    crypto = market.ticker(currency)[0]
    crypto_dailypercent = float(crypto.get('percent_change_24h'))
    await bot.say(currency + " " + "24 Hour Percent Change: \n" + "%.2f%%" % crypto_dailypercent)

@bot.command()
async def cryptoratio(currency1,currency2):
    """calculates ratio of first crypto to second crypto"""
    crypto1 = market.ticker(currency1)[0]
    crypto1_price = float(crypto1.get('price_usd'))
    crypto2 = market.ticker(currency2)[0]
    crypto2_price = float(crypto2.get('price_usd'))
    ratio = crypto1_price/crypto2_price
    await bot.say(currency1 + " " + "to" + " " + currency2 + " " + "Ratio: \n" + "%.4f%%" % (100*ratio))

@bot.command()
async def totalmarketcap():
    """pulls total cryptocurrency market cap"""
    cap = market.stats()
    total_cap = float(cap.get('total_market_cap_usd'))
    await bot.say("Total Market Cap: " + format(total_cap, ",f"))

@bot.command()
async def totalvolume():
    """pulls total 24hr market volume"""
    cap = market.stats()
    total_volume = float(cap.get('total_24h_volume_usd'))
    await bot.say("Total Market Volume: " + format(total_volume, ",f"))

@bot.command()
async def bitcoinpercentage():
    """pulls bitcoin percentage of total market cap"""
    cap = market.stats()
    cap = market.stats()
    bitcoin_percentage = float(cap.get('bitcoin_percentage_of_market_cap'))
    await bot.say("Bitcoin Percentage of Market Cap: " + "%.4f%%" % bitcoin_percentage)




bot.run('')
