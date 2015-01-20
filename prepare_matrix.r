Xsource = matrix(Xsourcevector,ncol=3,byrow=T)
dimnames(Xsource)[[2]] = c('vote_event_id','voter_id','option')
Xsource = as.data.frame(Xsource)
