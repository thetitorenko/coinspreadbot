from datetime import date, datetime
import gspread
import telebot


bot_token = 'BOT_TOKEN'
googlesheet_url = 'GOOGLESHEET_URL'
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account()

# Welcome message
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, I will adding coins to Google`s Spreadsheet. Enter expense in this pattern [CATEGORY:PRICE/:day/]')
    
    
@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    try:
        
        # Split message - category & price & (optional) day
        def splitmsg(message):
            dt_tod = date.today()
            if len(message.split(':')) == 3:
                category, price, day = message.split(':')
                if day in ['today', 'tod']:
                    day_str = f'{dt_tod.day}.{dt_tod.month}.{dt_tod.year}'
                elif day in ['tomorrow', 'tom']:
                    day_str = f'{dt_tod.day-1}.{dt_tod.month}.{dt_tod.year}'
                else:
                    day_str = f'{day}.{dt_tod.month}.{dt_tod.year}'
                day_dt = datetime.strptime(day_str, '%d.%m.%Y')
                day = str(day_dt)[:11]
                return category, price, day
            else:
                category, price = message.split(':')
                day_str = f'{dt_tod.day}.{dt_tod.month}.{dt_tod.year}' 
                day_dt = datetime.strptime(day_str, '%d.%m.%Y')
                day = str(day_dt)[:11]
                return category, price, day
        category, price, day = splitmsg(message.text)
        
        # Open spread and add expense
        sh = gc.open_by_url(googlesheet_url)
        sh.sheet1.append_row([day, category, price], value_input_option='USER_ENTERED')
        sh.sheet1.sort((1, 'asc'))
        
        # Send feadback message
        text_message = f'Coin added: {category} on price {price} kzt on {day}'
        bot.send_message(message.chat.id, text_message)
        
    # Incorrect format    
    except:
        bot.send_message(day, category, price)
        # bot.send_message(message.chat.id, 'Error. Incorrect form of input data')
    
    # Standby message    
    bot.send_message(message.chat.id, 'Enter expense in this pattern [CATEGORY:PRICE/:day/]')
  
    
if __name__ == '__main__':
    bot.polling(none_stop=True)