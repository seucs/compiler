alpha			[A-Za-z_]
digit			[0-9]
alphanum		[A-Za-z0-9_]
%%
[ \t\r\n]	{
	self.name = "IGNORE"
}
"{"
"}"
"=="
"="
"/"
"+"
"("
")"
"-"
"<"
">"
"<<"
">>"
"#"	
"*"
";"
">="
"<="
using
namespace
include	
int			
if			
else		
return		
float		
struct
{alpha}{alphanum}*	{
				self.name = "NAME"
			}
{digit}{digit}*		{
			self.name = "NUMBER"
			}

%%
