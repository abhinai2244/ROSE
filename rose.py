import telebot
from datetime import datetime

# Replace 'YOUR_TOKEN' with your actual bot token
BOT_TOKEN = '7898648025:AAEznfaTQFrA8rhhgiESZSLmGoOu3PkodKQ'
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize a blacklist
blacklist = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! How can I assist you today?")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ban [user_id] - Ban a user\n"
        "/unban [user_id] - Unban a user\n"
        "/kick [user_id] - Kick a user\n"
        "/blacklist [word] - Add a word to the blacklist\n"
        "/show_blacklist - Show all blacklisted words\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
        bot.reply_to(message, f'User {user_id} has been banned.')
    else:
        bot.reply_to(message, "Please reply to a user's message to ban them.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(chat_id=message.chat.id, user_id=user_id)
        bot.reply_to(message, f'User {user_id} has been unbanned.')
    else:
        bot.reply_to(message, "Please reply to a user's message to unban them.")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
        bot.reply_to(message, f'User {user_id} has been kicked from the group.')
    else:
        bot.reply_to(message, "Please reply to a user's message to kick them.")

@bot.message_handler(commands=['blacklist'])
def blacklist_word(message):
    if len(message.text.split()) > 1:
        word = message.text.split()[1]
        blacklist.add(word.lower())
        bot.reply_to(message, f'Added "{word}" to the blacklist.')
    else:
        bot.reply_to(message, "Please provide a word to blacklist.")

@bot.message_handler(commands=['show_blacklist'])
def show_blacklist(message):
    if blacklist:
        bot.reply_to(message, "Blacklisted words: " + ", ".join(blacklist))
    else:
        bot.reply_to(message, "The blacklist is empty.")

@bot.message_handler(func=lambda message: True)
def filter_blacklisted_words(message):
    for word in blacklist:
        if word in message.text.lower():
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            break

print('Bot is running...')
bot.infinity_polling()
