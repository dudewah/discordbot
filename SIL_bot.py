# pylint: disable=C0103,C0111,C0301

import pickle
import random
import asyncio
import os
import json
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

    # Some kind of confirmation that quote was added.
    display_name = ''
    if message.author.display_name != message.author.name:
        display_name = '(' + message.author.display_name + ')'
    print('Quote by ' + message.author.name + display_name + ' added:')
    print(message.content[9:])
    print('------')

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
    roll = random.randint(1, 1000)
    if roll > 500:
        return '<:justinsun:400529586162630657>'
    return '<:justin_sunbae:400530503985397760>'

def update_symbol_mapping():

    ''' symbol to currency_id map generator '''

    c_list = market.ticker(limit=0)
    result = {}

    for values in c_list:
        result[values.get('symbol').lower()] = values.get('id').lower()

    with open('symbol_map.json', 'w') as outfile:
        json.dump(result, outfile)

def convert_symbol_to_currency_id(symbol):

    ''' convert symbol to currency_id '''

    if not os.path.exists('symbol_map.json'):
        update_symbol_mapping()

    with open('symbol_map.json', 'r') as readfile:
        symbol_map = json.load(readfile)

    conversion = symbol_map.get(symbol.lower(), '')

    if conversion == '':
        return symbol
    return conversion

##############################################################
# General bot commands
##############################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=' with my BSD crew'))

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("addquote"):
            await addquote(message)
        elif 'SIL' in message.content:
            await bot.send_message(message.channel, getquote())
        elif 'justin sun' in message.content.lower():
            await bot.send_message(message.channel, randomsun())
        elif "moon" in message.content.lower():
            await bot.send_message(message.channel, ":full_moon:")
        elif "whale" in message.content.lower():
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
    """raises the 1st no. to the exponent of the 2nd no."""
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
async def summary(currency: str):
    '''pulls price summary for currency'''
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    crypto_price = float(crypto.get('price_usd'))
    crypto_price_satoshi = float(crypto.get('price_btc'))
    crypto_vol = float(crypto.get('24h_volume_usd'))
    crypto_rank = int(crypto.get('rank'))
    crypto_availsupply = float(crypto.get('available_supply'))
    crypto_marketcap = float(crypto.get('market_cap_usd'))
    crypto_hourlypercent = float(crypto.get('percent_change_1h'))
    crypto_dailypercent = float(crypto.get('percent_change_24h'))
    crypto_weeklypercent = float(crypto.get('percent_change_7d'))
    url = 'http://coinmarketcap.com/currencies/' + crypto.get('id')
    name = crypto.get('name')
    embed = discord.Embed(title='Summary for ' + name + '('+ symbol + ')', color=0x78C0D2, url=url)
    embed.add_field(name='Price in USD', value="$" + str(format(crypto_price, ",f")), inline=True)
    embed.add_field(name='Price in satoshis', value=str(format(crypto_price_satoshi, ",f")) + ' satoshis', inline=True)
    embed.add_field(name='Rank', value=str(crypto_rank), inline=True)
    embed.add_field(name='Market cap', value='$' + str(format(crypto_marketcap, ',.2f')), inline=True)
    embed.add_field(name='24h volume', value='$' + str(format(crypto_vol, ',.2f')), inline=True)
    embed.add_field(name='Circulation', value=str(format(crypto_availsupply, ",.2f")) + ' ' + symbol, inline=True)
    embed.add_field(name='Change 1h', value=str(format(crypto_hourlypercent, ',.2f')) + '%', inline=True)
    embed.add_field(name='Change 24h', value=str(format(crypto_dailypercent, ',.2f')) + '%', inline=True)
    embed.add_field(name='Change 7d', value=str(format(crypto_weeklypercent, ',.2f')) + '%', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def price(currency: str):
    """pulls price info for currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_price = float(crypto.get('price_usd'))
    header = 'Price of ' + name + '(' + symbol + ') in USD'
    text = "$" + str(format(crypto_price, ",f"))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def satoshis(currency: str):
    """pulls price in satoshis for a currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_price = float(crypto.get('price_btc'))
    header = 'Price of ' + name + '(' + symbol + ') in satoshis'
    text = str(format(crypto_price, ",f")) + ' satoshis'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def volume(currency: str):
    """pulls 24hr volume for currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_vol = float(crypto.get('24h_volume_usd'))
    header = 'Volume of ' + name + '(' + symbol + ') in last 24 hours in USD'
    text = '$' + str(format(crypto_vol, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def marketcap(currency: str):
    """pulls market cap for currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_marketcap = float(crypto.get('market_cap_usd'))
    header = 'Market cap of ' + name + '(' + symbol + ') in USD'
    text = '$' + str(format(crypto_marketcap, ',.2f'))
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def availablesupply(currency: str):
    """pulls current available supply for currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_availsupply = float(crypto.get('available_supply'))
    header = 'Current available supply of ' + name + '(' + symbol + ')'
    text = str(format(crypto_availsupply, ',.2f')) + ' ' + symbol
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalsupply(currency: str):
    """pulls current total supply for currency"""
    embed = discord.Embed()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_totalsupply = float(crypto.get('total_supply'))
    header = 'Current total supply of ' + name + '(' + symbol + ')'
    text = str(format(crypto_totalsupply, ',.2f')) + ' ' + symbol
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def hourlypercent(currency: str):
    """pulls 1hr percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_hourlypercent = float(crypto.get('percent_change_1h'))
    header = 'Percent price change in last hour for ' + name + '(' + symbol + ')'
    text = str(format(crypto_hourlypercent, ',.2f')) + '%'
    if crypto_hourlypercent >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def dailypercent(currency: str):
    """pulls 24hr percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_dailypercent = float(crypto.get('percent_change_24h'))
    header = 'Percent price change in last 24 hours for ' + name + '(' + symbol + ')'
    text = str(format(crypto_dailypercent, ',.2f')) + '%'
    if crypto_dailypercent >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def weeklypercent(currency: str):
    """pulls weekly percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    crypto_weeklypercent = float(crypto.get('percent_change_7d'))
    header = 'Percent price change in last 7 days for ' + name + '(' + symbol + ')'
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
    name1 = crypto1.get('name')
    crypto1_price = float(crypto1.get('price_usd'))
    crypto2 = market.ticker(currency2)[0]
    symbol2 = crypto2.get('symbol')
    name2 = crypto2.get('name')
    crypto2_price = float(crypto2.get('price_usd'))
    ratio = crypto1_price/crypto2_price * 100
    header = 'Ratio of ' + name1 + '(' + symbol1 + ') to ' + name2 + '(' + symbol2 + ')'
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
    header = 'Bitcoin (BTC) market share'
    text = str(format(bitcoin_percentage, ',.2f')) + '%'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def currencypercentage(currency: str):
    '''pulls currency's percentage of total market cap'''
    embed = discord.Embed()
    cap = market.stats()
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    currency_percentage = float(float(crypto.get('market_cap_usd'))/cap.get('total_market_cap_usd') * 100)
    header = name + '(' + symbol + ') market share'
    text = str(format(currency_percentage, ',.2f')) + '%'
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

bot.run('')
