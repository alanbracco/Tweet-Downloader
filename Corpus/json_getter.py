"""Twitter JSON getter.

Usage:
  json_getter.py [options]
  json_getter.py -h | --help

Options:
  -i <filename>     Input file to read tweets.
  -o <filename>     Output file to write tweets.
  -h --help         Show this screen.
"""
import os
import json
from docopt import docopt


def tweet_object(json, id):
    id = int(id)
    for tweet in json['tweets']:
        if id == tweet['id']:
            return tweet
    return None


if __name__ == '__main__':
    opts = docopt(__doc__)
    
    input_file = opts['-i']
    if input_file:
        ids = []
        with open(input_file, 'r') as file:
            for line in file.readlines():
                if '\t' in line and line != '\t':
                    id, _ = line.split('\t')
                    ids.append(id)

        output_file = opts['-o']
        if not output_file:
            output_file = 'final_tweets.json'
        outfile = open(output_file, 'w')
        jsons = {"tweets": []}

        i = 0
        for json_file_item in sorted(os.listdir('../JSONS')):
            id_in_this_file = True
            with open(os.path.join('../JSONS', json_file_item), 'r') as file:
                json_file = json.load(file)
                while id_in_this_file and i < len(ids):
                    id = ids[i]
                    tweet = tweet_object(json_file, id)
                    if not tweet:
                        id_in_this_file = False
                    else:
                        i += 1
                        jsons["tweets"].append(tweet)
            print("Processed:", json_file_item)

        print('\n', len(jsons["tweets"]), "tweets obtained")
        json.dump(jsons, outfile, sort_keys=True, indent=4,
                  separators=(',', ': '))
