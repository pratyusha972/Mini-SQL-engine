from pyparsing import Literal, CaselessLiteral, Word, upcaseTokens, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword

selectToken = Keyword("select", caseless=True)
fromToken   = Keyword("from", caseless=True)
#createTableToken = Keyword("create table", caseless=True)
integerToken = Keyword("integer", caseless=True) | Keyword("int", caseless=True)
#insertIntoToken = Keyword("insert into", caseless=True)
valuesToken = Keyword("values", caseless=True)
#deleteFromToken = Keyword("delete from", caseless=True)
#truncateToken = Keyword("truncate table", caseless=True)
#dropToken = Keyword("drop table", caseless=True)
#showTablesToken = Keyword("show tables", caseless=True)


ident          = Word( alphas, alphanums + "_$" ).setName("identifier")
columnName     =( delimitedList( ident, ".", combine=True ) )
functionCall   = Group( ident + '(' + columnName + ')')
columnNameList = Group( delimitedList( functionCall | columnName) )
tableName      = ( delimitedList( ident, ".", combine=True ) )
tableNameList  = Group( delimitedList( tableName ) )
field          = Group( ident + integerToken )
fieldList      = Group( delimitedList(field) )

and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)

binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-",exact=1)
intNum = Combine( Optional(arithSign) + Word( nums ) )
intNumList = Group( delimitedList(intNum) )

columnRval = intNum | columnName
whereCondition = Group(columnRval + binop + columnRval)
whereExpression = Group(whereCondition + Optional( (and_ | or_) + whereCondition))

# define the grammar
selectStmt      =  ( selectToken.setResultsName( "statementtype" ) +
                   ( '*' | columnNameList ).setResultsName( "columns" ) +
                   fromToken +
                   tableNameList.setResultsName( "tables" ) +
                   Optional( Group( CaselessLiteral("where") + whereExpression ), "" ).setResultsName("where") )

'''createStmt      =  ( createTableToken.setResultsName( "statementtype" ) +
                   ident.setResultsName("tablename") +
                   '(' +
                   fieldList.setResultsName("fieldlist") +
                   ')')

insertStmt      =  ( insertIntoToken.setResultsName( "statementtype" ) +
	                 ident.setResultsName("tablename") +
	                 valuesToken +
	                 '(' +
	               	 intNumList.setResultsName("tablevalues") +
	               	 ')' )

deleteStmt      =  ( deleteFromToken.setResultsName("statementtype") +
	                 ident.setResultsName("tablename") +
	                 CaselessLiteral("where") +
	                 whereExpression.setResultsName("where") )

truncateStmt    =  ( truncateToken.setResultsName("statementtype") +
                   ident.setResultsName("tablename") )

dropStmt        =  ( dropToken.setResultsName("statementtype") +
                   ident.setResultsName("tablename") )

showStmt        =  ( showTablesToken.setResultsName("statementtype") )'''

#simpleSQL = selectStmt | createStmt | insertStmt | deleteStmt | truncateStmt | dropStmt | showStmt
simpleSQL= selectStmt

def test( str ):
    #print str,"->"
    try:
        tokens = simpleSQL.parseString( str )
        print tokens.statementtype
        if tokens.statementtype == "select":
        	print "tokens.columns =", tokens.columns
        	print "tokens.tables =",  tokens.tables
        	print "tokens.where =", tokens.where
	return tokens.statementtype,tokens.columns,tokens.tables,tokens.where
    except ParseException, err:
        print " "*err.loc + "^\n" + err.msg
        print err
def manualtests():
	print
	statetype,columns,tables,where=test('Select distinct(A),distinct(B) from table1;')
	return statetype,columns,tables,where
	print

	'''print
	statetype,columns,tables,where=test('Select * from table1,table2;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('Select * from table2;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('Select B,C from table1 where A = 922;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('Select B,C from table1;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('Select A,B,C from table1 where A = 922;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('select A,B,C, D from table1,table2 where table1.A = 922;')
	return statetype,columns,tables,where
	print

	print
	statetype,columns,tables,where=test('select A,D from table1,table2 where table1.B = table2.B;')
	return statetype,columns,tables,where
	print'''


if __name__ == '__main__':
	statetype,columns,tables,where=manualtests()
	#while True:
	#	x = test(raw_input())
