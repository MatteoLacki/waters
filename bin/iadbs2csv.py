#! /usr/bin/python
import argparse
import json
from pprint import pprint
from pathlib import Path

from waters.parsers import iaDBsXMLparser


p = argparse.ArgumentParser(description="Get information on iaDBs.")
p.add_argument("iadbsxml",
               nargs="+",
               help="Paths to outputs of the iaDBs.")

args = p.parse_args()

print('Supplied xmls:')
pprint(args.iadbsxml)

for xml in args.iadbsxml:
    xml = Path(xml).expanduser()
    XML = iaDBsXMLparser(xml)
    info = XML.info()
    pprint(info)
    print('dumping to csv')
    XML.query_masses().to_csv(xml.parent/'query_masses.csv')
    XML.proteins().to_csv(xml.parent/'proteins.csv')
    XML.products().to_csv(xml.parent/'products.csv')

print()
print('Avoid trick of Loki.')
print('And have a nice day..')