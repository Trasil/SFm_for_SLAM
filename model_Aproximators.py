import numpy as np
from math import cos, sin, pi

#Общий интерфейс
class Aproximator:
    def __init__(self, n, name="Unknown"):
        self.name = name
        self.n = n
        self.k = 1
        
    def SF(self, X, A=np.eye(3)):
        return ( 
            self.k*A, 
            self.k*A.dot(self.B(X)) 
        )
    
    ########
    #Данную ф-ию необходимо реализовать самому
    def B(self, X):
        return X[-1].copy()
    
    
#Аппроксиматор, работающий с линейными формулами
class LineAproximator(Aproximator):
    def __init__(self, extr):
        super().__init__(extr.n, name = extr.name+"_Approximator");
        self.extr = extr
        try: self.k = extr.k
        except: self.k = 1
        
    def B(self, X):
        l = len(X)
        return np.array([
            [self.extr.extrapolation([ x[0,0] for x in X[-self.extr.n:l]  ])],
            [self.extr.extrapolation([ y[1,0] for y in X[-self.extr.n:l]  ])],
            [self.extr.extrapolation([ o[2,0] for o in X[-self.extr.n:l]  ])]
        ])
    
    
#Интерфейс чисто-линейных экстаполяторов (т.е. работающих с ф-ми одной переменной)
class MonoExtrapolator:
    def __init__(self, n=2, name="UnknownExtrapolator"):
        self.name = str(n) + "points_" + name
        self.n = n
        self.k = 1

    #Это переопределяем
    def extrapolation(self, X):
        # y = ax+b
        a = X[-1] - X[-2]
        b = X[-2]
        return a*2+b
    
    
    
####################
#Экстраполятор Фурье
class Furie(MonoExtrapolator):
    def __init__(self, n=3, size=3, h=1e-4, k = 1):
        super().__init__(name="Furie", n=n)
        self.size = size
        self.k = k
        
        # (fm.T*fm)*C=fm.T*X => A*C= b*X     # Ищем векотр C
        self.b = np.array([  self._furieItem(x) for x in [i*h for i in range(n)]  ]).T
        self.A   = self.b.dot(self.b.T)

        self.eX = np.array( self._furieItem(n*h) )
        
    def extrapolation(self, X):
        C = np.linalg.solve(self.A, self.b.dot(X))
        return self.eX.dot(C)


    def _furieItem(self, x):
        fur = [1]
        for i in range (1,self.size+1):
            fur.extend([sin(i*x), cos(i*x)]);
        return fur;
    
    
    
    
#########################################
#########################################
#########################################
#########################################
#########################################
Aproximators = {
    # Набор базовых аппроксиматоров
    "Classic": {
        "Furie" : lambda n=3, size=3, h=1e-4, k = 1 : LineAproximator( Furie(n=n, size=size, h=h, k = k ) ),
        "Mono"  : lambda                      : LineAproximator(      MonoExtrapolator()      ),
        
        
        # Штука на случай если надо апроксимировать задаваемым экстраполятором 
        "Self"  : lambda extr                 : LineAproximator(extr=extr)
    },
    
    
    # Интерфейсы для создания 
    #   собственных апроксиматоров и экстраполяторов
    "Interfaces" : {
        "Aproximator": Aproximator,          #Совсем базовая штука, нужна для прописания собств-го апроксиматора
        "MonoExtrapolator": MonoExtrapolator #Для задания функций экстрополирования
    }
}
