%load_ext autoreload
%autoreload 2
from pathlib import Path
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 5)
import numpy as np
import numpy as np
from platform import system

import xml.etree.cElementTree as ET

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser, df2text, col2format

if system() == 'Linux':
    data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
    data_f = Path('/home/matteo/Projects/WatersData/O200114_03').expanduser()
else:
    data_f = Path(r"Y:\TESTRES2\5P\S170317_04__v1")

pep3d = next(data_f.glob('*_Pep3D_Spectrum.xml'))
P3D = Pep3Dparser(pep3d)

# https://blog.etianen.com/blog/2013/04/14/python-xml/


events = ET.iterparse

