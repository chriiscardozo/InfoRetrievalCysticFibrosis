import csv
from util import *
import time
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize

READ='LEIA'
QUERIES='CONSULTAS'
EXPECTEDS='ESPERADOS'
AVAIBLE_INSTRUCTIONS=[READ,QUERIES,EXPECTEDS]

query_dict = {}
expected_list = []

def execute_read(file):
	print('\nCarregando arquivo', file)
	tree = ET.parse(file)
	root = tree.getroot()

	i = 0
	for item in root:
		i += 1
		query_number = item.find('QueryNumber').text
		query_text = item.find('QueryText').text

		tokens = word_tokenize(query_text)
		final_text = []
		for t in tokens:
			normalized = normalize_token(t)
			if(len(normalized) > 0):
				final_text.append(normalized)
		query_dict[query_number] = final_text

		records = item.find('Records')
		j = 0
		for child in records:
			j += 1
			result = [query_number, child.text, len([x for x in child.get('score') if int(x) > 0])]
			expected_list.append(result)
		print(str(j), ' scores de doc relevantes lidos para query', query_number)

	print(str(i), 'queries lidas')

def execute_write_queries(file):
	print("Escrevendo queries lidas em", file)
	with open(file, 'w') as f:
		writer = csv.writer(f, delimiter=';')
		i = 0
		writer.writerow(['QueryNumber','QueryText'])
		for key in query_dict:
			i += 1
			row = [key, query_dict[key]]
			writer.writerow(row)
		print(str(i), 'linhas escritas em', file)

def execute_write_expecteds(file):
	print("Escrevendo resultados esperados lidos em", file)
	with open(file, 'w') as f:
		writer = csv.writer(f, delimiter=';')
		i = 0
		writer.writerow(['QueryNumber','DocNumber', 'DocVotes'])
		for l in expected_list:
			i += 1
			writer.writerow(l)
		print(str(i), 'linhas escritas em', file)

def read_configurations(CFG_FILE):
	print("Lendo arquivo de configurações", CFG_FILE)
	i = 0
	with open(CFG_FILE, 'r') as f:
		for line in f.readlines():
			i += 1
			line = line.replace('\n','')
			tmp = line.split('=')
			command = tmp[0]
			if(command not in AVAIBLE_INSTRUCTIONS):
				erro("Instrucao incorreta: " + command + " (Linha: " + str(i) + ")")

			if(AVAIBLE_INSTRUCTIONS[i-1] != command):
				erro('Os comandos devem ser executados na ordem: ' + READ + ', ' + QUERIES + ', ' + EXPECTEDS + ' (Linha: ' + str(i) + ")")

			if(command == READ):
				execute_read(tmp[1])
			elif(command == QUERIES):
				execute_write_queries(tmp[1])
			elif(command == EXPECTEDS):
				execute_write_expecteds(tmp[1])

def exec(CFG_FILE='cfg/PC.CFG'):
	start = time.time()
	print("*** Iniciando Processador de Consultas ***")
	read_configurations(CFG_FILE)
	tempo(start, 'processador_consultas')