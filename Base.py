import time
import numpy as np
from   tqdm import tqdm
from model_DataGenerator import DataGenerator


def run(trains, data, steps = 10000):
    orig = [[0 for j in range(steps)] for i in range(2)] + [0]
    E2 = [[0 for i in range(steps)] for train in trains]
    E3 = [[0 for i in range(steps)] for train in trains]
    
    times = [[0 for i in range(steps)] for train in trains]
    
    
    for i in range(steps):
        U,Z = data.tic()
        
        orig[0][i] = data.X[-1][0,0]
        orig[1][i] = data.X[-1][1,0]
        
        try:
            orig[2] += np.linalg.norm(data.X[-1][:2,]-data.X[-2][:2,])
        except IndexError:
            pass
        
        for train, e2, e3, t in zip(trains, E2, E3, times):
            
            startPoint = time.perf_counter()
            X = train[0].step(U,Z)
            t[i] = time.perf_counter() - startPoint
            
            
            e2[i] = np.linalg.norm(data.X[-1][0:2]-X[0:2])
            e3[i] = np.linalg.norm(data.X[-1]-X)
            
    return orig, E2, E3, times
        
    
    


####################################################
####################################################
dG = lambda                                \
    seed=1,                                \
    tact = 10, start = (0,0),              \
    mn=(0.0,0.0), mx=(1,1), a=(0.5,0.5),   \
    epsU = 0.0, epsZR = 0.0, epsZO = 0.0:  \
        DataGenerator["Generators"][1](
            start=start, mn=mn, mx=mx, a=a, tact=tact,
            epsU = epsU, epsZR = epsZR, epsZO = epsZO,
            seed=seed
    )