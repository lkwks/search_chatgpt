import tweepy, datetime, requests
from os import environ

# workflow 설정 변경 가능한 환경변수들.
min_retweets = 1 if "min_retweets" not in environ else int(environ["min_retweets"])
search_lang = "ko" if "search_lang" not in environ else environ["search_lang"]
tweets_to_update = 100 if "tweets_to_update" not in environ else int(environ["tweets_to_update"])
search_keyword = "" if "search_keyword" not in environ else environ["search_keyword"]
search_account = "" if "search_account" not in environ else f" from:{environ["search_account"]}"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
auth.set_access_token(environ["access_token"], environ["access_token_secret"])

# Create API object
api = tweepy.API(auth)

# Define the search query
search_date = datetime.datetime.now() - datetime.timedelta(days=1)
search_date_str = search_date.strftime('%Y-%m-%d')
query = f"{search_keyword} min_retweets:{min_retweets} since:{search_date_str}{search_account}"

# Iterate over the tweets and retweet
for tweet in tweepy.Cursor(api.search_tweets, q=query, lang=search_lang).items(tweets_to_update):
    try:
        api.retweet(tweet.id)
    except Exception as e:
        print(e)
