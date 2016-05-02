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
