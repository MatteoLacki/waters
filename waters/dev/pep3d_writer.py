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
from io import StringIO
from decimal import Decimal

pd.set_option('display.max_columns', 100)
# pd.set_option('display.max_rows', None)

from fs_ops.csv import rows2csv

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser

data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
apex3d = next(data_f.glob('*_Apex3D.xml'))
pep3d  = next(data_f.glob('*_Pep3D_Spectrum.xml'))
iadbs  = next(data_f.glob('*_IA_workflow.xml'))

P3D = Pep3Dparser(pep3d)
P3D.get_all_tag_counts()

le = P3D.LE()
le.dtypes

%%time
x = df2text3(le, {'RTSD':'%.4e'})
x[:1000]

# he = P3D.HE()0

le['ADCResponse'] = 10000
le_s = le[:10]
le_s.dtypes


df = le_s.copy()
cols = df.columns
col2format = {'RTSD':'%.4e'}
col2format = {'RTSD':'%.4e', 'IntensitySD':'%.2e'}



for col, formatter in col2format.items():
    df.loc[:,col] = df.loc[:,col].apply(lambda x: formatter % x)
cols_simple2str = [c for c in cols if c not in col2format]
df.loc[:,cols_simple2str] = df[cols_simple2str].astype(np.str)




le_s.drop(col2format, axis=1)


le_s.Mass.astype(str).str.cat([le_s.Mass.astype(str),
                               le_s.Mass.astype(str)], sep=' ')

    

%%time
x = df2text2(le)

%%time
x = df2text(le)

x[:1000]

'%.4e' % Decimal(le_s.RTSD[0])



# should we do this every time as a post-processing? Why not! Let's add it.
data = next(P3D.root.iter('HE_DATA'))
data.text[:1000]
le_s.to_string(header=False, index=False, na_rep=-3, sep='..')

x = df2text(le)
x[:1000]
# infer the number of digits?
str(10.2)

le_s.to_string(header=False, index=False, index_names=False)


data.text = "\n      "+"\n      ".join(" ".join(row.astype(str)) for row in le_s.values)




data = next(P3D.root.iter('HE_DATA'))
data.text = 'test'

P3D.tree.write(pep3d.parent/'test.xml')

next(P3D.root.iter('PRECURSOR_BIN')).attrib
next(P3D.root.iter('PRECURSOR_BIN')).text
# P3D.root.findall('.//DATA..')
# P3D.root.remove(data)