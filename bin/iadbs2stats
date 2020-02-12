#! /usr/bin/python
import argparse
from pprint import pprint

from waters.parsers import paths2xmls, iaDBsXMLparser


p = argparse.ArgumentParser(description="Get information on iaDBs.")
p.add_argument("iadbsxml",
               nargs="+",
               help="Paths to outputs of the iaDBs. If ending with '.xml', will use directly. If supplied folders, these will be searched recursively for files ending with '_IA_workflow.xml'.")

args = p.parse_args()
xmls = list(paths2xmls(args.paths))

print('Supplied paths:')
pprint(xmls)

for xml in xmls:
    XML = iaDBsXMLparser(xml)
    info = XML.info()
    pprint(info)
    print('dumping to csv')
    rows2csv(xml.parent/'stats.csv', [list(info), list(info.values())])

print()
print('Let Thor enlight your path with lightnings!')
print('And have a nice day..')