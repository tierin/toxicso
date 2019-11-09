import json
import re
import xml.etree.ElementTree as ET


context = ET.iterparse(r'data/Posts.xml', events=('end', ))
so_data = []

with open('data/all_tags.json', 'r') as t:
    tags = json.load(t)
num = 0
num2 = 0
index = 1
try:
    for event, elem in context:
        if re.match('2019', elem.get('CreationDate')):
            break
        if re.match('2017|2018', elem.get('CreationDate')) and elem.get('PostTypeId') == '2':
            text = elem.get('Body')
            text = re.sub('<.*?>', '', text)
            text = re.sub('\n+', '', text)
            so_data.append({'Score': elem.get('Score'), 'Body': text, 'Tags': tags[elem.get('ParentId')]})
            num += 1
            if num % 1000 == 0:
                print(elem.get('CreationDate'))
            if num % 10000 == 0:
                with open('posts2018/so_posts_2017_18_{}.json'.format(index), 'w') as com:
                    json.dump(so_data, com)
                index += 1
                so_data = []
        else:
            num2 += 1
            if num2 % 100 == 0:
                print('100')
except:
    pass

with open('posts2018/so_posts_2017_18_last.json', 'w') as com:
    json.dump(so_data, com)
