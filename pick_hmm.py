import re
import sys


function_list = [ 'NAME.*KO:K02586', 'NAME.*KO:K02588', 'NAME.*KO:K02591' ]

end= re.compile(r'^//')
patts = [ re.compile(x) for x in function_list ]

hmmfile = sys.argv[1]

record = False
line = ''
with open(hmmfile, 'r') as fpin:
    for _line in fpin:
       prevline = line
       line = _line.strip()
       for patt in patts:
         match = patt.search(line)
         if match:
            record = True
            print(prevline)
            break

       if record:
         print(line)
            
       match = end.search(line)
       if match:
          record = False


