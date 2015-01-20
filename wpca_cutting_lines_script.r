# CUTTING LINES
# additional parameters:
# _N_FIRST_DIMENSIONS
# how many dimensions?
n_first_dimensions = 2

# loss function
LF = function(beta0) -1*sum(apply(cbind(y*(x%*%beta+beta0),zeros),1,min))

# preparing variables
normals = Xy[,1:n_first_dimensions]
loss_f = data.frame(matrix(0,nrow=dim(X)[1],ncol=4))
colnames(loss_f)=c("Parameter1","Loss1","Parameter_1","Loss_1")
parameters = data.frame(matrix(0,nrow=dim(X)[1],ncol=3))
colnames(parameters)=c("Parameter","Loss","Direction")

# x-values
xfull = Xproj[,1:n_first_dimensions]
# unit x-values
xfullu = Xproju[,1:n_first_dimensions]

#calculating all cutting lines
for (i in as.numeric(1:dim(X)[1])) {
#for (i in (1:2)) {
    if ((i %% modulo) == 0) {
        beta = Xy[i,1:n_first_dimensions]
        y = t(as.matrix(X[i,]))[,pI]
        x = xfullu[which(!is.na(y)),]
        y = y[which(!is.na(y))]
        zeros = as.matrix(rep(0,length(y)))
        # note: “10000” should be enough for any real-life case:
        res1 = optim(c(1),LF,method="Brent",lower=-10000,upper=10000)        
    # note: the sign is arbitrary, the real result may be -1*; we need to minimize the other way as well
        y=-y
        res2 = optim(c(1),LF,method="Brent",lower=-10000,upper=10000) 

        # the real parameter is the one with lower loss function
        # note: theoretically should be the same (either +1 or -1) for all divisions(rows), however, due to missing data, the calculation may lead to a few divisions with the other direction
        loss_f[i,] = c(res1$par,res1$value,res2$par,res2$value)
        if (res1$value<=res2$value) {
          parameters[i,] = c(res1$par,res1$value,1)
        } else {
          parameters[i,] = c(res2$par,res2$value,-1)
        }
    }
}
CuttingLines = list(normals=normals,parameters=parameters,loss_function=LF,weights=cbind(w1,w2))
cl = cbind(CuttingLines$normals,CuttingLines$parameters$Parameter,CuttingLines$parameters$Loss,w1,w2)
