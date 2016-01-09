import csv
from nltk import FreqDist, bigrams
from nltk.corpus import stopwords
import os
import pprint
import re
import string

# from
# www.datasciencebytes.com/bytes/
# 2014/11/04/filter-common-words-from-documents/
stopword_list = stopwords.words('english')
stopword_set = set(stopword_list)


def clean_input(input):
    input = re.sub("\n+", " ", input)
    input = re.sub(' +', " ", input)
    clean_input = list()
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            if item.lower() not in stopword_set:
                clean_input.append(item)
    return clean_input


def analyze_data(running_string):
    cleaned_input = clean_input(running_string)
    bigrams_output = bigrams(cleaned_input)
    bigrams_dist = FreqDist(bigrams_output)
    return bigrams_dist


def concat_csv():
    running_string = ""
    for fname in os.listdir():
        if 'csv' in fname:
            print("Found {0}".format(fname))
            with open(fname, newline='') as csvfile:
                rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in rdr:
                    try:
                        print(row[2])
                        running_string += " {0}".format(row[2])
                    except:
                        pass
    return running_string


if __name__ == "__main__":
    ppp = pprint.PrettyPrinter()
    running_string = concat_csv()
    print("Running String Length: {0}".format(len(running_string)))
    bigrams_dist = analyze_data(running_string)
    ppp.pprint(bigrams_dist.most_common(20))
