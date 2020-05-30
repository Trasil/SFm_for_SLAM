'''
В данном файле будет мешанина из различных испытываемых поездов
'''

import numpy as np

from model_math import *
from model_Trains import Trains
from model_Aproximators import Aproximators
######################
######################



class aX_const(Aproximators["Interfaces"]["Aproximator"]):
    def __init__(self, k = 1):
        self.n = 3
        self.name = "aX_const"
        self.k = k
        
    def B(self,X):
        return 3*X[-1]-3*X[-2]+X[-3]
    
    
    
'''#####################################'''
class aVO_const(Aproximators["Interfaces"]["Aproximator"]):
    def __init__(self, k = 1):
        self.n = 4
        self.name = "aVO_const"
        self.k = k
        
        self.VO = [np.zeros(2) for i in range(3)]
        
    def B(self, X):
        #Переводим в VO
        for i in range(-4, -1):
            self.VO[i+1][:] = X2VW(X[i], X[i+1])
            
        #Апроксимируем
        VO = 3*self.VO[-1]-3*self.VO[-2]+self.VO[-3]
        
        v = VO[0]
        w = VO[1]
        
        o = X[-1][2,0]
        return X[-1] + np.array([
            [v*cos(o)],
            [v*sin(o)],
            [w]
        ])
    
    
names = [
    "Ориг",
    "Фурье",
    "Уск",
    "Тряск"
]
    

extrs = [
    Aproximators["Classic"]["Furie"], 
    aX_const,
    aVO_const,
]
######################
######################
testTrains = lambda k = 1: [
    (Trains["Classic"]["origSF"](), names[0])
]+[ (Trains["Classic"]["extrSF"](extr(k = k)), names[i+1]) for i,extr in enumerate(extrs)]