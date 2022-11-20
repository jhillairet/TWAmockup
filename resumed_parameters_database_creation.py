# -*- coding: utf-8 -*-
"""
Creates a database of resumed parameters (mean, std, min, max) of the different
quantities measured during the test of the TWA mockup on TITAN.

"""
#%%
import numpy as np
import pandas as pd
from tqdm import tqdm
from glob import glob
from os.path import join
from nptdms import TdmsFile

from TWAdata.TWAdata import TWAdata, create_resumed_parameters

#%%
def tdms_files(directories):
    """
    List all .tdms files found in a list of directories.

    Parameters
    ----------
    directories : list
        List of directories.

    Returns
    -------
    tdms_files : list
        List of .tdms relative paths.

    """
    # keep only .hdf files
    tdms_files = []
    for directory in directories:
        name_filter = join(directory, '*.tdms')
        tdms_files.extend(glob(name_filter))
    return tdms_files

#%% list of data files found in the following subdirectories
directories = [
"data/2021-04-15_RF_Commissioning",
"data/2021-04-16_RF_Commissioning",
"data/2021-04-19_RF_Commissioning",
"data/2021-04-20_RF_Commissioning",
"data/2021-04-21_RF_Commissioning",
"data/2021-04-26_RF_Commissioning",
"data/2021-04-27_RF_Commissioning",
"data/2021-04-28_RF_Commissioning"
]

files = tdms_files(directories)

files = [files[i] for i in (1, -2, -1)]

#%% Create a database of resumed parameters
df = create_resumed_parameters(files)  # long runtime

#%% Saving file into a .hdf file for faster reopening
df.to_hdf('resumed_parameters_TWA_mockup.hdf', key='TWAmockup') 

# to be read with:
# df = pd.read_hdf('resumed_parameters_TWA_mockup.hdf').reset_index()
