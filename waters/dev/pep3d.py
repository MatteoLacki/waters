%load_ext autoreload
%autoreload 2
from pathlib import Path
from pprint import pprint
from collections import Counter
import pandas as pd
import csv
import json
import numpy as np
import xml.etree.cElementTree as ET
from plotnine import *
import sklearn
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

from fs_ops.csv import rows2csv

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser

P3D = Pep3Dparser(r"/home/matteo/Projects/WatersData/O190303_78/O190303_78_Pep3D_Spectrum.xml")
P3D.get_tag_counts()
P3D.get_all_tag_counts()

P3D.root.iter('DATA')
P3D.root.iter("FORMAT[@FRAGMENTATION_LEVEL='1']")
for t in P3D.root.findall("FORMAT[@FRAGMENTATION_LEVEL='1']/*"):
    print(t.attrib['NAME'])
P3D.root.findall("FORMAT[@FRAGMENTATION_LEVEL='0']/*[@NAME]")
P3D.root.findall("FORMAT")
P3D.root.findall("*/DATA")


lo = P3D.LE()
hi = P3D.HE()
hi.columns

(ggplot(lo) + geom_line(aes(x='np.log(RT)', y='np.log(ADCResponse)')))
(ggplot(lo) + geom_line(aes(x='RT', y='np.log(ADCResponse)')))
(ggplot(lo) + geom_line(aes(x='np.log(Intensity)', y='np.log(ADCResponse)')))
(ggplot(lo) + geom_line(aes(x='Intensity', y='ADCResponse')))
(ggplot(lo) + geom_boxplot(aes(x='pd.Categorical(Z)', y='np.log(ADCResponse)')))

(ggplot(lo) + geom_line(aes(x='AverageCharge', y='np.log(ADCResponse)')))

y = lo.ADCResponse
lo.columns
(ggplot(lo) + geom_point(aes(x='np.log(Intensity)', y='np.log(ADCResponse)')))


plt.scatter(np.log(lo.ADCResponse), np.log(lo.IntensitySD) )
plt.show()


mod = smf.ols(formula='np.log(ADCResponse) ~ np.log(Intensity) + np.log(IntensitySD)*C(Z)', 
    data=lo)
res = mod.fit()
res.summary()

# 666 the number of the beast! Hell and fire were spawn to be released!

plt.scatter(np.log(y), res.fittedvalues - np.log(y))
plt.show()


plt.scatter(y[1:], y[:-1])
plt.show()

lm = OLS(y, X).fit()
lm.summary()
X.columns

X['logI'] = np.log(X.Intensity)
Counter(X.Z)

lm = OLS(np.log(y), X[['Mass','logI']]).fit()
lm.summary()

plt.scatter(np.log(y), lm.fittedvalues-np.log(y))
plt.show()


