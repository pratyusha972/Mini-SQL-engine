from collections import OrderedDict
import itertools
import parsing
from parsing import test
global str
import csv
import sys
import re

def fileread(tName,fileData):
	with open(tName,'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			fileData.append(row)


def Display(fileData,columnNames,tableNames,dictionary):
	for data in fileData:
		for col in columnNames:
			print data[dictionary[tableNames[0]].index(col)],
		print


def evaluate(a,tableNames,dictionary,data):
	string = ""
	for i in a:
		if i == '=':
			string += i*2
		elif i in dictionary[tableNames[0]] :
			string += data[dictionary[tableNames[0]].index(i)]
		elif i.lower() == 'and' or i.lower() == 'or':
			string += ' ' + i.lower() + ' '
		else:
			string += i
		
	return string

def distinct(colList,columnName,tableName,dictionary):
	print "OUTPUT:"
	string = tableName + '.' + columnName
	print string
	
	colList = list(OrderedDict.fromkeys(colList))
	for col in range(len(colList)):
		print colList[col]


def aggregate(func,columnName,tableName,dictionary):

	print "hello"
	print "func:" , func
	if columnName == '*':
		sys.exit("error")
	if columnName not in dictionary[tableName]:
		sys.exit("error")

	tName = tableName + '.csv'
	fileData = []
	fileread(tName,fileData)
	colList = []
	for data in fileData:
		colList.append(int(data[dictionary[tableName].index(columnName)]))

	if func.lower() == 'max':
		print max(colList)
	elif func.lower() == 'min':
		print min(colList)
	elif func.lower() == 'sum':
		print sum(colList)
	elif func.lower() == 'avg':
		print sum(colList)/len(colList)
	elif func.lower() == 'distinct':
		distinct(colList,columnName,tableName,dictionary);
	else :
		print "ERROR"
		print "Unknown function : ", '"' + func + '"'

def distinct2(columnNames,tableNames,dictionary):

	list1=[]
	list1.append(columnNames[0][2])
	list1.append(columnNames[1][2])
	columnNames=list1

	header(columnNames,tableNames,dictionary)
	
	temp = []
	check = 0
	for tab in tableNames:
		tName = tab + '.csv'
		with open(tName,'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				i=0
				while i < len(columnNames):
					j=0
					while j < len(dictionary[tableNames[0]]):
						if columnNames[i] == dictionary[tableNames[0]][j]:
							index = j
						j+=1

					x = row[index]
					if x not in temp:
						temp.append(x)
						check =1
						print x,
					i+=1
				if check == 1 :
					check = 0
					print



def metadata(dictionary):
	f = open('metadata.txt','r')
	check = 0
	for line in f:
		if line.strip() == "<begin_table>":
			check = 1
			continue
		if check == 1:
			tableName = line.strip()
			dictionary[tableName] = [];
			check = 0
			continue
		if not line.strip() == '<end_table>':
			dictionary[tableName].append(line.strip());		


def process(dictionary,statetype,columns,tables,where):

	flag=0

	if len(where[0]) > 0:
		flag=1

		if len(where[0][1]) == 1:

			list1=[]
			i=0
			while i < len(where[0][1][0]):
				list1.append(where[0][1][0][i])
				i+=1
			object2 = []
			object2 = list1
		else:
			list2=[]
			i=0
			while i < len(where[0][1][0]):
				list2.append(where[0][1][0][i])
				i+=1
			list2.append(where[0][1][1])
			i=0
			while i < len(where[0][1][2]):
				list2.append(where[0][1][2][i])
				i+=1

			object2 = []
			object2 = list2


	if flag == 1:
		if len(object2) > 1 and len(tables) == 1:    ## checking for where
			object2[1] = (re.sub(' +',' ',object2[1])).strip();
			print "object2[1]:" , object2[1]
		#where(list1,columnNames,tableNames,dictionary)
			Where(object2,columns,tables,dictionary)
			return
		elif len(object2) > 1 and len(tables) > 1:
			object2[1] = (re.sub(' +',' ',object2[1])).strip();
			print "object2[1]:" , object2[1]
			wherejoin(object2,columns,tables,dictionary)
			return

	if(len(tables) > 1):      
		join(columns,tables,dictionary)
		return

	if columns[0][0] == "distinct" and columns[1][0] == "distinct":
		distinct2(columns,tables,dictionary)
		return
	
	if len(columns) == 1 and columns[0] != "*":
		col=columns[0]
		print "col:" , col
		if col[1] == "(" and col[3] == ")":
			print "shit"
			funcName = col[0]
			colName = col[2]
			aggregate(funcName,colName,tables[0],dictionary)
			return
		elif '(' in col or ')' in col:
			sys.exit("Syntax error")

	selectcolumns(columns,tables,dictionary);


def Where(whereStr,columnNames,tableNames,dictionary):
	
	print "yo"
	a=[]
	a = whereStr
	print "a1:" , a

	# print a

	if(len(columnNames) == 1 and columnNames[0] == '*'):
		columnNames = dictionary[tableNames[0]]

	header(columnNames,tableNames,dictionary)

	tName = tableNames[0] + '.csv'
	fileData = []
	fileread(tName,fileData)

	check = 0
	for data in fileData:
		string = evaluate(a,tableNames,dictionary,data)
		for col in columnNames:
			if eval(string):
				check = 1
				print data[dictionary[tableNames[0]].index(col)],
		if check == 1:
			check = 0
			print

def join(columnNames,tableNames,dictionary):
	
	tableNames=tableNames[::-1]

	l1 = []
	l2 = []
	fileread(tableNames[0] + '.csv',l1)
	fileread(tableNames[1] + '.csv',l2)

	fileData = []
	for item1 in l1:
		for item2 in l2:
			fileData.append(item2 + item1)

	dictionary["sample"] = []
	for i in dictionary[tableNames[1]]:
		dictionary["sample"].append(tableNames[1] + '.' + i)
	for i in dictionary[tableNames[0]]:
		dictionary["sample"].append(tableNames[0] + '.' + i)

	dictionary["test"] = dictionary[tableNames[1]] + dictionary[tableNames[0]]
	
	tableNames.remove(tableNames[0])
	tableNames.remove(tableNames[0])
	tableNames.insert(0,"sample")

	if(len(columnNames) == 1 and columnNames[0] == '*'):
		columnNames = dictionary[tableNames[0]]

	for i in columnNames:
		print i,
	print

	for data in fileData:
		for col in columnNames:
			if '.' in col:
				print data[dictionary[tableNames[0]].index(col)],
			else:
				print data[dictionary["test"].index(col)],
		print


def wherejoin(whereStr,columnNames,tableNames,dictionary):

	print "hello"
	tableNames=tableNames[::-1]
	
	l1 = []
	l2 = []
	fileread(tableNames[0] + '.csv',l1)
	fileread(tableNames[1] + '.csv',l2)

	fileData = []
	for item1 in l1:
		for item2 in l2:
			fileData.append(item2 + item1)

	# dictionary["sample"] = dictionary[b] + dictionary[a]
	dictionary["sample"] = []
	for i in dictionary[tableNames[1]]:
		dictionary["sample"].append(tableNames[1] + '.' + i)
	for i in dictionary[tableNames[0]]:
		dictionary["sample"].append(tableNames[0] + '.' + i)

	dictionary["test"] = dictionary[tableNames[1]] + dictionary[tableNames[0]]

	
	tableNames.remove(tableNames[0])
	tableNames.remove(tableNames[0])
	tableNames.insert(0,"sample")

	if(len(columnNames) == 1 and columnNames[0] == '*'):
		columnNames = dictionary[tableNames[0]]

	for i in columnNames:
		print i,
	print

	a = whereStr
	
	
	check = 0
	for data in fileData:
		string = evaluate(a,tableNames,dictionary,data)
		for col in columnNames:
			if eval(string):
				check = 1
				if '.' in col:
					print data[dictionary[tableNames[0]].index(col)],
				else:
					print data[dictionary["test"].index(col)],
		if check == 1:
			check = 0
			print

	del dictionary['sample']

def selectcolumns(columnNames,tableNames,dictionary):



	if len(columnNames) == 1 and columnNames[0] == '*':

		columnNames = dictionary[tableNames[0]]

	for i in columnNames:
		if i not in dictionary[tableNames[0]]:
			sys.exit("error")

	header(columnNames,tableNames,dictionary)

	tName = tableNames[0] + '.csv'
	fileData = []
	fileread(tName,fileData)
	
	Display(fileData,columnNames,tableNames,dictionary)





	
def header(columnNames,tableNames,dictionary):
	
	print "OUTPUT : "
	# Table headers
	string = ""
	for col in columnNames:
		for tab in tableNames:
			if col in dictionary[tab]:
				if not string == "":
					string += ','
				string += tab + '.' + col
	print string



if __name__ == "__main__":
	dictionary = {}
	metadata(dictionary)
	statetype,columns,tables,where=parsing.manualtests()
	process(dictionary,statetype,columns,tables,where)

