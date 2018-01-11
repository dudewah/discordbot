# pylint: disable=C0103,C0111,C0301

import pickle
import random
import asyncio
import os
import coinmarketcap
import discord
from discord.ext import commands

##############################################################
# Bot initialization
##############################################################

bot = commands.Bot(command_prefix="!")
market = coinmarketcap.Market()

##############################################################
# Helper functions
##############################################################

async def addquote(message):
    '''Add quote to the SIL flatfile'''
    if not os.path.isfile("SILquote_file.txt"):
        SILquote_list = []
    else:
        with open("SILquote_file.txt", "rb") as readfile:
            SILquote_list = pickle.load(readfile)
    SILquote_list.append(message.content[9:])
    with open("SILquote_file.txt", "wb") as writefile:
        pickle.dump(SILquote_list, writefile)

def getquote():
    '''Get quote from SIL flatfile'''
    if not os.path.isfile("SILquote_file.txt"):
        SILquote_list = []
    else:
        with open("SILquote_file.txt", "rb") as readfile:
            SILquote_list = pickle.load(readfile)
    return random.choice(SILquote_list)

def randomsun():
    '''get a random justin sun emoji'''
    roll = random.randint(0, 1)
    if roll == 1:
        return ':justin_sun:'
    return ':justin_sunbae:'

##############################################################
# General bot commands
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
            await addquote(message)
        elif 'SIL' in message.content:
            await bot.send_message(message.channel, getquote())
        elif 'justin sun' in message.content.lower():
            await bot.send_message(message.channel, randomsun())
        elif message.content.lower().startswith("moon"):
            await bot.send_message(message.channel, ":full_moon:")
        elif message.content.lower().startswith("whale"):
            await bot.send_message(message.channel, ":whale:")
    await bot.process_commands(message)

@bot.command()
async def multiply(left: float, right: float):
    """multiplies two numbers together"""
    embed = discord.Embed()
    header = str(left) + ' * ' + str(right)
    text = str(left * right)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def add(left: float, right: float):
    """Adds two numbers together."""
    embed = discord.Embed()
    header = str(left) + ' + ' + str(right)
    text = str(left + right)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def exponent(number: float, power: float):
    """raises the first number to the exponent of the second number"""
    embed = discord.Embed()
    header = str(number) + ' to the power of ' + str(power)
    text = str(number ** power)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def divide(left: float, right: float):
    """divides first number by second number"""
    embed = discord.Embed()
    header = str(left) + ' / ' + str(right)
    text = str(left / right)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def choose(*choices: str):
    """randomly chooses between multiple options"""
    embed = discord.Embed()
    text = random.choice(choices)
    embed.add_field(name='Bot has randomly chosen...', value=text, inline=True)
    await bot.say(embed=embed)

##############################################################
# Coin market cap commands
##############################################################

@bot.command()
async def price(currency: str):
    """pulls price info for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_price = float(crypto.get('price_usd'))
    header = 'Price of ' + symbol + ' in USD'
    text = "$" + str(format(crypto_price, ",f"))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def satoshis(currency: str):
    """pulls price in satoshis for a currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_price = float(crypto.get('price_btc'))
    header = 'Price of ' + symbol + ' in satoshis'
    text = str(format(crypto_price, ",f")) + ' satoshis'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def volume(currency: str):
    """pulls 24hr volume for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_vol = float(crypto.get('24h_volume_usd'))
    header = 'Volume of ' + symbol + ' in last 24 hours in USD'
    text = '$' + str(format(crypto_vol, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def marketcap(currency: str):
    """pulls market cap for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_marketcap = float(crypto.get('market_cap_usd'))
    header = 'Market cap of ' + symbol + ' in USD'
    text = '$' + str(format(crypto_marketcap, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def availablesupply(currency: str):
    """pulls current available supply for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_availsupply = float(crypto.get('available_supply'))
    header = 'Current available supply of ' + symbol
    text = str(format(crypto_availsupply, ',.2f')) + ' ' + symbol
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalsupply(currency: str):
    """pulls current total supply for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_totalsupply = float(crypto.get('total_supply'))
    header = 'Current total supply of ' + symbol
    text = str(format(crypto_totalsupply, ',.2f')) + ' ' + symbol
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def onehourpercent(currency: str):
    """pulls 1hr percent change for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_hourpercent = float(crypto.get('percent_change_1h'))
    header = 'Percent price change in last hour for ' + symbol
    text = str(format(crypto_hourpercent, ',.2f')) + '%'
    if crypto_hourpercent >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def dailypercent(currency: str):
    """pulls 24hr percent change for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_dailypercent = float(crypto.get('percent_change_24h'))
    header = 'Percent price change in last 24 hours for ' + symbol
    text = str(format(crypto_dailypercent, ',.2f')) + '%'
    if crypto_dailypercent >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def weeklypercent(currency: str):
    """pulls 24hr percent change for currency"""
    embed = discord.Embed()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    crypto_weeklypercent = float(crypto.get('percent_change_7d'))
    header = 'Percent price change in last 7 days for ' + symbol
    text = str(format(crypto_weeklypercent, ',.2f')) + '%'
    if crypto_weeklypercent >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def cryptoratio(currency1: str, currency2: str):
    """calculates ratio of first crypto to second crypto"""
    embed = discord.Embed()
    crypto1 = market.ticker(currency1)[0]
    symbol1 = crypto1.get('symbol')
    crypto1_price = float(crypto1.get('price_usd'))
    crypto2 = market.ticker(currency2)[0]
    symbol2 = crypto2.get('symbol')
    crypto2_price = float(crypto2.get('price_usd'))
    ratio = crypto1_price/crypto2_price * 100
    header = 'Ratio of ' + symbol1 + ' to ' + symbol2
    text = str(format(ratio, ',.4f')) + '%'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalmarketcap():
    """pulls total cryptocurrency market cap"""
    embed = discord.Embed()
    cap = market.stats()
    total_cap = float(cap.get('total_market_cap_usd'))
    header = 'Total market cap in USD'
    text = '$' + str(format(total_cap, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalvolume():
    """pulls total 24hr market volume"""
    embed = discord.Embed()
    cap = market.stats()
    total_volume = float(cap.get('total_24h_volume_usd'))
    header = 'Total market volume in last 24 hours in USD'
    text = '$' + str(format(total_volume, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def bitcoinpercentage():
    """pulls bitcoin percentage of total market cap"""
    embed = discord.Embed()
    cap = market.stats()
    bitcoin_percentage = float(cap.get('bitcoin_percentage_of_market_cap'))
    header = 'BTC market share'
    text = str(format(bitcoin_percentage, ',.2f')) + '%'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def currencypercentage(currency: str):
    '''pulls currency's percentage of total market cap'''
    embed = discord.Embed()
    cap = market.stats()
    crypto = market.ticker(currency)[0]
    symbol = crypto.get('symbol')
    currency_percentage = float(float(crypto.get('market_cap_usd'))/cap.get('total_market_cap_usd') * 100)
    header = symbol + ' market share'
    text = str(format(currency_percentage, ',.2f')) + '%'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

bot.run('')
