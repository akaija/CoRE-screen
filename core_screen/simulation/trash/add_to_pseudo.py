import numpy as np

uff_file = 'UFF_redux.csv'

names = np.genfromtxt(uff_file, skip_header=1, usecols=0, dtype=str, delimiter=',')

with open('pseudo_atoms.def', "a") as mix_file:
    for i in range(len(names)):
        mix_file.write(
            '%s  yes  C   C   0   12.0  0.0  0.0  1.0  1.0  0  0  absolute  0\n' % names[i])
