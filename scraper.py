from selenium import webdriver
from selenium.webdriver.common.by import By
from os import environ
import tweepy, datetime, requests, re


def tweet_update(api, msg: str) -> None:
    try:
        api.update_status(status=msg)
    except Exception as e:
        print(e)

def get_no(url: str) -> int:
    no_search = re.search(r'(?<=no=)\d+(?=&)', tco_url)
    return int(no_search.group()) if no_search else -1
        
def scrape_page():
    auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
    auth.set_access_token(environ["access_token"], environ["access_token_secret"])
    api = tweepy.API(auth)
    
    my_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline).items(100):
        tco_url_search = re.search(r'https://t\.co/[a-zA-Z0-9]+', tweet.text)
        if tco_url_search:
            my_tweets.append(get_no(requests.get(tco_url_search.group(), allow_redirects=True).url))
        
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(3)    
    
    driver.get(environ["site_url"])
    driver.maximize_window()    

    for elem in driver.find_elements(By.XPATH, '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr'):
        written_date = elem.find_element(By.XPATH, 'td[5]').get_attribute('title')
        if written_date == "": continue
            
        href = f"{elem.find_element(By.XPATH, './td[3]/a[1]').get_attribute('href')}"
        article_n = get_no(href)
        if article_n in my_tweets or article_n == -1: continue
        
        diff = datetime.datetime.now() - datetime.datetime.strptime(str(written_date), "%Y-%m-%d %H:%M:%S")
        if diff > datetime.timedelta(hours=24): continue
            
        tweet_update(api, href)
  
    driver.quit()

scrape_page()
