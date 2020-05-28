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

df2text(le[:4], {'Mass':'{:.4f}',
                 'MassSD':'{:.4f}',
                 'IntensitySD':'{:.2f}',
                 'AverageCharge':'{:.2f}',
                 'RT':'{:.4f}',
                 'RTSD':'{:.4e}',
                 'FWHM':'{:.4e}',
                 'LiftOffRT':'{:.4e}',
                 'InfUpRT':'{:.4e}',
                 'InfDownRT':'{:.4e}',
                 'TouchDownRT':'{:.4e}'})

le['ADCResponse'] = 10000
P3D.LE = le

he = P3D.HE
he['ADCResponse'] = 10000
P3D.HE = he

"{:.4f}".format(12121.20012)
"{:.4e}".format(12121.20012)
"%.4e" % 12121.20012


np.log10( le.loc[:,le.dtypes == np.float64] )


P3D.write(pep3d.parent/'test.xml')


df2text(le[:10])

