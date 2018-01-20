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
async def on_member_join(member):
    text = 'Hey, <@' + member.id + '> you thought you could escape me and my BSD in the Clutchfans Bitcoin thread huh?\n\nSIL'
    await bot.send_message(bot.get_channel('394681704041807872'), text)

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
    header = 'Bot has randomly chosen...'
    text = random.choice(choices)

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def magicball():
    '''Answer a question with a response'''

    responses = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Do not count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    ]

    random_number = random.randint(0, 19)
    if random_number >= 0 and random_number <= 9:
        embed = discord.Embed(color=0x60E87B)
    elif random_number >= 10 and random_number <= 14:
        embed = discord.Embed(color=0xECE357)
    else:
        embed = discord.Embed(color=0xD55050)

    header = 'Magic ball says...'
    text = responses[random_number]

    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command()
async def coinflip():
    '''Flips a coin'''

    random_number = random.randint(1, 1000)
    if random_number >= 500:
        text = 'It comes up tails'
    else:
        text = 'It comes up heads'

    header = 'Bot has flipped a coin...'

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rps(ctx):
    ''' Play a game of rps '''
    choice = ctx.message.content.split()[1].lower()
    if ctx.message.author.id == '177617966102216704':
        if choice == 'scissors':
            header = 'You win!'
            text = 'Bot has chosen paper'
        elif choice == 'paper':
            header = 'You win!'
            text = 'Bot has chosen rock'
        elif choice == 'rock':
            header = 'You win!'
            text = 'Bot has chosen scissors'
        else:
            header = 'You win!'
            text = 'Thinking out of the box, I like it!'
    else:
        if choice == 'scissors':
            header = 'You lose!'
            text = 'Bot has chosen rock'
        elif choice == 'paper':
            header = 'You lose!'
            text = 'Bot has chosen scissors'
        elif choice == 'rock':
            header = 'You lose!'
            text = 'Bot has chosen paper'
        else:
            header = 'You lose!'
            text = 'That is not a valid choice!'

    embed = discord.Embed()
    embed.add_field(name=header, value=text, inline=True)
    await bot.say(embed=embed)

##############################################################
# Coin market cap commands
##############################################################

@bot.command(pass_context=True)
async def summary(ctx):
    '''pulls price summary for currency'''
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

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

    text_0 = '```Summary for ' + name + '('+ symbol + ')\n'
    text_1 = 'Rank: ' + str(crypto_rank) + '\n\n'
    text_2 = 'Price in USD: $' + str(crypto_price) + '\n'
    text_3 = 'Price in BTC: ' + str(crypto_price_satoshi) + ' satoshi\n\n'
    text_4 = 'Market Cap: $' + str(crypto_marketcap) + '\n'
    text_5 = 'Volume 24h: $' + str(crypto_vol) + '\n'
    text_6 = 'Circulation: ' + str(crypto_availsupply) + ' ' + symbol + '\n\n'
    text_7 = 'Change 1h: ' + str(crypto_hourlypercent) + '%\n'
    text_8 = 'Change 24h: ' + str(crypto_dailypercent) + '%\n'
    text_9 = 'Change 7d: ' + str(crypto_weeklypercent) + '%```'

    text_message = text_0 + text_1 + text_2 + text_3 + text_4 + text_5 + text_6 + text_7 + text_8 + text_9
    await bot.delete_message(ctx.message)
    await bot.say(text_message)

@bot.command(pass_context=True)
async def price(ctx):
    """pulls price info for currency"""
    currency = ctx.message.content.split()[1]
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
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def satoshis(ctx):
    """pulls price in satoshis for a currency"""
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_price_satoshi = crypto.get('price_btc')
    if crypto_price_satoshi:
        crypto_price_satoshi = format(float(crypto_price_satoshi), ',f')

    header = 'Price of ' + name + '(' + symbol + ') in Satoshi'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_price_satoshi) + ' satoshi', inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def volume(ctx):
    """pulls 24hr volume for currency"""
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_vol = crypto.get('24h_volume_usd')
    if crypto_vol:
        crypto_vol = format(float(crypto_vol), ',.0f')

    header = 'Volume of ' + name + '(' + symbol + ') in last 24 hours in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(crypto_vol), inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def marketcap(ctx):
    """pulls market cap for currency"""
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_marketcap = crypto.get('market_cap_usd')
    if crypto_marketcap:
        crypto_marketcap = format(float(crypto_marketcap), ',.0f')

    header = 'Market cap of ' + name + '(' + symbol + ') in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(crypto_marketcap), inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def availablesupply(ctx):
    """pulls current available supply for currency"""
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_availsupply = crypto.get('available_supply')
    if crypto_availsupply:
        crypto_availsupply = format(float(crypto_availsupply), ',.0f')

    header = 'Current available supply of ' + name + '(' + symbol + ')'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_availsupply) + ' ' + symbol, inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def totalsupply(ctx):
    """pulls current total supply for currency"""
    currency = ctx.message.content.split()[1]
    crypto = market.ticker(convert_symbol_to_currency_id(currency))[0]
    symbol = crypto.get('symbol')
    name = crypto.get('name')

    crypto_totalsupply = crypto.get('total_supply')
    if crypto_totalsupply:
        crypto_totalsupply = format(float(crypto_totalsupply), ',.0f')

    header = 'Current total supply of ' + name + '(' + symbol + ')'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(crypto_totalsupply) + ' ' + symbol, inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def hourlypercent(ctx):
    """pulls 1hr percent change for currency"""
    currency = ctx.message.content.split()[1]
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
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def dailypercent(ctx):
    """pulls 24hr percent change for currency"""
    currency = ctx.message.content.split()[1]
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
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def weeklypercent(ctx):
    """pulls weekly percent change for currency"""
    currency = ctx.message.content.split()[1]
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
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def cryptoratio(ctx):
    """calculates ratio of first crypto to second crypto"""
    currency1 = ctx.message.content.split()[1]
    currency2 = ctx.message.content.split()[2]
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
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def totalmarketcap(ctx):
    """pulls total cryptocurrency market cap"""
    crypto = market.stats()

    total_cap = crypto.get('total_market_cap_usd')
    if total_cap:
        total_cap = format(float(total_cap), ',.0f')

    header = 'Total market cap in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(total_cap), inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def totalvolume(ctx):
    """pulls total 24hr market volume"""
    crypto = market.stats()

    total_volume = crypto.get('total_24h_volume_usd')
    if total_volume:
        total_volume = format(float(total_volume), ',.0f')

    header = 'Total market volume in last 24 hours in USD'

    embed = discord.Embed()
    embed.add_field(name=header, value='$' + str(total_volume), inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def bitcoinpercentage(ctx):
    """pulls bitcoin percentage of total market cap"""
    crypto = market.stats()

    bitcoin_percentage = crypto.get('bitcoin_percentage_of_market_cap')
    if bitcoin_percentage:
        bitcoin_percentage = format(float(bitcoin_percentage), ',.2f')

    header = 'Bitcoin (BTC) market share'

    embed = discord.Embed()
    embed.add_field(name=header, value=str(bitcoin_percentage) + '%', inline=True)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

bot.run('')
