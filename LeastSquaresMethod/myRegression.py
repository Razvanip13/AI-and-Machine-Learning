import numpy as np
# from sklearn import linear_model
# from sklearn.linear_model.stochastic_gradient import SGDRegressor
# from sklearn.metrics import mean_squared_error, r2_score

from math import exp
from math import log2
from math import sqrt
from numpy.linalg import inv
# from random import shuffle, random
# from logisticRegression import SGDLogisticTool, myLogisticRegression
 
class MyLinearUnivariateRegression:
    def __init__(self):
        self.intercept_ = []
        

    def __classic_multiply(self,X,Y):
        
        result=[]

        for _ in range(len(X)): 
            line=[] 
            for _ in range(len(Y[0])):
                line.append(0)
            result.append(line )


        # iterate through rows of X
        for i in range(len(X)):
        # iterate through columns of Y
            for j in range(len(Y[0])):
            # iterate through rows of Y
                for k in range(len(Y)):
                    result[i][j] += X[i][k] * Y[k][j]

        return result

    def __multiply(self,A,B): 

        l00=0 
        l01=0 
        l10=0
        l11=0

        for i in range(len(A)): 
            l00=l00+A[0][i]*B[i][0] 
            l01=l01+A[0][i]*B[i][1] 
            l10=l10+A[1][i]*B[i][0]
            l11=l11+A[1][i]*B[i][1]

        return [[l00,l01],[l10,l11]]
    
    def __calculateXTY(self,X,Y): 

        l00=0
        l01=0


        for i in range(len(X[0])):

            l00=l00+X[0][i]*Y[i]
            l01=l01+X[1][i]*Y[i]

        return [l00,l01]

    def __inverse(self,A): 

        det=A[0][0]*A[1][1]-A[0][1]*A[1][0]
        l00=A[1][1]/det
        l01=-A[0][1]/det 
        l10=-A[1][0]/det
        l11=A[0][0]/det 

        return [[l00,l01],[l10,l11]]

    def __transpusa(self,A): 

        line1=[]
        line2=[] 

        for i in range(len(A)): 

            line1.append(A[i][0])
            line2.append(A[i][1])


        return [line1,line2] 

    def __calculate_coefficients(self,XXT,XTY):

        b1=XXT[0][0]*XTY[0]+XXT[0][1]*XTY[1]
        b2=XXT[1][0]*XTY[0]+XXT[1][1]*XTY[1]

        return b1,b2 

    def __transpusa_classic(self,A):
        
        result=[]   

        for i in range(len(A)): 
            
            line=[]
            for j in range(len(A[0])): 
                line.append(A[j][i])
            result.append(line)
        
        return result

    def __classic_multiply(self,X,Y):
        
        the_multiplied=[]

        for _ in range(len(X)): 
            line=[] 
            for _ in range(len(Y[0])):
                line.append(0)
            the_multiplied.append(line)


        for i in range(len(X)):
            for j in range(len(Y[0])):
                for ji in range(len(Y)):
                    the_multiplied[i][j] += X[i][ji] * Y[ji][j]

        return the_multiplied

    def __modul(self,u): 

        suma=0

        for i in range(len(u)): 
            suma+=u[i]*u[i]
    
        # print(suma)
        return sqrt(suma)

    def __scalar(self,a,e): 
        
        suma=0

        for i in range(len(a)):
            suma+=a[i]*e[i] 

        return suma
    
    def __multiply_with_scalar(self,scalar,a):

        copie=a[:]

        for i in range(len(copie)): 

            copie[i]=copie[i]*scalar

        return copie

    def __substraction(self,a,b): 

        for i in range(len(a)): 

            a[i]=a[i]-b[i]

        return a

    def qr_decomposition(self,X): 

        R=[]
        Q=[]

        transpusa=self.__transpusa_classic(X)

        u=transpusa[0][:] 
        e=u[:]
        modul=self.__modul(u)

        for i in range(len(e)): 
            e[i]=e[i]/modul

        Q.append(e)


        for i in range(1,len(transpusa)):

            a=transpusa[i][:]
            print(a) 
            u=transpusa[i][:] 


            for j in range(len(Q)): 
                scalar=self.__scalar(a, Q[j])
                multiplied= self.__multiply_with_scalar(scalar, Q[j])
                u=self.__substraction(u, multiplied)
        
            e=u[:]        
            modul=self.__modul(e)

            for i in range(len(e)): 
                e[i]=e[i]/modul
            Q.append(e)
        
        R=[] 

        for i in range(0,len(X)): 
            linie=[] 
            for j in range(len(X[0])): 
                linie.append(0)
            R.append(linie)    

        for i in range(len(X)): 
            for j in range(i,len(X)): 
                R[i][j]=self.__scalar(transpusa[j], Q[i])


        return Q,R 

            


    # learn a linear univariate regression model by using training inputs (x) and outputs (y) 
    def fit(self, x, y):
        
        # XT=self.__transpusa(x) 
        # XXT=self.__inverse(self.__multiply(XT,x))
        # XTY=self.__calculateXTY(XXT,y) 
        # b1,b2=self.__calculate_coefficients(XXT,XTY)
        # self.intercept_.append(b1)
        # self.intercept_.append(b2)

        XT=self.__transpusa(x)
        
        # print(len(x))
        # print(len(XT))


        XXT=self.__inverse(self.__classic_multiply(XT,x))

        # print(XXT2)

        # XXT=self.qr_decomposition(self.__classic_multiply(XT, x))
        # print(len(XT))
        # print(len(XT[0]))
        # print(len(y))
        # print(len(y[0]))

        XTY=self.__classic_multiply(XT, y)
        coef=self.__classic_multiply(XXT, XTY)

        # print(coef)
        
        self.intercept_.append(coef[0][0])
        self.intercept_.append(coef[1][0])



    # predict the outputs for some new inputs (by using the learnt model)
    def predict(self, x):
        
        # print(x)

        return self.intercept_[0]*x[0]+self.intercept_[1]*x[1]
