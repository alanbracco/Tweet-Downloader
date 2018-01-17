"""Twitter Status reader.

Usage:
  reader.py [options]
  reader.py -h | --help

Options:
  -i <filename>     Input file to read tweets.
  -o <filename>     Output file to write tweets.
  -h --help         Show this screen.
"""
import os
import sys
import json
import pickle
from docopt import docopt


if __name__ == '__main__':

    opts = docopt(__doc__)

    input_file = opts['-i']
    if input_file:
        if input_file.endswith(".byte"):
            extension = 'byte'
            if not os.path.exists(input_file):
                sys.exit("File does not exist")
            with open(input_file, 'rb') as file:
                tweets = pickle.load(file)
                n = len(tweets)
        elif input_file.endswith(".json"):
            extension = 'json'
            with open(input_file, 'r') as json_file:
                tweets = json.load(json_file)["tweets"]
        else:
            sys.exit("Enter a valid file.")

        try:
            output_file = opts['-o']
            if not output_file:
                output_file = '{}_tweets'.format(n)

            if extension == 'byte':
                json_file = open(output_file + '.json', 'w')
                jsons = {"tweets": []}

            twnorm_file = open(output_file + '.txt', 'w')

            for tweet in tweets:


                if extension == 'byte':
                    json_string = json.dumps(tweet._json)
                    json_format = json.loads(json_string)
                    jsons["tweets"].append(json_format)
                else:
                    json_format = tweet

                id = json_format["id_str"]

                if "extended_tweet" in json_format.keys():
                    text = json_format["extended_tweet"]["full_text"]
                elif "full_text" in json_format.keys():
                    text = json_format["full_text"]
                else:
                    text = json_format["text"]
                text = text.replace('\n', ' ')
                text = text.replace('\t', ' ')
                twnorm =  id + '\t' + text + '\n'
                twnorm_file.write(twnorm)

            if extension == 'byte':
                json.dump(jsons, json_file, sort_keys=True, indent=4,
                          separators=(',', ': '))
                json_file.close()

            twnorm_file.close()
            print("JSON and TXT CREATED")

        except Exception as e:
            if extension == 'byte':
                json_file.close()
            twnorm_file.close()
            raise e
