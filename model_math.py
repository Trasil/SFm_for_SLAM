import numpy as np
from math import cos, sin, pi, atan

def R(o):
    co = cos(o); si = sin(o)
    
    return np.array([
        [co, -si, 0],
        [si,  co, 0],
        [ 0,   0, 1]
    ])

def plus(x1, x2):
    return x1+R(x1[2]).dot(x2)


def obr(X):
    x = X[0]; y = X[1]; o = X[2]
    a = pi - o; co = cos(a); si = sin(a)
    
    return np.array([
        co*x - si*y,
        si*x + co*y,
        -o
    ])



#Получение из двух точек поступат и поворот скоростей
def X2VW(X_i, Xi_1):
    w = Xi_1[2,0] - X_i[2,0]
    v = (Xi_1[0,0]-X_i[0,0])/cos(X_i[2,0]) if cos(X_i[2,0])!=0 else (Xi_1[1,0]-X_i[1,0])/sin(X_i[2,0])
    
    return v,w

#Полочение из скоростей скорости колёс
def VW2W(V, W, L=1, R=1):
    return (
        (V+L*W/2)/R,
        (V-L*W/2)/R
    )


#Получение угла ориентации
def getAngle(dx, dy): 
    _a = 0. 
    if (dx!=0.): 
        _a = atan(abs(dy/dx))

    if( dx>0. and dy > 0. ):
        _a += 0
    else:
        if ( dx<=0. and dy > 0. ):
            _a += pi/2
        else: 
            if ( dx<0. and dy <= 0. ): 
                _a += pi
            else:
                if ( dx>=0. and dy < 0. ):
                    _a += 3*pi/2

    return _a

def getO_Law(fx, fy, eps=1e-6):
    return lambda t: getAngle(fx(t+eps)-fx(t-eps), fy(t+eps)-fy(t-eps))
    