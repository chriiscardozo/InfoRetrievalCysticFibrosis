import csv
import numpy as np
from util import *
import time
import csv
from ast import literal_eval
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

READ='LEIA'
WRITE='ESCREVA'
AVAIBLE_INSTRUCTIONS=[READ,WRITE]
X = None
docs_dict = {}
mapping_texts = []
mapping_docs = []
tfidf_dict = {}
vectorizer = TfidfVectorizer()

non_alphabetic_regex = re.compile('[^A-Z]')

def execute_read(file):
	print('\nCarregando arquivo', file)
	with open(file, 'r') as f:
		reader = csv.reader(f, delimiter=';')
		for row in reader:
			term = row[0]
			docs = literal_eval(row[1])
			for d in docs:
				if(d in docs_dict):
					docs_dict[d].append(term)
				else:
					docs_dict[d] = [term]

	for key in docs_dict:
		mapping_docs.append(key)
		final_text = []
		for t in docs_dict[key]:
			term = non_alphabetic_regex.sub('', t)
			if(len(term) > 1):
				final_text.append(term)
		mapping_texts.append(' '.join(final_text))

	print("Calculando TF-IDF")
	X = vectorizer.fit_transform(mapping_texts)
	print("(Linhas, Colunas) da matriz de documentos/termos: ", X.shape)
	return X
	

def execute_write(file, X):
	print("Escrevendo modelo vetorial TF-IDF em", file)
	data = pd.DataFrame(X.todense(), index=mapping_docs, columns=vectorizer.get_feature_names())
	data.to_pickle(file)


def read_configurations(CFG_FILE):
	print("Lendo arquivo de configurações", CFG_FILE)
	i = 0
	X = None
	with open(CFG_FILE, 'r') as f:
		for line in f.readlines():
			i += 1
			line = line.replace('\n','')
			tmp = line.split('=')
			command = tmp[0]
			if(command not in AVAIBLE_INSTRUCTIONS):
				erro("Instrucao incorreta: " + command + " (Linha: " + str(i) + ")")

			if(AVAIBLE_INSTRUCTIONS[i-1] != command):
				erro('Os comandos devem ser executados na ordem: ' + READ + ', ' + WRITE + ' (Linha: ' + str(i) + ")")

			if(command == READ):
				X = execute_read(tmp[1])
			elif(command == WRITE):
				execute_write(tmp[1], X)

def exec(CFG_FILE='cfg/INDEX.CFG'):
	start = time.time()
	print("*** Iniciando Indexador ***")
	read_configurations(CFG_FILE)
	tempo(start, 'indexador')