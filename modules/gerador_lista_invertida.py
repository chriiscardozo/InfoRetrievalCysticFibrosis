import csv
import time
from util import *
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize

READ='LEIA'
WRITE='ESCREVA'
AVAIBLE_INSTRUCTIONS=[READ, WRITE]

inverse_dict = {}

def execute_read(file):
	print('\nCarregando arquivo', file)
	tree = ET.parse(file)
	root = tree.getroot()

	i_lidos = 0
	i_sem_text = 0
	for item in root:
		i_lidos += 1
		record_num = item.find('RECORDNUM').text.strip()
		text = ''

		if(item.find('ABSTRACT') is not None):
			text = item.find('ABSTRACT').text
		elif(item.find('EXTRACT') is not None):
			text = item.find('EXTRACT').text
		else:
			erro('Registro nao contem campo ABSTRACT ou EXTRACT (' + record_num + ')', False)
			i_sem_text += 1
			continue
		tokens = word_tokenize(text)
		for t in tokens:
			normalized = normalize_token(t)
			if(len(normalized) > 0):
				if(normalized in inverse_dict):
					inverse_dict[normalized].append(record_num)
				else:
					inverse_dict[normalized] = [record_num]

	print('Leu', str(i_lidos), 'registros (',str(i_sem_text),'sem ABSTRACT/EXTRACT ). Total:',str(i_lidos - i_sem_text ))
	print(str(len(inverse_dict.keys())), 'tokens encontrados ate o momento')
	print('\n')

def execute_write(file):
	print('Escrevendo resultados em', file)

	with open(file, 'w') as f:
		writer = csv.writer(f, delimiter=';')
		i = 0
		for key in inverse_dict:
			i += 1
			row = [key, [int(x) for x in inverse_dict[key]]]
			writer.writerow(row)
		print(str(i), 'linhas escritas em', file)

def read_configurations(CFG_FILE):
	print("Lendo arquivo de configurações", CFG_FILE)
	i = 0
	write_executed = False
	with open(CFG_FILE, 'r') as f:
		for line in f.readlines():
			i += 1
			line = line.replace('\n','')
			tmp = line.split('=')
			command = tmp[0]
			if(command not in AVAIBLE_INSTRUCTIONS):
				erro("Instrucao incorreta: " + command + " (Linha: " + str(i) + ")")

			if(command == READ):
				if(write_executed): erro('Não pode executar ' + READ + ' depois de WRITE (Linha: ' + str(i) + ")")
				execute_read(tmp[1])
			elif(command == WRITE):
				if(write_executed): erro('Apenas um comando ' + WRITE + ' deve ser executado (Linha: ' + str(i) + ")")
				write_executed = True
				execute_write(tmp[1])

def exec(CFG_FILE='cfg/GLI.CFG'):
	start = time.time()
	print("*** Iniciando Gerador de Lista Invertida ***")
	read_configurations(CFG_FILE)
	print(tempo(start, 'gerador_lista_invertida'))