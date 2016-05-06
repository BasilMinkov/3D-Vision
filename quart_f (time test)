import numpy as np
import math
import random as rd
import time

def quart_f(coef):

    if coef[0] != 0:

        a3 = float(coef[1]/coef[0])
        a2 = float(coef[2]/coef[0])
        a1 = float(coef[3]/coef[0])
        a0 = float(coef[4]/coef[0])

        T1 = -a3/4
        T2 = (a2**2) - 3*a3*a1 + 12*a0
        T3 = (2*(a2**3) - 9*a3*a2*a1 + 27*(a1**2) + 27*(a3**2)*a0 - 72*a2*a0)/2
        T4 = (-a3**3 + 4*a3*a2 - 8*a1)/32
        T5 = (3*(a3**2) - 8*a2)/48

        if T3**2 - T2**3 < 0:
            return []
        else:
            R1 = math.sqrt(T3**2 - T2**3)

        R2 = abs(T3 + R1)**(1.0/3) #Error
        R3 = (1.0/12)*(T2/R2 + R2) #Error

        if T3 + R1 < 0: #Error
            R2 = -R2 #Error

        if T5 + R3 < 0:
            return []
        else:
            R4 = math.sqrt(T5 + R3)

        R5 = 2*T5 - R3

        if abs(T4) < 1e-10 and abs(R4) < 1e-10:
            R6 = 1
            R4 = 0
        else:
            R6 = T4/R4

        answer = []

        if R5 - R6 >= 0: #-1: #Error
            answer.append( T1 - R4 - math.sqrt(R5 - R6) )
            answer.append( T1 - R4 + math.sqrt(R5 - R6) )

        if R5 + R6 >= 0: # -1: #Error
            answer.append( T1 + R4 - math.sqrt(R5 + R6) )
            answer.append( T1 + R4 + math.sqrt(R5 + R6) )

        return answer

    if coef[0] == 0:
        coef.remove(1)
        return np.roots(coef)

def recalc(coef,roots):
    vals = []
    for r in roots:
        vals.append(coef[0]*r**4 + coef[1]*r**3 + coef[2]*r**2 + coef[3]*r +coef[4])
    return vals

num_iteration = 10000
rseed = time.time() * 1000

#Only random functions
rd.seed(rseed)
t0 = time.time()
for i0 in range(0,num_iteration):
    coef =[rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000]
t0 = time.time() - t0

#Basil' roots
rd.seed(rseed)
t1 = time.time()
for i1 in range(0,num_iteration):
    coef =[rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000]
    real_roots1 = quart_f(coef)
t1 = time.time() - t1

#Numpy's roots
rd.seed(rseed)
t2 = time.time()
for i2 in range(0,num_iteration):
    coef =[rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000,rd.random()*1000]
    roots2 = np.roots(coef)
t2 = time.time() - t2

print(t0,t1,t2)
print("Ratio: %.1f") % (t2/t1)
