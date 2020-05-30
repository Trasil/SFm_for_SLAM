from math import cos,sin,pi,fabs,atan2
import numpy as np
import random

from model_math import R


#######################
#Закон генерации данных
class Law:
    def __init__(self, start=(0.1,0.1), mn=(0,0), mx=(3*pi/2,3*pi/2), a=(pi/4,pi/4), tact = 10):
        self.a = a
        self.max = mx
        self.min = mn
        
        self.w = start
        
        self.t = 0
        self.tact = tact
        
        self.type = "W"
        
    def tic(self):
        self.t += 1  
        
        if (self.t % self.tact == 0):
            self.w = self._tac()
            
        return self.w
    
    #Для изменения закона генерации переопределяется эта ф-я
    def _tac(self):
        w = [0,0]
        for i in range(2):
            l = max(self.min[i], self.w[i] - self.a[i])
            r = min(self.max[i], self.w[i] + self.a[i])
            
            w[i] = random.uniform(l,r)
            
        return (w[0], w[1])


#Физическая модель робота
class Robot:
    def __init__(self, R=0.045, L=0.15, X=np.zeros((3,1)), law = Law()):
        self.X = X.copy()
        self.R = R
        self.L = L
        
        self.law = law
        
        if law.type == "W": self.step = self._stepW
        if law.type == "X": self.step = self._stepX
        
    def _stepW(self):
        w = self.law.tic()
        
        v = self.R*(w[0]+w[1])/2
        w = self.R*(w[1]-w[0])/self.L
        
        o = self.X[2,0]
        self.X += np.array([
            [v*cos(o)],
            [v*sin(o)],
            [w]
        ])
        
        return self.X.copy()
    
    def _stepX(self):
        self.X = self.law.tic()
        return self.X.copy()
    

############################################
#Добавление шумов
def _addNoiseU(X, err):
    ex = err*X[0,0]; noiseX = lambda: (random.random()-0.5)*2*ex 
    ey = err*X[1,0]; noiseY = lambda: (random.random()-0.5)*2*ey 
    eo = err*pi/2;   noiseO = lambda: (random.random()-0.5)*2*eo 
    noise = lambda: np.array([[noiseX()],[noiseY()],[noiseO()]]) 
    return X+noise() 

def _addNoiseZ(X, errR, errO=0):
    #er = errR; noiseR =  (rand()-0.5)*2*er 
    er = errR; noiseR = random.random()*er
    
    ef = pi  ; noiseF =  (random.random()-0.5)*2*ef 
    
    eo = errO; noiseO =  (random.random()-0.5)*2*eo 
    
    noise = np.array([
        [noiseR*cos(noiseF)],
        [noiseR*cos(noiseF)],
        [noiseO]
    ]) 
    return X+noise




#########################################   
#Генератор данных
class Data:
    def __init__(self, rob, noise = (lambda U: _addNoiseU(U, 0), lambda Z: _addNoiseZ(Z, 0,0)), seed = 1):
        self.rob = rob
        
        self.X = []
        self.noise = noise
        
        self.tic = self._tic0
        
        random.seed(seed)
    
    def _tic0(self):
        self.X.append(self.rob.X.copy())
        self.tic = self._ticN
        
        return None, self.noise[1](self.X[0])
    
    def _ticN(self):
        X = self.rob.step()
        self.X.append(X)
        
        U = R(-self.X[-1][2,0]).dot(self.X[-1]-self.X[-2])
        Z = X.copy()
        
        return self.noise[0](U), self.noise[1](Z)
    
    
    
    
############################################
#Полезные конструкторы для Data
def createDG_classicLaw(start=(0,0), mn=(0,0), mx=(1.6,1.6), a=(0.16,0.16), tact = 100, epsU=0, epsZR=0, epsZO=0, seed = 1):
    law = Law(start=start, mn=mn,mx=mx, a=a, tact=tact)
    robot = Robot(law = law)
    
    nU = lambda U: _addNoiseU(U, epsU)
    nZ = lambda Z: _addNoiseZ(Z, epsZR, epsZO)
    noise = (nU, nZ)
    
    data = Data(robot, noise=noise, seed=seed)
    return data
    
        
def createDG_withLaw(law = Law(), epsU=0, epsZR=0, epsZO=0, seed = 1):
    robot = Robot(law = law)
    
    nU = lambda U: _addNoiseU(U, epsU)
    nZ = lambda Z: _addNoiseZ(Z, epsZR, epsZO)
    noise = (nU, nZ)
    
    data = Data(robot, noise=noise, seed=seed)
    return data
#############################################
#Словарь
DataGenerator = {
    "Interfaces": {
        "Robot": Robot,
        "Law": Law,
        "Data": Data
    },
    "Generators":[
        createDG_withLaw,
        createDG_classicLaw
    ]
}
