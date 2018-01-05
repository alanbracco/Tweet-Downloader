"""Twitter streaming.

Usage:
  stream.py [options]
  stream.py -h | --help

Options:
  -l <n>            Stream at most <n> tweets.
  -o <filename>     Output tweets to file.
  -m <n>            Save to several files, <n> tweets per file.
  -s                Only short texts
  -h --help         Show this screen.
"""
from docopt import docopt
import pickle
import os
import sys

# http://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html
import tweepy


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, output=None, limit=None,
                 limit_per_file=None, only_short=False):
        self.tweets = []
        self.output = output
        self.limit = limit or float('inf')
        self.limit_per_file = limit_per_file or float('inf')
        self.count = 0
        self.count_per_file = 0
        self.only_short = only_short
        if output:
            self.file_count = 0
            if limit_per_file:
                output = output.format(self.file_count)
            self.output_file = open(output, 'wb')
        super().__init__()

    def on_status(self, status):

        if hasattr(status, "retweeted_status"):
            return True

        if self.only_short and status.truncated:
            return True

        has_attrs = (hasattr(status, "place") and 
                     hasattr(status.place, "country"))
        if not (has_attrs and status.place.country == 'Argentina'):
            return True

        self.tweets.append(status)
        self.count += 1


        size = 100
        x = int((float(self.count)/self.limit)*size)
        perc = round((float(self.count)/self.limit)*100, 1)
        msg = ("Downloading tweets..." +
               "{}% ({}/{})".format(perc, self.count, self.limit) +
               ' '*(len(str(self.limit)) + 6 - (len(str(perc))+len(str(self.count)))) +
               '[' + '#'*x + ' '*(size-x) + ']')
        progress(msg)

        if self.output and self.limit == self.count:
            print('')
            pickle.dump(self.tweets, self.output_file)

        self.count_per_file += 1
        if self.count == self.limit:
            return False
        if self.output and self.count_per_file >= self.limit_per_file:
            self.count_per_file = 0
            self.file_count += 1
            self.output_file.close()
            output = self.output.format(self.file_count)
            self.output_file = open(output, 'wb')


# https://apps.twitter.com/app/14234803/keys
consumer_key = os.environ['STREAM_CONSUMER_KEY']
consumer_secret = os.environ['STREAM_CONSUMER_SECRET']
access_token = os.environ['STREAM_ACCESS_TOKEN']
access_token_secret = os.environ['STREAM_ACCESS_TOKEN_SECRET']


if __name__ == '__main__':
    opts = docopt(__doc__)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    args = {
        'output': opts['-o'],
        'limit': opts['-l'] and int(opts['-l']),
        'limit_per_file': opts['-m'] and int(opts['-m']),
        'only_short': opts['-s'],
    }
    streamListener = MyStreamListener(**args)
    stream = tweepy.Stream(auth=api.auth, listener=streamListener)

    # filter_level=none|low|medium
    track = "*".split()
    locations = [-70.5309656, -55.0521142, -52.9664178, -29.21408]
    languages = ['es']
    stream.filter(track=track, locations=locations)
