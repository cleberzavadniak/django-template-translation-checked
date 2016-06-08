#!env python3

import sys
import re

import bs4

"""
Usage:
    pip install bs4
    python3 find-texts-without-trans.py <your-template-file.html>
"""


def clean_template(tpl):
    no_variables = re.sub(r'{{([^}]+)}}', r'VAR(\1)', tpl)
    return re.sub(r'{%([^}]+)%}', r'COMMAND(\1)', no_variables)


def find_not_translated_texts(template):
    soup = bs4.BeautifulSoup(template, 'html.parser')

    for line in soup.text.split('\n'):
        text = line.strip()
        if not text:
            continue

        if ('trans' not in text and
                'COMMAND(' not in text and
                'VAR(' not in text):
            yield text


def print_occurrences(occurrences):
    for occurrence in occurrences:
        print('{}'.format(occurrence))


def main(file_path):
    with open(file_path) as file_object:
        tpl = file_object.read()

    template = clean_template(tpl)
    occurrences = find_not_translated_texts(template)

    print_occurrences(occurrences)


if __name__ == '__main__':
    main(sys.argv[1])
