# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:43:05 2021

@author: JH218595
"""
#%%
import numpy as np
from nptdms import TdmsFile
import pandas as pd
from tqdm import tqdm

from TWAdata.TWAdata import TWAdata

#%%
# medium size
tdms_filename = 'data/test_files/TWA_2021-04-14_13-26-42_UTC_F55,000000M.tdms'
# # big size
# tdms_filename = 'data/test_files/TWA_2021-04-14_13-56-06_UTC_F55,000000M.tdms'

data = TWAdata(tdms_filename)

# plot something
data.df.plot(y='TC1_raw')