#! /usr/bin/python
import argparse
import json
from pprint import pprint
from pathlib import Path

from waters.parsers import iaDBsXMLparser
from waters.write import rows2csv


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
    rows2csv(xml.parent/'stats.csv', [list(info), list(info.values())])

print()
print('Let Thor enlight your path with lightnings!')
print('And have a nice day..')