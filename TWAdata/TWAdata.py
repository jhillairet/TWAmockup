import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from nptdms import TdmsFile

class TWAdata():
    def __init__(self, tdms_filename:str):
        '''
        TWA Mockup data 

        Parameters
        ----------
        tdms_filename : str
            path to a .tdms file

        Returns
        -------
        TWAdata : TWAdata object 

        '''
        # raw data are store in an internal dictionnary
        self._raw_data = {}
    
        try:
            print(f'Reading {tdms_filename} data... please wait...')
            # The TdmsFile.read method reads all data into memory immediately. 
            # For large TDMS files, TdmsFile.open is more memory efficient but slower
            # with TdmsFile.open(tdms_filename) as tdms_file:
            tdms_file = TdmsFile.read(tdms_filename)    
            for group in tdms_file.groups():
                #group_name = group.name    
                    
                for channel in tqdm(group.channels()):
                    channel_name = channel.name
                    # Access dictionary of properties:
                    properties = channel.properties
                    # Access numpy array of data for channel:
                    self.raw_data[channel_name + '_raw'] = channel[:]
                
            ## time properties
            self._raw_data['start_time'] = properties['wf_start_time']    
            self._raw_data['time_step'] = properties['wf_increment']  # time step
            
            # convert raw_data into a pandas DataFrame
            self._df = pd.DataFrame(self.raw_data)
            # time delta is assumed constant
            dt = pd.Timedelta(value=self._raw_data['time_step'], unit='seconds')
            
            # for absolute and relative time vectors
            time_absolute, time_relative = [], []
            for idx in range(len(self._df)):
                time_absolute.append(self.raw_data['start_time'] + idx*dt)
                time_relative.append(idx * dt)
            self._df['time_absolute'] = time_absolute
            self._df['time'] = time_relative
            self._df.set_index('time', inplace=True)

            # TODO post processing
            self.raw_TOS_to_TOS()

        except Exception as e: # hu ho...
            print(e)

    def __repr__(self) -> str:
        '''
        TWAdata description
        '''
        return 'TWA mockup data object. .df property contains: \n' + \
            str(self.df.columns.to_list())

    @property
    def df(self) -> pd.DataFrame:
        '''
        Return TDMS data as a pandas DataFrame object

        Returns
        -------
        df : pandas DataFrame
            TDMS data and relative and absolute time

        '''
        return self._df
    
    @property
    def raw_data(self) -> dict:
        '''
        Raw data as a dictionnary

        Returns
        -------
        raw_data : dict
            raw data

        '''
        return self._raw_data
        
    def cable_calib(self, cable, fMHz):
        '''
        Provides calibration coefficients for a cable.
        The coefficients are loss/gain and phase.
        The loss is retuned as positive, i.e. a gain.
        
        Parameters
        ----------
        cable : str
            cable name.
        fMHz : float
            frequency in [MHz].

        Returns
        -------
        tuple with loss and phase at the given fMHz.

        '''
        loss={'cable_1':{'a':-0.006880,'b':-0.2925},
              'cable_2':{'a':-0.006925,'b':-0.2946},
              'cable_3':{'a':-0.007031,'b':-0.3093},
              'cable_4':{'a':-0.008467,'b':-0.3984},
              'cable_5':{'a':-0.008295,'b':-0.3969},
              'cable_6':{'a':-0.009292,'b':-0.3934},}

        phase={'cable_1':{'a':-5.075995,'b':357.665306},
               'cable_2':{'a':-5.067552,'b':357.572827},
               'cable_3':{'a':-5.073765,'b':357.553137},
               'cable_4':{'a':-6.660815,'b':357.220690},
               'cable_5':{'a':-6.634197,'b':357.173558},
               'cable_6':{'a':-7.059244,'b':357.081008},}
        
        cable_loss = loss[cable]['a'] * fMHz + loss[cable]['b']
        cable_phase = phase[cable]['a'] * fMHz + phase[cable]['b']
        
        return (-cable_loss,cable_phase)
        
    def raw_TOS_to_TOS(self):
        '''
        calibration for TOS (AD8302)

        Returns
        -------
        None.

        '''
        self._def['TOS'] = 32.824 * self._def['TOS_raw'] - 29.717

        