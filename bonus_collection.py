import json
import os
import nltk
import ssl
import gensim
from gensim.utils import simple_preprocess
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# #download punkt and stopwords
# nltk.download()

pymorphy2_analyzer = MorphAnalyzer()
stop_words = stopwords.words('russian')
stop_words.extend(["служба", "работа", 'клиент', "год", 'компания', 'рабочий', 'день', 'собеседование', 'требование',
                   'испытательный', 'срок', 'корпоративный'])

category_list = ['official', 'living', 'vacation', 'coworkers', 'office', 'education', 'salary', 'location', 'extra',
                 'growth', 'tasks', 'dms', 'social', 'discount', 'hours', 'disko', 'food', 'remote', 'drive', 'hotel',
                 'tech', 'clothes', 'sport']

with open('specialization_list.json') as data_file:
    file = json.load(data_file)

spec_id_list = []
for item in file:
    for specialization in item['specializations']:
        spec_id = specialization['id']
        spec_id_list.append(spec_id)
print(spec_id_list)


# токенизация и удаление пунктуации
def sentences_to_words(sentences):
    yield gensim.utils.simple_preprocess(sentences, deacc=True)  # deacc=True убирает пунктуацию


def text_lemmatizer(sentences):
    data_words_lemmatized = []
    for sentence in range(len(sentences)):
        sentence_lemms = []
        for word in sentences[sentence]:
            lemma = str(pymorphy2_analyzer.parse(word)[0].normal_form)
            sentence_lemms.append(lemma)
        data_words_lemmatized.append(sentence_lemms)
    return data_words_lemmatized


def remove_stopwords(description):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in description]


def make_bigrams(description):
    bigram = gensim.models.Phrases(description, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return [bigram_mod[doc] for doc in description]


def find_bonus_category(bigram):
    for sentence in bigram:
        for word in sentence:
            official_list = ['тк', 'рф', 'кодекс', 'официальный', 'трудоустройство', 'трудоустроиство', 'оформление']
            if word in official_list:
                jsonText['official'] = 1

            living_list = ['жилье', 'жильё', 'аренда', 'проживание']
            if word in living_list:
                jsonText['living'] = 1

            vacation_list = ['отпуск', 'больничный']
            if word in vacation_list:
                jsonText['vacation'] = 1

            coworkers_list = ['коллектив', 'дружный', 'сотрудник', 'команда']
            if word in coworkers_list:
                jsonText['coworkers'] = 1

            office_list = ['офис', 'территория']
            if word in office_list:
                jsonText['office'] = 1

            education_list = ['школа', 'обучение', 'образование', 'курс', 'стажировка']
            if word in education_list:
                jsonText['education'] = 1

            salary_list = ['заработный', 'плата', 'оклад', 'заработной', 'своевременный', 'стабильный', 'белый', 'доход', 'зарплата', 'зп']
            if word in salary_list:
                jsonText['salary'] = 1

            location_list = ['место', 'центр', 'метро']
            if word in location_list:
                jsonText['location'] = 1

            extra_list = ['выплата', 'поддержка', 'компенсация', 'премия', 'стипендия', 'выслуга', 'бонус']
            if word in extra_list:
                jsonText['extra'] = 1

            growth_list = ['развиваться', 'развитие', 'знание', 'умение', 'рост', 'карьерный']
            if word in growth_list:
                jsonText['growth'] = 1

            tasks_list = ['задача']
            if word in tasks_list:
                jsonText['tasks'] = 1

            dms_list = ['дмс', 'страхование', 'медицинский']
            if word in dms_list:
                jsonText['dms'] = 1

            social_list = ['социальный', 'пакет', 'соц']
            if word in social_list:
                jsonText['social'] = 1

            discount_list = ['скидка']
            if word in discount_list:
                jsonText['discount'] = 1

            hours_list = ['график', 'пятидневный', 'неделя', 'смена', 'полный', 'сдельный', 'вахтовый', 'сменный', 'выездной', 'пятинедельный']
            if word in hours_list:
                jsonText['hours'] = 1

            disko_list = ['мероприятие', 'участие', 'вечеринка', 'корпоратив']
            if word in disko_list:
                jsonText['disko'] = 1

            food_list = ['питание', 'столовый', 'столовая', 'буфет', 'печенье', 'кофе', 'фрукты']
            if word in food_list:
                jsonText['food'] = 1

            remote_list = ['удаленный', 'удалённый']
            if word in remote_list:
                jsonText['remote'] = 1

            drive_list = ['проезд', 'дорога']
            if word in drive_list:
                jsonText['drive'] = 1

            hotel_list = ['путевка', 'путёвка']
            if word in hotel_list:
                jsonText['hotel'] = 1

            tech_list = ['оборудование', 'техника', 'снаряжение']
            if word in tech_list:
                jsonText['tech'] = 1

            clothes_list = ['одежда', 'форма']
            if word in clothes_list:
                jsonText['clothes'] = 1

            sport_list = ['спортивный', 'зал', 'спорт', 'бассейн', 'бассеин', 'фитнес']
            if word in sport_list:
                jsonText['sport'] = 1


for spec in spec_id_list:
    vacancy_list = [f for f in os.listdir('./docs/specialization/{}/'.format(spec))
                    if
                    not f.startswith('.') and os.path.isfile(os.path.join('./docs/specialization/{}/'.format(spec), f))]
    for vacancy in vacancy_list:
        with open('./docs/specialization/{}/{}'.format(spec, vacancy), "r", encoding='utf8') as jsonFile:
            jsonText = json.load(jsonFile)

        bonus_description = jsonText['bonus_description']

        for category in category_list:
            jsonText['{}'.format(category)] = 0

        if bonus_description != '':
            bonus_words = list(sentences_to_words(bonus_description))
            bonus_words = [x for x in bonus_words if x]
            bonus_words_lemmatized = list(text_lemmatizer(bonus_words))
            bonus_words_nostops = remove_stopwords(bonus_words_lemmatized)
            bonus_bigrams = make_bigrams(bonus_words_nostops)
            find_bonus_category(bonus_bigrams)
        else:
            os.remove('./docs/specialization/{}/{}'.format(spec, vacancy))
            print('removed {} vacancy file'.format(vacancy))

        with open('./docs/specialization/{}/{}'.format(spec, vacancy), "w", encoding='utf8') as jsonFile:
            json.dump(jsonText, jsonFile, ensure_ascii=False)
