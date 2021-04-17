from random import randint, seed


def generateARandomPermutation(n):
    perm = [i for i in range(n)]
    pos1 = randint(0, n - 1)
    pos2 = randint(0, n - 1)
    perm[pos1], perm[pos2] = perm[pos2], perm[pos1]
    return perm

# permutation-based representation
class Chromosome:
    def __init__(self, problParam = None):
        self.__problParam = problParam  #problParam has to store the number of nodes/cities
        self.__repres = generateARandomPermutation(self.__problParam['noNodes'])
        self.__fitness = 0.0
    
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
    
    def crossover(self, c):
        # order XO

        return self.cx_cross(c)
    

    def ox_cross(self,c):

        # order XO
        pos1 = randint(-1, self.__problParam['noNodes'] - 1)
        pos2 = randint(-1, self.__problParam['noNodes'] - 1)
        if (pos2 < pos1):
            pos1, pos2 = pos2, pos1 
        k = 0
        newrepres = self.__repres[pos1 : pos2]
        for el in c.__repres[pos2:] +c.__repres[:pos2]:
            if (el not in newrepres):
                if (len(newrepres) < self.__problParam['noNodes'] - pos1):
                    newrepres.append(el)
                else:
                    newrepres.insert(k, el)
                    k += 1

        offspring = Chromosome(self.__problParam)
        offspring.repres = newrepres
        return offspring


    def cx_cross(self,c):

        mark=[0 for _ in range(len(self.__repres))]

        child=[-1 for _ in range(len(self.__repres))]

        parent1=self.__repres[:]
        parent2=c.repres[:]

        counter=0 

        second_phase=False

        while counter<len(parent1):

            if not second_phase:
                
                nod=-1
                for i in range(len(parent1)):
                    if mark[i]==0:
                        nod=i 
                        break 
                
                while True: 
                    
                    counter+=1
                    mark[nod]=1 
                    child[nod]=parent1[nod]

                    next_value=parent2[nod]

                    for i in range(len(parent1)):

                        if parent1[i]==next_value: 
                            nod=i 
                            break
                    
                    if mark[nod]==1: 
                        second_phase=True 
                        break 
            else: 

                nod=-1
                for i in range(len(parent2)):
                    if mark[i]==0:
                        nod=i 
                        break 
                
                while True: 
                    
                    counter+=1
                    mark[nod]=1 
                    child[nod]=parent2[nod]

                    next_value=parent1[nod]

                    for i in range(len(parent2)):

                        if parent2[i]==next_value: 
                            nod=i 
                            break
                    
                    if mark[nod]==1: 
                        second_phase=False 
                        break 
                
        #print(child)

        offspring=Chromosome(self.__problParam)
        offspring.repres=child

        return offspring



    def mutation(self):

        self.rsm_mutation()

    def insert_mutation(self):

        # insert mutation
        pos1 = randint(0, self.__problParam['noNodes'] - 1)
        pos2 = randint(0, self.__problParam['noNodes'] - 1)
        if (pos2 < pos1):
            pos1, pos2 = pos2, pos1
        el = self.__repres[pos2]
        del self.__repres[pos2]
        self.__repres.insert(pos1 + 1, el)       

    def rsm_mutation(self):

        #reverse sequence mutation
        pos1=randint(0,self.__problParam['noNodes']-2)
        pos2=randint(pos1+1,self.__problParam['noNodes']-1)

        while pos1<pos2:

            self.__repres[pos1],self.__repres[pos2]=self.__repres[pos2],self.__repres[pos1]
            pos1+=1
            pos2-=1 
        
        
    def __str__(self):
        return "\nChromo: " + str(self.__repres) + " has fit: " + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness