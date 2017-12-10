# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:59:28 2017

@author: hp
"""
import re
from collections import defaultdict
from os.path import exists
# Regex rules for matching different types of tokens
rules = [																														
			(r'[\"][^\"]*?[\"]|[\'][^\']*?[\']',																		    					'LITERAL: STRING'),
			(r'\-?\b\d*\.\d+\b',												    							 								'LITERAL: DOUBLE'),
			(r'\-?\b\d+\b',												     																	'LITERAL: INT'),
			(r'\bint\b|\bdouble\b|\bbool\b|\bstruct\b|\bchar\b|\bstring\b',																		'KEYWORD: ELEMENTARY DATATYPE'),
			(r'\bvector\b|\bset\b|\btree\b|\blist\b|\bqueue\b|\bstack\b|\bdataContainer\b|\bmodel\b|\btestResults\b|\bclassificationModel\b',	'KEYWORD: COMPLEX DATATYPE'),
			(r'\bprintf\b|\bscanf\b|\bsigma\b|\bsigmoid\b|\bexp\b|\bconnect\b',																	'KEYWORD: STANDARD FUNCTION'),
			(r'\btrainModel\b|\btestModel\b|\bclassify\b|\bloadModelFromFile\b|\bsaveModelToFile\b|\bclassifyFromFile\b',						'KEYWORD: MODEL FUNCTION'),
			(r'\bget\b|\bput\b|\bpost\b|\bdelete\b',																							'KEYWORD: HTTP FUNCTION'),
			(r'\bfor\b|\bwhile\b|\bdo\b|\buntilConverge\b|\brange\b|\biterator\b',																'KEYWORD: ITERATION'),
			(r'\bif\b|\belse\b|\bswitch\b|\bcase\b|\bcontinue\b|\bbreak\b|\breturn\b|\bin\b',													'KEYWORD: DECISION/BRANCH STATEMENT'),
			(r'\baudio\b|\bimage\b|\bcsv\b|\btxt\b|\bxls\b',																					'KEYWORD: EXTENDED TYPE'),
			(r'\bANN\b|\bRGD\b|\bnaiveBayes\b|\bKNN\b',																							'KEYWORD: MODEL TYPE'),
			(r'\bfrom\b|\bimport\b|\bvoid\b|\btrue\b|\bfalse\b|\bnonBlocking\b|\bdatabase\b',													'KEYWORD: OTHERS'),		
			(r'\+\+|\-\-|\^\=|\|\||\&\&|\!\=|\=\=|\?|\:\=',                   																	'OPERATORS: COMPLEX'),
			(r'\-|\+|\/|\*|\^|\||\&|\=|\<|\>|\!',                   																			'OPERATORS: SIMPLE'),
			(r'\{|\}|\[|\]|\(|\)|\;|\,|\.|\:',                                                         											'DELIMITERS'),   
			(r'(?<=\s)[a-zA-Z][a-zA-Z0-9_]*',                                                            										'IDENTIFIERS')
]

# To analyse tokens and store the output in a new file "outputf"
def lexAnalyser(file, outputf):

	# to remove multi comments
	multiComments = re.compile('\/\*(.|\s)*?\*\/') 						# regex for matching C style multiline comments
	while multiComments.search(file) is not None:
		mlc = multiComments.search(file)		   						# mlc contains first occurence of multiline comment in the code
		linesInComment = 0
		if mlc != None:
			mlc = mlc.group()
			linesInComment = len(re.findall('\n',mlc)) 						# finding no. of lines spanned by multiline comment mlc
		file = multiComments.sub(" %s"%('\n'*linesInComment), file, 1) 	# replacing the multiline comment by its line span

	# To remove single-line comments
	singleComments = re.compile('\/\/(.*)')								# regex for matching C style single line comments
	file = singleComments.sub(' ', file) 								# replacing all single line comments with a whitespace

	tokens = defaultdict(lambda: defaultdict(list)) 						# tokens[tokenType][lineNumber] is a list of tokens of tokenType in lineNumber
	# To get all the tokens
	lines = file.split('\n')												# lines is a list of lines in the code
	presentLine = 1															# starting with line number 1
	for line in lines:
		linecode = ' ' + line 												# adding a whitespace before every line for easily matching identifiers
		for rule, tokenType in rules:
			tokens[tokenType][presentLine] = re.findall(rule, linecode)		# for every rule in rules list(line 12), storing all matches in dictionary
			substitute = re.compile(rule)
			linecode = substitute.sub(' ', linecode)						# replacing the matches with a whitespace in the code(line code)
		linecode = linecode.strip()
		if linecode != '':													# if linecode is not empty after stripping whitespace, the
			tokens['Lex Errors'][presentLine] = [linecode]				# remaining content has not matched any rule of the language and is a lexical error
		presentLine = presentLine + 1

	
	output = open(outputf, 'w')
	# Might overwrite contents of existing files, in write mode.


	# Writing tokens category wise
	for rule, tokenType in rules:
		output.write('%r:\n' % tokenType)
		pos = output.tell()
		for i in range(1, presentLine ):   
			if tokens[tokenType][i] != []:
				output.write('\tIn line %d: %r \n' % (i, ','.join(map(str, tokens[tokenType][i]))))
		if pos == output.tell():
			output.write("\tNONE\n")

	# last part -> Lexical errors
	output.write('LEXICAL ERRORS:\n')
	pos = output.tell()
	for i in range(1, presentLine ):
			if tokens['Lexical Errors'][i] != []:
				output.write('\tIn line %d: %r \n' % (i, ','.join(map(str, tokens['Lexical Errors'][i]))))
	if pos == output.tell():
		output.write("\tNONE")
	output.close()
	return


def main():
	print ("Enter filename for analyzing or 0 to exit")
	f = input(">>> ")
	while f != '0':  # checking for existence of file "f"
		while exists(f) == False :
			print ("File '%s' does not exist in this directory , Please enter complete path" % f)
			print ("Renter filename or press 0 to exit")
			f = input(">>> ")
			if f == '0':
				exit(0)


		f1 = open(f)	#  file to be analysed
		file = f1.read() # copy contents of file
		f1.close()	# close file
		outputf = input('Enter destination file:')
		print ("Generating Tokens")
		lexAnalyser(file, outputf) #calling lex function
		print ("Results stored in %s" % outputf)
		print ("Enter another filename or 0 to exit")
		f = input(">>> ")

if __name__ == '__main__':
	main()