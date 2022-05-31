import requests as requests
from bs4 import BeautifulSoup


def get_language():
    languages = ['english', 'french']
    message = 'Type "en" if you want to translate from French into English,' \
              ' or "fr" if you want to translate from English into French:\n'
    user_input = input(message)
    while user_input not in ['en', 'fr']:
        user_input = input(message)
    if user_input == 'en':
        languages = languages[::-1]
    return tuple(languages)


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
    print('200 OK')
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


def translator():
    language_1, language_2 = get_language()
    word = get_word()
    print_message(language_1, word)
    url = get_url(language_1, language_2, word)
    page = get_page(url)
    translations = get_translations(page)
    examples = get_examples(page)
    print('Translations')
    print(translations)
    print(examples)


if __name__ == '__main__':
    translator()
