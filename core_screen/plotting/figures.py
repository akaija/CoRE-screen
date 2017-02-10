import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import numpy as np
from sqlalchemy import *

from core_screen.plotting.queries import *

def get_x(x):
    if x == 'GA':
        return query_GA()
    elif x == 'SA':
        return query_SA()
    elif x == 'VF':
        return query_VF()

def get_limits(x):
    if x == 'GA':
        return [0., 300.]
    elif x == 'SA':
        return [0., 4000.]
    elif x == 'VF':
        return [0., 1.]

def plot_CS(x, y):
    """
    Args:
        x
        y ('GA', 'SA', 'VF')

    Returns:
        None

    """
    x_ = x
    y_ = y
    x = get_x(x)
    y = get_x(y)

    my_dpi = 96
    plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
    plt.xlim(*get_limits(x_))
    plt.ylim(*get_limits(y_))
#    plt.xlabel(x_)
#    plt.ylabel(y_)
    plt.scatter(x, y, marker='o', facecolors='k', edgecolors='none', alpha=0.6, s=10)
    plt.tick_params(axis='both', which='both', labelbottom='off', labelleft='off')
    plt.savefig(
            '%s_%s_plot.png' % (x_, y_),
            dpi=my_dpi,
            transparent = True,
            bbox_inches = 'tight',
            pad_inches = 0
    )
    plt.cla()
