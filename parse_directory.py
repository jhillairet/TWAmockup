# -*- coding: utf-8 -*-
"""
Parse all .tdms data in a directory and create a large dataframe containing
all the (meaningfull) results
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from TWAdata.TWAdata import TWAdata
from glob import glob

#%%
tdms_files = glob('data/2021-04-20_RF_Commissioning/*.tdms')

df = pd.DataFrame()
#%%
for tdms_file in tqdm(tdms_files):
    _data = TWAdata(tdms_file)
    df = pd.concat([df, _data.df.query('Pig > 10e3')])


#%% TOS vs frequency
fig, ax = plt.subplots()
df.query('Pig>30e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='RL', ax=ax, kind='scatter', label='RL')
ax.set_ylabel('S11 [dB]')
ax.set_title('S11 vs frequency - 50 kW shots')

#%% ILG vs frequency
fig, ax = plt.subplots()
df.query('Pig>30e3 and Pig<60e3 and fMHz != 58.5').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='RLG', ax=ax, label='Generator', kind='scatter', color='C0')
df.query('Pig>30e3 and Pig<60e3 and fMHz != 58.5').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='RL', ax=ax, label='Load', kind='scatter', color='C1')

ax.set_ylabel('S11 [dB]')
ax.set_title('S11 vs frequency - 50 kW shots')

#%% voltage vs frequency
fig, ax = plt.subplots()
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V1', ax=ax, kind='scatter', color='C0')
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V2', ax=ax, kind='scatter', color='C1')
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V3', ax=ax, kind='scatter', color='C2')
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V4', ax=ax, kind='scatter', color='C3')
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V5', ax=ax, kind='scatter', color='C4')
df.query('Pig>40e3 and Pig<60e3').groupby('fMHz').mean().reset_index().plot(x='fMHz', y='V6', ax=ax, kind='scatter', color='C5')


#%% Tc temperature vs time
fig, ax = plt.subplots()
df.plot(x='time_absolute', y='TC1', ax=ax)
df.plot(x='time_absolute', y='TC2', color='C1', ax=ax )
df.plot(x='time_absolute', y='TC3', color='C2', ax=ax)

#%%
fig, ax = plt.subplots()
df.groupby('fMHz').mean().reset_index().plot(x='fMHz', y='Pig', kind='scatter')

#%% Voltage vs forward power in the antenna
with plt.style.context('seaborn'):
    fig, ax = plt.subplots()
    df['Pig_kW'] = df['Pig']/1e3
    df.plot(x='Pig_kW', y='V1', kind='scatter', ax=ax, color='C0', alpha=0.5)
    df.plot(x='Pig_kW', y='V2', kind='scatter', ax=ax, color='C1', alpha=0.5)
    df.plot(x='Pig_kW', y='V3', kind='scatter', ax=ax, color='C2', alpha=0.5)
    df.plot(x='Pig_kW', y='V4', kind='scatter', ax=ax, color='C3', alpha=0.5)
    df.plot(x='Pig_kW', y='V5', kind='scatter', ax=ax, color='C4', alpha=0.5)
    df.plot(x='Pig_kW', y='V6', kind='scatter', ax=ax, color='C5', alpha=0.5)
    ax.set_xlabel('Forward Power [kW]')
    ax.set_ylabel('Strap Voltage [kV]')
    ax.legend([f'V{idx}' for idx in range(1,7)])
