import telegram
bot = telegram.Bot(token='203410933:AAG6avZhedGbVsGZjgEa1x5u-DuNZ3BcjTE')
# Generate a bot ID here: https://core.telegram.org/bots#botfather

#Request latest messages
print bot.getMe()

updates = bot.getUpdates()
print [u.message.text for u in updates]

chat_id = bot.getUpdates()[-1].message.chat_id

bot.sendMessage(chat_id=chat_id, text="ALERT! Wifi perimeter violation Mac addrs.")

