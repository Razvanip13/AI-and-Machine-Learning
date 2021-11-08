from random import random
from random import randint
from random import uniform
import numpy

from numpy.lib.function_base import append


class Kmeans: 

    def __init__(self, n_clusters=3):
        self.__centroids = []
        self.__centro_labels=[]
        self.__labels = []
        self.__centro_colors = []
        self.__nclusters=n_clusters

    def __russian_roullete(self,distances):
        
        chei = [key for key in distances.keys()]
        proportions = [distance/sum(distances) for distance in distances]
        cumsums = numpy.cumsum(numpy.array(proportions)).tolist()

        # print(cumsums)

        probability=uniform(0,1)

        index = -1
        for i in range(len(cumsums)-1): 
            if probability>=cumsums[i] and probability<cumsums[i+1]: 
                index = i 
                break 
        
        return chei[index]

    def __kmeansplusplus(self,X_train,y_train):

        first = randint(0,len(X_train)-1) 
        self.__centroids.append(X_train[first])
        self.__centro_labels.append(first)
        self.__centro_colors.append(y_train[first])


        k=1
        while k<self.__nclusters:
            
            distances={}
            for i in range(len(X_train)):
                if i not in self.__centro_labels:
                    distances[i] = 100000

            for j in range(len(self.__centroids)):

                for i in range(len(X_train)):
                    if i not in self.__centro_labels:
                        values = [(xfeature - cfeature)*(xfeature-cfeature) for xfeature,cfeature in zip(X_train[i],self.__centroids[j])]
                        distance = sum(values)
                        if(distance<distances[i]):
                            distances[i] = distance

            new_centro_poz = self.__russian_roullete(distances)
            self.__centroids.append(X_train[new_centro_poz])
            self.__centro_labels.append(new_centro_poz)
            self.__centro_colors.append(y_train[new_centro_poz])

            k+=1
    
    def __knn(self,X_train,y_train,kn=5):
        
        relabeled=[-1 for _ in X_train]

        for i in range(len(self.__centroids)):

            distances=[]
            for j in range(len(X_train)): 

                values = [(xfeature - cfeature)*(xfeature-cfeature) for xfeature,cfeature in zip(X_train[j],self.__centroids[i])]
                distance = sum(values)
                distances.append([j,distance])

            distances=sorted(distances,key=lambda x: x[1])
            distances=distances[:kn]

            # print(distances)

            dic={}
            for pair in distances:
                
                # print(pair)

                if y_train[pair[0]] in dic: 
                    dic[y_train[pair[0]]]+=1
                else:
                    dic[y_train[pair[0]]]=0

            maxim=-1 
            value=-1

            for k,v in dic.items():
                
                if maxim<v: 
                    maxim=v 
                    value=k
            
            for j in range(len(self.__labels)):
                if self.__labels[j] == i: 
                    relabeled[j] = value


        return relabeled

    
    def fit_predict(self,X_train,y_train, maxIter = 30, minim=0, maxim = 5):
        

        self.__kmeansplusplus(X_train,y_train)

        print(self.__centro_colors)


        for el in self.__centroids:
            print(el)

        # return None 
        # self.__centroids = []
        self.__labels = [ -1 for _ in X_train]

        # for i in range(self.__nclusters): 
        #     centro = [minim +(random()*(maxim-minim)) for _ in X_train[0]]
        #     self.__centroids.append(centro)

        time_to_stop = False 
        iteration = 0

        while iteration<maxIter:
            
            time_to_stop = True 

            for j in range(len(X_train)): 
                
                mindistance=1000000
                the_centro=-1

                for i in range(len(self.__centroids)):
                    
                    values = [(xfeature - cfeature)*(xfeature-cfeature) for xfeature,cfeature in zip(X_train[j],self.__centroids[i])]
                    distance = sum(values) 

                    if mindistance>distance: 
                        mindistance = distance
                        the_centro = i 
                        # the_centro = self.__centro_colors[i]


                if self.__labels[j] != the_centro:
                    time_to_stop = False 

                self.__labels[j] = the_centro

            if time_to_stop: 
                print("It's time to stop")
                break

            for i in range(len(self.__centroids)): 
                for feature_index in range(len(self.__centroids[i])): 

                    # values = [ X_train[j][feature_index] for j in range(len(self.__labels)) if self.__labels[j] == i]

                    values=[] 
                    for j in range(len(self.__labels)): 
                        if self.__labels[j]==i:
                            values.append(X_train[j][feature_index])

                    self.__centroids[i][feature_index]= sum(values)/len(values)

            print("Iteration " + str(iteration) +" --------------")
            for i in range(len(self.__centroids)):
                print(self.__centroids[i])

            print("----------------------------")

            iteration+=1

        # return self.__labels

        return self.__knn(X_train,y_train,kn=7)


    def predictOnesSample(self, x): 
        
        mindistance=1000000
        verdict=-1

        for i in range(len(self.__centroids)):                    
            values = [(xfeature - cfeature)*(xfeature-cfeature) for xfeature,cfeature in zip(x,self.__centroids[i])]
            distance = sum(values) 

            if mindistance>distance: 
                mindistance = distance
                verdict = i 

        return verdict 
    
    def predict(self, inTest,threshold=0.5):
        
        computedLabels = [self.predictOnesSample(sample) for sample in inTest]
        return computedLabels

