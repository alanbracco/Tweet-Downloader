"""To CSV format.

Usage:
  to_csv.py [options]
  to_csv.py -h | --help

Options:
  -i <filename>     Input file.
  -o <filename>     Output file.
  -h --help         Show this screen.
"""
import os
import sys
from docopt import docopt

if __name__ == '__main__':

    opts = docopt(__doc__)

    input_file = opts['-i']
    if input_file:
        if not os.path.exists(input_file):
            sys.exit("File does not exist")

        with open(input_file, 'r') as file:
            output_file = opts['-o']
            if not output_file:
                output_file = "to_import.csv"
            output_file = os.path.join("Parts", "csvs", output_file)
            with open(output_file, 'w') as outfile:
                for line in file.readlines():
                    id, text = line.split("\t")
                    text = text.replace('"', '""')
                    if text[-1] == '\n':
                        text = text[:-1]
                    outfile.write(id + ',' + '"' + text + '"' + '\n')
