import tweepy, time, datetime
from os import environ

# Put search keyword and retweet numbers 
search_keyword = environ["search_keyword"]
min_retweets = int(environ["min_retweets"])
tweets_to_update = int(environ["tweets_to_update"])
get_my_tweets_n = int(environ["get_my_tweets_n"])
lang = environ["search_lang"]

# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ["consumer_key"], environ["consumer_secret"])
auth.set_access_token(environ["access_token"], environ["access_token_secret"])

# Create API object
api = tweepy.API(auth)

# Define the search query and the maximum number of tweets to retrieve
now_date = datetime.datetime.now()
search_date = datetime.datetime(now_date.year, now_date.month, now_date.day-1).strftime('%Y-%m-%d')
query = f"{search_keyword} min_retweets:{min_retweets} since:{search_date}"

# Search for tweets matching the query and store the results
tweets = tweepy.Cursor(api.search_tweets, q=query, lang=lang).items(tweets_to_update)

# Get the list of tweet ids that have already been tweeted
my_tweets = []
for tweet in tweepy.Cursor(api.user_timeline).items(get_my_tweets_n):
    my_tweets.append(tweet.text)

# Iterate over the tweets and tweet each one to the private account
# if it hasn't already been tweeted and if it's written in English
i = 1
for tweet in tweets:
    for my_tweet in my_tweets:
        if f"https://twitter.com/twitter/statuses/{tweet.id}" in my_tweet:
            break
    else:
        time.sleep(5)
        try:
            api.update_status(status=f"https://twitter.com/twitter/statuses/{tweet.id}")
            print(f"tweeting {i}th tweet completed.")
            i += 1
        except Exception as e:
            print(e, tweet.id, len(my_tweets), my_tweets[-1])
