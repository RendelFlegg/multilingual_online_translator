import requests as requests
from bs4 import BeautifulSoup


def get_language():
    languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
                 '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian',
                 '12': 'russian', '13': 'turkish'}
    translated_languages = []
    print('Hello, welcome to the translator. Translator supports: ')
    for key, value in languages.items():
        print(f'{key}. {value.capitalize()}')
    user_language = input('Type the number of your language: \n')
    while user_language not in languages:
        user_language = input('Type the number of your language: \n')
    user_number = input('Type the number of language you want to translate to: \n')
    while user_number not in languages and user_number != '0':
        user_number = input('Type the number of language you want to translate to: \n')
    if user_number == '0':
        translated_languages = [languages[number] for number in languages if number != user_language]
    else:
        translated_languages.append(languages[user_number])
    return languages[user_language], translated_languages


def get_word():
    return input('Type the word you want to translate:\n')


def print_message(language, word):
    print(f'You chose "{language[:2]}" as a language to translate "{word}".')


def get_url(language_1, language_2, word):
    return f'https://context.reverso.net/translation/{language_1}-{language_2}/{word}'


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    while page.status_code != 200:
        page = requests.get(url, headers=headers)
    return page


def get_translations(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(id='translations-content')
    spans = content.find_all('span', {'class': 'display-term'})
    return [span.text.lstrip() for span in spans]


def get_examples(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(id='examples-content')
    spans = content.find_all('span', {'class': 'text'})
    return [span.text.lstrip() for span in spans]


def print_translations(language, translations):
    print(f'\n{language.capitalize()} Translations:')
    for translation in translations:
        print(translation)
    print()


def print_examples(language, examples):
    examples_tuples = zip(*[iter(examples)]*2)
    print(f'{language.capitalize()} Examples:')
    for example in examples_tuples:
        print(f'{example[0]}:')
        print(example[1])
        print()


def print_dictionary(dictionary):
    for language in dictionary:
        print_translations(language, dictionary[language]['translations'])
        print_examples(language, dictionary[language]['examples'])


def update_dictionary(dictionary, user_language, translated_languages, word):
    multilanguage = len(translated_languages) > 1
    for language in translated_languages:
        url = get_url(user_language, language, word)
        page = get_page(url)
        translations = get_translations(page)
        examples = get_examples(page)
        if multilanguage:
            translations = translations[:1]
            examples = examples[:2]
        dictionary[language] = {'translations': translations, 'examples': examples}


def write_translations(word, language, translations):
    with open(f'{word}.txt', 'a', encoding='utf-8') as f:
        f.write(f'{language.capitalize()} Translations:\n')
        for translation in translations:
            f.write(f'{translation}\n')
        f.write('\n')


def write_examples(word, language, examples):
    examples_tuples = zip(*[iter(examples)]*2)
    with open(f'{word}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{language.capitalize()} Examples:\n')
        for example in examples_tuples:
            f.write(f'{example[0]}:\n')
            f.write(f'{example[1]}\n')
            f.write('\n')


def write_file(dictionary, word):
    for language in dictionary:
        write_translations(word, language, dictionary[language]['translations'])
        write_examples(word, language, dictionary[language]['examples'])


def read_file(word):
    with open(f'{word}.txt', 'r', encoding='utf-8') as f:
        print(f.read())


def translator():
    dictionary = {}
    user_language, translated_languages = get_language()
    word = get_word()
    update_dictionary(dictionary, user_language, translated_languages, word)
    write_file(dictionary, word)
    read_file(word)


if __name__ == '__main__':
    translator()

