#from truths import *
import re
import time
import numpy as np
from tt import BooleanExpression,TruthTable,to_primitives
from prettytable import PrettyTable

start_time = time.time()
def createTestVariables(entries):
	testVariables = []
	finalMatrix = []
	nvar = len(entries)
	if nvar <2:
		return print("Not enough arguments generate test inputs")
	
	for i in range((2**nvar), 0 , -1):
		aux = bin(pow(2,nvar)-i)
		aux = aux[2:]
		testVariables.append(aux)
	

	for line in range(0,len(testVariables)):
		zerosToFill = nvar - len(testVariables[line])
		if zerosToFill > 0:
			tempList = []
			for x in range(0,zerosToFill):
				tempList.append('0')
			for newaux in testVariables[line]:
				tempList.append(newaux)
			#print(tempList)	
			
			finalMatrix.append(tempList)

		else:
			tempList = list(testVariables[line]) 
			finalMatrix.append(tempList)

	finalMatrix = np.matrix(finalMatrix, dtype = 'int')
	return finalMatrix

def getTruthTables(archive = 'circuito.txt'):
	with open(archive, 'r') as myfile:
	    data=myfile.read().strip()
	    myfile.close()
	data = data.split('\n')
	originalData = data.copy()


	#Aqui é gerado um CIRCUITO IDEAL e um CIRCUITO COM FALHA, a partir da descrição de um circuito com falha
	#O cicuito ideal trata p0 como uma porta funcionando, enquanto que o com falha atribui 0 a qualquer valor da porta.
	for line in range(len(data)):
		if (data[line].find('p0') != -1) and (data[line].find('p1') != -1):
			dataaux = data[line].replace('p0', '0')
			dataaux = dataaux.replace('p1', '1')
			data.append(dataaux)
		else:				
			if (data[line].find('p1') != -1) and (data[line].find('p0') < 0):
				dataaux = data[line].replace('p1', '1')				
				data.append(dataaux)
			if (data[line].find('p0') != -1) and (data[line].find('p1') < 0):
				dataaux = data[line].replace('p0', '0')				
				data.append(dataaux)
	results = []
	symbol  = []
	saidas = []
	#Aqui é separado a expressão lógica da igualdade: [S=(entrada <Operação> entrada)] vira [S][entrada <Operação> entrada]
	for line in range(len(data)):
		data[line] = data[line].split('=')
		saidas.append(data[line][0])
		data[line].pop(0)
	for line in range(len(data)):
		symbol.append(BooleanExpression(data[line][0]).symbols)
		results.append(TruthTable(str(data[line][0])).results)
	return results, symbol, saidas, data, originalData

results, symbols, saidas, data, originalData = getTruthTables()


finalMatrices = []
prettytables = []

for i in range(len(results)):
	s = createTestVariables(symbols[i])
	#print(s,results)
	mymatrix = np.column_stack((s,results[i]))
	mymatrix = np.array(mymatrix)
	finalMatrices.append(mymatrix)
	prettyaux = PrettyTable()
	prettyaux.field_names = np.hstack((symbols[i],saidas[i]))
	for j in mymatrix:
		prettyaux.add_row(j)
	prettytables.append(prettyaux)


with open('saída.txt', 'w') as myfile:
	for i in range(len(prettytables)):
		myfile.write("Análise do circuito\n\nFunção lógica: {0}\n\nTabela verdade:\n{1}\n\n#################################################\n\n".format(str(saidas[i])+'='+str(data[i][0]), prettytables[i]))
	myfile.write("\n\nTEMPO DE EXECUÇÃO: {0} SEGUNDOS\n\n".format(time.time() - start_time))
	myfile.close()

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def diagnosticoFalha(data = originalData):
	fail = 0
	newtime=time.time()
	saidas=[]
	exprComFalha = ''
	tabComFalha = 0
	for line in originalData:
		data = line.split('=')
		saidas.append(data[0])
		data.pop(0)
		tabSemFalha = TruthTable(data[0])
		expr = data[0].replace('p0', 'Z')
		expr = expr.replace('p1','Z')
		newexpr = BooleanExpression(expr)
		if (data[0].find('p0') != -1):
			exprComFalha = data[0].replace('p0', '0')
			#print(exprComFalha)
			tabComFalha = TruthTable(exprComFalha)
			fail = 1
		elif (data[0].find('p1') != -1):
			exprComFalha = data[0].replace('p1', '1')
			#print(exprComFalha)
			tabComFalha = TruthTable(exprComFalha)
			fail = 1
		else:
			with open('Diagnostico.txt', 'w') as diagnosefail:
				diagnosefail.write("Não há falhas para se diagnosticar.")
				diagnosefail.close()
				continue
		with open('Diagnostico.txt', 'w') as diagnosefail:
			diagnosefail.write("######### Análise do Circuito: {} #########\n\n".format(saidas[0]+'='+data[0]))
			for s in newexpr.symbols:
				ocorrencias = findOccurrences(expr,s)
				for o in ocorrencias:
					templist = list(''.join(expr))
					templist[o] = '1'
					finalExpr = ''.join(templist)
					tempTruth = TruthTable(finalExpr)
					if (len(tabComFalha.results) == (len(tempTruth.results))):
						if tabComFalha.equivalent_to(tempTruth):
							finalExpr = finalExpr.replace('Z', 'XX')
							finalExpr = finalExpr.replace('1', 'PortaPresaEm1')
							diagnosefail.write("-> Possível falha para o circuito: {}\n".format(finalExpr))
					print("Expressão: {}\n {} \n Falha: {}\n".format(finalExpr,tempTruth,tabComFalha))
					templist = list(''.join(expr))
					templist[o] = '0'
					finalExpr = ''.join(templist)
					tempTruth = TruthTable(finalExpr)
					if (len(tabComFalha.results) == (len(tempTruth.results))):
						if tabComFalha.equivalent_to(tempTruth):
							finalExpr = finalExpr.replace('Z', 'XX')
							finalExpr = finalExpr.replace('0', 'PortaPresaEm0')
							diagnosefail.write("-> Possível falha para o circuito: {}\n".format(finalExpr))


					print("Expressão: {}\n {} \n Falha: {}\n".format(finalExpr,tempTruth,tabComFalha))
			diagnosefail.write("\n\nTempo de execução do diagnóstico: {} segundos.".format(time.time() - newtime))
			diagnosefail.close()
			
		
	
	#print(saidas)
diagnosticoFalha()