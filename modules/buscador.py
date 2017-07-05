import csv
from ast import literal_eval
import time
from util import *
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

MODEL='MODELO'
QUERIES='CONSULTAS'
RESULTS='RESULTADOS'
AVAIBLE_INSTRUCTIONS=[MODEL,QUERIES,RESULTS]

def execute_model(file):
	print('\nCarregando arquivo de modelo', file)
	return pd.read_pickle(file)

def execute_queries(file):
	print('\nCarregando arquivo de queries')
	queries = {}

	with open(file, 'r') as f:
		reader = csv.reader(f, delimiter=';')

		next(reader) # pass the header stuff
		for row in reader:
			query_id = row[0]
			values = literal_eval(row[1])

			queries[query_id] = values
	return queries

def execute_results(file, df, queries):
	print('\nCalculando ranking usando todas dimensões')

	feature_names = df.columns.values.tolist()
	docs_index = []
	tfidf = []

	for row in df.iterrows():
		index, data = row
		docs_index.append(index)
		tfidf.append(data.tolist())


	with open(file, 'w') as f:
		writer = csv.writer(f, delimiter = ';')

		i = 1
		total = len(queries)
		for q_id in queries:
			
			print('Query', str(i), 'de', str(total))
			i += 1
			doc_ids = []
			rank = []
			query = queries[q_id]
			
			vec_query = []
			for w in feature_names:
				if w.upper() in query: vec_query.append(1)
				else: vec_query.append(0)

			for index, vec_doc in enumerate(tfidf):
				sim = cosine_similarity(np.array([vec_query]), np.array([vec_doc]))
				doc_ids.append(index)
				rank.append(sim[0][0])

			rank, doc_ids = (list(t) for t in zip(*sorted(zip(rank, doc_ids))))
			rank.reverse()
			doc_ids.reverse()

			for pos, doc_id in enumerate(doc_ids):
				writer.writerow([q_id, [(pos+1), doc_id, rank[pos]]])

def read_configurations(CFG_FILE):
	print("Lendo arquivo de configurações", CFG_FILE)
	i = 0

	df = None
	queries = {}
	with open(CFG_FILE, 'r') as f:
		for line in f.readlines():
			i += 1
			line = line.replace('\n','')
			tmp = line.split('=')
			command = tmp[0]
			if(command not in AVAIBLE_INSTRUCTIONS):
				erro("Instrucao incorreta: " + command + " (Linha: " + str(i) + ")")

			if(command == MODEL):
				df = execute_model(tmp[1])
			elif(command == QUERIES):
				queries = execute_queries(tmp[1])
			elif(command == RESULTS):
				execute_results(tmp[1], df, queries)

def exec(CFG_FILE='cfg/BUSCA.CFG'):
	start = time.time()
	print("*** Iniciando Buscador ***")
	read_configurations(CFG_FILE)
	tempo(start, 'buscador')