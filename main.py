import modules.gerador_lista_invertida as gli
import modules.processador_consultas as pc
import modules.indexador as index
import modules.buscador as busca
import sys
import time
from util import tempo

def main():
	start = time.time()
	if('gli' in sys.argv):
		gli.exec()
	if('pc' in sys.argv):
		pc.exec()
	if('index' in sys.argv):
		index.exec()
	if('busca' in sys.argv):
		busca.exec()

	if(len(sys.argv) == 1):
		gli.exec()
		pc.exec()
		index.exec()
		busca.exec()

	tempo(start, 'executar_tudo')

if __name__ == '__main__':
	main()