%load_ext autoreload
%autoreload 2
from pathlib import Path
from pprint import pprint
from collections import Counter
import pandas as pd
import csv
import json
import numpy as np
import xml.etree.cElementTree as ET
from plotnine import *
import sklearn
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

from fs_ops.csv import rows2csv

from waters.parsers import XMLparser, iaDBsXMLparser, Pep3Dparser, Apex3Dparser

data_f = Path('~/Projects/WatersData/O190303_78').expanduser()
apex3d = next(data_f.glob('*_Apex3D.xml'))
pep3d = next(data_f.glob('*_Pep3D_Spectrum.xml'))
iadbs = next(data_f.glob('*_IA_workflow.xml'))
I = iaDBsXMLparser(iadbs)
A = Apex3Dparser(apex3d)
A.LE()
A.HE()
