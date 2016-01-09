import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
import re
import time

file_name = str(time.time())

csv_file = open("{0}.csv".format(file_name), 'w+')
writer = csv.writer(csv_file)

ppp = pprint.PrettyPrinter()
# poast_dict = dict()
# poast_dict_count = 0
poast_set = set()

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

    print("Poast Set Length: {0}".format(len(poast_set)))
    time.sleep(5)

print("break")
