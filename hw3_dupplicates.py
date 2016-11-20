# -*- coding: utf-8 -*-

import os
from simhash import Simhash

"""

 Наша программа работает с файлами в формате .txt, скачанными краулерами и уже очищенными от html тегов.
 Программа поочередно открывает файлы, приводит к нижнему регистру и заменяет одинаковые графемы для латиницы и
 кириллицы на кириллицу. Далее программа попарно сравнивает содержимое файлов с использованием алгоритма simhash
 (файлы сравниваются за минимальное количество операций) и для каждой пары говорит, являются ли они дубликатами.

  Поиск дубликатов выявляет случаи полного совпадения, когда:
  1. файл является полной копией
  2. файл представляет собой удвоенную копию
  3. файлы отличаются только порядком абзацев
  4. файлы отличаются пунктуацией и количеством пробелов
  5. файл отличается от исходного графемой (латиница vs кириллица)
  6. файлы отличаются регистром

"""

files = [f for f in os.listdir('./') if f.endswith('.txt')]
# print(files)


def open_file(filepath):
	"""Открытие файлв"""
	with open(filepath) as rabbits:
		text = rabbits.read()
		return text


def text_cleanization(text):
	"""Замена английские буквы на русские."""
	text = text.lower()
	text = text.replace('a', 'а')
	text = text.replace('e', 'е')
	text = text.replace('y', 'у')
	text = text.replace('o', 'о')
	text = text.replace('p', 'р')
	text = text.replace('x', 'х')
	text = text.replace('c', 'с')
	return text


if __name__ == '__main__':
	for _i in range(0, len(files)):
		text1 = open_file(files[_i])
		text1 = text_cleanization(text1)
		for _a in range(_i+1, len(files)):
			text2 = open_file(files[_a])
			text2 = text_cleanization(text2)
			if Simhash(text1).distance(Simhash(text2)) == 0:
				print(str(files[_i]) + ' ' + str(files[_a]) + ' - ДУБЛИКАТ')
			else:
				print(str(files[_i]) + ' ' + str(files[_a]) + ' - НЕ ДУБЛИКАТ')
