from triangle_project.algorithms.Fischler_and_Bolles import *
from triangle_project.essential_functions.technical_issues import *

# These functions are used for exhaustive simulation essential for the first part of a project.


def hist_base(tAngles, vAnglesAB, vAnglesBC, vAnglesCA, info=False):
    """
    Returns numbers of each of 15 interpretations for the given intervals
    of tAngles (angles in the base of tetrahedron) and vAngles (visual angles at apex)
    """

    iteration = 0
    l = len(list(tAngles))
    hb = [0 for a in range(0, 25)]
    print_progress(iteration, l, prefix='Progress:', suffix='', bar_length=100)
    for angle_a in tAngles:
        if info:
            print('angle A = %s' % angle_a)
        for angle_b in tAngles:
            if info:
                print('angle B = %s' % angle_b)
            if angle_a + angle_b < 180 and angle_a <= angle_b <= (180 - angle_a - angle_b):
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
        print_progress(iteration, l, prefix='Progress:', suffix='', bar_length=50)
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
        tAngles = range(1, 180, 1)  # Triangle
        range_n = range(i * 10 + 1, (i + 1) * 10, 1)  # Visual angles at apex
        vAnglesAB, vAnglesBC, vAnglesCA = range_n, range_n, range_n
        # name = str('Triangle angles: %r, Visual angles at apex: %r') % (tAngles, range_n)
        # filename = '/Users/basilminkov/PycharmProjects/3D Vision/Output Figures/%s.png' % name
        if info:
            print('Range {lo} - {hi}'.format(lo=i * 10 +1, hi=(i + 1) * 10))
        hist_list = hist_base(tAngles, vAnglesAB, vAnglesBC, vAnglesCA)
        if info:
            print('Input list for histogram: ', hist_list, '\n')
        # plot_bars(len(hist_list), hist_list, name, filename)
        f.write(str(hist_list)[1:-1])
        f.write('\n')
        f.close()

def angle_min_max():
    tAngles = range(0, 180, 1)  # Triangle
    vAnglesAB = range(0, 180, 1)  # Visual angles at apex
    vAnglesBC = range(0, 180, 1)  # Visual angles at apex
    vAnglesCA = range(0, 180, 1)  # Visual angles at apex

    histTotal = [0 for a in range(0, 25)]
    histMin = [[0 for x in range(25)] for y in range(18)]
    histMax = [[0 for x in range(25)] for y in range(18)]

    for angle_a in tAngles:
        print('angle_a = %d' % angle_a)
        for angle_b in tAngles:
            angle_c = (180 - angle_a - angle_b)
            if angle_a + angle_b < 180 and angle_a <= angle_b <= angle_c:
                for angle_ab in vAnglesAB:
                    for angle_bc in vAnglesBC:
                        for angle_ca in vAnglesCA:
                            results = p_tet(angle_a, angle_b, angle_ab, angle_bc, angle_ca)
                            histTotal[int(results)] += 1
                            indexMin = int(min(angle_ab, angle_bc, angle_ca) / 10)
                            indexMax = int(max(angle_ab, angle_bc, angle_ca) / 10)
                            histMin[indexMin][int(results)] += 1
                            histMax[indexMax][int(results)] += 1

    f = open('simulation_3types.txt', 'a')

    f.write('Total Hist\n')
    f.write(str(histTotal))
    f.write('\n\n')
    print(histTotal)

    print('\n\n\nHist Min(Angle)\n')
    f.write('\n\n\nHist Min(Angle)\n')
    for a in range(0, 18, 1):
        print(histMin[a])
        f.write('%d-%d\n' % (a * 10, a * 10 + 10))
        f.write(str(histMin[a]))
        f.write('\n\n')

    print('\n\n\nHist Max(Angle)\n')
    f.write('\n\n\nHist Max(Angle)\n')
    for a in range(0, 18, 1):
        print(histMax[a])
        f.write('%d-%d\n' % (a * 10, a * 10 + 10))
        f.write(str(histMax[a]))
        f.write('\n\n')

    f.close()