import json
import re
import xml.etree.ElementTree as ET


context = ET.iterparse('data/Comments.xml', events=('end', ))
so_data = []

with open('data/all_tags.json', 'r') as t:
    tags = json.load(t)

with open('data/all_answers_ids.json', 'r') as t:
    answers_ids = json.load(t)


num = 0
num2 = 0
index = 1
for event, elem in context:
    try:
        if re.match('2019', elem.get('CreationDate')):
            break
        if re.match('2017|2018', elem.get('CreationDate')):
            text = elem.get('Text')
            text = re.sub('<.*?>', '', text)
            text = re.sub('\n+', '', text)
            if tags.get(elem.get('PostId')) is not None:
                tag = tags[elem.get('PostId')]
            else:
                a = answers_ids[elem.get('PostId')]
                tag = tags[answers_ids[elem.get('PostId')]]
            so_data.append({'Score': elem.get('Score'), 'Body': text, 'Tags': tag})
            num += 1
            if num % 1000 == 0:
                print(elem.get('CreationDate'))
            if num % 10000 == 0:
                with open('comments2018/so_comments{}.json'.format(index), 'w') as com:
                    json.dump(so_data, com)
                index += 1
                so_data = []

    except (KeyError, TypeError) as E:
        print(E)
        continue

with open('comments2018/so_comments_last.json', 'w') as com:
    json.dump(so_data, com)
