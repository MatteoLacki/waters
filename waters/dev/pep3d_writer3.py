%load_ext autoreload
%autoreload 2
from pathlib import Path
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 5)
import numpy as np
import numpy as np
from platform import system

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser, df2text, col2format

if system() == 'Linux':
    data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
    data_f = Path('/home/matteo/Projects/WatersData/O200114_03').expanduser()
else:
    data_f = Path(r"Y:\TESTRES2\5P\S170317_04__v1")

pep3d = next(data_f.glob('*_Pep3D_Spectrum.xml'))


P3D = Pep3Dparser(pep3d)
P3D.get_all_tag_counts()

del P3D

le = P3D.LE
he = P3D.HE

le['ADCResponse'] = 10000
P3D.LE = le
he['ADCResponse'] = 10000
P3D.HE = he

P3D.write(pep3d.parent/(pep3d.stem + "_ADCResponse10000.xml"))

# compare outputs: with check sums:
from syncFiles.syncFiles import check_sum
from waters.parsers import iaDBsXMLparser

ia_workflows = list(data_f.glob('*_IA_Workflow*.xml'))

for iw in  ia_workflows:
	print(check_sum(iw))
# check sums do differ: what about the data?
orig = ia_workflows[0]
mod = ia_workflows[1]

parsed = [iaDBsXMLparser(i) for i in ia_workflows]
prots  = [i.proteins() for i in parsed]
prods  = [i.products() for i in parsed]
