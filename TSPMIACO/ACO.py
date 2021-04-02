from Ant import Ant
import math 
import random 
from random import uniform
from random import randint

class ACO: 

    def __init__(self, param = None, problParam = None):
        self.__param = param
        self.__problParam = problParam
        self.__population = []
        self.__problParam['pheroMat'] = self.__create_pheromon_Mat() 
        self.__klong=[]
        self.__kshort=[]
        self.__t=0
        self.__tm=randint(self.__problParam['minim'],self.__problParam['maxim'])
        self.__randomCountElimination=0
        self.__previousBest=0
        self.__wechange=False

        self.__long_term_init()
    
    @property
    def population(self):
        return self.__population

    @property
    def khsort_population(self):
        return self.__kshort

    def __create_pheromon_Mat(self):

        pheroMat=[] 
                
        for _ in range(self.__problParam['noNodes']):
            linie=[self.__problParam['init']]* self.__problParam['noNodes']
            pheroMat.append(linie);

        return pheroMat

    def __initialisation(self):
     
        self.__population=[]

        for _ in range(self.__param['popSize']):
            c=Ant(self.__problParam)
            self.__population.append(c)

    def __pacoIncrease(self,repres,i):
        self.__problParam['pheroMat'][repres[i]][repres[i+1]]=  self.__problParam['pheroMat'][repres[i]][repres[i+1]]+ (self.__problParam['max'] - self.__problParam['init'])/self.__param['popSize']
        self.__problParam['pheroMat'][repres[i+1]][repres[i]]=  self.__problParam['pheroMat'][repres[i+1]][repres[i]]+ (self.__problParam['max'] - self.__problParam['init'])/self.__param['popSize']
 

    
    def __pacoDecrease(self,repres,i): 
        self.__problParam['pheroMat'][repres[i]][repres[i+1]]=  self.__problParam['pheroMat'][repres[i]][repres[i+1]] - (self.__problParam['max'] - self.__problParam['init'])/self.__param['popSize']
        self.__problParam['pheroMat'][repres[i+1]][repres[i]]=  self.__problParam['pheroMat'][repres[i+1]][repres[i]] - (self.__problParam['max'] - self.__problParam['init'])/self.__param['popSize']

    def __sacoUpdate(self):
        bestAnt=self.best_ant()

        #print(bestAnt)
        repres=bestAnt.repres
        l_best=bestAnt.fitness

        for i in range(-1,len(repres)-1): 
            self.__problParam['pheroMat'][repres[i]][repres[i+1]]= (1- self.__problParam['rho'])* self.__problParam['pheroMat'][repres[i]][repres[i+1]]+ self.__problParam['rho']* 1/l_best
            self.__problParam['pheroMat'][repres[i+1]][repres[i]]= (1- self.__problParam['rho'])* self.__problParam['pheroMat'][repres[i+1]][repres[i]]+ self.__problParam['rho']* 1/l_best



    def __pacoUpdate(self):
        
        if len(self.__klong)>=self.__param['popSize']:
            
            repres=self.__klong[0].repres

            for i in range(-1,len(repres)-1): 
                self.__pacoDecrease(repres,i)
            del self.__klong[0]
        
        self.__klong.append(self.best_ant())

        bestAnt=self.__best_klong()
        repres=bestAnt.repres

        for i in range(-1,len(repres)-1): 
            self.__pacoIncrease(repres,i)

    def __generalUpdate(self):        
        #self.__sacoUpdate()
        self.__pacoUpdate()

    def oneGeneration(self): 
        
        self.__initialisation()    

        for _ in range(self.__problParam['noNodes']-1): 

            for i in range(len(self.__population)): 
                self.__population[i].makeAStep()

        for i in range(len(self.__population)): 
            self.__population[i].close_circuit()

        self.__generalUpdate()


    def __long_term_init(self):

        self.__klong=[]
        
        for _ in range(self.__problParam['longSize']):
            c=Ant(self.__problParam)
            self.__klong.append(c)

        for _ in range(self.__problParam['noNodes']-1): 
            
            for i in range(len(self.__klong)): 
                self.__klong[i].makeAStep()

        for i in range(len(self.__klong)): 
            self.__klong[i].close_circuit()
        

    def __short_term_init(self):

        self.__kshort=[]
        
        for _ in range(self.__problParam['shortSize']):
            c=Ant(self.__problParam)
            self.__kshort.append(c)

    def __inver_over(self): 

        bestLong=self.__best_klong() 
        selection=bestLong.repres[:]

        poz1=-1 
        poz2=-1

        poz1=random.randint(0,len(selection)-2)
        c=selection[poz1]
        
        #print("Selectie: " + str(selection)+ " "+ str(poz1))

        count=0

        while count<5: 

            if uniform(0,1)<=self.__problParam['pinver']:
                
                poz2=random.randint(0,len(selection)-1)

                while poz1==poz2: 
                    poz2=random.randint(0,len(selection)-1)

                cprim=selection[poz2]
             
            else: 
                
                ant2=self.__klong[random.randint(0,len(self.__klong)-1)]

                #print("Furnica 2 : " + str(ant2.repres)+ " " + str(poz1+1))

                if poz1==len(selection)-1:
                    cprim=ant2.repres[0]
                else: 
                    cprim=ant2.repres[poz1+1] 

                for i in range(len(selection)): 
                    if cprim==selection[i]: 
                        poz2=i 
                        break 

                
            if poz1+1==poz2 or poz1-1==poz2:
                break 
            
            if poz1<poz2:
                a=poz1+1 
                b=poz2 
            else: 
                a=poz2+1 
                b=poz1

            while a<b:
                selection[a],selection[b]=selection[b],selection[a]
                a+=1
                b-=1  

            poz1=poz2

            count+=1


        return selection

    def __macoUpdate(self):

        if len(self.__klong)>=self.__problParam['longSize']:
            del self.__klong[0]

        self.__klong.append(self.best_kshort_ant())

    

        roundRobin=math.floor(self.__problParam['r']*self.__problParam['shortSize'])

        for _ in range(roundRobin):
            c=Ant(self.__problParam) 
            c.repres=self.__inver_over() 
            c.calculate_cost()
            self.__kshort.append(c)


        self.__kshort=sorted(self.__kshort,key=lambda x : x.fitness)[:self.__problParam['shortSize']]


        for i in range(len(self.__kshort)):             
            repres=self.__kshort[i].repres[:]

            for i in range(-1,len(repres)-1): 
                self.__pacoIncrease(repres, i)


            


    def __findClosestIndex(self,best): 

        m= 1000000
        closestIndex=-1

        for ji in range(len(self.__klong)):
            
            ant=self.__klong[ji]

            edges=0

            for i in range(-1,len(best.repres)-1): 
                
                for j in range(-1,len(ant.repres)-1): 

                    if best.repres[i]==ant.repres[j] and best.repres[i+1]==ant.repres[j+1]: 
                        edges+=1 
                        break 
                
            
            if 1-edges/self.__problParam['noNodes']<m: 
                m=1-edges/self.__problParam['noNodes']
                closestIndex=ji

        #print(m)

        return closestIndex



    def __UpdateMemory(self,dchange): 
        
        self.__randomCountElimination+=1

        if self.__t==self.__tm: 
            bestAnt=self.best_ant() 

        if dchange < self.__problParam['change'] and self.__problParam['dynamic']==True and self.__t!=0:
            bestAnt=self.__previousBest

        if self.__randomCountElimination<=self.__problParam['longSize']:
            del self.__klong[0] 
            self.__klong.append(bestAnt) 
        else: 
            closeIndex=self.__findClosestIndex(bestAnt)

            if self.__klong[closeIndex].fitness> bestAnt.fitness: 
                self.__klong[closeIndex]=bestAnt



    def __macoUpdate2(self):


        if len(self.__kshort)>=self.__problParam['shortSize']:
            del self.__kshort[0]

        self.__kshort.append(self.best_ant())

        dchange=uniform(0, 1)
        if dchange < self.__problParam['change'] and self.__problParam['dynamic']==True and self.__t!=0:
            self.__dynamicChange()

        if self.__t==self.__tm or (dchange < self.__problParam['change'] and self.__problParam['dynamic']==True and self.__t!=0): 
            self.__UpdateMemory(dchange)
            self.__tm=self.__t+randint(self.__problParam['minim'], self.__problParam['maxim'])
        
        if self.__t==0: 

            for i in range(len(self.__kshort)):             
                repres=self.__kshort[i].repres[:]

                for i in range(-1,len(repres)-1): 
                    self.__pacoIncrease(repres, i)
        else: 

            #print("Imigranti")

            roundRobin=math.floor(self.__problParam['r']*self.__problParam['shortSize'])

            for _ in range(roundRobin):
                c=Ant(self.__problParam) 
                c.repres=self.__inver_over() 
                c.calculate_cost()

                #print("Tatic "+ str(self.__best_klong()))
                #print(c)

                self.__kshort.append(c)
            '''
            eliminate=sorted(self.__kshort,key=lambda x : x.fitness)[self.__problParam['shortSize']:]
            for el in eliminate: 
                repres=el.repres[:]
                for i in range(-1,len(repres)-1): 
                    self.__pacoDecrease(repres, i)
            '''


            self.__kshort=sorted(self.__kshort,key=lambda x : x.fitness)[:self.__problParam['shortSize']]


            for i in range(len(self.__kshort)):             
                repres=self.__kshort[i].repres[:]

                for i in range(-1,len(repres)-1): 
                    self.__pacoIncrease(repres, i)

    
    def __dynamicChange(self): 


        for i in range(self.__problParam['noNodes']):

            for j in range(i,self.__problParam['noNodes']): 

                if uniform(0, 1)< self.__problParam['change']: 


                    new_value=randint(1, self.__problParam['maxvalue'])
                    self.__problParam['network'][i][j]=new_value
                    self.__problParam['network'][j][i]=new_value






    def macoGeneration(self): 

        self.__initialisation() 


        
        for _ in range(self.__problParam['noNodes']-1): 

            for i in range(len(self.__population)): 
                self.__population[i].makeAStep()

        for i in range(len(self.__population)): 
            self.__population[i].close_circuit()


        self.__macoUpdate2()
        self.__t+=1
        self.__previousBest=self.best_ant()
        


    

    def best_ant(self):

        bestAnt=self.__population[0]
        best_cost=bestAnt.fitness

        for i in range(1,len(self.__population)):
            if self.__population[i].fitness<best_cost:
                best_cost=self.__population[i].fitness
                bestAnt=self.__population[i]

        return bestAnt

    def best_kshort_ant(self):

        bestAnt=self.__kshort[0]
        best_cost=bestAnt.fitness

        for i in range(1,len(self.__kshort)):
            if self.__kshort[i].fitness<best_cost:
                best_cost=self.__kshort[i].fitness
                bestAnt=self.__kshort[i]

        return bestAnt

    def __best_klong(self):

        bestAnt=self.__klong[0]
        best_cost=bestAnt.fitness

        for i in range(1,len(self.__klong)):
            if self.__klong[i].fitness<best_cost:
                best_cost=self.__klong[i].fitness
                bestAnt=self.__klong[i]

        return bestAnt

    

