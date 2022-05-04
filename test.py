import json
import re


with open('specialization_list.json') as data_file:
    file = json.load(data_file)

with open('./docs/specialization/1.10/36636144.json', "r", encoding='utf8') as jsonFile:
    jsonText = json.load(jsonFile)

# description = jsonText['description_cleaned']
# print(description)
# delimiter_list = ['условия', 'гарантируем', 'гарантии', 'предоставляем']
# position_list = []
# no_bonus = 0
# for delimiter in delimiter_list:
#     position_list.append(description.find(delimiter))
# if any(i > 0 for i in position_list):
#     index = position_list.index(min([i for i in position_list if i > 0]))
#     print(position_list)
#     print(index)
#     print(delimiter_list[index])
# else:
#     no_bonus += 1



    # bonus_text = description.split("{}".format(delimiter))
    # if len(bonus_text) >= 2:
    #     print(bonus_text[1])
    #     break

# pattern = re.compile(r'([а-яa-z]((т.п.|т.д.|пр.|г.)|[^?!.\(]|\([^\)]*\))*[.?!])')
# for i, sent in enumerate(pattern.findall(description)):
#     print('[{}]{}'.format(i+1, sent[0]))
