import numpy as np

def regression(y,trend):
    y = np.array(y)
    y = np.flip(y)
    X = np.arange(1,len(y)+1)
    A = np.vstack([X, np.ones(len(X))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    if trend == "up":        
        if m > 0:
            return 1
        else:
            return 0
    else:
        if m < 0:
            return 1
        else:
            return 0 