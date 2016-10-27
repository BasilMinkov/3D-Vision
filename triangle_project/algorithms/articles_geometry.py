import math
import numpy as np

"""
Some algorithms dealing with simple geometry that are useful for various articles on vision science stimuli analysis
are stored hear. Basically these functions are used to prepare data for Fischler and Bolles algorithm (2016).
"""


"""
The Measurement of Shape-Constancy (Gottheil & Bitterman, 1951)

There is a tetrahedron. Triangle ABC is the base of the tetrahedron. It represents the 3D triangle.
In all the cases it is assumed that the plane of 2D triangle is perpendicular to the observer's visual axis =>
angles ADE, BDE are straight.

1. distance = DE : D ∈ AB
    a. slanted_case1(altitude, distance, slant): In this case the 3D triangle is slanted and equilateral.
    b. straight_case1(altitude, distance): In this case the 3D triangle is not slanted.
       Angle alpha is equal to angle beta.

2. distance = CE
    a. slanted_case2(altitude, distance, slant): In this case the 3D triangle is slanted and equilateral.
    b. straight_case2(altitude, distance): In this case the 3D triangle is not slanted.
       Angle alpha is equal to angle beta.

3. distance = EH, where H – orthocenter
    a. slanted_case3(altitude, distance, slant): In this case the 3D triangle is slanted and equilateral.
    b. straight_case3(altitude, distance): In this case the 3D triangle is not slanted.
       Angle alpha is equal to angle beta.
"""


# 1. distance = DE : D ∈ AB


def slanted_case1(altitude=9, distance=300, slant=65):
    """ In this case the 3D triangle is slanted and equilateral. """

    angle_ce = np.radians(slant)

    # 3D angles
    angle_a = np.radians(60)
    angle_b = angle_a
    # angle_c = angle_a

    # Visual angles
    angle_ab = 2*np.arctan(altitude/(np.tan(angle_b)*distance))
    angle_bc = np.arccos((altitude**2 + distance ** 2 - (2*altitude*distance*np.cos(angle_ce)) +
                          (altitude/np.tan(angle_b))**2 + distance**2)/(2*np.sqrt(((altitude**2 +
                            distance**2 - 2*altitude*distance*angle_ce)*((altitude/np.tan(angle_b))**2+distance**2)))))
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca # Most of numpy functions uses radians.
    # Perhaps, it's better to keep radians and check the rest of the code, as multiplied concertation
    # to certain degree causes floating point errors.


def straight_case1(altitude=18, distance=300):
    """ In this case the 3D triangle is not slanted. Angle alpha is equal to angle beta. """

    base = 18/np.sqrt(3)  # same as in the slanted case according to the article, as base remains stable

    # 3D angles
    angle_a = np.radians(np.arctan((2*altitude)/base))
    angle_b = angle_a
    # angle_c = np.radians(60)

    # Visual angles
    angle_ab = 2*np.arctan(altitude/(np.tan(angle_b)*distance))  # make it simpler !!!
    angle_bc = (2*(distance**2) + altitude**2 + (altitude/np.tan(angle_b))**2 -
                (altitude**2)*((np.tan(angle_b)**2+1)/np.tan(angle_b)))/(2*np.sqrt((altitude**2 +
                    distance**2)*((altitude/np.tan(angle_b))**2+distance)))
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca


# 2. distance = CE


def slanted_case2(altitude=9, distance=300, slant=65):
    """ In this case the 3D triangle is slanted and equilateral. """

    angle_ce = np.radians(slant)

    # 3D angles
    angle_a = np.radians(60)
    angle_b = angle_a
    # angle_c = angle_a

    # Visual angles
    angle_ab = 2*np.arctan((altitude*np.sin(angle_ce))/(np.tan(angle_b)*np.sin(2*np.pi-np.arcsin(angle_ce +
                                                        np.arcsin((np.sin(angle_ce)*altitude)/distance)))))
    angle_bc = np.arccos(((distance**2+(altitude/(np.tan(angle_b)*np.sin(angle_ab/2)))**2-(altitude/np.sin(angle_b))**2)
                          *np.sin(angle_a)*np.sin(angle_ab/2))/((2*(altitude**2))/np.tan(angle_b)))
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca


def straight_case2(altitude=18, distance=300):
    """ In this case the 3D triangle is not slanted. Angle alpha is equal to angle beta. """

    base = 18/np.sqrt(3)  # same as in the slanted case according to the article, as base remains stable

    # 3D angles
    angle_a = np.radians(np.arctan((2*altitude)/base))
    angle_b = angle_a
    # angle_c = np.radians(60)

    # Visual angles
    angle_ab = 2*np.arctan(altitude/(np.tan(angle_b)*distance))  # make it simpler !!!
    angle_bc = (2*(distance**2) + altitude**2 + (altitude/np.tan(angle_b))**2 -
                (altitude**2)*((np.tan(angle_b)**2+1)/np.tan(angle_b)))/(2*np.sqrt((altitude**2 +
                    distance**2)*((altitude/np.tan(angle_b))**2+distance)))
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca


# 3. distance = EH, where H – orthocenter.


def slanted_case3(altitude=9, distance=300, slant=65):
    """ In this case the 3D triangle is slanted and equilateral. """

    angle_ce = np.radians(slant)

    # 3D angles
    angle_a = np.radians(60)
    angle_b = angle_a
    # angle_c = angle_a

    # Visual angles
    angle_ab = 2*np.arctan((altitude*np.sin(angle_ce))/(np.tan(angle_b)*np.sin(2*np.pi-np.arcsin(angle_ce +
                                                        np.arcsin((np.sin(angle_ce)*altitude)/distance)))))
    angle_bc = angle_ab  #
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca


def straight_case3(altitude=18, distance=300):
    """ In this case the 3D triangle is not slanted. Angle alpha is equal to angle beta. """

    base = 18/np.sqrt(3)  # same as in the slanted case according to the article, as base remains stable

    # 3D angles
    angle_a = np.radians(np.arctan((2*altitude)/base))
    angle_b = angle_a
    # angle_c = np.radians(60)

    # Visual angles
    angle_ab = 2*np.arctan(altitude/(np.tan(angle_b)*distance))  # make it simpler !!!
    angle_bc = (2*(distance**2) + altitude**2 + (altitude/np.tan(angle_b))**2 -
                (altitude**2)*((np.tan(angle_b)**2+1)/np.tan(angle_b)))/(2*np.sqrt((altitude**2 +
                    distance**2)*((altitude/np.tan(angle_b))**2+distance)))
    angle_ca = angle_bc  # because of the assumption

    return angle_a, angle_b, angle_ab, angle_bc, angle_ca

# Other functions


def p_tet_sp(angle_a, angle_ab, angle_ad, angle_cd):
    """ Returns an array with angles of interest (angle_b, angle_bc, angle_ac). Summer 2016. """

    if (0 > angle_a) or (angle_a > 178) or (0 > angle_ab) or (angle_ab > 178) or (0 > angle_ad) or (angle_ad > 178) or \
            (0 > angle_cd) or (angle_cd > 178):
        return exit('Does not exist 1')  # Angles of the same triangle should be at least equal to 1

    if angle_ad >= angle_ab:
        return exit('Does not exist 2')  # Angle_ab = Angle_ad + Angle_bd

    if 0 < angle_ab - angle_ad < 180:
        angle_bd = angle_ab - angle_a
    else:
        return exit('Does not exist 3')

    angle_b = math.atan(
        (math.tan(math.radians(angle_a)) * math.tan(math.radians(angle_ad))) / math.tan(math.radians(angle_bd)))

    angle_bc = math.asin(math.cos(math.radians(angle_ad)) * math.sqrt(
        ((math.tan(math.radians(angle_ad)) ** 2) + (math.sin(math.radians(angle_cd)) ** 2))))

    angle_ac = math.asin(math.cos(math.radians(angle_bd)) * math.sqrt(
        ((math.tan(math.radians(angle_bd)) ** 2) + (math.sin(math.radians(angle_cd)) ** 2))))

    if 180 <= angle_a + angle_b:
        return exit('Does not exist 4')  # Angle_a + Angle_b + Angle_c = 180

    return [angle_b, angle_bc, angle_ac]