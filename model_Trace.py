from model_DataGenerator import DataGenerator
from math import pi
import numpy as np


scal = 0.09 
class Law_Snake (DataGenerator["Interfaces"]["Law"]):
    def __init__(self):
        super().__init__()
        self.tact = 200
        self.w = [1.8-self.a[0]*scal/2,1.8]
        
        self.flag = 1
        
    def _tac(self):
        w = list(self.w)
        
        w[0] += self.a[0]*self.flag*scal
        #w[1] -= self.a[1]*self.flag/2
        
        self.flag = 0 - self.flag
        
        return tuple(w)
    
    
class Law_Circle (DataGenerator["Interfaces"]["Law"]):
    def __init__(self):
        super().__init__()
        self.tact = 10
        self.w = [1.9,1.6]
        
        self.l = 0.1
        self.r = 0.
        
    def _tac(self):
        w = list(self.w)
        
        w[1] += 0.00125
        
        return tuple(w)
    
    
class Law_Line (DataGenerator["Interfaces"]["Law"]):
    
    R=0.045
    L=0.15
    n_t = 800
    
    start = 800
    
    def __init__(self):
        super().__init__()
        self.tact = 1
        self.w = [1.8,1.8]
        
        self.ad = (pi/2/self.n_t)*self.L/self.R/2
        
    def _tac(self):
        w = list(self.w)
        
        if self.t==self.start:
            w[0] += self.ad
            w[1] -= self.ad
        
        if self.t==self.start+self.n_t:
            w[0] -= self.ad
            w[1] += self.ad
        
        return tuple(w)
    
    
class Law_Random (DataGenerator["Interfaces"]["Law"]):
    def __init__(self):
        super().__init__()
        self.tact = 10
    
Trace = {
    "Snake": Law_Snake,
    "Circle": Law_Circle,
    "Line": Law_Line,
    "Random": Law_Random
    
}
