import time

import numpy as np
from model_math import *
from numpy.linalg import norm, inv

from model_Aproximators import Aproximators


class Train:
    def __init__(self, n=2, H=np.eye(3)):
        self.n = n-1
        self.H = H.copy()
        
        self.R = np.eye(3)
        self.Q = np.eye(3)
        self.O = np.eye(3)
        
        #Тут будет траектория
        self.X = []

        #Инициализация первых шагов алгоритма
        self.step = self._step0
        
        
    def _step0(self, U,Z):
        self.X.append(Z.copy())
        self.n -= 1
        
        if (self.n == 0):
            self.n = len(self.X)+1
            self.step = self._step
        else:
            self.step = self._stepInit

        return self.X[-1]
    
    def _stepInit(self, U,Z):
        self.X.append(self._origSF(U,Z))

        self.n -= 1

        if (self.n == 0):
            self.n = len(self.X)+1
            self.step = self._step

        return self.X[-1]
    
    
    def _step(self, U,Z):
        X = self._SF(U,Z)

        #Сохранение результата и его выдача
        for i in range(len(self.X)-1):
            self.X[i] = self.X[i+1]
            
        self.X[-1] = X
        return self.X[-1]

    def _origSF(self, U,Z):
        o = self.X[-1][2,0]+U[2,0]
        self.R[0,0] = self.R[1,1] = cos(o)
        self.R[1,0] = sin(o); self.R[0,1] = -self.R[1,0]

        P = self.R.dot(self.Q).dot(self.R.T)

        s1 = P + self.H.T.dot(self.O).dot(self.H)
        s2 = self.H.T.dot(Z) + P.dot(self.X[-1] + self.R.dot(U))

        return inv(s1).dot(s2)
    
    #########################
    #Функция для переопределения
    def _SF(self, U,Z):
        return self._origSF(U,Z)
    
    
########################################################################
#######################################################################
#######################################################################
class Train_extrSF(Train):
    def __init__(self, extr):
        super().__init__(n=extr.n+1)
        self.extr = extr

    def _SF(self, U,Z):
        o = self.X[-1][2,0]+U[2,0]
        self.R[0,0] = self.R[1,1] = cos(o)
        self.R[1,0] = sin(o); self.R[0,1] = -self.R[1,0]

        P = self.R.dot(self.Q).dot(self.R.T)
        s = self.extr.SF(self.X)

        s1 = P + self.H.T.dot(self.O).dot(self.H)                 + s[0]#/10
        s2 = self.H.T.dot(self.O).dot(Z) + P.dot(self.X[-1] + self.R.dot(U))  + s[1]#/10

        return inv(s1).dot(s2)
    
    
########################################################################
########################################################################
########################################################################
Trains = {
    "Classic" : {
        "origSF": lambda : Train(),
        "extrSF": lambda extr: Train_extrSF(extr)
    },
    
    "Interfaces" : {
        "Train" : Train
    }
}