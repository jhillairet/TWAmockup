# -*- coding: utf-8 -*-
"""
S11 vs frequency for the antenna at 50°C 

"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from TWAdata.TWAdata import TWAdata
from glob import glob

#%%
tdms_files = glob('data/2021-04-26_RF_Commissioning/*.tdms')

# keep only the files concerning the frequency scan, that is from 13-55-22 to 14-32-51
tdms_files = tdms_files[-46:-11]  # could be smarter, but eh...

df = pd.DataFrame()
#%%
for tdms_file in tqdm(tdms_files):
    _data = TWAdata(tdms_file)
    df = pd.concat([df, _data.df.query('Pig > 10e3')])


#%% TOS vs frequency
fig, ax = plt.subplots()
df.query('Pig > 10e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='RL', ax=ax, kind='scatter', label='RL - 50 degC')
ax.set_ylabel('S11 [dB]')
ax.set_title('S11 vs frequency - 200 kW shots - 50 degC')

fig.savefig('TWAmockup_s11_vs_f_50degC.png')

