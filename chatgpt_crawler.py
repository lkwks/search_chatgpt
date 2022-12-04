import tweepy
from os import environ
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
auth.set_access_token(environ["access_token"], environ["access_token_secret"])

# Create API object
api = tweepy.API(auth)

# Define the search query and the maximum number of tweets to retrieve
query = "ChatGPT min_retweets:10"
max_tweets = 20

# Search for tweets matching the query and store the results
tweets = {}
for lang in ["en", "ko"]:
    tweets[lang] = tweepy.Cursor(api.search_tweets, q=query, lang=lang).items(max_tweets)


# Get the list of tweet ids that have already been tweeted
my_tweets = []
for tweet in tweepy.Cursor(api.user_timeline).items(100):
    my_tweets.append(tweet.text)

# Iterate over the tweets and tweet each one to the private account
# if it hasn't already been tweeted and if it's written in English

i = 1
for lang in ["en", "ko"]:
    for tweet in tweets[lang]:
        for my_tweet in my_tweets:
            if f"https://twitter.com/twitter/statuses/{tweet.id}" in my_tweet:
                break
        else:
            time.sleep(5)
            try:
                api.update_status(status=f"https://twitter.com/twitter/statuses/{tweet.id}")
                i += 1
                print(f"tweeting {i}th tweet completed.")
            except Exception as e:
                print(e)
