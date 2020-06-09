%load_ext autoreload
%autoreload 2
from collections import Counter
from pathlib import Path
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 5)
import numpy as np
from pprint import pprint

from waters.parsers import iaDBsXMLparser

data_f = Path(r"/home/matteo/Projects/WatersData/ADCResppnse")
files = list(data_f.glob('*IA*.xml'))

I0 = iaDBsXMLparser(files[0])
I1 = iaDBsXMLparser(files[1])
I2 = iaDBsXMLparser(files[2])

diff = lambda d0, d1: (d1 != d0).any(1)

I0.get_all_tag_counts()
I0.parameters()
PR0 = I0.products()
PR1 = I1.products()
sum(diff(PR0, PR1))
PR0[diff(PR0, PR1)]
sum(diff(PR0.iloc[:,:14], PR1.iloc[:,:14]))
Counter(PR0.LOSS_TYPE)
Counter(PR1.LOSS_TYPE) # dass siehst gut aus.

prots = I0.proteins()
peps  = I0.peptides()
prods = I0.products()

I0.query_masses()
pd.DataFrame(I0.iter_query_masses())

Counter(len(qm) for qm in I0.root.iter('QUERY_MASS'))
Counter(len(qm) for qm in I0.root.iter('PEPTIDE'))
QM0 = I0.query_masses()
QM1 = I1.query_masses()
sum(diff(QM0, QM1))

I0.count_proteins_per_hit()
I1.count_proteins_per_hit()

h0 = I0.hits()
h1 = I1.hits()
h2 = I2.hits()

def diff_iter(h0, h1):
    for c in h0.columns:
        h0c = h0[c]
        h1c = h1[c]
        h0c.fillna('', inplace=True)
        h1c.fillna('', inplace=True)
        diff = h0c != h1c
        if any(diff):
            yield c, pd.concat([h0c[diff], h1c[diff]], axis=1)


dict(diff_iter(h0,h1))
H0 = h0.sort_values(by=['SEQ_START', 'SEQ_END', 'SEQ_COVERAGE']).reset_index()
H0 = h0.sort_values(by=list(h0.columns)).reset_index()
H1 = h1.sort_values(by=['SEQ_START', 'SEQ_END', 'SEQ_COVERAGE']).reset_index()
H1 = h1.sort_values(by=list(h1.columns)).reset_index()
H2 = h2.sort_values(by=['SEQ_START', 'SEQ_END', 'SEQ_COVERAGE']).reset_index()
H2 = h2.sort_values(by=list(h2.columns)).reset_index()

files
diff = dict(diff_iter(H0, H2))
diff = dict(diff_iter(H0, H1))
diff = dict(diff_iter(H1, H2))
IDX = diff['index']
IDX.columns = 'A','B'
IDX = IDX.sort_values(['A','B'])
list(IDX.iterrows())

diff['SEQ_fragment_ion']


prod0 = I0.products()
prod1 = I1.products()
prod2 = I2.products()
dict(diff_iter(prod0, prod1))

prod0 = I0.products()
prod1 = I1.products()
prod2 = I2.products()

def no_id(prod):
    P = prod.copy()
    # iloc[:,1:]
    return P.sort_values(by=list(P.columns[1:])).reset_index()

P0, P1, P2 = [no_id(x) for x in (prod0, prod1, prod2)]
diffIdx = dict(diff_iter(P0,P1))['index']

def show_cyles(df):
    df.columns = 'A','B'
    df = df.sort_values(['A','B'])
    return list(df.iterrows())

x = show_cyles(diffIdx)
for p in x:
    if x[0][1].B == '324':
        print(x[0][1])