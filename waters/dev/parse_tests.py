%load_ext autoreload
%autoreload 2
from waters.parsers import XMLparser, iaDBsXMLparser, Apex3Dparser, Pep3Dparser
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

data_f = Path('~/Projects/WatersData').expanduser()
apexPaths = list(data_f.glob('*/*_Apex3D.xml'))

apex3d = next(data_f.glob('*/*_Apex3D.xml'))
pep3d  = next(data_f.glob('*/*_Pep3D_Spectrum.xml'))
iaDBs  = next(data_f.glob('*/*_IA_workflow.xml'))

A = Apex3Dparser(apex3d)
A.LE
A.HE

P = Pep3Dparser(pep3d)
P.LE
P.HE

IA = iaDBsXMLparser(iaDBs)