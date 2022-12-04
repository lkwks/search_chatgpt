import tweepy
from os import environ

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
tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en,ko").items(max_tweets)

# Get the list of tweet ids that have already been tweeted
tweeted_ids = []
for tweet in tweepy.Cursor(api.user_timeline).items(max_tweets):
    tweeted_ids.append(tweet.id)

# Iterate over the tweets and tweet each one to the private account
# if it hasn't already been tweeted and if it's written in English
for tweet in tweets:
    if tweet.id not in tweeted_ids and (tweet.lang == "en" or tweet.lang == "ko"):
        api.update_status(status=tweet.url, in_reply_to_status_id=tweet.id)
