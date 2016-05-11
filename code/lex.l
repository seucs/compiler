alpha			[A-Za-z]
digit			[0-9]
alphanum		[A-Za-z0-9]
%%
[ \t\r\n]	{
	self.name = "IGNORE"
	if self.str == "\n": self.lexer.lineno += 1
}
int			
if			
else		
return		
float		
struct
"("
")"
"{"
"}"
"["
"]"
"=="
"="
";"		
","			
"."
"+"		
"-"			
"*"			
"/"

{alpha}{alphanum}*	{
				self.name = "NAME"
			}

{digit}+		{
			self.name = "NUMBER"
			self.value	= int(self.str)
			}

%%
