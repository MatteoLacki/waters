%load_ext autoreload
%autoreload 2
from pathlib import Path
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 5)
import numpy as np
import numpy as np
from platform import system
from collections import Counter

import xml.etree.cElementTree as ET

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser, df2text, col2format, get_search_stats

if system() == 'Linux':
    data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
    data_f = Path('/home/matteo/Projects/WatersData/O200114_03').expanduser()
else:
    data_f = Path(r"Y:\TESTRES2\5P\S170317_04__v1")

# pep3d = next(data_f.glob('*_Pep3D_Spectrum.xml'))
# P3D = Pep3Dparser(pep3d)
iadb = next(data_f.glob('*_IA_workflow.xml'))

X = iaDBsXMLparser(iadb)
for elem in X:
    print(elem)

tag_counts = X.get_tag_counts()
tag_counts['QUERY_MASS']

{"raw_file": "", "acquired_name": "I200725_15", "sample_description": "2020-092-06 Imre"i, "queries_cnt": 317091, "hits_cnt": 2584, "peptides_cnt": 68382, "proteins_cnt": 2780}

# del X
# get_search_stats(iadb)

next(X.filter_iter('DATA'))

el = next(X.__iter__())
el.tag

Counter(el.attrib['ID'] for el in X if el.tag == 'PROTEIN')
# https://blog.etianen.com/blog/2013/04/14/python-xml/
X.attributesDF('PROTEIN')
X.attributesDF('PEPTIDE')

X.parameters()
next(X.iter_query_masses())

el = next(X.attributes_iter('PARAM'))
dict(el.values() for el in X.attributes_iter('PARAM'))

el = next(X.attributes_iter('PARAM'))
tuple(el.values())
A, B = el.values()

el = next((el for el in X if el.tag == "HIT"))
X.count_proteins_per_hit()
X.hits()


get_search_stats()
X.prot_ids()
X.proteins()
next(X.iter_peptides())
X.peptides()
X.query_masses()

get_search_stats(iadb)


def iter_elements(handle):
    events = ET.iterparse(handle, events=("start", "end",))
    _, root = next(events)  # Grab the root element.
    for event, elem in events:
        if event == "end":
            yield elem
            root.clear()

for a in iter_elements(iadb):
    print(a)
