%load_ext autoreload
%autoreload 2
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

I0.get_all_tag_counts()
I0.parameters()
I0.products()
I0.proteins()
I0.peptides()
I0.query_masses()

hit = I0.root.iter('HIT')
a = next(hit)
a.attrib
for b in a:
    print(b)
    print(b.attrib)
    print()

I0.count_proteins_per_hit()
I1.count_proteins_per_hit()


def iterrator(I0):
    for hit_id, hit in enumerate(I0.root.iter('HIT')):
        for prot in hit:
            prot_attrib = {f'PROT_{k}':v for k,v in prot.attrib.items()}
            seq_matches = []
            for node in prot:
                if node.tag == 'SEQUENCE_MATCH':
                    seq_match = node.attrib
                    seq_match['fragment_ion'] = ";".join(fii.attrib['IDS'] for fii in node.iter('FRAGMENT_ION')).replace(',','')
                    seq_matches.append(seq_match)
                else:
                    prot_attrib[f'PROT_{node.tag}'] = node.text
            prot_attrib['HIT'] = hit_id
            for seq_att in seq_matches:
                row = {f"SEQ_{k}":v for k,v in seq_att.items()}
                row.update(prot_attrib)
                yield row

D0 = pd.DataFrame(iterrator(I0)) 
D1 = pd.DataFrame(iterrator(I1))
# Need to compare those!
# pd.concat([D0,D1]).drop_duplicates(keep=False)
