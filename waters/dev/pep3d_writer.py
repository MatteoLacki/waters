%load_ext autoreload
%autoreload 2
from pathlib import Path
from collections import Counter
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 30)
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
import statsmodels.api as sm
from platform import system

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser, df2text, col2format

if system() == 'Linux':
    data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
    data_f = Path('/home/matteo/Projects/WatersData/O200114_03').expanduser()
else:
    data_f = Path(r'C:\SYMPHONY_VODKAS\WatersData\OHeLa100\O190302_01')
    data_f = Path(r"C:\SYMPHONY_VODKAS\WatersData\O190303_78")
pep3d  = next(data_f.glob('*_Pep3D_Spectrum.xml'))

P3D = Pep3Dparser(pep3d)
P3D.get_all_tag_counts()

le = P3D.LE
he = P3D.HE

le['Intensity'] = 10000
P3D.LE = le
df = le[:5].copy()




le.MobilitySD.hist()
Counter(le.MobilitySD)
le.Mobility.hist(bins=1000)
plt.show()

plt.scatter(le.ADCResponse, le.Intensity)
plt.show()
plt.scatter(le.ADCResponse, le.MassSD)
plt.show()
# # No LE == 1
# LE_1 = np.fromstring("770,777,779,781,782,783,784,785,786,788,791,795,801,802,803,806,810,815,820,821,832,833,838,840,842,845,849,850,851,855,858,859,860,863,866,867,869,870,872,873,876,878,880,881,885", sep=',', dtype=int)
# he.loc[LE_1]

plt.scatter(he.ADCResponse, he.Intensity, s=.1)
plt.show()

plt.scatter(np.log(he.Mass), np.log(he.Intensity) - np.log(he.ADCResponse), s=.1, c=pd.Categorical(he.Z))
plt.show()

Counter(he.Z)
heZ1 = he[he.Z==1]
plt.scatter(np.log(heZ1.Mass), np.log(heZ1.Intensity) - np.log(heZ1.ADCResponse), s=.1)
plt.scatter(np.log(heZ1.Mass), np.log(heZ1.ADCResponse), s=.1)
plt.show()

plt.scatter(np.log(heZ1.Intensity), np.log(heZ1.ADCResponse), s=.1)


plt.hist(np.log(heZ1.Intensity) - np.log(heZ1.ADCResponse), bins=100)
plt.scatter(np.log(heZ1.Mass), (np.log(heZ1.Intensity) - np.log(heZ1.ADCResponse)), s=.1)
plt.show()

plt.hist(7.0175 - .4963*np.log(heZ1.Mass) + 1.0037*np.log(heZ1.Intensity) - np.log(heZ1.Intensity), bins=1000)
plt.show()


mod = ols(formula='np.log(ADCResponse) ~ 1 + np.log(Mass) + np.log(Intensity)', data=heZ1)
res = mod.fit()
print(res.summary())
plt.scatter(np.log(heZ1.ADCResponse), res.fittedvalues-np.log(heZ1.ADCResponse), s=.1)
plt.show()

huber_t = sm.RLM.from_formula(formula='np.log(ADCResponse) ~ 1 + np.log(Mass) + np.log(Intensity)', data=heZ1)
hub_results = huber_t.fit()
print(hub_results.params)
print(hub_results.bse)
print(hub_results.summary(yname='y',
            xname=['var_%d' % i for i in range(len(hub_results.params))]))
plt.scatter(np.log(heZ1.ADCResponse), hub_results.fittedvalues-np.log(heZ1.ADCResponse), s=.1)
plt.show()

# Models per charge.
models = {}
for Z, D in he.groupby(he.Z):
    models[Z] = sm.RLM.from_formula(formula='np.log(ADCResponse) ~ 1 + np.log(Mass) + np.log(Intensity)', data=D).fit()

ZZ = []
Intercepts = []
for Z,M in models.items():
    ZZ.append(Z)
    Intercepts.append(M.params['Intercept'])
ZZ = np.array(ZZ)
Intercepts = np.array(Intercepts)
plt.plot(np.log(ZZ), Intercepts)
plt.show()


M = sm.RLM.from_formula(formula='np.log(ADCResponse) ~ 1 + np.log(Mass) + np.log(Intensity) + np.log(Z)', data=he).fit()
M.params

plt.scatter(np.log(le.ADCResponse), 7.057521 - np.log(le.Mass)/2 + np.log(le.Intensity) + np.log(le.Z) - np.log(le.ADCResponse), s=.1)
plt.show()

np.mean(np.abs(np.exp(M.fittedvalues-np.log(he.ADCResponse))))

plt.scatter(np.log(he.ADCResponse), M.fittedvalues-np.log(he.ADCResponse), s=.1)
plt.show()




le['ADCResponse'] = 10000
P3D.LE = le


he['ADCResponse'] = 10000
P3D.HE = he

P3D.write(pep3d.parent/'test.xml')


