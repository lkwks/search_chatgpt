from selenium import webdriver
from selenium.webdriver.common.by import By
from os import environ
import tweepy
import datetime


def tweet_update(msg: str) -> None:
    if weather_msg == "": return
    auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
    auth.set_access_token(environ["access_token"], environ["access_token_secret"])
    api = tweepy.API(auth)
    try:
        api.update_status(status=msg)
    except Exception as e:
        print(e)

try:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # chrome driver
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(3)    
    
    driver.get(environ["site_url"])
    driver.maximize_window()    

    article_elements = driver.find_elements(By.XPATH, '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr')
    for elem in article_elements:
        written_date = elem.find_element(By.XPATH, 'td[5]').get_attribute('title')
        print(written_date)
        diff = datetime.datetime.now() - datetime.datetime.strptime(str(written_date), "%Y-%m-%d %H:%M:%S")
        if diff <= datetime.timedelta(hours=int(environ["check_period"])):
            title_elem = elem.find_element(By.XPATH, './td[3]/a[1]')
            tweet_update(f"{title_elem.text} {title_elem.get_attribute('href')}")
    

except Exception as e:
    print(e)    
    driver.quit()

finally:
    print("finally...")
    driver.quit()
