import tweepy, time, datetime, requests, re
from os import environ

# Put search keyword and retweet numbers 
search_keyword = environ["search_keyword"]
min_retweets = int(environ["min_retweets"])
tweets_to_update = int(environ["tweets_to_update"])
get_my_tweets_n = int(environ["get_my_tweets_n"])
lang = environ["search_lang"]
now_date = datetime.datetime.now()
search_date = datetime.datetime(now_date.year, now_date.month, now_date.day-1).strftime('%Y-%m-%d')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
auth.set_access_token(environ["access_token"], environ["access_token_secret"])

# Create API object
api = tweepy.API(auth)

# Get the list of tweet ids that have already been tweeted
my_tweets = []
for tweet in tweepy.Cursor(api.user_timeline).items(get_my_tweets_n):
    tco_url = re.search(r'https://t\.co/[a-zA-Z0-9]+', tweet.text).group()
    my_tweets.append(requests.get(tco_url, allow_redirects=True).url)

# Define the search query and the maximum number of tweets to retrieve
query = f"{search_keyword} min_retweets:{min_retweets} since:{search_date}"

# Iterate over the tweets and tweet each one to the private account
for tweet in tweepy.Cursor(api.search_tweets, q=query, lang=lang).items(tweets_to_update):
    for my_tweet in my_tweets:
        if f"{tweet.id}" in my_tweet:
            break
    else:
        time.sleep(5)
        try:
            api.update_status(status=f"https://twitter.com/twitter/statuses/{tweet.id}")
        except Exception as e:
            print(e)
