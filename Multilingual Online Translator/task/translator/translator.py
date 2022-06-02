import sys
import requests as requests
from bs4 import BeautifulSoup


class WrongLanguage(Exception):
    def __init__(self, language):
        super().__init__(f"Sorry, the program doesn't support {language}")


class WrongWord(Exception):
    def __init__(self, word):
        super().__init__(f'Sorry, unable to find {word}')


def get_user_language():
    print('Hello, welcome to the translator. Translator supports: ')
    for key, value in languages.items():
        print(f'{key}. {value.capitalize()}')
    user_language = input('Type the number of your language: \n')
    return user_language


def get_user_command():
    user_command = input('Type the number of language you want to translate to: \n')
    while user_command not in [*languages, '0']:
        user_command = input('Type the number of language you want to translate to: \n')
    if user_command == '0':
        user_command = 'all'
    return user_command


def get_languages(user_language, user_command):
    if user_command not in [*languages.values(), 'all']:
        raise WrongLanguage(user_command)
    else:
        translated_languages = []
        if user_command == 'all':
            translated_languages = [languages[number] for number in languages if languages[number] != user_language]
        else:
            translated_languages.append(user_command)
        return translated_languages


def get_word():
    return input('Type the word you want to translate:\n')


def print_message(language, word):
    print(f'You chose "{language[:2]}" as a language to translate "{word}".')


def get_url(language_1, language_2, word):
    return f'https://context.reverso.net/translation/{language_1}-{language_2}/{word}'


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return page
    elif page.status_code == 404:
        word = url[url.rfind('//') + 1:]
        raise WrongWord(word)


def get_translations(page):
    """Parsing translations with gender"""
    soup = BeautifulSoup(page.content, 'html.parser')
    translations = soup.find_all('a', {"class": 'translation'})
    translation_list = [translation.get_text().strip() for translation in translations]
    return translation_list


def get_translations_alt(page):
    """Parsing translations without gender"""
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
    multilingual = len(translated_languages) > 1
    for language in translated_languages:
        url = get_url(user_language, language, word)
        page = get_page(url)
        translations = get_translations(page)
        examples = get_examples(page)
        if multilingual:
            translations = translations[:1]
            examples = examples[:2]
        dictionary[language] = {'translations': translations, 'examples': examples}


def write_translations(word, language, translations):
    with open(f'{word}.txt', 'a', encoding='utf-8') as f:
        f.write(f'{language.capitalize()} Translations:\n')
        for translation in translations:
            f.write(f'{translation.lower()}\n')


def write_examples(word, language, examples):
    examples_tuples = zip(*[iter(examples)]*2)
    with open(f'{word}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{language.capitalize()} Examples:\n')
        for example in examples_tuples:
            f.write(f'{example[0]}:\n')
            f.write(f'{example[1]}\n')
            f.write('\n')
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
    args = sys.argv
    if len(args) == 1:
        user_language = get_user_language()
        user_command = get_user_command()
        word = get_word()
    else:
        user_language = args[1]
        user_command = args[2]
        word = args[3]
    try:
        translated_languages = get_languages(user_language, user_command)
        update_dictionary(dictionary, user_language, translated_languages, word)
        write_file(dictionary, word)
        read_file(word)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    except (WrongLanguage, WrongWord) as err:
        print(err)


languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
             '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian',
             '12': 'russian', '13': 'turkish'}


if __name__ == '__main__':
    translator()

