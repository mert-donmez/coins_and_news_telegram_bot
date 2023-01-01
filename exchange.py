import ccxt
import telebot

class Exchange:
    def __init__(self, telegram_api_key,telegram_user_id):
        self.telegram_api_key = telegram_api_key
        self.telegram_user_id = telegram_user_id
        self.exchange_name = "binance" 
        self.coins_ = ["BTC/USDT","ETH/USDT","SOL/USDT","USDT/TRY"] # coins to be tracked
        
    
    def get_coin_price(self,coin): # get coin price from exchange
        try:
            exchange = ccxt.binance()
            ticker = exchange.fetch_ticker(coin) 
            print("success: Coin datas are fetched from exchange")
            return ticker["last"]
        except:
            print("error: Coin datas couldn't be fetched from exchange")
            return "error"

    def send_message(self,coin,price): # send message to telegram
        try:
            bot = telebot.TeleBot(self.telegram_api_key)
            bot.send_message(self.telegram_user_id,f"{coin} : {price}")
            print("success: Message sent to telegram")
        except:
            print("error: Message couldn't be sent to telegram")
    
    def run(self): 
        for coin in self.coins_:
            price = self.get_coin_price(coin)
            self.send_message(coin,price)


        
            
    

    

    



    




    





    

