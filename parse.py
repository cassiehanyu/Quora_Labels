from html.parser import HTMLParser
import json
from bs4 import BeautifulSoup
import re
import os

json_format = '{{\'id\':{}, \'url\':\'{}\', \'topics\':{}, \'answers\': {}, \'related_questions\':{}}},'
answers_format = '{{\'answer\':\'{}\', \'answer_url\':\'{}\', \'num_views\':\'{}\', \'author_url\':\'{}\', \'answered_at\':\'{}\'}},'
#base = "/scratch/quora/merged/"
base = '/home/leon/'
title_list = ["ui_qtext_rendered_qtext","rendered_qtext"]
label_list = ["HoverMenu TopicNameLink topic_name","TopicNameLink HoverMenu topic_name"]

f1 = open('query_labels_5.csv', 'w+')


def parse_to_json(raw, uri=""):
    record = {}
    record["url"] = uri
    record["answers"] = []
    record["labels"] = []
    record["related"] = []
    record["answer_count"] = 0
    record["answer"] = ""
    record["question"] = ""
    soup = BeautifulSoup(raw, 'html.parser')
    for title in title_list:
        content = soup.select_one("span[class={0}]".format(title))
        if content != None:
            record["question"] = content.text
            break
    answer_count = soup.select_one("div[class={0}]".format("answer_count"))
    if answer_count != None:
        answer_count = answer_count.text
        if len(answer_count) !=0:
            match = re.findall("\d+",answer_count)
            if len(match) != 0:
                count = match[0]
                record["answer_count"] = (int)(count)
    answer = soup.select_one("div[class={0}]".format("ui_qtext_expanded"))
    if answer != None:
        record["answer"] = answer.text
    labels = soup.find_all(attrs={'class': re.compile(r'\b(HoverMenu|TopicNameLink|topic_name|TopicName)\b')})
    if labels != None:
        for label in labels:
            r = {}
            if len(label.text) == 0:
                continue
            r["label"] = label.text
            r["url"] = label.get("href")
            record["labels"].append(r)

    related = soup.find_all(attrs={'class': 'question_link'})
    if related != None:
        for item in related:
            r = {}
            r["question"] = item.text
            r["url"] = item.get("href")
            record["related"].append(r)

    labels = record["labels"]
    tags = []
    for label in labels:
        if label['url'] is not None:
            print(label['label'])
            # tags.append(label['label'])

    # f1.write(','.join(tags) + "\n")
    print("labels:", record['labels'])
    f1.write(str(record['labels']) + "\n")
    # print(json.dumps(record,ensure_ascii=False))

all_files = os.listdir('crawled')

for file_name in all_files:
    if file_name.startswith("query_content_5"):
        f = open("crawled/" + file_name)

        for line in f.readlines():
            data = json.loads(line)
            print("query:", data['query'])
            f1.write(data['query'].strip() + "\t")
            parse_to_json(data['content'])

