# loads datapackage

# usage: datapackage.read("https://raw.githubusercontent.com/michalskop/datapackages/master/cz-senat-10-2014-2016-roll-call-votes/datapackage.json")

# datapackage MUST have the resources in local path with slash, e.g. 'data/data.csv', and NOT in absolute path, e.g. 'http://example.com/data.csv'

import requests
import csv

def row2header(row):
    header = {}
    j = 0
    for h in row:
        header[h] = j
        j = j + 1
    return header

def row2data(row,header):
    out = {}
    j = 0
    for h in header:
        try:
            out[h] = row[header[h]]
        except:
            out[h] = None
    return out


# reads data from datapackage
def read(url):
    # get datapackage.json
    r = requests.get(url)
    datapackage = r.json()
    
    # get path of the datapackage
    path_li = url.split('/')
    del(path_li[-1])
    path = '/'.join(path_li) + '/'
    
    # extract info from datapackage
    dp = {}
    data = {}
    for resource in datapackage['resources']:
        dp[resource['name']] = resource
        data[resource['name']] = []
    
    # read resources and put them into data
    headers = {}
    for key in data:
        i = 0
        r = requests.get(path + dp[key]["path"])
        r.encoding = "utf-8"    #necessary for correct encoding, not sure why
        csvdata = r.text
        csvreader = csv.reader(csvdata.splitlines())
        for row in csvreader:
            if i == 0:
                headers[key] = row2header(row)
                #print(key,headers[key])
            else:
                data[key].append(row2data(row,headers[key]))
            i = i + 1

    return data
    
#data = read("http://localhost/michal/project/datapackages/cl-camara-2006-2010-roll-call-votes/datapackage.json")



