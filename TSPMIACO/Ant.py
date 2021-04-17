from random import randint
from random import uniform

class Ant:

    def __init__(self, problParam=None):
        self.__problParam = problParam 
        self.__fitness=0
        self.__repres = []
        self.__repres.append(randint(0, self.__problParam['noNodes']-1))

    
    @property
    def repres(self):
        return self.__repres 
    
    @property
    def fitness(self):
        return self.__fitness 
    
    @repres.setter
    def repres(self, l = []):
        self.__repres = l 
    
    @fitness.setter 
    def fitness(self, fit = 0.0):
        self.__fitness = fit 


    def calculate_cost(self): 

        sum=0 
        for i in range(-1,self.__problParam['noNodes']-1): 
            sum=sum+self.__problParam['network'][i][i+1]
        self.__fitness=sum

    def __permis(self):

        permise=[]

        for i in range(self.__problParam['noNodes']): 
            if i not in self.__repres: 
                permise.append(i)

        return permise


    def __bestNode(self,i):

        best=-1
        nod=-1 

        for j in self.__permis(): 
            value= self.__problParam['pheroMat'][i][j]**self.__problParam['alpha']*(1/self.__problParam['network'][i][j])**self.__problParam['beta']
            if value>best: 
                best=value 
                nod=j

        return nod

    def __sigma_sum(self,i):

        sum=0
        for j in self.__permis(): 
            value= self.__problParam['pheroMat'][i][j]**self.__problParam['alpha']*(1/self.__problParam['network'][i][j])**self.__problParam['beta']
            sum=sum+value
        return sum

    def __cumulative_sums(self,i):


        cumsums=[0] 
        totalsum=self.__sigma_sum(i) 

        for j in self.__permis():
            value= self.__problParam['pheroMat'][i][j]**self.__problParam['alpha']*(1/self.__problParam['network'][i][j])**self.__problParam['beta']
            probability=value/totalsum 
            cumsums.append(cumsums[-1]+probability)
            
        return cumsums

    def __ruleta(self,i): 

        cumsums=self.__cumulative_sums(i)
        permise=self.__permis()
        probability=uniform(0,1)

        for i in range(len(cumsums)-1): 
            if probability>=cumsums[i] and probability<cumsums[i+1]: 
                return permise[i]


    def __local_Update(self,i,j):      
        self.__problParam['pheroMat'][i][j] = (1- self.__problParam['phi'])* self.__problParam['pheroMat'][i][j]+ self.__problParam['phi']* self.__problParam['init']
        self.__problParam['pheroMat'][j][i] = (1- self.__problParam['phi'])* self.__problParam['pheroMat'][j][i]+ self.__problParam['phi']* self.__problParam['init']
        
    

    def makeAStep(self):

        q=uniform(0,1)

        if q<=self.__problParam['qo']:        
            j=self.__bestNode(self.__repres[-1])
        else:        
            j=self.__ruleta(self.__repres[-1])
         
        self.__fitness=self.__fitness+self.__problParam['network'][self.__repres[-1]][j]
        self.__repres.append(j) 
        #self.__local_Update(self.__repres[-2], self.__repres[-1])
        


    def build_the_path(self):

        for _ in range(self.__problParam['noNodes']-1):
            q=uniform(0,1)

            if q<=self.__problParam['qo']:        
                j=self.__bestNode(self.__repres[-1])
            else:        
                j=self.__ruleta(self.__repres[-1])
            
            self.__fitness=self.__fitness+self.__problParam['network'][self.__repres[-1]][j]
            self.__repres.append(j) 


    def close_circuit(self):
        self.__fitness=self.__fitness+self.__problParam['network'][self.__repres[0]][self.__repres[-1]]



    def __str__(self):
        return "\nAnt: " + str(self.__repres) + " has fit: " + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness
