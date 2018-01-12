"""From CSV format.

Usage:
  from_csv.py [options]
  from_csv.py -h | --help

Options:
  -i <filename>     Input file.
  -o <filename>     Output file.
  -h --help         Show this screen.
"""
import csv
import sys
from docopt import docopt

if __name__ == '__main__':

    opts = docopt(__doc__)

    input_file = opts['-i']
    if input_file:
        if not os.path.exists(input_file):
            sys.exit("File does not exist")

        with open(input_file, "r") as infile:
            reader = csv.reader(infile)
            with open(input_file.replace(".csv", ".txt"), "w") as outfile:
                i = 0
                for row in reader:
                    if i == 0:
                        i += 1
                        continue
                    id = row[0]
                    text = row[1]
                    corrections = row[2].split(' | ')
                    insult = row[3]
                    outfile.write(id + '\t' + text + '\n')
                    if corrections != ['']:
                        for correction in corrections:
                            outfile.write('\t' + correction + '\n')
