from exchange import Exchange
import telegram_token as token
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from news import News
import time
from find_last_tweet import FindLastTweet



bot = telebot.TeleBot(token.TELEGRAM_BOT_TOKEN)


def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")

def get_user_id_from_message(message):
    return message.chat.id

     
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Coins", callback_data="coins"),
                           InlineKeyboardButton("News", callback_data="news"))
    return markup

def set_bist_link():
    find_last_tweet_bist = FindLastTweet(token.BIST_URL)
    time.sleep(5)
    last_bist_news_link = find_last_tweet_bist.search_all_links()
    return last_bist_news_link

def set_coin_link():
    find_last_tweet_coin = FindLastTweet(token.COIN_URL) 
    time.sleep(5)
    last_coin_news_link = find_last_tweet_coin.search_all_links()
    return last_coin_news_link

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "coins":
        print(f"Message received from user:",call.from_user.first_name,"\nchat_id:",call.message.chat.id,"at:",get_current_time(),"\n")    
        bot.answer_callback_query(call.id, f"Merhaba {call.from_user.first_name}\nSaat {get_current_time()} itibariyle fiyatlar şu şekildedir: ")
        chat_id_ = get_user_id_from_message(call.message)
        try:
            exchange = Exchange(token.TELEGRAM_BOT_TOKEN,chat_id_)
            exchange.run() 
        except:
            bot.send_message(chat_id_,"Bir hata oluştu. \n bir süre sonra tekrar deneyin.")

    elif call.data == "news":
        print(f"Message received from user:",call.from_user.first_name,"\nchat_id:",call.message.chat.id,"at:",get_current_time(),"\n")     
        bot.answer_callback_query(call.id, f"Merhaba {call.from_user.first_name}\nSon tweetler şu şekildedir:")
        chat_id_ = get_user_id_from_message(call.message)
        bot.send_message(chat_id_,"Tweetler yükleniyor.. Bu işlem biraz zaman alabilir..")
        
        news_coin = News(token.TELEGRAM_BOT_TOKEN,chat_id_,set_coin_link())
        news_bist = News(token.TELEGRAM_BOT_TOKEN,chat_id_,set_bist_link())

        try:
            bot.send_message(chat_id_,"Son Coin tweeti:")
            news_coin.run()
        except:
            bot.send_message(chat_id_,"Tweet alınamadı. \n bir süre sonra tekrar deneyin.")
            print("error: Coin tweet couldn't be fetched from exchange")
        try:
            bot.send_message(chat_id_,"Son Borsa İstanbul tweeti:")
            news_bist.run()
        except:
            bot.send_message(chat_id_,"Tweet alınamadı. \n bir süre sonra tekrar deneyin.")
            print("error: Bist tweet couldn't be fetched from exchange")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    try:
        bot.send_message(message.chat.id, "Coinler mi ? / Haberler mi?", reply_markup=gen_markup())
        print("success: Program started")
    except:
        print("error: Program couldn't be started")

bot.infinity_polling()