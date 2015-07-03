# calculates WPCA

# requires data["voters"], data["vote_events"], data["votes"]
# data["groups"] is needed if party is required

import operator
import numpy
import rpy2.robjects as robjects
R = robjects.r

# calculates WPCA
# dim: number of dimensions returned, cl: whether to calculate cutting lines, nth: whether calculate all cutting lines or just every n-th cutting line
# party: valid options are 'most'; TODO 'last' and 'first'
def calculate(data, dim=2, cl=False, nth=1, grp=False):

    # sort votes
    data["votes"] = sorted(data["votes"],key=operator.itemgetter("vote_event_id","voter_id"))

    # reorder for easier access:
    voters = {}
    for voter in data["voters"]:
        voters[voter['id']] = voter
    vote_events = {}
    for vote_event in data["vote_events"]:
        vote_events[vote_event['id']] = vote_event
        
    # parties   
    group_opts = ['most']
    if grp and (grp in group_opts):
    
        # reorder for easier access:
        groups = {}
        for gr in data["groups"]:
            groups[gr['id']] = gr
            
        ns = {}
        for vote in data["votes"]:
            try:
                ns[vote['voter_id']][vote['group_id']] += 1
            except:
                try:
                    ns[vote['voter_id']][vote['group_id']] = 1
                except:
                    ns[vote['voter_id']] = {}
                    ns[vote['voter_id']][vote['group_id']] = 1
        for key in ns:
            sort = sorted(ns[key].items(), key=operator.itemgetter(1), reverse=True)
            voters[key]['group_id'] = sort[0][0]
        
            
#        TODO
#if group in ['first','last']:
#            try:
#                data["vote_events"] = sorted(data["vote_events"],key=operator.itemgetter("start_date","id"))
#            except:
#                data["vote_events"] = sorted(data["vote_events"],key=operator.itemgetter("id"))
#            if group == 'first':
#                for ve in data
#            ...
#            ...
            

    # load into row vector in R
        # if there are duplicities for (vote_event_id,voter_id), the first option is considered only
    votecheck = {}
    Xsourcevector = []

    for row in data["votes"]:
        try:
            votecheck[row["vote_event_id"]]
        except:
            votecheck[row["vote_event_id"]] = {}
        try:
            votecheck[row["vote_event_id"]][row["voter_id"]]
        except:
            Xsourcevector.append(row["vote_event_id"])
            Xsourcevector.append(row["voter_id"])
            Xsourcevector.append(row["option"])
            votecheck[row["vote_event_id"]][row["voter_id"]] = True
    
    # prepare X_source (R)
    robjects.globalenv["X_source_vector"] = robjects.StrVector(Xsourcevector)
    R.source("prepare_matrix.r")

    # calculate WPCA
    R.source("wpca_script.r")

    # put into object
    wpca = {"voters":[]}
    i = 0   # all people
    k = 0   # cutted people
    rXproj = numpy.array(robjects.globalenv['X_proj_unit'])
    rXpeople = robjects.globalenv['X_people']
    rXvote_events = robjects.globalenv['X_vote_events']
    
    wpca['sigma'] = []
    for s in robjects.globalenv['sigma']:
        wpca['sigma'].append(s)
    
    dims = min(dim,len(wpca['sigma']))
    for item in robjects.globalenv['person_I']:
        if item:
            it = voters[rXpeople[i]]
            #dimensions
            for di in range(1,dims+1):
                it['wpca:d'+str(di)] = rXproj[k,di-1]
            #group
            if grp and (grp in group_opts):
                for key in groups[voters[rXpeople[i]]['group_id']]:
                    it['group:'+key] = groups[voters[rXpeople[i]]['group_id']][key]
            wpca['voters'].append(it)
            k = k + 1
        i = i + 1
    
    
    # CUTTING LINES
    wpca['vote_events'] = []
    if cl:
        # calculate
        robjects.globalenv["modulo"] = int(nth)
        R.source("wpca_cutting_lines_script.r")
        
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
            }
            for key in vote_events[rXvote_events[i]]:
                it[key] = vote_events[rXvote_events[i]][key]
            wpca['vote_events'].append(it)
            i = i + 1
    
    
    return wpca    



#data = datapackage.read("http://localhost/michal/project/datapackages/mx-camara-62-2012-2015-roll-call-votes/datapackage.json")
##data = datapackage.read("http://localhost/michal/project/datapackages/cl-camara-2006-2010-roll-call-votes/datapackage.json")

#wpca = calculate(data,dim=3,cl=True,nth=100,grp='most')
#import csv
#with open("dev/trial.csv","w") as fout:
#    csvw = csv.writer(fout)
#    for row in wpca["people"]:
#        csvw.writerow([row["name"],row["wpca:d1"],row["wpca:d2"],row['group:name']])
