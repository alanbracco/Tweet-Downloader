"""
Download Tweets by ID using Tweepy.

Usage:
  tweets_by_id.py [options]
  tweets_by_id.py -h | --help

Options:
  -i <filename>       Input file.
  -o <filename>       Output file.
  -h --help           Show this screen.
"""
import os
import sys
import pickle
import tweepy
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

    input_file = opts['-i']
    output_file = opts['-o']
    if input_file and output_file:
        if not os.path.exists(input_file):
            sys.exit("File does not exist")
        with open(input_file, 'r') as in_file:
            # API
            cred = AUTH_DATA[0]

            auth = tweepy.OAuthHandler(cred['consumer_key'],
                                       cred['consumer_secret'])
            auth.set_access_token(cred['access_token'],
                                  cred['access_token_secret'])

            api = tweepy.API(auth_handler=auth,
                             wait_on_rate_limit=True,
                             wait_on_rate_limit_notify=True)

            tweets = []
            for line in in_file.readlines():
                if '\t' in line:
                    id, _ = line.split('\t')
                    try:
                        tweet = api.get_status(id=id, tweet_mode='extended')
                        tweets.append(tweet)
                    except Exception:
                        print('Tweet with id {id} not found.'.format(id=id))

            if len(tweets) > 0:
                with open(output_file, 'wb') as out_file:
                    pickle.dump(tweets, out_file) 