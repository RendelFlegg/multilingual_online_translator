import requests as requests
from bs4 import BeautifulSoup


def get_language():
    languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
                 '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian',
                 '12': 'russian', '13': 'turkish'}
    print('Hello, welcome to the translator. Translator supports: ')
    for key, value in languages.items():
        print(f'{key}. {value.capitalize()}')
    number_1 = input('Type the number of your language: \n')
    while number_1 not in languages:
        number_1 = input('Type the number of your language: \n')
    number_2 = input('Type the number of language you want to translate to: \n')
    while number_2 not in languages:
        number_2 = input('Type the number of language you want to translate to: \n')
    return languages[number_1], languages[number_2]


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


def translator():
    language_1, language_2 = get_language()
    word = get_word()
    url = get_url(language_1, language_2, word)
    page = get_page(url)
    translations = get_translations(page)
    examples = get_examples(page)
    print_translations(language_2, translations)
    print_examples(language_2, examples)


if __name__ == '__main__':
    translator()
