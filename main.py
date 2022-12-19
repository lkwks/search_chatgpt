import tweepy, datetime, requests
from os import environ

# Put search keyword and retweet numbers 
search_keyword = environ["search_keyword"]
min_retweets = int(environ["min_retweets"])
tweets_to_update = int(environ["tweets_to_update"])

# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
auth.set_access_token(environ["access_token"], environ["access_token_secret"])

# Create API object
api = tweepy.API(auth)

# Define the search query
search_date = datetime.datetime.now() - datetime.timedelta(days=1)
search_date_str = search_date.strftime('%Y-%m-%d')
query = f"{search_keyword} min_retweets:{min_retweets} since:{search_date_str}"

# Iterate over the tweets and retweet
for tweet in tweepy.Cursor(api.search_tweets, q=query, lang=environ["search_lang"]).items(tweets_to_update):
    try:
        api.retweet(tweet.id)
    except Exception as e:
        print(e)
