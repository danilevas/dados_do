# import re

# minha_string = "eu ante- riormente fiz besteira"
# meu_regex = r'a(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e(?:-?\s*)r(?:-?\s*)i(?:-?\s*)o(?:-?\s*)r(?:-?\s*)m(?:-?\s*)e(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e'

# match = re.search(meu_regex, minha_string)
# print(match)

import re

texto = "an- terior - mente - com- panheiro"

resultado = re.sub(r'(?<! )- ', '', texto)
print(resultado)