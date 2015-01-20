#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#import csv
#import json
#import operator
#import optparse
#import cgitb; cgitb.enable() # Optional; for debugging only

#parser = optparse.OptionParser()
#parser.add_option('-d', '--datapackage', dest="datapackage")

#options, remainder = parser.parse_args()

#try:
#    datapackage = json.loads(open(options.datapackage).read())

#    path_li = options.datapackage.split('/')
#    del(path_li[-1])
#    path = '/'.join(path_li) + '/'


#    def row2header(row):
#        header = {}
#        j = 0
#        for h in row:
#            header[h] = j
#            j = j + 1
#        return header

#    def row2data(row,header):
#        out = {}
#        j = 0
#        for h in header:
#            out[h] = row[header[h]]
#        return out

#    # extract info from datapackage
#    dp = {}
#    for resource in datapackage['resources']:
#        if resource["name"] == "people":
#            dp["people"] = resource
#        if resource["name"] == "vote_events":
#            dp["vote_events"] = resource
#        if resource["name"] == "votes":
#            dp["votes"] = resource

#    # load into variable
#    headers = {}
#    data = {"people":[],"votes":[],"vote_events":[]}
#    for key in data:
#        i = 0
#        with open(path + dp[key]["path"], 'r') as csvfile:
#            csvreader = csv.reader(csvfile)
#            for row in csvreader:
#                if i == 0:
#                    headers[key] = row2header(row)
#                else:
#                    data[key].append(row2data(row,headers[key]))
#                i = i + 1
#    # reorder for easier access:
#    people = {}
#    for person in data["people"]:
#        people[person['identifier']] = person
#    vote_events = {}
#    for vote_event in data["vote_events"]:
#        vote_events[vote_event['identifier']] = vote_event
#        
#    # sort votes
#    data["votes"] = sorted(data["votes"],key=operator.itemgetter("vote_event_id","voter_id"))

#except:
#    data = {};
#    print('nothing')

#print("Content-Type: application/json;charset=utf-8")
#print()
#print(data)
