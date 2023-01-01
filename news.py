from tweetcapture import TweetCapture
import asyncio
import telebot
import os

class News:

    def __init__(self, token, chat_id,url):
        self.token = token
        self.chat_id = chat_id
        self.url = url


    def take_screenshot_from_url(self, url): 
        try:
            print("success: Screenshot taken")
            tweet = TweetCapture() 
            asyncio.run(tweet.screenshot(url, "mode3.png", mode=3, night_mode=0))
            bot = telebot.TeleBot(self.token)
            bot.send_photo(self.chat_id, open("mode3.png", "rb"))
        except:
            print("error: Screenshot couldn't be taken")


    def delete_picture(self): # delete picture after sending it to telegram
        try:
            os.remove("mode3.png")
            print("success: Picture deleted")
        except:
            print("error: Picture couldn't be deleted")

    def run(self):
        self.take_screenshot_from_url(self.url)
        self.delete_picture()
        







        