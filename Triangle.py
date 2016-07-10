import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import essential_functions as ef


def plot_bars(n_groups, interps, name, filename):
    """
    Returns a bar-plot for given number of bars, values of bars,
    name of a bar-plot and location of an output figure.
    """

    index = np.arange(n_groups)
    plt.bar(index, interps, width=1, alpha=0.6, color='r')
    plt.xlabel('Number Of Interpretations')
    plt.ylabel('Number Of Solutions')
    plt.title(name)
    plt.xticks(index + 0.5, index)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()


def p_tet_sp(angle_a, angle_ab, angle_ad, angle_cd):
    """ Returns an array with angles of interest (angle_b, angle_bc, angle_ac) """

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
    g_roots = ef.quart_f(p)

    # Tada: Do we still need the following paragraph?
    list_x = []
    for x in g_roots:
        if 0 < x.real:
            list_x.append(x.real)

    if not list_x:  # if list_x is empty
        # Revise this "print" line.
        # print "Case A: (%d, %d, %d) and (%d, %d, %d)" % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return 20

    num_sol = 0
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
        # print("Case B: (%d, %d, %d) and (%d, %d, %d)") % (angle_a, angle_b, angle_c, angle_ab, angle_bc, angle_ca)
        return 21

    return num_sol


def hist_base(tAngles, vAnglesAB, vAnglesBC, vAnglesCA, info=False):
    """
    Returns numbers of each of 15 interpretations for the given intervals
    of tAngles (angles in the base of tetrahedron) and vAngles (visual angles at apex)
    """

    iteration = 0
    l = len(list(tAngles))
    hb = [0 for a in range(0, 25)]
    ef.print_progress(iteration, l, prefix='Progress:', suffix='', bar_length=100)
    for angle_a in tAngles:
        if info:
            print('angle A = %s' % angle_a)
        for angle_b in tAngles:
            if info:
                print('angle B = %s' % angle_b)
            if angle_a + angle_b < 180 and angle_a < angle_b < (180 - angle_a - angle_b):
                for angle_ab in vAnglesAB:
                    if info:
                        print('angle AB = %s' % angle_ab)
                    for angle_bc in vAnglesBC:
                        if info:
                            print('angle BC = %s' % angle_bc)
                        for angle_ca in vAnglesCA:
                            if info:
                                print('angle CA = %s' % angle_ca)
                            results = p_tet(angle_a, angle_b, angle_ab, angle_bc, angle_ca)
                            hb[int(results)] += 1
                            if info:
                                print(hb)
        iteration += 1
        ef.print_progress(iteration, l, prefix='Progress:', suffix='', bar_length=50)
    return hb


def exhaustive_test_5d_space():
    """ Tada, please, wright the documentation """

    tAngles = range(1, 180, 1)  # Triangle
    vAnglesAB = range(1, 180, 1)  # Visual angles at apex
    vAnglesBC = range(1, 180, 1)  # Visual angles at apex

    angle_step = range(0, 180, 10)
    for a in angle_step:
        print('%d-%d') % (a, a + 10)
        vAnglesCA = range(a, a + 10, 1)  # Visual angles at apex
        hist_list = hist_base(tAngles, vAnglesAB, vAnglesBC, vAnglesCA)
        print(hist_list)

        f = open('simulation_exhaustive.txt', 'a')
        f.write('%d-%d\n' % (a, a + 10))
        f.write(str(hist_list))
        f.write('\n\n')
        f.close()

        # Tada: We can add some lines in this function to plot a histogram.


def apex_by_ten(info=True):
    """ Calculates 18 bar-plots for groups of 10 visual angles at apex """

    for i in range(18):
        f = open('apex_by_ten.csv', 'a')
        tAngles = range(1, 5, 1)  # Triangle
        range_n = range(i * 10, (i + 1) * 10, 1)  # Visual angles at apex
        vAnglesAB, vAnglesBC, vAnglesCA = range_n, range_n, range_n
        name = str('Triangle angles: %r, Visual angles at apex: %r') % (tAngles, range_n)
        filename = '/Users/basilminkov/PycharmProjects/3D Vision/Output Figures/%s.png' % name
        if info:
            print('Range {lo} - {hi}'.format(lo=i * 10, hi=(i + 1) * 10))
        hist_list = hist_base(tAngles, vAnglesAB, vAnglesBC, vAnglesCA)
        if info:
            print('Input list for histogram: ', hist_list, '\n')
        plot_bars(len(hist_list), hist_list, name, filename)
        f.write(str(hist_list)[1:-1])
        f.write('\n')
        f.close()


def ten_step():
    """ Calculates overall bar-plot with 10 degree step """

    tAngles = range(1, 180, 10)  # Triangle
    vAngles = range(1, 180, 10)  # Visual angles at apex
    name = str('Overall')
    filename = '/Users/basilminkov/PycharmProjects/3D Vision/Output Figures/%s.png' % name
    hist_list = hist_base(tAngles, vAngles)
    plot_bars(len(hist_list), hist_list, name, filename)


def real_mult_log(data='apex_by_ten.csv', excel=True, name='Bar Plots Info.xlsx'):
    """ Creates a data frame and excel book (if excel=True) with all the essential data about
    simulation. Default input data – .csv file, got after implementing the apex_by_ten function.
    Default output book's name is Bar Plots Info.xlsx. """

    if excel:
        writer = pd.ExcelWriter(name)
    df = pd.read_csv(data, header=None)
    invalid = df.loc[:, [10, 11]].sum(axis=1)
    zero = df.loc[:, [20, 21]].sum(axis=1)
    df1 = pd.concat([invalid, zero], axis=1).rename(columns={0: 'Invalid', 1: 'Zeros'})
    df2 = pd.concat([df1, df.loc[:, 0:4]], axis=1)
    for i in range(df2.shape[0]):
        real = df2.iloc[i, :]
        real.name = 'Real'
        by_ten = df2.iloc[i, :].apply(lambda x: x * 10 if x != 1 else x)
        by_ten.name = 'MultByTen'
        log_ten = df2.iloc[i, :].apply(lambda x: np.log10(x) if x != 0 else 0)
        log_ten.name = 'Log10'
        df3 = pd.concat([real, by_ten, log_ten], axis=1).transpose()
        if excel:
            df3.to_excel(writer, 'Range {}'.format(i+1))
    if excel:
        writer.save()
    return df3
