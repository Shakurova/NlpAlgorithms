# -*- coding: utf-8 -*-

""" Реализация алгоритма вычисления tf-idf. """

import os
import csv
import string
import pymorphy2
from nltk.tokenize import TreebankWordTokenizer
from math import log

files = [f for f in os.listdir('./culture_texts/') if f.endswith('.txt')]

morph = pymorphy2.MorphAnalyzer()
tokenizer = TreebankWordTokenizer()

RUS_LETTERS = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALL_LETTERS_SET = set(list(RUS_LETTERS + string.ascii_lowercase))

TARGET_FILE = '0000'

KEYWORDS = ['оркестр', 'чайковский', 'турне', 'китай', 'пекин', 'тяньцзинь', 'шэньян', 'шанхай', 'нанкин', 'ухань', 'федосеев', 'великобритания', 'концерт']


def open_file(filepath):
	""" Открытие файла. """
	with open(filepath) as sholochov:
		text = sholochov.read()
		return text


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
	# лемматизация
	clean_word_list = set(morph.parse(word)[0].normal_form for word in word_list)

	return clean_word_list


def count_tfidf(KEYWORDS, filename, TARGET_FILE):

	count_word_dict = {}
	count_doc_dict = {}
	tf_dic = {}
	idf_dic = {}
	tfidf_dic = {}

	print('\nCount(w) - сколько раз слово встретилось в документе:')
	for _w in KEYWORDS:
		count_w = 0
		for word in texts_dic[TARGET_FILE]:
			if _w == word:
				count_w += 1
		count_word_dict[_w] = count_w
		print(_w, count_w)

	print('\nCount(doc) - в скольких документах встретилось слово:')
	for _w in KEYWORDS:
		count_doc = 0
		for doc in texts_dic:
			if _w in texts_dic[doc]:
				count_doc += 1
		count_doc_dict[_w] = count_doc
		print(_w, count_doc)

	doc_len = len(texts_dic[TARGET_FILE])
	print('\nДлина текста: ', doc_len)

	N = len(files)
	print('\nОбщее количество документов: ', N)

	print('\nTF = Count(w) / DocLength:')
	for _w in KEYWORDS:
		tf = float(count_word_dict[_w]) / float(doc_len)
		tf_dic[_w] = tf
		print(_w, tf)

	print('\nIDF = log(N / Count(doc)):')
	for _w in KEYWORDS:
		idf = log(float(N) / float(count_doc_dict[_w]))
		idf_dic[_w] = idf
		print(_w, idf)

	print('\nTF-IDF = TF * IDF:')
	for _w in KEYWORDS:
		tfidf = tf_dic[_w] * idf_dic[_w]
		tfidf_dic[_w] = tfidf
		print(_w, tfidf)

	print('Запись результатов в файл...')
	with open(filename, 'w') as tfidf_results:
		writer = csv.writer(tfidf_results, delimiter=str(';'))
		writer.writerow(('Слово', 'Count(w)', 'LengthDoc', 'TF', 'DF', 'Count(doc)', 'IDF', 'TF*IDF'))
		# отсортированный по значениям словарь
		sorted_tfidf = [(k, tfidf_dic[k]) for k in sorted(tfidf_dic, key=tfidf_dic.get, reverse=True)]
		for _w, v in sorted_tfidf:
			writer.writerow((str(_w), str(count_word_dict[_w]), str(doc_len), str(tf_dic[_w]), str(N),
							str(count_doc_dict[_w]), str(idf_dic[_w]), str(tfidf_dic[_w])))

	return count_word_dict, count_doc_dict, doc_len, N, tf_dic, idf_dic, tfidf_dic

if __name__ == '__main__':

	vocabulary = []  # все уникальные слова документа
	texts_dic = {}  # словарь: название текста: сет его слов

	for f in files:
		text = open_file('./culture_texts/' + str(f))
		clean_word_list = text_to_words(text)
		for _o in clean_word_list:
			vocabulary.append(_o)
		texts_dic[f[-8:-4:]] = clean_word_list

	print('Вычисление TF*IDF для ключевых слов...')
	count_tfidf(KEYWORDS, 'tfidf_culture_results.csv', TARGET_FILE)

	print('Вычисление TF*IDF для всех слов текста')
	count_tfidf(texts_dic[TARGET_FILE], 'tfidf_culture_results_all.csv', TARGET_FILE)
