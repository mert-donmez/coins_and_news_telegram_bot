import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FindLastTweet:

    def __init__(self, url):
        self.url = url
        self.last_tweet_link = None
        self.driver = uc.Chrome()
        self.driver.get(self.url)

    def search_all_links(self): 
        lnks = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "a"))) 
        try:
            for lnk in lnks: 
                if "/status/" in lnk.get_attribute("href"): # if link contains "/status/" then it is a tweet link
                    self.last_tweet_link = lnk.get_attribute("href")
                    print("success: Last tweet's link was found: ",self.last_tweet_link)
                    break
            self.driver.quit()
            return self.last_tweet_link
        except:
            print("error: Last tweet's link was not found")
            self.driver.quit()
            return None
    


    