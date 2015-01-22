#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# calling: http://localhost/cgi-bin/wpca/load_datapackage.cgi?datapackage=/home/michal/dev/wpca/praha_2010-2014/datapackage.json

# notes: http://httpd.apache.org/docs/2.2/howto/cgi.html
# nano /etc/apache2/sites-enabled/000-default.conf
# or nano /etc/apache2/sites-available/test.kohovolit.sk.conf
# set proper rigths
# ln

#print("Content-Type: text/html;charset=utf-8")
#print()

data = {}

import cgi

import csv
import json
import operator
#import optparse
#import cgitb; cgitb.enable() # Optional; for debugging only

# from terminal:
#parser = optparse.OptionParser()
#parser.add_option('-d', '--datapackage', dest="datapackage")
#options, remainder = parser.parse_args()

# from web:
args = cgi.FieldStorage()
arguments = {}
for i in args.keys():
    arguments[i] = args[i].value

try:
    datapackage = json.loads(open(arguments['datapackage']).read())

    #path_li = options.datapackage.split('/')
    path_li = arguments['datapackage'].split('/')
    del(path_li[-1])
    path = '/'.join(path_li) + '/'

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
            out[h] = row[header[h]]
        return out

    # extract info from datapackage
    dp = {}
    for resource in datapackage['resources']:
        if resource["name"] == "people":
            dp["people"] = resource
        if resource["name"] == "vote_events":
            dp["vote_events"] = resource
        if resource["name"] == "votes":
            dp["votes"] = resource

    # load into variable
    headers = {}
    data = {"people":[],"votes":[],"vote_events":[]}

    for key in data:
        i = 0
        with open(path + dp[key]["path"], 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if i == 0:
                    headers[key] = row2header(row)
                else:
                    data[key].append(row2data(row,headers[key]))
                i = i + 1
                
                


        
    # sort votes
    data["votes"] = sorted(data["votes"],key=operator.itemgetter("vote_event_id","voter_id"))

except:
    data = {};

print("Content-Type: application/json;charset=utf-8")
print()
print(json.dumps(data))


