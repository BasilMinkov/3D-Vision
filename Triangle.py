import numpy as np
import math
import matplotlib.pyplot as plt

def plot_bars(n_groups, interps):
    index = np.arange(n_groups)
    info = plt.bar(index, interps, width=1, alpha=0.6, color='r')
    plt.xlabel('Number Of Interpretations')
    plt.ylabel('Number Of Solutions')
    plt.title('Number Of Solutions For Each Number Of Interpretations')
    plt.xticks(index+0.5, index)
    plt.tight_layout()
    plt.show()

def quart_f(zero, a, b, c, d):

    if zero != 0:

        a3 = float(a/zero)
        a2 = float(b/zero)
        a1 = float(c/zero)
        a0 = float(d/zero)

        T1 = -a3/4
        T2 = (a2 ** 2) - 3*a3*a1 + 12*a0
        T3 = (2*(a2**3) - 9*a3*a2*a1 + 27*(a1**2) + 27*(a3**2)*a0 - 72*a2*a0)/2
        T4 = (-a3**3 + 4*a3*a2 - 8*a1)/32
        T5 = (3*(a3**2) - 8*a2)/48

        if T3**2 - T2**3 < 0:
            return []
        else:
            R1 = math.sqrt(T3**2 - T2**3)

        R2 = (T3 + R1)**(1/3)
        R3 = (1/12)*(T2/R2 + R2)

        if T5 + R3 < 0:
            return []
        else:
            R4 = math.sqrt(T5 + R3)

        R5 = 2*T5 - R3
        R6 = T4/R4

        answer = []

        if R5 - R6 > -1:
            r1 = T1 - R4 - math.sqrt(R5 - R6)
            r2 = T1 - R4 + math.sqrt(R5 - R6)
            answer.append(r1)
            answer.append(r2)

        if R5 + R6 > -1:
            r3 = T1 + R4 - math.sqrt(R5 + R6)
            r4 = T1 + R4 + math.sqrt(R5 + R6)
            answer.append(r3)
            answer.append(r4)

        return answer

    if zero == 0:
        return np.roots(a, b, c, d) # Here begins the cubic function.

def p_tetrahedron(angle_a, angle_b, angle_ab, angle_bc, angle_ca):
    # Valid tetrahedron
    if angle_ab <= 0 or 180 <= angle_ab  or  angle_bc <= 0 or 180 <= angle_bc  or  angle_ca <= 0 or 180 <= angle_ca:
        return [0,10]

    if angle_ab+angle_bc < angle_ca or angle_bc+angle_ca < angle_ab or angle_ca+angle_ab < angle_bc:
        return [0,10]

    if angle_a <= 0 or 180 <= angle_a  or  angle_b <= 0 or 180 <= angle_b:
        return [0,10]

    # Valid triangle
    if 180 <= angle_a + angle_b:
        return [0,10]

    if 360 <= angle_ab + angle_bc + angle_ca:
        return [0,10]

    angle_c = 180 - (angle_a + angle_b)

    cosAB = math.cos(math.radians(angle_ab))
    cosBC = math.cos(math.radians(angle_bc))
    cosCA = math.cos(math.radians(angle_ca))

    cosA = math.cos(math.radians(angle_a))
    sinA = math.sin(math.radians(angle_a))
    cosB = math.cos(math.radians(angle_b))
    sinB = math.sin(math.radians(angle_b))

    # Valid triangle and valid image but invalid tetrahedron
    if (180-angle_ab)+(180-angle_bc) < angle_b:
        return [0,11]
    if (180-angle_bc)+(180-angle_ca) < angle_c:
        return [0,11]
    if (180-angle_ca)+(180-angle_ab) < angle_a:
        return [0,11]

    Rab = 1
    Rbc = Rab/(cosB+sinB*cosA/sinA)
    Rca = Rab/(cosA+sinA*cosB/sinB)

    K1 = (Rbc ** 2) / (Rca ** 2)
    K2 = (Rbc ** 2) / (Rab ** 2)

    G4 = (K1 * K2 - K1 - K2) ** 2 - 4 * K1 * K2 * (cosBC ** 2)
    G3 = 4 * (K1 * K2 - K1 - K2) * K2 * (1 - K1) * cosAB + 4 * K1 * cosBC * (
        (K1 * K2 + K2 - K1) * cosCA + 2 * K2 * cosAB * cosBC)
    G2 = (2 * K2 * (1 - K1) * cosAB) ** 2 + 2 * (K1 * K2 + K1 - K2) * (K1 * K2 - K1 - K2) + 4 * K1 * (
        (K1 - K2) * (cosBC ** 2) + (1 - K2) * K1 * (cosCA ** 2) - 2 * K2 * (1 + K1) * cosAB * cosCA * cosBC)
    G1 = 4 * (K1 * K2 + K1 - K2) * K2 * (1 - K1) * cosAB + 4 * K1 * (
        (K1 * K2 - K1 + K2) * cosCA * cosBC + 2 * K1 * K2 * cosAB * (cosCA ** 2))
    G0 = (K1 * K2 + K1 - K2) ** 2 - 4 * (K1 ** 2) * K2 * (cosCA ** 2)

    p = [G4, G3, G2, G1, G0]
    g_roots = list(np.roots(p))

    list_x = []
    for x in g_roots:
        if x.imag == 0 and 0 < x.real:
            list_x.append(x.real)

    if list_x == []:
        # Revise this "print" line.
        # print "Case A: (%d, %d, %d) and (%d, %d, %d)" % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return [0,20]

    numSolutions = 0
    typeSolutions = 0
    for x in list_x:

        if x**2 - 2*x*cosAB + 1 <= 0:
            continue

        a = Rab / math.sqrt(x**2 - 2*x*cosAB + 1)  # A24
        #b = x * a
        # a > 0 and b > 0 because Rab > 0

        m1 = 1-K1
        p1 = 2*(K1*cosCA - x*cosBC)
        q1 = (x**2 - K1)

        m2 = 1
        p2 = 2*(-x*cosBC)
        q2 = x**2 * (1-K2) + 2*x*K2*cosAB - K2

        if m1*q2-m2*q1 != 0:
            c = a * ((p2*q1 - p1*q2) / (m1*q2 - m2*q1))
            if c > 0:
                numSolutions += 1
        else:
            typeSolutions += 1
            if (cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)) > 0: # it is, perhaps, always true (> 0)
                y1 = cosCA + math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y1 > 0:
                    numSolutions += 1

                y2 = cosCA - math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y2 > 0:
                    numSolutions += 1
            else:
                continue

    if numSolutions == 0:
        # Revise this "print" line.
        print("Case B: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return [0,21]
    return [numSolutions, typeSolutions]

def hist_base(tAngles, vAngles):
    # hist_base = {a: 0 for a in range(0, 15)}
    hist_base = [0 for a in range(0, 15)]
    for angle_a in tAngles:
        #print "angleA=%d" %angle_a
        for angle_b in tAngles:
            #print "angleB=%d" %angle_b

            if 180 <= angle_a + angle_b:
                continue

            if angle_a < angle_b:
                continue

            if angle_b < (180 - angle_a - angle_b):
                continue

            for angle_ab in vAngles:
                for angle_bc in vAngles:
                    for angle_ca in vAngles:
                        results = p_tetrahedron(angle_a, angle_b, angle_ab, angle_bc, angle_ca)
                        hist_base[int(results[0])] += 1

                        if results[1]==1 or results[1]==2:
                            # Revise this "print" line.
                            print("Case C: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, (180 - angle_a - angle_b), angle_ab, angle_bc, angle_ca)

    return hist_base

tAngles = range(1, 180, 1) # Triangle
vAngles = range(10, 20, 1)  # Visual angles at apex

hb = hist_base(tAngles, vAngles)
print(hb)
plot_bars(len(hb), hb)

# An example from Fischler & Bolles (1981)
# angle_abbcca = math.degrees(math.acos(5.0/8.0))
# print p_tetrahedron(60,60,angle_abbcca,angle_abbcca,angle_abbcca)
