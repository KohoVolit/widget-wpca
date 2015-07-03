# calculates WPCA from datapackage
# reads parameters from arg

# examples:
# resource, cutting_lines, nth cutting_line, dimensions, how to assign group
# calculate_wpca.py https://raw.githubusercontent.com/michalskop/datapackages/master/cz-senat-10-2014-2016-roll-call-votes/datapackage.json
# calculate_wpca.py https://raw.githubusercontent.com/michalskop/datapackages/master/cz-senat-10-2014-2016-roll-call-votes/datapackage.json yes
# calculate_wpca.py https://raw.githubusercontent.com/michalskop/datapackages/master/cz-senat-10-2014-2016-roll-call-votes/datapackage.json yes 100
# calculate_wpca.py https://raw.githubusercontent.com/michalskop/datapackages/master/cz-senat-10-2014-2016-roll-call-votes/datapackage.json yes 100 3 most

import datapackage
import wpca
import sys
import json

result = {}

#try:
data = datapackage.read(sys.argv[1])
try:
    if sys.argv[2] == 'yes':
        cl = True
    else:
        cl = False
except:
    cl = False
try:
    nth = int(sys.argv[3])
except:
    nth = 1
try:
    dim = int(sys.argv[4])
except:
    dim = 2
try:
    grp = sys.argv[5]
except:
    grp = None

result = wpca.calculate(data,dim=dim,cl=cl,nth=nth,grp=grp)

#except:
#    nothing = None

print(json.dumps(result))
