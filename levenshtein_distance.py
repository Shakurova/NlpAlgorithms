# -*- coding: utf-8 -*-

import numpy
import string
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()
RUS_LETTERS = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALL_LETTERS_SET = set(list(RUS_LETTERS + string.ascii_lowercase))

string1 = 'distance'
string2 = 'ditsance'


def text_to_words(text_text):
	""" Нормализация текста, преобразование текста твита в склеенные пробелом леммы. """
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

	return word_list


def levenshtein_distance(string1, string2):
	""" Реализация алгоритма подсчета расстояние Левенштейна. """
	matrix = numpy.zeros((len(string1) + 1, len(string2) + 1))
	for _l1 in range(0, len(string1) + 1):
		for _l2 in range(0, len(string2) + 1):
			if _l1 == 0 and _l2 == 0:
				matrix[_l1, _l2] = 0
			elif _l1 == 0 and _l2 > 0:
				matrix[_l1, _l2] = _l2
			elif _l2 == 0 and _l1 > 0:
				matrix[_l1, _l2] = _l1
			elif _l1 > 0 and _l2 > 0:
				if string1[_l1-1] == string2[_l2-1]:
					m = 0
					matrix[_l1, _l2] = min(matrix[_l1, _l2-1]+1, matrix[_l1-1, _l2]+1, matrix[_l1-1, _l2-1] + m)
				else:
					m = 1
					matrix[_l1, _l2] = min(matrix[_l1, _l2-1]+1, matrix[_l1-1, _l2]+1, matrix[_l1-1, _l2-1] + m)
	return matrix


def levenshtein_distance_improved(string1, string2):
	""" Реализация алгоритма подсчета расстояние Левенштейна. """
	matrix = numpy.zeros((len(string1) + 1, len(string2) + 1))
	for _l1 in range(0, len(string1) + 1):
		for _l2 in range(0, len(string2) + 1):

			if _l1 == 0 and _l2 == 0:
				matrix[_l1, _l2] = 0

			elif _l1 == 0 and _l2 > 0:
				matrix[_l1, _l2] = _l2

			elif _l2 == 0 and _l1 > 0:
				matrix[_l1, _l2] = _l1

			elif _l1 > 0 and _l2 > 0:

				if string1[_l1-1] == string2[_l2-1]:
					m = 0
					matrix[_l1, _l2] = min(matrix[_l1, _l2-1]+1, matrix[_l1-1, _l2]+1, matrix[_l1-1, _l2-1] + m)

				elif string1[_l1-2] == string2[_l2-1] and string1[_l1-1] == string2[_l2-2]:
					m = 1
					matrix[_l1, _l2] = min(matrix[_l1-1, _l2-2]+1, matrix[_l1-2, _l2-1]+1, matrix[_l1-2, _l2-2] + m)

				else:
					m = 1
					matrix[_l1, _l2] = min(matrix[_l1, _l2-1]+1, matrix[_l1-1, _l2]+1, matrix[_l1-1, _l2-1] + m)
	return matrix

print(levenshtein_distance(string1, string2))
print('*'*30)
print(levenshtein_distance_improved(string1, string2))
print('Расстояние Левенштейна для слов', string1, string2, 'равно', int(levenshtein_distance_improved(string1, string2)[len(string1), len(string2)]))


print('Создание словаря')
word_set = set()
with open('war_and_peace.txt') as vocab:
	for line in vocab:
		words = text_to_words(line)
		for _w in words:
			if _w != '':
				word_set.add(_w)


text = 'Пьер, приехав вперед, как домашний человек, рпошел в кабинед князь Андрея и тотчас же, по привычке, ' \
	   'лег на диван, взл первую попавшуюся с плки книг (это были Записки Цезаря) и принился, облокотившись, ' \
	   'читать ее из середины.'

clean_text = []
for _w in text_to_words(text):
	if _w in word_set:
		clean_text.append(_w)
	else:
		lev = 15
		for v in word_set:
			if int(levenshtein_distance_improved(_w, v)[len(_w), len(v)]) < lev:
				lev = min(lev, int(levenshtein_distance_improved(_w, v)[len(_w), len(v)]))
				nearest = v
		clean_text.append(nearest)


print('Исправленный текст: ', ' '.join(clean_text))

