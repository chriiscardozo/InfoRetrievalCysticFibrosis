from unicodedata import normalize
import string
import time
import re
from nltk.stem.porter import *

stemmer = PorterStemmer()

def tempo(start, task, minutes=False):
	den = 1.0
	units = " segundos"
	if(minutes):
		den = 60.0
		units = " minutos\t"

	print("T =",round((time.time()-start)/den), units, " (", task, ")")

def erro(msg, exiting=True):
	print("[Erro]", msg)
	if(exiting): exit(0)


def normalize_token(token, stemming=True):
	token = normalize('NFKD', token).encode('ASCII','ignore').decode('ASCII')
	if(not re.fullmatch('[' + string.punctuation + ']+', token)):
		if(stemming): return stemmer.stem(token).upper()
		else: return token.upper()
	else: return ''
