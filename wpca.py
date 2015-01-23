#!/usr/bin/env python3

import csv
import json
import operator
import numpy
import requests
import sys
import rpy2.robjects as robjects
r=robjects.r

#exec(open("load_datapackage.py").read())
url = sys.argv[1]
req = requests.get(url)
data = req.json()

# reorder for easier access:
people = {}
for person in data["people"]:
    people[person['id']] = person
vote_events = {}
for vote_event in data["vote_events"]:
    vote_events[vote_event['id']] = vote_event

# load into row vector in R
Xsourcevector = []
for row in data["votes"]:
    Xsourcevector.append(row["vote_event_id"])
    Xsourcevector.append(row["voter_id"])
    Xsourcevector.append(row["option"])
    
robjects.globalenv["Xsourcevector"] = robjects.StrVector(Xsourcevector)
r.source("prepare_matrix.r")

# calculate WPCA
r.source("wpca_script.r")

# put into object
wpca = {"people":[]}
i = 0   # all people
k = 0   # cutted people
rXproj = numpy.array(robjects.globalenv['Xproju'])
rXpeople = robjects.globalenv['Xpeople']
rXvote_events = robjects.globalenv['Xvote_events']
for item in robjects.globalenv['pI']:
    if item:
        it = {
            'id': people[rXpeople[i]]['id'],
            'name': people[rXpeople[i]]['name'],
            'party': people[rXpeople[i]]['party'],
            'wpca:d1': rXproj[k,0],
            'wpca:d2': rXproj[k,1]    
        }
        try:
            it['color'] = people[rXpeople[i]]['color']
        except:
            nothing = 0
        wpca['people'].append(it)
        k = k + 1
    i = i + 1

# CUTTING LINES
wpca['vote_events'] = []
try:
    if sys.argv[2] == 'yes':
        # modulo
        try:
            robjects.globalenv["modulo"] = int(sys.argv[3])
        except:
            robjects.globalenv["modulo"] = 1
        # calculate
        r.source("wpca_cutting_lines_script.r")

        # put into object
        rcl = numpy.array(robjects.globalenv['cl'])
        i = 0   # all vote events
        for ve in rcl:
            rcl_li = list(rcl[i])
            it = {
                'normal_x': rcl_li[0],
                'normal_y': rcl_li[1],
                'cl_beta0': rcl_li[2],
                'loss': rcl_li[3],
                'w1': rcl_li[4],
                'w2': rcl_li[5],
                'id': vote_events[rXvote_events[i]]["id"],
                'motion:name': vote_events[rXvote_events[i]]["motion:name"],
                'start_date': vote_events[rXvote_events[i]]["start_date"],
                'result': vote_events[rXvote_events[i]]["result"]
            }
            wpca['vote_events'].append(it)
            i = i + 1
except:
    nothing = None

print(json.dumps(wpca))
