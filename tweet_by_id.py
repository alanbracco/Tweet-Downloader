"""
Download Tweets by ID using Tweepy.

Usage:
  tweet_by_id.py [options]
  tweet_by_id.py -h | --help

Options:
  -i <id>       Tweet ID
  -h --help     Show this screen.
"""
import os
import sys
import tweepy
import pickle
from docopt import docopt


consumer_key = os.environ['SEARCH_CONSUMER_KEY']
consumer_secret = os.environ['SEARCH_CONSUMER_SECRET']
access_token = os.environ['SEARCH_ACCESS_TOKEN']
access_token_secret = os.environ['SEARCH_ACCESS_TOKEN_SECRET']

AUTH_DATA = [
    dict(consumer_key=consumer_key,
         consumer_secret=consumer_secret,
         access_token=access_token,
         access_token_secret=access_token_secret),
]


if __name__ == '__main__':
    opts = docopt(__doc__)

    # Opciones
    id = opts['-i']
    if id:
        id = int(id)
    else:
        sys.exit("No input ID")

    # API
    cred = AUTH_DATA[0]

    auth = tweepy.OAuthHandler(cred['consumer_key'],
                               cred['consumer_secret'])
    auth.set_access_token(cred['access_token'],
                          cred['access_token_secret'])

    api = tweepy.API(auth_handler=auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    tweet = api.get_status(id=id, tweet_mode='extended')

    with open('output_id', 'wb') as f:
        pickle.dump([tweet], f)