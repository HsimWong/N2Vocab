# -*- coding:utf-8 -*-
from requests import get
from bs4 import BeautifulSoup as bs
# from openpyxl import Workbook as wb
import openpyxl as opxl
import json
# import json

def get_word_info(word):
	url = 'https://cjjc.weblio.jp/content/' + word
	r = str(get(url).content, 'utf-8')
	bs_obj = bs(r, 'html.parser')
	entries = bs_obj.findAll('div', {'class':"Edrct"})
	word_info = []
	for entry in entries:
		key_list = entry.findAll('p')
		reading = key_list[0].text[3:]
		info = str(key_list[1].text)
		translation = info[4:info.find("中国語品詞")]
		word_type = info[info.find("中国語品詞")+5: info.find('対訳の関係')]
		entry_info = {"reading":reading, "translation":translation, "word_type":word_type}
		word_info.append(entry_info)
	return word_info

def get_word_list():
	word_keys = []
	wb = opxl.load_workbook("./vocab_list.xlsx")
	records = wb['Sheet1'].rows
	for record in records:
		kana = record[1].value
		# print(kana)
		kanji = record[2].value
		# print(kana, end = ',')
		# print(kanji)
		if kanji == None:
			word_keys.append(kana)
		else:
			word_keys.append(kanji)
	return word_keys

if __name__ == '__main__':
	word_keys = get_word_list()
	word_dic = {}
	i = 0
	for word_key in word_keys:
		if i % 20 == 0:
			print(i, end = ",")
		i += 1	
		try:
			word_info = get_word_info(word_key)
			word_dic.update({word_key:word_info})
		except:
			print("%s not found"%word_key)

	# a = {'a':[1,2], 'b':[3,4]}
	with open("dic_info.json", 'w') as f:
            str_info = json.dumps(word_dic, ensur_ascii = False)
            f.write(str_info)
