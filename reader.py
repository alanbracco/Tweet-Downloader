"""Twitter Status reader.

Usage:
  reader.py [options]
  reader.py -h | --help

Options:
  -i <filename>     Input file to read tweets.
  -o <filename>     Output file to write tweets.
  -r                Create raw tweets file
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
        if not os.path.exists(input_file):
            sys.exit("File does not exist")
        with open(input_file, 'rb') as file:
            tweets = pickle.load(file)
            n = len(tweets)

            if opts['-r']:
                with open('raw', 'w') as raw:
                    raw.write(str(tweets))
                    print("RAW CREATED")

        try:
            output_file = opts['-o']
            if not output_file:
                output_file = '{}_tweets'.format(n)
            json_file = open(output_file + '.json', 'w')
            twnorm_file = open(output_file + '.txt', 'w')
            jsons = {"tweets": []}

            for i, tweet in enumerate(tweets):

                json_string = json.dumps(tweet._json)
                json_format = json.loads(json_string)

                jsons["tweets"].append(json_format)

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

            json.dump(jsons, json_file, sort_keys=True, indent=4,
                      separators=(',', ': '))

            json_file.close()
            twnorm_file.close()
            print("JSON and TXT CREATED")

        except Exception as e:
            json_file.close()
            twnorm_file.close()
            raise e
