import numpy as np
import matplotlib.pyplot as plt

# These functions are used for making bar plots from the experimental data.

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


def plot_log_bars(n_groups, interps, name, filename):
    """
    Returns a logarithmic bar-plot for given number of bars, values of bars,
    name of a bar-plot and location of an output figure.
    """

    index = np.arange(n_groups)
    plt.bar(index, interps, width=1, alpha=0.6, color='r')
    plt.ylim([10 ** 0, 10 ** 8])
    plt.xlabel('Number Of Interpretations')
    plt.ylabel('Number Of Solutions')
    plt.title(name)
    plt.yscale('log')
    plt.xticks(index + 0.5, [0, 1, 2, 3, 4])
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()