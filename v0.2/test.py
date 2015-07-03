# test


import datapackage  #local
import wpca #local

data = datapackage.read("http://localhost/michal/project/datapackages/cz-praha-2010-2014-roll-call-votes/datapackage.json")
wpca = calculate(data,dim=3,cl=True,modulo=10,grp='most')
import csv
with open("dev/trial.csv","w") as fout:
    csvw = csv.writer(fout)
    for row in wpca["people"]:
        csvw.writerow([row["name"],row["wpca:d1"],row["wpca:d2"],row['group:name']])
