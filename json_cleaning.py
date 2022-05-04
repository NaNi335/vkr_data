import json
import re
import os
import unicodedata

with open('specialization_list.json') as data_file:
    file = json.load(data_file)

spec_id_list = []
empty_bonus_list = []
bonus_descriptions_file = open('bonus_descriptions.txt', 'a')
bonus_list = []

for item in file:
    for specialization in item['specializations']:
        spec_id = specialization['id']
        spec_id_list.append(spec_id)
print(spec_id_list)


def remove_params(json_text):
    params_to_remove = ('premium', 'billing_type', 'relations', 'insider_interview', 'response_letter_required',
                        'allow_messages', 'site', 'response_url', 'code', 'hidden', 'quick_responses_allowed',
                        'accept_incomplete_resumes', 'negotiations_url', 'suitable_resumes_url', 'apply_alternate_url',
                        'has_test')
    for p in params_to_remove:
        json_text.pop(p, None)


def remove_html_tags(string):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', string)


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'[]', string)


def clean_description(json_text):
    cleaned_text = remove_html_tags(json_text['description'])
    cleaned_text = str.lower(cleaned_text)
    cleaned_text = remove_emoji(cleaned_text)
    cleaned_text = cleaned_text.replace('&quot', '')
    cleaned_text = unicodedata.normalize("NFKC", cleaned_text)
    return cleaned_text


def find_bonus_description(description):
    delimiter_list = ['условия', 'гарантируем', 'гарантии', 'предоставляем', 'предлагаем', 'почему к нам',
                      'наше предложение', 'работа у нас - это', 'тк рф', 'у вас будет', 'мы можем предложить',
                      'получаешь', 'предложить', 'работать в Nexign – это значит']
    position_list = []
    for delimiter in delimiter_list:
        position_list.append(description.find(delimiter))
    if any(i > 0 for i in position_list):
        bonus_list.append(vacancy)
        index = position_list.index(min([i for i in position_list if i > 0]))
        description_parts = description.split("{}".format(delimiter_list[index]))
        bonus_text = description_parts[1]
    else:
        empty_bonus_list.append(vacancy)
        bonus_text = ''
    return bonus_text, empty_bonus_list


for spec in spec_id_list:
    vacancy_list = [f for f in os.listdir('./docs/specialization/{}/'.format(spec))
                    if not f.startswith('.') and os.path.isfile(os.path.join('./docs/specialization/{}/'.format(spec), f))]
    for vacancy in vacancy_list:
        with open('./docs/specialization/{}/{}'.format(spec, vacancy), "r", encoding='utf8') as jsonFile:
            jsonText = json.load(jsonFile)

        remove_params(jsonText)
        cleaned_description = clean_description(jsonText)
        bonus_description, empty_bonus_list = find_bonus_description(cleaned_description)

        jsonText['description_cleaned'] = '{}'.format(cleaned_description)
        jsonText['bonus_description'] = '{}'.format(bonus_description)

        bonus_descriptions_file.write(bonus_description)
        bonus_descriptions_file.write('\n')

        with open('./docs/specialization/{}/{}'.format(spec, vacancy), "w", encoding='utf8') as jsonFile:
            json.dump(jsonText, jsonFile, ensure_ascii=False)

    print(spec)
print(len(bonus_list))
print(len(empty_bonus_list))
print(empty_bonus_list)


