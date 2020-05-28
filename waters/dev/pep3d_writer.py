%load_ext autoreload
%autoreload 2
from pathlib import Path
from collections import Counter
import pandas as pd
pd.set_option('display.max_columns', 100)
import numpy as np

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser, df2text

data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
pep3d  = next(data_f.glob('*_Pep3D_Spectrum.xml'))

P3D = Pep3Dparser(pep3d)
P3D.get_all_tag_counts()

le = P3D.LE
le['ADCResponse'] = 10000
P3D.LE = le

he = P3D.HE
he['ADCResponse'] = 10000
P3D.HE = he

P3D.write(pep3d.parent/'test.xml')


