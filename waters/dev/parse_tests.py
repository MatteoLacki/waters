%load_ext autoreload
%autoreload 2
from waters.parsers import XMLparser, iaDBsXMLparser, Apex3Dparser
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')


path = Path('/home/matteo/Projects/waters/data/T181207_07')
apex = path/'T181207_07_Apex3D.xml'
pep3d = path/'T181207_07_Pep3D_Spectrum.xml'

# A = XMLparser(apex)
# # P = XMLparser(pep3d)
# A.get_all_tag_counts()
# P.get_tag_counts()


# LE = next(A.root.iter('LE'))
# LE.text[:100]
# LE.text[-200:]

# HE = next(A.root.iter('HE'))
# HE.text[:100]
# HE.text[-200:]
# LE.text.count('\n')
# HE.text.count('\n')

A = Apex3Dparser(apex)
le = A.LE()
plt.plot(le.RT, le.Intensity)

he = A.HE()
le.to_hdf(apex.with_suffix('.hdf5'), 'LE', format='fixed')
he.to_hdf(apex.with_suffix('.hdf5'), 'HE', format='fixed')

rt_bins = np.linspace(he.RT[0], he.RT[len(he.RT)-1], 10000)
Ibin, rt_bins = np.histogram(he.RT, rt_bins, weights=he.Intensity)
rt_mids = (rt_bins[:-1] + rt_bins[1:])/2
plt.plot(rt_mids, Ibin)


he.to_hdf(apex.with_suffix('.hdf5'), 'HE', complevel=9)

pd.read_hdf(apex.with_suffix('.hdf5'), 'HE')

plt.hist(x.Mobility, bins=300)
len(Counter(x.Mobility))

x.Intensity.hist(bins=1000)
I = x.Intensity
plt.hist(I[I<8000], bins=100)
plt.hist(np.log(I), bins=100)




