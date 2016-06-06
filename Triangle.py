import numpy as np
import math
import matplotlib.pyplot as plt


def plot_bars(n_groups, interps):
    """ Returns a 15-interpretation bar plot for hist_list. Demands package matplotlib.pyplot as plt. """

    index = np.arange(n_groups)
    info = plt.bar(index, interps, width=1, alpha=0.6, color='r')
    plt.xlabel('Number Of Interpretations')
    plt.ylabel('Number Of Solutions')
    plt.title('Number Of Solutions For Each Number Of Interpretations')
    plt.xticks(index + 0.5, index)
    plt.tight_layout()
    plt.show()


def quart_f(coef):
    """ Returns only real roots of the equation for maximum four coefficients.
    Works much faster than numpy.roots() function as uses analytical method. """

    if coef[0] != 0:

        a3 = float(coef[1] / coef[0])
        a2 = float(coef[2] / coef[0])
        a1 = float(coef[3] / coef[0])
        a0 = float(coef[4] / coef[0])

        T1 = -a3 / 4
        T2 = (a2 ** 2) - 3 * a3 * a1 + 12 * a0
        T3 = (2 * (a2 ** 3) - 9 * a3 * a2 * a1 + 27 * (a1 ** 2) + 27 * (a3 ** 2) * a0 - 72 * a2 * a0) / 2
        T4 = (-a3 ** 3 + 4 * a3 * a2 - 8 * a1) / 32
        T5 = (3 * (a3 ** 2) - 8 * a2) / 48

        if T3 ** 2 - T2 ** 3 < 0:
            return []
        else:
            R1 = math.sqrt(T3 ** 2 - T2 ** 3)

        R2 = abs(T3 + R1) ** (1.0 / 3)  # Error 
        # Tada, we actually should not use abs, as it may cause new unexisting roots.

        if T3 + R1 < 0:  # Error
            R2 = -R2  # Error

        R3 = (1.0 / 12) * (T2 / R2 + R2)  # Error

        if T5 + R3 < 0:
            return []
        else:
            R4 = math.sqrt(T5 + R3)

        R5 = 2 * T5 - R3

        if abs(T4) < 1e-10 and abs(R4) < 1e-10:
            R6 = 1
            R4 = 0
        else:
            R6 = T4 / R4

        answer = []

        if R5 - R6 >= 0:  # -1: #Error
            answer.append(T1 - R4 - math.sqrt(R5 - R6))
            answer.append(T1 - R4 + math.sqrt(R5 - R6))

        if R5 + R6 >= 0:  # -1: #Error
            answer.append(T1 + R4 - math.sqrt(R5 + R6))
            answer.append(T1 + R4 + math.sqrt(R5 + R6))

        return answer

    if coef[0] == 0:  # Here begins the cubic function, that should be written after the conference.
        roots = np.roots(coef)
        list_x = []
        for x in roots:
            if x.imag == 0:
                list_x.append(x.real)
            return list_x

def p_tet_sp(angle_a, angle_ab, angle_ad, angle_cd):
    """Returns an array with angles of interest (angle_b, angle_bc, angle_ac)."""

    if (0 > angle_a) or (angle_a > 178) or (0 > angle_ab) or (angle_ab > 178) or (0 > angle_ad) or (angle_ad > 178) or (0 > angle_cd) or (angle_cd > 178):
    return error('Does not exist 1') # angles of the same triangle should be at least equal to 1

    if angle_ad >= angle_ab:
        return error('Does not exist 2')

    if 0 < angle_ab - angle_ad < 180:
        angle_bd = angle_ab - angle_a
    else: 
        return error('Does not exist 3')
    
    angle_b = arctg((math.tg(math.radians(angle_ad))*math.tg(math.radians(angle_ad)))/math.tg(math.radians(angle_ab - angle_ad)))

    angle_bc = arcsin(math.cos(math.radians(angle_ad))*math.sqrt(((math.tg(math.radians(angle_ad))**2)+((math.sin(math.radians(angle_cd))**2)))

    angle_ac = arcsin(math.cos(math.radians(angle_bd))*math.sqrt(((math.tg(math.radians(angle_bd))**2)+((math.sin(math.radians(angle_cd))**2)))

    if 180 <= angle_a + angle_b:
        return error('Does not exist4')
    
    return [angle_b, angle_bc, angle_ac]

def p_tet(angle_a, angle_b, angle_ab, angle_bc, angle_ca):
    """ Returns number of solutions and type of solutions for the given tetrahedron angles."""

    # Valid tetrahedron
    if angle_ab <= 0 or 180 <= angle_ab or angle_bc <= 0 or 180 <= angle_bc or angle_ca <= 0 or 180 <= angle_ca:
        return [0, 10]

    if angle_ab + angle_bc < angle_ca or angle_bc + angle_ca < angle_ab or angle_ca + angle_ab < angle_bc:
        return [0, 10]

    if angle_a <= 0 or 180 <= angle_a or angle_b <= 0 or 180 <= angle_b:
        return [0, 10]

    # Valid triangle
    if 180 <= angle_a + angle_b:
        return [0, 10]

    if 360 <= angle_ab + angle_bc + angle_ca:
        return [0, 10]

    angle_c = 180 - (angle_a + angle_b)

    cosAB = math.cos(math.radians(angle_ab))
    cosBC = math.cos(math.radians(angle_bc))
    cosCA = math.cos(math.radians(angle_ca))

    cosA = math.cos(math.radians(angle_a))
    sinA = math.sin(math.radians(angle_a))
    cosB = math.cos(math.radians(angle_b))
    sinB = math.sin(math.radians(angle_b))

    # Valid triangle and valid image but invalid tetrahedron
    if (180 - angle_ab) + (180 - angle_bc) < angle_b:
        return [0, 11]
    if (180 - angle_bc) + (180 - angle_ca) < angle_c:
        return [0, 11]
    if (180 - angle_ca) + (180 - angle_ab) < angle_a:
        return [0, 11]

    Rab = 1
    Rbc = Rab / (cosB + sinB * cosA / sinA)
    Rca = Rab / (cosA + sinA * cosB / sinB)

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
    g_roots = quart_f(p)

    list_x = []
    for x in g_roots:
        if 0 < x.real:
            list_x.append(x.real)

    if not list_x:  # if list_x is empty
        # Revise this "print" line.
        # print "Case A: (%d, %d, %d) and (%d, %d, %d)" % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return [0, 20]

    num_sol = 0
    type_sol = 0
    for x in list_x:
        if x ** 2 - 2 * x * cosAB + 1 <= 0:
            continue

        a = Rab / math.sqrt(x ** 2 - 2 * x * cosAB + 1)  # A24
        # b = x * a
        # a > 0 and b > 0 because Rab > 0

        m1 = 1 - K1
        p1 = 2 * (K1 * cosCA - x * cosBC)
        q1 = (x ** 2 - K1)

        m2 = 1
        p2 = 2 * (-x * cosBC)
        q2 = x ** 2 * (1 - K2) + 2 * x * K2 * cosAB - K2

        if m1 * q2 - m2 * q1 != 0:
            c = a * ((p2 * q1 - p1 * q2) / (m1 * q2 - m2 * q1))
            if c > 0:
                num_sol += 1
        else:
            type_sol += 1
            if (cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)) > 0:  # it is, perhaps, always true (> 0)
                y1 = cosCA + math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y1 > 0:
                    num_sol += 1
                y2 = cosCA - math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y2 > 0:
                    num_sol += 1
            else:
                continue

    if num_sol == 0:
        # Revise this "print" line.
        print("Case B: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return [0, 21]
    return [num_sol, type_sol]


def hist_base(tAngles, vAngles):
    """ Returns numbers of each of 15 interpretations for the given intervals 
    of tAngles (angles in the base of tetrahedron) and vAngles (visual angles at apex). """

    hb = [0 for a in range(0, 15)]
    for angle_a in tAngles:
        # print("angleA=%d") %angle_a
        for angle_b in tAngles:
            # print("angleB=%d") %angle_b
            if 180 <= angle_a + angle_b and angle_a < angle_b < (180 - angle_a - angle_b):
                for angle_ab in vAngles:
                    for angle_bc in vAngles:
                        for angle_ca in vAngles:
                            results = p_tet(angle_a, angle_b, angle_ab, angle_bc, angle_ca)
                            hb[int(results[0])] += 1
                            if results[1] == 1 or results[1] == 2:
                                # Revise this "print" line.
                                print("Case C: (%d, %d, %d) and (%d, %d, %d)") % (
                                    angle_a, angle_b, (180 - angle_a - angle_b), angle_ab, angle_bc, angle_ca)

    return hb


tAngles = range(1, 180, 1)  # Triangle
vAngles = range(10, 20, 1)  # Visual angles at apex

hist_list = hist_base(tAngles, vAngles)
print(hist_list)
plot_bars(len(hist_list), hist_list)

# An example from Fischler & Bolles (1981)
# angle_abbcca = math.degrees(math.acos(5.0/8.0))
# print p_tetrahedron(60,60,angle_abbcca,angle_abbcca,angle_abbcca)
