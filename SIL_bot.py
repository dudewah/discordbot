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
# Bot initialization #
##############################################################

bot = commands.Bot(command_prefix="!")
market = coinmarketcap.Market()

##############################################################
# Helper functions #
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
    header = str(left) + ' * ' + str(right)
    text = str(left * right)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def add(left: float, right: float):
    """Adds two numbers together."""
    header = str(left) + ' + ' + str(right)
    text = str(left + right)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def subtract(left: float, right: float):
    """Subtract two numbers."""
    header = str(left) + ' - ' + str(right)
    text = str(left - right)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def exponent(number: float, power: float):
    """raises the 1st no. to the exponent of the 2nd no."""
    header = str(number) + ' to the power of ' + str(power)
    text = str(number ** power)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def divide(left: float, right: float):
    """divides first number by second number"""
    header = str(left) + ' / ' + str(right)
    text = str(left / right)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def choose(*choices: str):
    """randomly chooses between multiple options"""
    header = 'Bot has randomly chose...'
    text = random.choice(choices)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

##############################################################
# Coin market cap commands
##############################################################

@bot.command()
async def summary(currency: str):
    '''pulls price summary for currency'''
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')
    url = 'http://coinmarketcap.com/currencies/' + crypto.get('id')

    crypto_price = crypto.get('price_usd')
    if crypto_price and float(crypto_price) >= 1.0:
        crypto_price = format(float(crypto_price), ',.2f')
    elif crypto_price and float(crypto_price) < 1.0:
        crypto_price = format(float(crypto_price), ',f')

    crypto_price_satoshi = crypto.get('price_btc')
    if crypto_price_satoshi:
        crypto_price_satoshi = format(float(crypto_price_satoshi), ',f')

    crypto_rank = crypto.get('rank')

    crypto_availsupply = crypto.get('available_supply')
    if crypto_availsupply:
        crypto_availsupply = format(float(crypto_availsupply), ',.0f')

    crypto_vol = crypto.get('24h_volume_usd')
    if crypto_vol:
        crypto_vol = format(float(crypto_vol), ',.0f')

    crypto_marketcap = crypto.get('market_cap_usd')
    if crypto_marketcap:
        crypto_marketcap = format(float(crypto_marketcap), ',.0f')

    crypto_hourlypercent = crypto.get('percent_change_1h')
    if crypto_hourlypercent:
        crypto_hourlypercent = format(float(crypto_hourlypercent), ',.2f')

    crypto_dailypercent = crypto.get('percent_change_24h')
    if crypto_dailypercent:
        crypto_dailypercent = format(float(crypto_dailypercent), ',.2f')

    crypto_weeklypercent = crypto.get('percent_change_7d')
    if crypto_weeklypercent:
        crypto_weeklypercent = format(float(crypto_weeklypercent), ',.2f')

    embed = discord.Embed(title='Summary for ' + name + '('+ symbol + ')', color=0x78C0D2, url=url)
    embed.add_field(name='Price in USD', value="$" + str(crypto_price), inline=True)
    embed.add_field(name='Price in Satoshi', value=str(crypto_price_satoshi) + ' satoshi', inline=True)
    embed.add_field(name='Rank', value=str(crypto_rank), inline=True)
    embed.add_field(name='Market Cap', value='$' + str(crypto_marketcap), inline=True)
    embed.add_field(name='Volume 24h', value='$' + str(crypto_vol), inline=True)
    embed.add_field(name='Circulation', value=str(crypto_availsupply) + ' ' + symbol, inline=True)
    embed.add_field(name='Change 1h', value=str(crypto_hourlypercent) + '%', inline=True)
    embed.add_field(name='Change 24h', value=str(crypto_dailypercent) + '%', inline=True)
    embed.add_field(name='Change 7d', value=str(crypto_weeklypercent) + '%', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def price(currency: str):
    """pulls price info for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_price = crypto.get('price_usd')
    if crypto_price and float(crypto_price) >= 1.0:
        crypto_price = format(float(crypto_price), ',.2f')
    elif crypto_price and float(crypto_price) < 1.0:
        crypto_price = format(float(crypto_price), ',f')

    header = 'Price of ' + name + '(' + symbol + ') in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(crypto_price), inline=True)
    await bot.say(embed=embed)

@bot.command()
async def satoshis(currency: str):
    """pulls price in satoshis for a currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_price_satoshi = crypto.get('price_btc')
    if crypto_price_satoshi:
        crypto_price_satoshi = format(float(crypto_price_satoshi), ',f')

    header = 'Price of ' + name + '(' + symbol + ') in Satoshi'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_price_satoshi) + ' satoshi', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def volume(currency: str):
    """pulls 24hr volume for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_vol = crypto.get('24h_volume_usd')
    if crypto_vol:
        crypto_vol = format(float(crypto_vol), ',.0f')

    header = 'Volume of ' + name + '(' + symbol + ') in last 24 hours in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(crypto_vol), inline=True)
    await bot.say(embed=embed)

@bot.command()
async def marketcap(currency: str):
    """pulls market cap for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_marketcap = crypto.get('market_cap_usd')
    if crypto_marketcap:
        crypto_marketcap = format(float(crypto_marketcap), ',.0f')

    header = 'Market cap of ' + name + '(' + symbol + ') in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(crypto_marketcap), inline=True)
    await bot.say(embed=embed)

@bot.command()
async def availablesupply(currency: str):
    """pulls current available supply for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_availsupply = crypto.get('available_supply')
    if crypto_availsupply:
        crypto_availsupply = format(float(crypto_availsupply), ',.0f')

    header = 'Current available supply of ' + name + '(' + symbol + ')'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_availsupply) + ' ' + symbol, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalsupply(currency: str):
    """pulls current total supply for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_totalsupply = crypto.get('total_supply')
    if crypto_totalsupply:
        crypto_totalsupply = format(float(crypto_totalsupply), ',.0f')

    header = 'Current total supply of ' + name + '(' + symbol + ')'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_totalsupply) + ' ' + symbol, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def hourlypercent(currency: str):
    """pulls 1hr percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_hourlypercent = crypto.get('percent_change_1h')
    if crypto_hourlypercent:
        crypto_hourlypercent = format(float(crypto_hourlypercent), ',.2f')

    header = 'Percent price change in last hour for ' + name + '(' + symbol + ')'

    if float(crypto_hourlypercent) >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=str(crypto_hourlypercent) + '%', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def dailypercent(currency: str):
    """pulls 24hr percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_dailypercent = crypto.get('percent_change_24h')
    if crypto_dailypercent:
        crypto_dailypercent = format(float(crypto_dailypercent), ',.2f')

    header = 'Percent price change in last 24 hours for ' + name + '(' + symbol + ')'

    if float(crypto_dailypercent) >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=str(crypto_dailypercent) + '%', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def weeklypercent(currency: str):
    """pulls weekly percent change for currency"""
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_weeklypercent = crypto.get('percent_change_7d')
    if crypto_weeklypercent:
        crypto_weeklypercent = format(float(crypto_weeklypercent), ',.2f')

    header = 'Percent price change in last 7 days for ' + name + '(' + symbol + ')'

    if float(crypto_weeklypercent) >= 0:
        embed = discord.Embed(color=0x60E87B)
    else:
        embed = discord.Embed(color=0xD55050)
    embed.add_field(name=header, value=str(crypto_weeklypercent) + '%', inline=True)
    await bot.say(embed=embed)

@bot.command()
async def cryptoratio(currency1: str, currency2: str):
    """calculates ratio of first crypto to second crypto"""
    crypto1 = market.ticker(convert_symbol_to_currency_id(currency1))[0]
    symbol1 = crypto1.get('symbol')
    name1 = crypto1.get('name')
    crypto1_price = crypto1.get('price_usd')

    crypto2 = market.ticker(convert_symbol_to_currency_id(currency2))[0]
    symbol2 = crypto2.get('symbol')
    name2 = crypto2.get('name')
    crypto2_price = crypto2.get('price_usd')

    header = 'Ratio of ' + name1 + '(' + symbol1 + ') to ' + name2 + '(' + symbol2 + ')'
    if crypto1_price and crypto2_price:
        ratio = format(float(crypto1_price)/float(crypto2_price) * 100.0, ',.2f') + '%'
    else:
        ratio = 'N/A.'

    embed = discord.Embed()
    embed.add_field(name=header, value=ratio, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalmarketcap():
    """pulls total cryptocurrency market cap"""
    crypto = market.stats()

    total_cap = crypto.get('total_market_cap_usd')
    if total_cap:
        total_cap = format(float(total_cap), ',.0f')

    header = 'Total market cap in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(total_cap), inline=True)
    await bot.say(embed=embed)

@bot.command()
async def totalvolume():
    """pulls total 24hr market volume"""
    crypto = market.stats()

    total_volume = crypto.get('total_24h_volume_usd')
    if total_volume:
        total_volume = format(float(total_volume), ',.0f')

    header = 'Total market volume in last 24 hours in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(total_volume), inline=True)
    await bot.say(embed=embed)

@bot.command()
async def bitcoinpercentage():
    """pulls bitcoin percentage of total market cap"""
    crypto = market.stats()

    bitcoin_percentage = crypto.get('bitcoin_percentage_of_market_cap')
    if bitcoin_percentage:
        bitcoin_percentage = format(float(bitcoin_percentage), ',.2f')

    header = 'Bitcoin (BTC) market share'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(bitcoin_percentage) + '%', inline=True)
    await bot.say(embed=embed)

bot.run('')
