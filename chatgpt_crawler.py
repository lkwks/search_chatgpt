import tweepy
from os import environ
import time

# Authenticate to Twitter
try:
    auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
    auth.set_access_token(environ["access_token"], environ["access_token_secret"])
except:
    raise

# Create API object
api = tweepy.API(auth)

# Define the search query and the maximum number of tweets to retrieve
query = "ChatGPT min_retweets:10"
max_tweets = 100

# Search for tweets matching the query and store the results
tweets = {}
for lang in ["en", "ko"]:
    tweets[lang] = tweepy.Cursor(api.search_tweets, q=query, lang=lang).items(max_tweets)


# Get the list of tweet ids that have already been tweeted
tweeted_ids = []
for tweet in tweepy.Cursor(api.user_timeline).items(10):
    tweeted_ids.append(tweet.id)

# Iterate over the tweets and tweet each one to the private account
# if it hasn't already been tweeted and if it's written in English

i = 1
for lang in ["en", "ko"]:
    for tweet in tweets[lang]:
        if tweet.id not in tweeted_ids and tweet.lang == lang:
            time.sleep(5)
            api.update_status(status=f"{tweet.text[:50]}... https://twitter.com/twitter/statuses/{tweet.id}")
            i += 1
            print(f"tweeting {i}th tweet completed.")
