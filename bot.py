import telebot
import random
from datetime import date
from persiantools.jdatetime import JalaliDate
from telebot.types import InlineQueryResultArticle
from gtts import gTTS
import qrcode



bot = telebot.TeleBot('2109255980:AAHz0JhNLqIXWwxX6TSIB14bhRgSpop6kAc')
random_number = random.randint(0,9)

#======================================= start ===========================================#

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Wellcome ' + message.from_user.first_name + ' press /help to see menu') 

@bot.message_handler(commands=['help' , 'menu'])
def send_welcome(message):
    bot.reply_to(message, '''  
        /game for start game 
        /age for calculate your age  
        /voice for make string to voice 
        /max for show max number of the list 
        /argmax for index of bigest number 
        /qrcode  
        /help 
    ''') 

#======================================== Game ============================================#

@bot.message_handler(commands=['game'])
def game(message):
    bot.reply_to(message, 'quess number (0,10)  or write newGame for new game : ')
    bot.register_next_step_handler_by_chat_id(message.chat.id,play_game) 

def play_game(message):
    if message.text == 'newGame':
         global random_number
         random_number = random.randint(0,9)
         bot.reply_to(message, 'quess number (0,10)  or write newGame for new game : ')
         bot.register_next_step_handler_by_chat_id(message.chat.id,play_game) 
    else:
            if int(message.text) > random_number :
                bot.reply_to(message, 'quess smaller ! ')
                bot.register_next_step_handler_by_chat_id(message.chat.id,play_game) 
            elif int(message.text) < random_number :
                bot.reply_to(message, 'quess bigger ! ')
                bot.register_next_step_handler_by_chat_id(message.chat.id,play_game)  
            else:
              keyboard = telebot.types.InlineKeyboardMarkup()
              button_x64 = telebot.types.InlineKeyboardButton(text='new Game', callback_data='x64')
              keyboard.add(button_x64)

              button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
              keyboard.add(button_x32)
 
              bot.send_message(message.from_user.id, "You guess right ! :", reply_markup=keyboard)
              
#============================================ age ================================================#

@bot.message_handler(commands=['age'])
def age(message):
     bot.reply_to(message, 'enter your age in this format 1378-01-27 : ')
     bot.register_next_step_handler(message,age_handler)    

def age_handler(message):
     mt_date = JalaliDate.fromisoformat(message.text).to_gregorian()
     today = date.today()
     age = today.year - mt_date.year -((today.month, today.day) < (mt_date.month, mt_date.day))
     keyboard = telebot.types.InlineKeyboardMarkup()
     button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
     keyboard.add(button_x32)   
     bot.send_message(message.from_user.id,'you are '+  str(age)+ ' years old ', reply_markup=keyboard)
      

#============================================== max number =======================================#
@bot.message_handler(commands=['max'])
def maximum(message):
    bot.reply_to(message, 'enter number in this format 2,3,4,5,6 ')
    bot.register_next_step_handler(message,max_handler)
    
def max_handler(message):
    all_num = list(map(int,message.text.split(',')))
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
    keyboard.add(button_x32)   
    bot.send_message(message.from_user.id,'max number is : ' + str(max(all_num)), reply_markup=keyboard)
    
#============================================== max index =======================================#
@bot.message_handler(commands=['argmax'])
def arg_maximum(message):
    bot.reply_to(message, 'enter number in this format 2,3,4,5,6 ')
    bot.register_next_step_handler(message,max_index_handler)
    
def max_index_handler(message):
    all_num = list(map(int,message.text.split(',')))
    max_num = max(all_num)
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
    keyboard.add(button_x32)   
    bot.send_message(message.from_user.id,'your max number index is  : ' + str(all_num.index(max_num)+1), reply_markup=keyboard)
 
 
#============================================== voice ===========================================#
@bot.message_handler(commands=['voice'])
def voice(message):
    bot.reply_to(message, 'please enter english sentence (if its slow please wait ...) : ')
    bot.register_next_step_handler(message,voice_handler)
    
    
def voice_handler(message):
    mytext = message.text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.ogg")
    myobj = open("welcome.ogg",'rb')
    bot.send_voice(message.chat.id,myobj)
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
    keyboard.add(button_x32)   
    bot.send_message(message.from_user.id,'for contiue : ', reply_markup=keyboard)
    
    
    
#=========================================== qrcode ==============================================#
@bot.message_handler(commands=['qrcode'])
def voice(message):
    bot.reply_to(message, 'please enter english sentence (if its slow please wait ...) : ')
    bot.register_next_step_handler(message,qr_code_handler)
    
def qr_code_handler(message):
     url = qrcode.make(message.text)
     url.save('myqr.png')
     url = open('myqr.png','rb')
     bot.send_photo(message.chat.id,url)
     keyboard = telebot.types.InlineKeyboardMarkup()
     button_x32 = telebot.types.InlineKeyboardButton(text='Menu', callback_data='x32')
     keyboard.add(button_x32)   
     bot.send_message(message.from_user.id,'for contiue : ', reply_markup=keyboard)
     
#=========================================== callBack func =======================================#
              
@bot.callback_query_handler(func=lambda call:True)            
def callback_worker(call):
    if call.data == "x64":
         global random_number
         random_number = random.randint(0,9)
         bot.reply_to(call.message, 'quess number (0,10)  or write newGame for new game : ')
         bot.register_next_step_handler_by_chat_id(call.message.chat.id,play_game) 

    if call.data == "x32":
        send_welcome(call.message)


bot.polling(none_stop=True)
