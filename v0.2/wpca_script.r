# INPUT PARAMETERS
# _X_RAW_DB, _LO_LIMIT_1
# raw data in csv using db structure, i.e., a single row contains:
# code of representative, code of division, encoded vote (i.e. one of -1, 1, 0, NA)
# for example:
# “Joe Europe”,”Division-007”,”1”

#Xsource = read.csv("data/votes.csv")

# lower limit to eliminate from calculations, e.g., .1; number
lo_limit = .1

# we may need to install and/or load some additional libraries
# install.packages("reshape2")
library("reshape2", lib.loc=c("/home/michal/R/x86_64-pc-linux-gnu-library/3.1","/usr/local/lib/R/site-library"))

# reorder data; divisions x persons
X_source$vote_event_id = as.factor(X_source$vote_event_id)
X_source$voter_id = as.factor(X_source$voter_id)

X_source$option_numeric = rep(0,length(X_source$option))
X_source$option_numeric[X_source$option=='yes'] = 1
X_source$option_numeric[X_source$option=='no'] = -1
X_source$option_numeric[X_source$option=='abstain'] = -1    #may be 0 in some parliaments
X_source$option_numeric[X_source$option=='not voting'] = -1
X_source$option_numeric[X_source$option=='absent'] = NA
X_source$option_numeric[X_source$option=='paired'] = NA
X_source$option_numeric = as.numeric(X_source$option_numeric)

#prevent reordering, which is behaviour of acast:
X_source$voter_id = factor(X_source$voter_id, levels=unique(X_source$voter_id))
X_raw = acast(X_source,voter_id~vote_event_id,value.var='option_numeric')
X_people = dimnames(X_raw)[[1]]
X_vote_events = dimnames(X_raw)[[2]]
X_raw = apply(X_raw,1,as.numeric)

# WEIGHTS
# weights 1 for divisions, based on number of persons in division
w1 = apply(abs(X_raw)==1,1,sum,na.rm=TRUE)/max(apply(abs(X_raw)==1,1,sum,na.rm=TRUE))
w1[is.na(w1)] = 0
# weights 2 for divisions, "100:100" vs. "195:5"
w2 = 1 - abs(apply(X_raw==1,1,sum,na.rm=TRUE) - apply(X_raw==-1,1,sum,na.rm=TRUE))/apply(!is.na(X_raw),1,sum)
w2[is.na(w2)] = 0
# total weights:
w = w1 * w2

# analytical charts for weights:
#plot(w1)
#plot(w2)
#plot(w1*w2)

# MISSING DATA
# index of missing data; divisions x persons
I = X_raw
I[!is.na(X_raw)] = 1
I[is.na(X_raw)] = 0


# EXCLUSION OF REPRESENTATIVES WITH TOO FEW VOTES (WEIGHTED)
# weights for non missing data; division x persons
I_w = I*w
# sum of weights of divisions for each persons; vector of length “persons”
s = apply(I_w,2,sum)
person_w = s/sum(w)
# index of persons kept in calculation; vector of length “persons”
person_I = person_w > lo_limit

# cutted (omitted) persons with too few weighted votes; division x persons
X_c = X_raw[,person_I]
# scale data; divisions x persons (mean=0 and sd=1 for each division); scaled cutted persons with too few weighted votes; division x persons
X_c_scaled = t(scale(t(X_c),scale=TRUE))
# scaled with NA->0 and cutted persons with too few weighted votes; division x persons
X_c_scaled_0 = X_c_scaled
X_c_scaled_0[is.na(X_c_scaled_0)] = 0
# weighted scaled with NA->0 and cutted persons with too few weighted votes; division x persons
X = X_c_scaled_0 * sqrt(w)  # X is shortcut for X_c_scaled_0_w

# “X’X” MATRIX
# weighted X’X matrix with missing values substituted and excluded persons; persons x persons
C = t(X) %*% X

# DECOMPOSITION
# eigendecomposition
Xe=eigen(C)
# W (rotation values of persons)
V = Xe$vectors
# projected divisions into dimensions
Xy = X %*% V

# analytical charts of projection of divisions and lambdas
#plot(Xy[,1],Xy[,2])
#plot(sqrt(Xe$values[1:min(10,dim(Xy))]))

# lambda matrix
sigma = sqrt(Xe$values)
sigma[is.na(sigma)] = 0
lambda = diag(sigma)

# projection of persons into dimensions
X_proj = V %*% lambda
# unit-standardized projection of persons into dimensions
X_proj_unit = X_proj / sqrt(apply(X_proj^2,1,sum))
    
# analytical charts
#plot(X_proj[,1],X_proj[,2])
#plot(X_proj_unit[,1],X_proj_unit[,2])

## lambda^-1 matrix
#lambda_1 = diag(sqrt(1/Xe$values))
#lambda_1[is.na(lambda_1)] = 0

## U (rotation values of divisions)
#U = X %*% V %*% lambda_1

## analytical charts
## second projection
#X_proj2 = t(X) %*% U
## second unit scaled projection of persons into dimensions
#X_proj2_unit = X_proj2 / sqrt(apply(X_proj2^2,1,sum))
## they should be equal:
#plot(X_proj[,1],X_proj2[,1])
##plot(X_proj[,2],X_proj2[,2])
