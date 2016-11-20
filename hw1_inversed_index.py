# -*- coding: utf-8 -*-

import os
import csv
import string
import pymorphy2
from nltk.tokenize import TreebankWordTokenizer
from stop_words import get_stop_words

morph = pymorphy2.MorphAnalyzer()
tokenizer = TreebankWordTokenizer()

RUS_LETTERS = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALL_LETTERS_SET = set(list(RUS_LETTERS + string.ascii_lowercase))


files_sholovhov = [f for f in os.listdir('./') if f.endswith('.txt')]


def open_file(filepath):
	""" Открытие файла. """
	with open(filepath) as sholochov:
		text = sholochov.read()
		return text


def text_to_words(text_text):
	""" Нормализация текста. """
	# привод к нижнему регистру
	text_text = text_text.lower()
	# очищение от не-букв
	letters_only = ''
	for _c in text_text:
		if _c in ALL_LETTERS_SET:
			letters_only += _c
		else:
			letters_only += ' '
	# удаление множественных пробелов
	while '  ' in letters_only:
		letters_only = letters_only.replace('  ', ' ')
	# токенизация
	word_list = tokenizer.tokenize(letters_only)
	# лемматизация
	clean_word_list = (morph.parse(word)[0].normal_form for word in word_list)
	# удаление стоп-слов
	clean_word_list = set(word for word in clean_word_list if word not in get_stop_words('ru'))

	return clean_word_list


if __name__ == '__main__':
	vocabulary = []  # все уникальные слова документа
	texts = []  # массив сетов текстов

	print('Создание сетов')
	for _i in range(0, len(files_sholovhov)):
		text = open_file(files_sholovhov[_i])
		clean_word_list = text_to_words(text)
		for _o in clean_word_list:
			vocabulary.append(_o)
		texts.append(clean_word_list)

	print('Запись в файл')
	with open('inveresed_index.csv', 'w') as ii:
		ii_writer = csv.writer(ii, delimiter='\t')
		ii_writer.writerow(['Слово', 'Документы'])
		for _w in vocabulary:
			c = []
			for _t in texts:
				if _w in _t:
					c.append(str(texts.index(_t)))
			ii_writer.writerow([_w, ','.join(c)])
