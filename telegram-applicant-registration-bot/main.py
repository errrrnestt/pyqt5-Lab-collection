# ───■ INITIALIZATION & CONFIGURATION ■───
import telebot
from telebot import types

bot = telebot.TeleBot('')

# ┌────────────────────────────────────────────────────────┐
# │ GLOBAL USER DATA STORAGE                               │
# └────────────────────────────────────────────────────────┘
name = ""
surname = ""
nomer = ""
group = ""
spec = ""
age = 0

# ───■ MAIN MESSAGE HANDLER ■───
@bot.message_handler(content_types=['text'])
def start(message):
    # Check confirmation responses
    if message.text == 'Yes':
        bot.send_message(message.chat.id, "Ok! I have saved your data!")
    elif message.text == 'No':
        bot.send_message(message.chat.id, "Starting over! Please type /reg")
    
    # Check registration command
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Hello! I am a bot that will register you for your practice retake! What is your name?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Type /reg to find out what to do next!")

# ───■ STAGE 1: PERSONAL INFO INPUT ■───
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "What is your last name?")
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "How old are you?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    s = message.text    
    if s.isdigit():  
        age = int(message.text)    
        bot.send_message(message.from_user.id, "What is your phone number?")
        bot.register_next_step_handler(message, get_nomer)
    else:
        # Validation fallback if input is not a number
        bot.send_message(message.from_user.id, "Age must be a number!!!")
        bot.register_next_step_handler(message, get_age)

# ───■ STAGE 2: MAJOR SELECTION (INLINE KEYBOARD) ■───
def get_nomer(message):
    global nomer
    nomer = message.text
    
    keyboard = types.InlineKeyboardMarkup()
    key_spec1 = types.InlineKeyboardButton(text='051 Economics', callback_data='spec1')
    keyboard.add(key_spec1)
    key_spec2 = types.InlineKeyboardButton(text='071 Accounting and Taxation', callback_data='spec2')
    keyboard.add(key_spec2)
    key_spec3 = types.InlineKeyboardButton(text='123 Computer Engineering', callback_data='spec3')
    keyboard.add(key_spec3)
    key_spec4 = types.InlineKeyboardButton(text='133 Industrial Machinery Engineering', callback_data='spec4')
    keyboard.add(key_spec4)
    
    bot.send_message(message.from_user.id, text="Select your major:", reply_markup=keyboard)

# ───■ STAGE 3: CALLBACK PROCESSING & CONFIRMATION ■───
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global spec
    # Constructing the final summary string
    q = f"You are {age} years old. Your name is {surname} {name}. Phone: {nomer}. Major: "
        
    if call.data == "spec1":
        spec = "Economics"
    elif call.data == "spec2":
        spec = "Accounting and Taxation"
    elif call.data == "spec3":
        spec = "Computer Engineering"
    elif call.data == "spec4":
        spec = "Industrial Machinery Engineering"

    # Confirmation keyboard setup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Yes')
    itembtn2 = types.KeyboardButton('No')
    markup.add(itembtn1, itembtn2)
    
    bot.send_message(call.message.chat.id, text=q + spec, reply_markup=markup)

# ───■ APPLICATION POLLING LOOP ■───
bot.polling(none_stop=True, interval=0)