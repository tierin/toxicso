import xml.etree.ElementTree as ET
import json

context = ET.iterparse('data/xmltest.xml', events=('end',))

num = 0
all_tags = {}

# я не смогла разобраться с возникающей ошибкой
try:
    for event, elem in context:
            if elem.get('PostTypeId') == '1':
                tags = elem.get('Tags')
                all_tags[elem.get('Id')] = tags
                num += 1
except ET.ParseError:
    pass
with open('data/all_tags.json', 'w') as f:
    json.dump(all_tags, f)

