import requests
import json
import time
import os

# Создание списка с id специализаций

with open('specialization_list.json') as data_file:
    file = json.load(data_file)

spec_id_list = []
for item in file:
    for specialization in item['specializations']:
        spec_id = specialization['id']
        spec_id_list.append(spec_id)
print(spec_id_list)
#
# # Создание папок специализаций
# for i in spec_id_list:
#     directory = "{}/pages".format(i)
#     parent_dir = "/Users/nani/PycharmProjects/vkr/data_parsing/docs/specialization/"
#     path = os.path.join(parent_dir, directory)
#     os.makedirs(path)
#     print("Directory '% s' created" % directory)


def get_page(sid, p):
    params = {
        'specialization': sid,
        'page': p,
        'per_page': 10
    }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data


for spec_id in spec_id_list:
    for page in range(1, 6):
        jsObj = json.loads(get_page(spec_id, page))
        nextFileName = './docs/specialization/{}/pages/{}.json'.format(spec_id, len(os.listdir('./docs/specialization/{}/pages'.format(spec_id))))

        f = open(nextFileName, mode='w', encoding='utf8')
        f.write(json.dumps(jsObj, ensure_ascii=False))
        f.close()

        print(spec_id, page)

        if (jsObj['pages'] - page) <= 1:
            break

        time.sleep(0.1)

print('Страницы поиска собраны')