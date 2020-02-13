%load_ext autoreload
%autoreload 2
from pathlib import Path
from pprint import pprint
from collections import Counter
import pandas as pd
import csv
import json

from fs_ops.csv import rows2csv

from waters.parsers import XMLparser, iaDBsXMLparser

data_path = Path("~/Projects/waters/data/T181207_07/T181207_07_IA_workflow.xml").expanduser()
assert data_path.exists()
iaDBsXML = iaDBsXMLparser(data_path)

prots = iaDBsXML.prot_ids()
iaDBsXML.get_tag_counts()
iaDBsXML.proteins()
iaDBsXML.products()
iaDBsXML.get_tag_counts()
iaDBsXML.parameters()
iaDBsXML.query_masses()
iaDBsXML.count_proteins_per_hit()
info = iaDBsXML.info()


rows2csv(Path("~/Projects/waters/data/info.csv").expanduser(),
         [list(info), list(info.values())])


scripts_loc = Path(r"C:\Users\stefan\AppData\Local\Programs\Python\Python38\Scripts")
sendto_loc = Path(r"C:\Users\stefan\AppData\Roaming\Microsoft\Windows\SendTo")
os.link(scripts_loc/"iadbs2csv.py", sendto_loc/"_iadbs2csv.py")
os.link(scripts_loc/"iadbs2stats.py", sendto_loc/"_iadbs2stats.py")

prots.columns
tree = iaDBsXML.tree
tree.

data_path2 = Path("~/Projects/waters/data/T180222_10/T180222_10_IA_workflow.xml").expanduser()
iaDBsXML2 = iaDBsXMLparser(data_path2)
print(iaDBsXML.get_tag_counts())


def find_iaDBs_outputs(root):
	return list(root.glob("**/*_IA_workflow.xml"))

find_iaDBs_outputs(Path(r"Y:\RES\2018-071"))

def xmls(paths):
    for p in paths:
        p = Path(p)
        if p.is_file() and p.suffix == '.xml':
            yield p
        if p.is_dir():
            yield from p.glob("**/*_IA_workflow.xml")

list(xmls([r"Y:\RES\2018-071",]));suffix