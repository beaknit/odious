import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import FreqDist, bigrams
from nltk.corpus import stopwords
import pprint
import re
import string
import time

file_name = str(time.time())

csv_file = open("{0}.csv".format(file_name), 'w+')
writer = csv.writer(csv_file)

# from http://www.datasciencebytes.com/bytes/2014/11/04/filter-common-words-from-documents/
stopword_list = stopwords.words('english')
stopword_set = set(stopword_list)


ppp = pprint.PrettyPrinter()
# poast_dict = dict()
# poast_dict_count = 0
poast_set = set()

running_string = ""


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

while True:
    # Gather Data
    try:
        html = urlopen("http://boards.4chan.org/r9k")
        bsObj = BeautifulSoup(html, "html.parser")
        poasts = bsObj.findAll("blockquote", {"class": "postMessage"})
    except Exception as e:
        print("Exception:  {0}".format(str(e)))
        time.sleep(1)
        continue

    for poast in poasts:
        # Strip leading 'm' character
        poast_id = poast.attrs['id'][1:]
        # if not poast_dict.get(poast_id):
        if poast_id not in poast_set:
            poast_set.add(poast_id)
            # poast_dict_count += 1
            in_reply_to_regex = '\>*\s*\>*([0-9]*)(.*)'
            result = re.match(in_reply_to_regex, poast.get_text())
            original_text = result.group(0)
            first_match = result.group(1)
            second_match = result.group(2)
            print('----------------------------------------------------')
            print("Post ID: {0}".format(poast_id))
            print("Reply-To: {0}".format(first_match))
            print("Comment: {0}".format(second_match.lower()))
            print("Original Text: {0}".format(original_text))

            # Persist to CSV
            writer.writerow((
                poast_id, first_match, second_match.lower(), original_text))
            # TODO: Push to Dynamo or DocDB

            # Use a list of poast_ids to dedupe posts
            # poast_dict[poast_id] = (first_match, second_match, original_text)
            # poast_list.append((
            #    poast.attrs['id'],
            # [result.group(0)],
            # result.group(1),
            # poast.text))
            running_string += " " + second_match.lower()

    # Analyze Data
    cleaned_input = clean_input(running_string)
    bigrams_output = bigrams(cleaned_input)
    bigrams_dist = FreqDist(bigrams_output)
    ppp.pprint(bigrams_dist.most_common(20))
    print("Running String Length: {0}".format(len(running_string)))
    print("Poast Set Length: {0}".format(len(poast_set)))
    time.sleep(5)

print("break")
