import gspread
from datetime import date
import telebot


bot_token = 'BOT_TOKEN'
googlesheet_url = 'GOOGLESHEET_URL'
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account()

# Welcome message
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, I will adding coins to Google`s Spreadsheet Enter expense in this pattern [CATEGORY:PRICE]')
    
    
@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    try:
        today = date.today().strftime('%d.%m.%Y')
        
        # Split message into 2 parts - category & price
        category, price = message.text.split(':', -1)
        text_message = f'Coin added: {category} on price {price} kzt'
        bot.send_message(message.chat.id, text_message)
        
        # Open spread and add expense
        sh = gc.open_by_url(googlesheet_url)
        sh.sheet1.append_row([today, category, price])
    except:
        bot.send_message(message.chat.id, 'Error. Incorrect form of input data')
        
    bot.send_message(message.chat.id, 'Enter expense in this pattern [CATEGORY:PRICE]')
    
if __name__ == '__main__':
    bot.polling(none_stop=True)