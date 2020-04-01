%load_ext autoreload
%autoreload 2
from waters.parsers import XMLparser, iaDBsXMLparser, Apex3Dparser
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

data_f = Path('~/Projects/WatersData').expanduser()
apexPaths = list(data_f.glob('*/*_Apex3D.xml'))

apex3d = next(data_f.glob('*/*_Apex3D.xml'))
pep3d = next(data_f.glob('*/*_Pep3D_Spectrum.xml'))

A = Apex3Dparser(apex3d)
le = A.LE()
he = A.HE()
A.get_all_tag_counts()




plt.plot(le.RT, le.Intensity)
plt.show()
plt.hist(le.Fwhm, 1000)



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




