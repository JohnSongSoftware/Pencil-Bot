#!/usr/bin/python
# This is a Text based discord Bot that will interface with users via commands
# given from the text channels in discord.

# ################### Copyright (c) 2016 RamCommunity #################
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO LIST
#########################################I
# google search
# jukebox
#########################################
import discord
from discord.ext import commands
import random
import logging
import json
import os
import sys
import asyncio

logging.basicConfig(level=logging.INFO)

# Local Constants
options_location = 'options/'
prefix = "!"
# AUTO_MESSAGE_DELAY is in seconds
SETTINGS = {}
BOT_COMMANDS = {};
AUTO_MESSAGES = ['With Kevin`s Mom', 'Toradota!', "With Josh's Heart"]

# Used for specific bot functions
QUEUE_ID = {}
# Used for specific bot functions

description = '''Pencil bot, the only bot that'll write your future.'''
bot = commands.Bot(command_prefix=prefix, description=description)
token = 'MjQ1NTkxMTUxNjA2NzU5NDI1.CwO-Qw.WNXDIYw5XZ6QUd6jJ_z-ZfTapy4';

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description="Exit command for closing the bot")
@asyncio.coroutine
def quit():
    """Exit command for closing the bot."""
    save()
    yield from bot.say("``Bot is now exiting.``")
    sys.exit(0)


@bot.command(description='Rolls a dice in NdN formats')
@asyncio.coroutine
def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        yield from bot.say('``Format has to be in NdN!``')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    yield from bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
@asyncio.coroutine
def choose(*choices : str):
    """Chooses between multiple choices."""
    yield from bot.say("I have chosen: ``" + "**" + random.choice(choices) + "**")


@bot.command(description='Prints external phrases')
@asyncio.coroutine
def externalCommands(content='repeating...'):
    """Clears all the custom commands."""
    total = ''
    for command in BOT_COMMANDS:
        total += ' **!' + command +' **'
    total += ' **!' + "addQueue" +' **'
    total += ' **!' + "leaveQueue" +' **'
    total += ' **!' + "statusQueue" +' **'
    yield from bot.say("``The following external commands are :``" + total)


@bot.command(description='Enter the huequeilibrium.............', pass_context=True)
@asyncio.coroutine
def blue(ctx):
    """Enter the huequilbrium."""
    yield from bot.say("``ENTER THE HUEQUEILIBRIUM :``" + "http://www.colorhexa.com/" + rgb2hex(0, 0, random.randint(0, 255)) + " " + ctx.message.author.mention)


@bot.command(description='Joins the available queue', pass_context=True)
@asyncio.coroutine
def joinQueue(ctx):
    message = ctx.message
    if ctx.message.channel.name == "quickplay":
        if message.author.id in QUEUE_ID:
            yield from bot.send_message(message.channel, "``User `` **" + message.author.mention + " **``  has already been enrolled in the queue.``")
        else:
            QUEUE_ID[message.author.id] = message.author.mention
            yield from bot.send_message(message.channel, "``User `` **" + message.author.mention + " **``  has successfully been enrolled in the queue.``")

        if len(QUEUE_ID) == 6:
            total = ""
            for value in QUEUE_ID.values():
                total += (str(value)) + " "

            yield from bot.say("``The Queue is now full and starting:``" + total)
            QUEUE_ID.clear()


@bot.command(description='Leaves the aviliable queue', pass_context=True)
@asyncio.coroutine
def leaveQueue(ctx):
    message = ctx.message
    if ctx.message.channel.name == "quickplay":
        if message.author.id in QUEUE_ID:
            del QUEUE_ID[message.author.id]
            yield from bot.send_message(message.channel, "``User `` **" + message.author.mention + " **``  has successfully been removed.``")
        else:
            yield from bot.send_message(message.channel, "``User `` **" + message.author.mention + " **``  is not in the queue.``")


@bot.command(description='Leaves the aviliable queue', pass_context=True)
@asyncio.coroutine
def statusQueue(ctx):
    message = ctx.message
    if ctx.message.channel.name == "quickplay":
        total = ""
        for value in QUEUE_ID.values():
            total += (str(value)) + " "
        yield from  bot.send_message(message.channel, "``Currently `` **" + total + " **`` are in the queue.``")
        '''yield from  bot.send_message(message.channel, "``There are currently `` **" + (str(len(QUEUE_ID))) + " **`` people in the queue.``")'''


@bot.event
@asyncio.coroutine
def on_message(message):
    """Main processing loop for external commands"""
    author = message.author

    # If it's a bot talking
    if author.bot:
        return

    # Processes raw messages first
    yield from bot.process_commands(message)

    if message.content.startswith(prefix):
        partitions = message.content.split(" ")
        token = partitions[0][1:]
        # Adding new commands
        if message.content.startswith('!addCommand'):
            if(len(partitions) > 2):
                total = len(partitions[1]) + 12
                BOT_COMMANDS[partitions[1]] = message.content[total:]
                yield from bot.send_message(message.channel, "``Command `` **" + partitions[1] + " **``  has successfully been added.``")
            else:
                yield from bot.send_message(message.channel, "Cannot add the above command.")
        # Deleteing added commands
        elif message.content.startswith('!deleteCommand'):
            partitions = message.content.split(" ")
            if(len(partitions) > 1):
                del BOT_COMMANDS[partitions[1]]
                yield from bot.send_message(message.channel, "``Command `` **" + partitions[1] + " **`` has successfully been deleted.``")
            else:
                yield from bot.send_message(message.channel, "``The command ``** " + partitions[1] + " **``   cannot be found.``")
        elif token in BOT_COMMANDS:
            # Says the message allocated to the command title
            yield from bot.send_message(message.channel, BOT_COMMANDS[token])
        #
        #else:
        #    yield from bot.send_message(message.channel, "``The command `` **" + token + " **`` cannot be found.``")


'''
@bot.command(description='Clears all the custom commands')
@asyncio.coroutine clear(content='repeating...'):
    """Clears all the custom commands."""
    yield from bot.say("*** ALL CUSTOM COMMANDS HAVE BEEN WIPED. ***")
    BOT_COMMANDS = {}
'''


@asyncio.coroutine
def auto_message():
    '''
    () -> ()
    Changes the play text periodly
    '''
    yield from bot.wait_until_ready()
    while not bot.is_closed:
        new_key = random.choice(AUTO_MESSAGES)
        yield from bot.change_presence(game=discord.Game(name=new_key))
        yield from asyncio.sleep(SETTINGS['AUTO_MESSAGE_DELAY'])


def rgb2hex(r,g,b):
    hex = "{:02x}{:02x}{:02x}".format(r,g,b)
    return hex
def hex2rgb(hexcode):
    rgb = tuple(map(ord,hexcode[1:].decode('hex')))
    return rgb


def save():
    '''
    () -> ()
    Saves the file paths needed for extras.
    '''
    with open(options_location + 'commands.json', 'w') as commands_file:
        json.dump(BOT_COMMANDS, commands_file)
    print("Saved some info!!")


def create():
    '''
    () -> ()
    Creates the file paths needed for extras.
    '''
    # Creates the command folder and files
    if not os.path.exists(options_location):
        os.makedirs(options_location)

    if not os.path.exists(options_location + 'commands.json'):
        with open(options_location + 'commands.json', 'w+') as commands_file:
            pass

    if not os.path.exists(options_location + 'settings.json'):
        with open(options_location + 'settings.json', 'w+') as settings_file:
            pass


def load():
    '''
    () -> ()
    Loads the file paths needed for extras.
    '''
    with open(options_location + 'commands.json', 'r') as commands_file:
        BOT_COMMANDS.update(json.load(commands_file))

    with open(options_location + 'settings.json', 'r') as settings_file:
        SETTINGS.update(json.load(settings_file))


def setup():
    '''
    () -> ()
    Setups the bot
    '''
    # Create the dirs
    create()

    # Load the dirs
    load()

    # Used for auto messaging
    if(SETTINGS['AUTO_MESSAGE']):
        try:
            bot.loop.create_task(auto_message())
        except:
            print('Something went wrong with auto messaging')
    # Running the bot now
    bot.run(token)

setup()
