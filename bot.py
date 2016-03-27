#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Example Bot to show some of the functionality of the library
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and the CLI-Loop is entered, where all text inputs are
inserted into the update queue for the bot to handle.

Usage:
Repeats messages with a delay.
Reply to last chat from the command line by typing "/reply <text>"
Type 'stop' on the command line to stop the bot.
"""
import telegram
from time import sleep
import logging

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0
bot = telegram.Bot(token='203410933:AAG6avZhedGbVsGZjgEa1x5u-DuNZ3BcjTE') 


# Define a few (command) handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """ Answer in Telegram """
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    """ Answer in Telegram """
    bot.sendMessage(update.message.chat_id, text='Help!')


def any_message(bot, update):
    """ Print to console """

    # Save last chat_id to use in reply handler
    global last_chat_id
    last_chat_id = update.message.chat_id

    logger.info("New message\nFrom: %s\nchat_id: %d\nText: %s" %
                (update.message.from_user,
                 update.message.chat_id,
                 update.message.text))


def unknown_command(bot, update):
    """ Answer in Telegram """
    bot.sendMessage(update.message.chat_id, text='Command not recognized!')

