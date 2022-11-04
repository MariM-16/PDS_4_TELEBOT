import telebot
from Group import Group
from telebot.types import ForceReply, ReplyKeyboardMarkup

API_KEY = "5782287054:AAH2SeAqkIe7DxZQdoUv_uvMZLoli8bxdOE"
bot = telebot.TeleBot(API_KEY)

# List of Groups dataclass
users = {}



@bot.message_handler(commands=["users"])
def getUsers(message):
    if message.chat.id not in users.keys():
        bot.reply_to(message, "No Users registered.")
    else:
        bot.reply_to(message, users[message.chat.id].members)


@bot.message_handler(commands=['number'])
def number(message):
    if users[message.chat.id].game_state:
        return
    else:
        users[message.chat.id].game_state = True
        markup = ForceReply()
        msg = bot.reply_to(message, 
            "Ingrese el numero máximo y la cantidad de intentos separados por un espacio.", reply_markup=markup)
        bot.register_next_step_handler(msg, askNumberSettings)


def askNumberSettings(message):
    global maxNum, tries
    
    list = message.text.split()
    maxNum = list[0]
    tries = list[1]

    

@bot.message_handler(commands=["end"])
def endGame(message):
    if game_state:
        game_state = False
        bot.reply_to(message, "Game ended.")


# Listens to standard texts
@bot.message_handler(content_types=["text"])
def newUser(message):
    # Add the user to the list of players
    if message.chat.id not in users.keys():
        users[message.chat.id] = Group()
        users[message.chat.id].members.append([message.from_user.id])
        # Debug print
        bot.reply_to(message, f"User {message.from_user.id} added to {users[message.chat.id]}.")

    elif message.from_user.id not in users[message.chat.id]:
        users[message.chat.id].append(message.from_user.id)
        # Debug print
        bot.reply_to(message, f"User {message.from_user.id} added to {message.chat.id}.")



# Main loop
if __name__ == "__main__":
    print("Starting...")
    # Info for telegram app on each command
    bot.set_my_commands([
        telebot.types.BotCommand("users", "Get all the group users."),
        telebot.types.BotCommand("number", "Guess a number."),
        telebot.types.BotCommand("end", "End the current game."),
    ])
    # Starts listening
    bot.infinity_polling()