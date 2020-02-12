%load_ext autoreload
%autoreload 2
from pathlib import Path
from pprint import pprint
from collections import Counter
import pandas as pd
import csv
import json

from waters.parsers import XMLparser, iaDBsXMLparser, rows2csv
from waters.write import rows2csv


data_path = Path("~/Projects/waters/data/T181207_07/T181207_07_IA_workflow.xml").expanduser()
assert data_path.exists()
iaDBsXML = iaDBsXMLparser(data_path)


# iaDBsXML.json_tag_counts('/home/matteo/Projects/waters/data/T181207_07_stats.json')
# iaDBsXML.csv_tag_counts('/home/matteo/Projects/waters/data/T181207_07_stats.csv')
# del tag_counts['GeneratedBy']

prots = iaDBsXML.prot_ids()
len(prots)

tree = iaDBsXML.tree
root = tree.getroot()

iaDBsXML.get_tag_counts()
iaDBsXML.proteins()
iaDBsXML.products()
iaDBsXML.get_tag_counts()
iaDBsXML.parameters()
iaDBsXML.query_masses()
iaDBsXML.count_proteins_per_hit()



h = next(root.iter('HIT'))
Counter(len(h) for h in root.iter('HIT'))

prots.columns
tree = iaDBsXML.tree


data_path2 = Path("~/Projects/waters/data/T180222_10/T180222_10_IA_workflow.xml").expanduser()
iaDBsXML2 = iaDBsXMLparser(data_path2)
print(iaDBsXML.get_tag_counts())


