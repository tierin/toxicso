import xml.etree.ElementTree as ET
import json

context = ET.iterparse('data/xmltest.xml', events=('end',))

num = 0
all_tags = {}

try:
    for event, elem in context:
        if elem.get('PostTypeId') == '2':
            parent_id = elem.get('ParentId')
            all_tags[elem.get('Id')] = parent_id
            num += 1
except ET.ParseError:
    pass
with open('data/all_answers_ids.json', 'w') as f:
    json.dump(all_tags, f)

