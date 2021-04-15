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
import matplotlib.pyplot as plt
#%%
# medium size
tdms_filename = 'data/2021-04-15_RF_Commissioning/TWA_2021-04-15_09-52-00_UTC_F55,500000M.tdms'
# # big size
# tdms_filename = 'data/test_files/TWA_2021-04-14_13-56-06_UTC_F55,000000M.tdms'

data = TWAdata(tdms_filename)

#%%
# plot something
fig, ax = plt.subplots(5,1, sharex=True)
data.df.plot(y='V1', ax=ax[0])
data.df.plot(y='V2', ax=ax[0])
data.df.plot(y='V3', ax=ax[0])
data.df.plot(y='V4', ax=ax[0])
data.df.plot(y='V5', ax=ax[0])
data.df.plot(y='V6', ax=ax[0])

data.df.plot(y='TOS', ax=ax[1])

data.df.plot(y='Pig', ax=ax[2])
data.df.plot(y='Prg', ax=ax[2])
data.df.plot(y='Piout', ax=ax[2])

data.df.plot(y='Vac1', ax=ax[3])
data.df.plot(y='Vac2', ax=ax[3])

data.df.plot(y='TC1', ax=ax[4])
data.df.plot(y='TC2', ax=ax[4])
data.df.plot(y='TC3', ax=ax[4])

ax[3].set_yscale('log')