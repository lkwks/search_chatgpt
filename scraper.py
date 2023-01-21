from os import environ
import tweepy, datetime, requests, re
from bs4 import BeautifulSoup


def tweet_update(api, msg: str) -> None:
    try:
        api.update_status(status=msg)
    except Exception as e:
        print(e)

def get_no(url: str) -> int:
    no_search = re.search(r'(?<=no=)\d+(?=&)', url)
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
    
    soup = BeautifulSoup(requests.get(environ["site_url"]).text, 'html.parser')

    for elem in soup.select('#container > section:nth-of-type(1) > article:nth-of-type(2) > div:nth-of-type(2) > table > tbody > tr'):
        written_date = elem.select_one('td:nth-of-type(5)')['title']
        if written_date == "": continue
        
        href = elem.select_one('td:nth-of-type(3) > a:nth-of-type(1)')['href']
        article_n = get_no(href)
        if article_n in my_tweets or article_n == -1: continue
    
        diff = datetime.datetime.now() - datetime.datetime.strptime(str(written_date), "%Y-%m-%d %H:%M:%S")
        if diff > datetime.timedelta(hours=24): continue
    
        if "search_keyword" in environ:
            if environ["search_keyword"] not in elem.select_one('td:nth-of-type(3) > a:nth-of-type(1)').text: continue
            if len(elem.select_one('td:nth-of-type(3) > a:nth-of-type(1)').text) > 20: continue                
                
        tweet_update(api, href)
  

scrape_page()
