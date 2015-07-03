X_source = matrix(X_source_vector,ncol=3,byrow=T)
dimnames(X_source)[[2]] = c('vote_event_id','voter_id','option')
X_source = as.data.frame(X_source)
