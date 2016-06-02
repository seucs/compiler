%nonassoc	LOW  /* dummy token to suggest shift on else */
%nonassoc	else /* higher than LOW */

%nonassoc	'=='
%left		'+'	'-'
%left		'*'	'/'
%left		'.'	'['	/* C compatible precedence rules */

%%
program		: declarations
		;

declarations	: declaration declarations
		| epsilon
		;

declaration	: fun_declaration
		| var_declaration
		;

fun_declaration	: type NAME '(' parameters ')' block {
		  pass
		  }
		;

parameters	: more_parameters   { 
			p[0] = p[1]
			}

		| epsilon	{ 
			p[0] = []
			}
		;

more_parameters	: parameter ',' more_parameters  { 
				p[0] = p[1] + p[2]
				}

		| parameter		{ 
				p[0] = [p[1]]
				}
		;

parameter	: type NAME {
				p[0] = (p[1], p[2])
			}
		;

block		: '{' var_declarations statements '}' { 
		  	pass
		  	}
		;

var_declarations : var_declaration var_declarations
		| epsilon
		;

var_declaration	: type NAME ';'	{ 
			names[p[2]] = None 
			}
		;

type :    int	
		| float
		;

statements	: statement ';' statements
		| epsilon
		;

statement	: if '(' exp ')' statement {
				if p[3]:
					if_flag = True
			}

		| if '(' exp ')' statement else statement {
				if p[3]:
					if_flag = True
		}

		| lexp '=' exp	{ 
			if if_flag:
				names[p[1]] = p[3]
				if_flag = False
			}

		| return exp { 
			return_value = p[2];
			}

		| block
		;

lexp	: var			{
			p[0] = p[1]
			}
		;

exp		: exp '+' exp		{ 
			p[0] = p[1] + p[3] 
			}

		| exp '-' exp		{ 
			p[0] = p[1] - p[3]
			}

		| exp '*' exp		{ 
			p[0] = p[1] * p[3]
			}

		| exp '/' exp	{ 
			p[0] = p[1] / p[3] 
			}

		| exp '==' exp		{ 
			p[0] = (p[1] == p[3])
			}

		| '(' exp ')'	{ 
			p[0] = p[2]
			}

		| '-' exp 	{ 
			p[0] = -p[2] 
			}

		| var		{ 
			p[0] = names[p[1]]
			}

		| NUMBER 		{ 
			p[0] = p[1] 
			}

		| NAME '(' ')'	{ 
			pass
			}

		| NAME '(' exps ')'	{ 
			$$ = check_fun_call(scope,$1,&$3); 
			}
		;

exps	: exp 		{ 
			$$ = types_list_insert(0,$1); 
			}

		| exp ',' exps	{ 
			$$ = types_list_insert($3,$1); 
			}
		;

var		: NAME 			{ 
			p[0] = p[1]
			}
		;
%%
