import requests
import json
from tqdm import tqdm
import re
import string
import time

count = 0
file_path_base = "crawled/query_content_4_{}.json"
# file_path_base = "crawled/test.json"
file_path = ""
punctuation = '!"#$%&\'()*,.:;<=>?@[\\]^_`{|}~'

def get_query_page(query):
    url = "https://www.quora.com/{}"
    processed = re.sub('[%s]' % re.escape(punctuation), '', query)
    processed = processed.strip().replace("-", " ")
    processed = processed.strip().replace("/", " ")

    processed = re.sub(' +', ' ', processed).strip()
    processed = processed.strip().replace(" ", "-")

    url = url.format(processed)
    try:
        ret = requests.get(url, timeout=10)

        if ret.status_code == 403:
            print("forbidden started...")
        elif ret.status_code != 200:
            with open("crawled/not_succeed.txt", "a+") as f:
                f.write(query + "\n")
            # print(query)
        else:
            json_obj = {"query": query, "content": ret.text}
            with open(file_path, "a+") as f:
                f.write(json.dumps(json_obj) + "\n")

    except Exception as e:
        print(e)
        with open("crawled/not_succeed.txt", "a+") as f:
            f.write(query + "\n")
        # print(query)


with open('Quora3.txt') as f:
    sentence = f.readlines()

for sent in tqdm(sentence):
    if count % 1000 == 0:
        file_count = int(count / 1000)
        file_path = file_path_base.format(str(file_count))
        print(file_path, count)

    get_query_page(sent)

    count += 1
    time.sleep(0.4)
