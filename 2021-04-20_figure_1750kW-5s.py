# -*- coding: utf-8 -*-
"""
TWA mockup 600 kW/ 5s
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from TWAdata.TWAdata import TWAdata
#%%
filename='TWA_2021-04-20_14-37-15_UTC_F55,500000M'
tdms_filename = 'data/2021-04-20_RF_Commissioning/'+filename+'.tdms'

data = TWAdata(tdms_filename)

# title for graphs
title = np.datetime_as_string(data._raw_data['start_time'])+' - '+str(data.fMHz)+'MHz'


#%%
# plot something
with plt.style.context('seaborn'):
    
    fig, ax = plt.subplots(4,1, sharex=True)
    ax[0].set_title(title)
    data.df['Pig_kW'] = data.df['Pig']/1e3
    data.df.plot(y='Pig_kW', ax=ax[0])
    ax[0].set_ylabel('[kW]')
    ax[0].legend(('RF Power',))
    
    data.df.plot(y='V1', ax=ax[1])
    data.df.plot(y='V2', ax=ax[1])
    data.df.plot(y='V3', ax=ax[1])
    data.df.plot(y='V4', ax=ax[1])
    data.df.plot(y='V5', ax=ax[1])
    data.df.plot(y='V6', ax=ax[1])
    ax[1].set_ylabel('[kV]')
    ax[1].legend(ncol=3)
    
    data.df.plot(y='RL', ax=ax[2])
    ax[2].set_ylabel('[dB]')
    ax[2].legend(('Return Loss',))
    
    data.df.plot(y='Vac1', ax=ax[3])
    data.df.plot(y='Vac2', ax=ax[3])
    ax[3].set_ylabel('Pressure \n [Pa]')
    ax[3].set_yscale('log')
    ax[3].set_ylim(1e-5, 1e-2)
    
    ax[0].set_title('TWA mockup - '+title)
    
    [a.grid(True) for a in ax]
    ax[3].grid(True, which='minor')
    ax[-1].set_xlabel('Time [s]')
    ax[-1].set_xticklabels(['0','1','2','3','4','5','6','7'])
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.05)
    fig.savefig('TWAmockup_1750kW-5s.png', dpi=150)