import numpy as np

uff_file = 'UFF_redux.csv'

names = np.genfromtxt(uff_file, skip_header=1, usecols=0, dtype=str, delimiter=',')
sigmas = np.genfromtxt(uff_file, skip_header=1, usecols=1, dtype=str, delimiter=',')
epsilons = np.genfromtxt(uff_file, skip_header=1, usecols=2, dtype=str, delimiter=',')

with open('force_field_mixing_rules.def', "a") as mix_file:
    for i in range(len(names)):
        mix_file.write(
                '%s\t\tlennard-jones\t%s\t%s\n' % (names[i], epsilons[i], sigmas[i])
        )
