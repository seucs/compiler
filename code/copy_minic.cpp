
%token	int float NAME struct if else return NUMBER '(' ')' '{' '}'
%token	'[' ']' '=' ';' ',' '.' '+' '-' '*' '/' '=='

%type	<name>	NAME
%type	<value>	NUMBER
%type	<type>	type parameter exp lexp
%type	<tlist>	parameters more_parameters exps
%type	<sym>	field var
%type	<slist>	fields

/*	associativity and precedence: in order of increasing precedence */

%nonassoc	LOW  /* dummy token to suggest shift on else */
%nonassoc	else /* higher than LOW */

%nonassoc	'=='
%left		'+'	'-'
%left		'*'	'/'
%left		U'-'	/* dummy token to use as precedence marker */
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

fun_declaration	: type NAME {
			$<sym>$ = symtab_insert(scope,$2,0);
			scope = symtab_open(scope); 
			scope->function = $<sym>$;
			}

		  '(' parameters ')' {
			$<sym>3->type = types_fun($1,$5);
			}

		  block	{ 
		  scope = scope->parent; 
		  }
		;

parameters	: more_parameters	{ 
			$$ = $1; 
			}

		| epsilon	{ 
			$$ = 0; 
			}
		;

more_parameters	: parameter ',' more_parameters  { 
				$$ = types_list_insert($3,$1); 
				}

		| parameter		{ 
				$$ = types_list_insert(0,$1); 
				}
		;

parameter	: type NAME {
			symtab_insert(scope,$2,$1);
			$$ = $1; 
			}
		;

block		: '{' 		{  
			scope = symtab_open(scope); 
			}

		  var_declarations statements '}' { 
		  	scope = scope->parent;
		  	}
		;

var_declarations : var_declaration var_declarations
		| epsilon
		;

var_declaration	: type NAME ';'	{ 
			symtab_insert(scope,$2,$1); 
			}
		;

type :    int			{ 
			$$ = types_simple(int_t); 
			}

		| float			{ 
			$$ = types_simple(float_t); 
			}

		| type '*'	{ 
			$$ = types_array($1); 
			}

		| struct '{' fields '}' { 
			$$ = types_record($3); 
			}
		;

fields		: field fields		{ 
			$$ = symtab_list_insert($2,$1); 
			}

		| epsilon		{
			$$ = 0; 
			}
		;

field		: type NAME ';'	{ 
			$$ = symtab_info_new($2,$1); 
			}
		;

statements	: statement ';' statements
		| epsilon
		;

statement	: if '(' exp ')' statement
		| if '(' exp ')' statement else statement
		| lexp '=' exp	{ 
			check_'='ment($1,$3); 
			}

		| return exp { 
			check_'='ment(scope->function->type->info.fun.target,$2); 
			}

		| block
		;

lexp		: var			{ 
			$$ = $1->type; 
			}

		| lexp '[' exp ']' { 
			$$ = check_array_access($1,$3); 
			}

		| lexp '.' NAME		{ 
			$$ = check_record_access($1,$3); 
			}
		;

exp		: exp '.' NAME		{ 
			$$ = check_record_access($1,$3); 
			}

		| exp '[' exp ']'	{ 
			$$ = check_array_access($1,$3); 
			}

		| exp '+' exp		{ 
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
			p[0] = p[1] == p[3]
			}

		| '(' exp ')'	{ 
			p[0] = p[2]
			}

		| '-' exp 	{ 
			p[0] = -p[2] 
			}

		| var		{ 
			$$ = $1->type; 
			}

		| NUMBER 		{ 
			p[0] = p[1] 
			}

		| NAME '(' ')'	{ 
			$$ = check_fun_call(scope,$1,0); 
			}

		| NAME '(' exps ')'	{ 
			$$ = check_fun_call(scope,$1,&$3); 
			}
		;

exps		: exp 		{ 
			$$ = types_list_insert(0,$1); 
			}

		| exp ',' exps	{ 
			$$ = types_list_insert($3,$1); 
			}
		;

var		: NAME 			{ 
			$$ = check_symbol(scope,$1); 
			}
		;
%%
