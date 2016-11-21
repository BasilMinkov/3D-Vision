from triangle_project.essential_functions.polynomial_equation import *

# Some algorithms based on Fischler & Bolles article (1981) are stored here.

def p_tet(angle_a, angle_b, angle_ab, angle_bc, angle_ca):
    """ Returns number of solutions and type of solutions for the given tetrahedron angles """

    # Valid tetrahedron
    if angle_ab <= 0 or 180 <= angle_ab or angle_bc <= 0 or 180 <= angle_bc or angle_ca <= 0 or 180 <= angle_ca:
        return 10

    if angle_ab + angle_bc < angle_ca or angle_bc + angle_ca < angle_ab or angle_ca + angle_ab < angle_bc:
        return 10

    if angle_a <= 0 or 180 <= angle_a or angle_b <= 0 or 180 <= angle_b:
        return 10

    # Valid triangle
    if 180 <= angle_a + angle_b:
        return 10

    if 360 <= angle_ab + angle_bc + angle_ca:
        return 10

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
        return 11
    if (180 - angle_bc) + (180 - angle_ca) < angle_c:
        return 11
    if (180 - angle_ca) + (180 - angle_ab) < angle_a:
        return 11

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
        if 0 < x.real and x.real not in list_x:
            list_x.append(x.real)

    if not list_x:  # if list_x is empty
        return 20

    tooSmall = 0.000000001
    
    num_sol = 0
    for x in list_x:
        if x ** 2 - 2 * x * cosAB + 1 <= 0:
            continue

        a = Rab / math.sqrt(x ** 2 - 2 * x * cosAB + 1)  # A24
        b = x * a
        # a > 0 and b > 0 because Rab > 0
        
        if angle_a == angle_bc and a < tooSmall:
            continue
        if angle_b == angle_ca and b < tooSmall:
            continue

        m1 = 1 - K1
        p1 = 2 * (K1 * cosCA - x * cosBC)
        q1 = (x ** 2 - K1)

        m2 = 1
        p2 = 2 * (-x * cosBC)
        q2 = x ** 2 * (1 - K2) + 2 * x * K2 * cosAB - K2

        if m1 * q2 - m2 * q1 != 0:
            c = a * ((p2 * q1 - p1 * q2) / (m1 * q2 - m2 * q1))
            
            if angle_c == angle_ab and c < tooSmall:
                continue
                
            if c > 0:
                num_sol += 1
        else:
            if (cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)) > 0:  # it is, perhaps, always true (> 0)
                y1 = cosCA + math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y1 > 0:
                    num_sol += 1
                    if angle_c == angle_ab and y1*a < tooSmall:
                        num_sol -= 1
                        
                y2 = cosCA - math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y2 > 0:
                    num_sol += 1
                    if angle_c == angle_ab and y2*a < tooSmall:
                        num_sol -= 1

            else:
                continue

    if num_sol == 0:
        # Revise this "print" line.
        # print("Case B: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return 21

    return num_sol


def p_tet_calc(angle_a, angle_b, angle_ab, angle_bc, angle_ca):
    """ Returns number of solutions and type of solutions for the given tetrahedron angles """

    # Valid tetrahedron
    if angle_ab <= 0 or 180 <= angle_ab or angle_bc <= 0 or 180 <= angle_bc or angle_ca <= 0 or 180 <= angle_ca:
        return []

    if angle_ab + angle_bc < angle_ca or angle_bc + angle_ca < angle_ab or angle_ca + angle_ab < angle_bc:
        return []

    if angle_a <= 0 or 180 <= angle_a or angle_b <= 0 or 180 <= angle_b:
        return []

    # Valid triangle
    if 180 <= angle_a + angle_b:
        return []

    if 360 <= angle_ab + angle_bc + angle_ca:
        return []

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
        return []
    if (180 - angle_bc) + (180 - angle_ca) < angle_c:
        return []
    if (180 - angle_ca) + (180 - angle_ab) < angle_a:
        return []

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

    # Tada: Do we still need the following paragraph?
    list_x = []
    for x in g_roots:
        if 0 < x.real:
            list_x.append(x.real)

    if not list_x:  # if list_x is empty
        # Revise this "print" line.
        # print "Case A: (%d, %d, %d) and (%d, %d, %d)" % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return []

    num_sol = []
    for x in list_x:
        if x ** 2 - 2 * x * cosAB + 1 <= 0:
            continue

        a = Rab / math.sqrt(x ** 2 - 2 * x * cosAB + 1)  # A24
        b = x * a
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
                num_sol.append([a, b, c])
        else:
            if (cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)) > 0:  # it is, perhaps, always true (> 0)
                y1 = cosCA + math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y1 > 0:
                    num_sol.append([a, b, y1 * a])
                y2 = cosCA - math.sqrt((cosCA ** 2) + (((Rca ** 2) - (a ** 2)) / (a ** 2)))  # A27
                if y2 > 0:
                    num_sol.append([a, b, y2 * a])
            else:
                continue

                # if num_sol == 0:
                # Revise this "print" line.
                # print("Case B: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
                # return 21

    return num_sol
