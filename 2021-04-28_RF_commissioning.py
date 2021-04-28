# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:43:05 2021

@author: JH218595
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from TWAdata.TWAdata import TWAdata
#%%
filename='TWA_2021-04-28_07-46-35_UTC_F55,500000M'
tdms_filename = 'data/2021-04-28_RF_Commissioning/'+filename+'.tdms'

data = TWAdata(tdms_filename)

# title for graphs
title = np.datetime_as_string(data._raw_data['start_time'])+' - '+str(data.fMHz)+'MHz'

##%%

#full window
#mng = plt.get_current_fig_manager()
#mng.frame.Maximize(True)

# plot something
fig, ax = plt.subplots(7,1, sharex=True)
ax[0].set_title(title)

data.df.plot(y='V1', ax=ax[0])
data.df.plot(y='V2', ax=ax[0])
data.df.plot(y='V3', ax=ax[0])
data.df.plot(y='V4', ax=ax[0])
data.df.plot(y='V5', ax=ax[0])
data.df.plot(y='V6', ax=ax[0])

data.df.plot(y='RL', ax=ax[1], label='RL')
data.df.plot(y='RLG', ax=ax[1], label='RLGen')

data.df['Ptg'] = data.df['Pig']-data.df['Prg']
data.df.plot(y='Pig', ax=ax[2])
data.df.plot(y='Piout', ax=ax[2])
data.df.plot(y='Ptg', ax=ax[2])
data.df.plot(y='Piin', ax=ax[2])

data.df.plot(y='Prg', ax=ax[3])

data.df.plot(y='Vac1', ax=ax[4])
data.df.plot(y='Vac2', ax=ax[4])

data.df.plot(y='TC1', ax=ax[5])
data.df.plot(y='TC2', ax=ax[5])
data.df.plot(y='TC3', ax=ax[5])

data.df.plot(y='Pm1', ax=ax[6])
data.df.plot(y='Pm2', ax=ax[6])
data.df.plot(y='Pm3', ax=ax[6])
data.df.plot(y='Pm4', ax=ax[6])
data.df.plot(y='Pm5', ax=ax[6])
data.df.plot(y='Pm6', ax=ax[6])

ax[4].set_yscale('log')
