"""
Download Tweets using Tweepy.

Usage:
  tweet_downloader.py [options]
  tweet_downloader.py -h | --help

Options:
  -n <num>            Download <n> tweets
  -o <filename>       Metadata tweets to file (is a list) with format:
                          "<filename>_metadata.byte".
  -h --help           Show this screen.
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


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # Opciones
    metadata_filename = opts['-o']
    if not metadata_filename:
        metadata_filename = "output"

    max_tweets = opts['-n']
    if not max_tweets:
        max_tweets = 1
    else:
        max_tweets = int(max_tweets)

    # API
    cred = AUTH_DATA[0]

    auth = tweepy.OAuthHandler(cred['consumer_key'],
                               cred['consumer_secret'])
    auth.set_access_token(cred['access_token'],
                          cred['access_token_secret'])

    api = tweepy.API(auth_handler=auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    # ACA CAMBIA EL STRING POR LAS PALABRAS QUE QUIERAS BUSCAR
    search_kw = "*"

    with open(metadata_filename, 'wb') as f:
        try:
            tweets_count = 0  # Contador de tweets
            tw_ids = set()  # Para evitar tweets repetidos

            places = api.geo_search(query="Argentina", granularity="country")
            place_id = places[0].id
            cursor = tweepy.Cursor(api.search, q=search_kw,
                                   place_id=place_id, lang='es', tweet_mode='extended')

            tweets = []
            for tweet in cursor.items():

                size = 100
                x = int((float(tweets_count)/max_tweets)*size)
                perc = round((float(tweets_count)/max_tweets)*100, 1)
                msg = ("Downloading tweets..." +
                       "{}% ({}/{})".format(perc, tweets_count, max_tweets) +
                       ' '*(len(str(max_tweets)) + 6 - (len(str(perc))+len(str(tweets_count)))) +
                       '[' + '#'*x + ' '*(size-x) + ']')
                progress(msg)

                if tweets_count == max_tweets:
                    print("")
                    break
                retweeted = hasattr(tweet, "retweeted_status")
                truncated = tweet.truncated
                extended = hasattr(tweet, "extended_tweet")
                if not (retweeted or tweet.id in tw_ids or
                        (truncated and not extended)):
                    tw_ids.add(tweet.id)
                    tweets.append(tweet)
                    tweets_count += 1
            pickle.dump(tweets, f)

        except Exception as e:
            print("### Warning: Error durante la descarga de tweets ###")
            raise e
