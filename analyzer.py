"""Twitter JSON analyzer.

Usage:
  analyzer.py [options]
  analyzer.py -h | --help

Options:
  -i <filename>     Input file to read json tweets.
  -h --help         Show this screen.
"""
import os
import sys
import json
from docopt import docopt
from collections import Counter
import datetime
import calendar


def sorted_counter(in_list):
    counter_list = list(Counter(in_list).items())
    return sorted(counter_list, key=lambda x: x[1], reverse=True)

def to_timestamp(time):
    SOURCE_TIME_FORMAT = "%a %b %d %H:%M:%S %z %Y"
    time_struct = datetime.datetime.strptime(time, SOURCE_TIME_FORMAT)
    timestamp = calendar.timegm(time_struct.timetuple())
    return timestamp

def timestamp_to_localtime(timestamp):
    local_time = datetime.datetime.fromtimestamp(timestamp)
    MY_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    return local_time.strftime(MY_TIME_FORMAT)

if __name__ == '__main__':
    opts = docopt(__doc__)

    input_file = opts['-i']
    if input_file:
        if not os.path.exists(input_file):
            sys.exit("File does not exist")

        with open(input_file, 'r') as json_file:
            json_data = json.load(json_file)
            langs = [tweet["lang"] for tweet in json_data["tweets"]]
            locations = [tweet["place"]["full_name"]
                         for tweet in json_data["tweets"]]

            print("LANGUAGES:")
            lang_items = sorted_counter(langs)
            for lang in lang_items:
                print(lang[0] + ':', lang[1])

            print("\nLOCATIONS:")
            locations_items = sorted_counter(locations)
            for location in locations_items:
                if ',' in location[0]:
                    city, country = location[0].split(',')
                    if country != " Argentina":
                        print(location[0] + ':', location[1])
                    else:
                        print(city + ':', location[1])
                else:
                    print(location[0] + ':', location[1])

            times = []
            for tweet in json_data["tweets"]:
                if tweet["truncated"]:
                    assert "extended_tweet" in tweet.keys()
                    assert "full_text" in tweet["extended_tweet"].keys()
                else:
                    assert "extended_tweet" not in tweet.keys()

                times.append(to_timestamp(tweet["created_at"]))

            sorted_times = sorted(times)
            start = sorted_times[0]
            end = sorted_times[-1]
            print("\nFROM: {}".format(timestamp_to_localtime(start)))
            print("TO: {}".format(timestamp_to_localtime(end)))
