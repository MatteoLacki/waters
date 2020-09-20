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
apex = next(data_f.glob('*_Apex3D.xml'))
pep3d = next(data_f.glob('*_Pep3D_Spectrum.xml'))

P = Pep3Dparser(pep3d)

pep3dPath = pep3d.parent/f"{pep3d.stem}.hdf5"
P.to_hdf(pep3dPath)
Pep3Dparser.hdf2pd(pep3dPath, 1)
Pep3Dparser.hdf2pd(pep3dPath, 2)