import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from nptdms import TdmsFile

# Allows copy/paste to clipboard using crtl+c command
plt.rcParams['toolbar'] = 'toolmanager'

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
        
        self.fMHz = float(tdms_filename.split('_')[-1].split('.')[0].replace(',', '.').strip('M').strip('F'))
    
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
            
            ## load calibration for filters
            self._filter_calib=pd.read_csv('calibration_filtres_TWA.csv',sep=';',decimal=',')
            print('Calibration for filters loaded')
            
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
            self._df['fMHz'] = self.fMHz
            self._df.set_index('time', inplace=True)
            self._df['time_seconds'] = self._df.index.total_seconds() # time in seconds (for plots)
            
            # Post processing
            self.raw_TOS_to_RL()
            self.raw_V_to_V()
            self.raw_vac_to_vac()
            self.raw_Piout_to_Piout()
            self.raw_Piin_to_Piin()
            self.raw_Pgen_to_Pgen()
            self.raw_Tc_to_Tc()
            self.raw_Vm_to_Pm()

        except Exception as e: # hu ho...
            print(e)

    def __repr__(self) -> str:
        '''
        TWAdata description
        '''
        return f'TWA mockup data object ({self.fMHz} MHz). .df property contains: \n' + \
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
        
    def cable_calib(self, cable: str, fMHz: float):
        '''
        Provides calibration coefficients for a cable.
        The coefficients are loss/gain and phase.
        The loss is retuned as positive, i.e. a gain.
        Cables:
            cable_1 -> _6 cables in vacuum
            cable_ext -> external cables
        
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
        
        loss={'cable_1':{'a':-0.00688043,'b':-0.292487},
              'cable_2':{'a':-0.00692513,'b':-0.294647},
              'cable_3':{'a':-0.00703144,'b':-0.309332},
              'cable_4':{'a':-0.00846781,'b':-0.398441},
              'cable_5':{'a':-0.00829548,'b':-0.396912},
              'cable_6':{'a':-0.00929207,'b':-0.393463},
              'cable_ext_V1':{'a':-0.00390899,'b':-0.184557},
              'cable_ext_V2':{'a':-0.00392781,'b':-0.181615},
              'cable_ext_V3':{'a':-0.00395946,'b':-0.180526},
              'cable_ext-V4':{'a':-0.00388784,'b':-0.181224},
              'cable_ext_V5':{'a':-0.00393421,'b':-0.183850},
              'cable_ext_V6':{'a':-0.00387728,'b':-0.183060},
              'cable_ext_I1':{'a':-0.00394063,'b':-0.182488},
              'cable_ext_I2':{'a':-0.00389165,'b':-0.181592},
              'cable_ext_I3':{'a':-0.00389101,'b':-0.181285},
              'cable_ext_I4':{'a':-0.00391256,'b':-0.182377},
              'cable_ext_I5':{'a':-0.00391093,'b':-0.184288},
              'cable_ext_I6':{'a':-0.00392298,'b':-0.180535},
              'cable_Pin_FWD':{'a':-0.00551798,'b':-0.284362},
              'cable_Pin_REV':{'a':-0.00391024,'b':-0.188052},
              'cable_Pout_FWD':{'a':-0.00563724,'b':-0.274108},
              }

        
        phase = {'cable_1':{'a':-5.07599542,'b':357.665306},
                'cable_2':{'a':-5.06755164,'b':357.572827},
                'cable_3':{'a':-5.07376499,'b':357.553137},
                'cable_4':{'a':-6.66081523,'b':357.220690},
                'cable_5':{'a':-6.63419692,'b':357.173558},
                'cable_6':{'a':-7.05924373,'b':357.081008},
                'cable_ext_V1':{'a':17.43764638,'b':-896.843234},
                'cable_ext_V2':{'a':17.44427920,'b':-896.848321},
                'cable_ext_V3':{'a':17.44358479,'b':-896.860553},
                'cable_ext_V4':{'a':17.43886993,'b':-896.831885},
                'cable_ext_V5':{'a':17.43986903,'b':-896.843898},
                'cable_ext_V6':{'a':17.43651233,'b':-896.823611},
                'cable_ext_I1':{'a':17.44437836,'b':-896.849706},
                'cable_ext_I2':{'a':17.56778993,'b':-906.284931},
                'cable_ext_I3':{'a':17.44274311,'b':-896.839019},
                'cable_ext_I4':{'a':17.56441039,'b':-906.279570},
                'cable_ext_I5':{'a':17.44432332,'b':-896.834457},
                'cable_ext_I6':{'a':17.44150241,'b':-896.831472},
                'cable_Pin_FWD':{'a':-5.28892990,'b':358.127319},
                'cable_Pin_REV':{'a':17.44959362,'b':-896.812723},
                'cable_Pout_FWD':{'a':-5.27727579,'b':358.145731},
                }
        
        cable_loss = loss[cable]['a'] * fMHz + loss[cable]['b']
        cable_phase = phase[cable]['a'] * fMHz + phase[cable]['b']
        
        return (-cable_loss,cable_phase)
        
    def raw_TOS_to_RL(self):
        '''
        calibration for Return Loss (RL) at the antenna (AD8302)


        Returns
        -------
        None.

        '''
        self._df['RL'] = 32.824 * self._df['TOS_raw'] - 29.717

    def AD8310_calib(self, card: str, Vdc: float):
        '''
        provides the transformation Vdc => dBm for the AD8310 cards

        Parameters
        ----------
        card : str
            one of the calibrated cards ('V1' to 'V7')
        Vdc : float
            measured voltage.

        Returns
        -------
        dBm : float
            the Vdc value in dBm

        '''
        cards={'V1':{'a':41.127, 'b':-95.067},
               'V2':{'a':40.667, 'b':-95.274},
               'V3':{'a':40.780, 'b':-93.895},
               'V4':{'a':41.578, 'b':-97.553},
               'V5':{'a':40.933, 'b':-96.822},
               'V6':{'a':41.155, 'b':-96.649},
               'V7':{'a':40.851, 'b':-96.176},
               'V8':{'a':41.389, 'b':-98.451},}
        
        return cards[card]['a'] * Vdc + cards[card]['b']
    
    def V_probe_calib(self, probe: str, fMHz: float):
        '''
        Provides the calibrated coefficient of the voltage probe
        expressed in kV/V.

        Parameters
        ----------
        probe : str
            one of the calibrated probes ('V1' to 'V6')
        fMHz : float
            the frequency in [MHz].

        Returns
        -------
        kV_V : float
            the voltage probe coefficient in kV/V.

        '''
        probes = {'V1':297.662,
                  'V2':293.318,
                  'V3':245.413,
                  'V4':325.128,
                  'V5':320.402,
                  'V6':283.714,}
        
        return probes[probe]/fMHz
    
    def dBm_to_Vrf(self, dBm: float) -> float:
        '''
        Transform dBm in Vrf

        Parameters
        ----------
        dBm : float
            value in [dBm].

        Returns
        -------
        Vrf : float
            value in [V]

        '''
        return 10**((dBm-13)/20)*np.sqrt(2)
    
    def raw_V_to_V(self):
        '''
        Process the raw voltage signals
        
        The result is a voltage in Volt
        '''
        card_stage = self.AD8310_calib('V1', self._df['V1_raw'])
        cable_stage = self.cable_calib('cable_1', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V1', self.fMHz)
        self._df['V1'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V2', self._df['V2_raw'])
        cable_stage = self.cable_calib('cable_2', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V2', self.fMHz)
        self._df['V2'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V3', self._df['V3_raw'])
        cable_stage = self.cable_calib('cable_3', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V3', self.fMHz)
        self._df['V3'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V3', self._df['V3_raw'])
        cable_stage = self.cable_calib('cable_3', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V3', self.fMHz)
        self._df['V3'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V4', self._df['V4_raw'])
        cable_stage = self.cable_calib('cable_4', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V4', self.fMHz)
        self._df['V4'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V5', self._df['V5_raw'])
        cable_stage = self.cable_calib('cable_5', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V5', self.fMHz)
        self._df['V5'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
        
        card_stage = self.AD8310_calib('V6', self._df['V6_raw'])
        cable_stage = self.cable_calib('cable_6', self.fMHz)[0]
        probe_coeff = self.V_probe_calib('V6', self.fMHz)
        self._df['V6'] = self.dBm_to_Vrf(card_stage + cable_stage + 20) * probe_coeff
    
    def raw_vac_to_vac(self):
        '''
        Process the raw vacuum signals
        
        The result is a pressure in Pascal
        '''
        self._df['Vac1'] = 10**(1.667*self._df['Vac1_raw']-9.333)
        self._df['Vac2'] = 10**(1.667*self._df['Vac2_raw']-9.333)
        
    def raw_Piout_to_Piout(self):
        '''
        Process the raw input power into the water load.
        
        40.737*Vraw - 92.731: calibration AD8310
        42 dBm: attenuator (-19.645dB -20dB -3dB )
        61 dB: Spinner coupler attenuation
        0.5 dB: cable loss
        
        added filters on 2021-0-20
        
        The result is in dBm --> Power in Watts
        '''
        cable_att_dB = self.cable_calib('cable_Pout_FWD', self.fMHz)[0]
        Piout_dBm = self.AD8310_calib('V7', self._df['Piout_raw'])
        
        if self.df['start_time'][0] > np.datetime64('2021-04-20 11:55:00'):
            # 2021/04/20: filters have been added to the forward and reflected 
            # power at the antenna input
            print('Adding filter to the loss chain')
            att_filter = self._filter_calib.query('Freq_MHz == {}'.format(self.fMHz))['OUT_FWD'].values[0]
            print('Filter value @ {} : {}'.format(self.fMHz,att_filter))
            self._df['Piout'] = 10**((Piout_dBm + 42.645 + 61 + att_filter + cable_att_dB) / 10)/1e3
        else:
            self._df['Piout'] = 10**((Piout_dBm + 42.645 + 61 + cable_att_dB) / 10)/1e3
        
    def raw_Piin_to_Piin(self):
        '''
        Process the raw input power into the antenna.
        
        41.389*Vraw - 98.451: calibration AD8310
        42 dBm: attenuator (-18.957dB att, -13dB att, -10dB splitter )
        61 dB: Spinner coupler attenuation
        0.5 dB: cable loss
        0.55 dB: filter on 
        
        The result is in dBm --> Power in Watts
        '''
        cable_att_dB = self.cable_calib('cable_Pin_FWD', self.fMHz)[0]
        Piin_dBm = self.AD8310_calib('V8', self._df['Piin_raw'])
        
        if self.df['start_time'][0] > np.datetime64('2021-04-21 07:00:00'):
            # 2021/04/20: filters have been added to the forward and reflected 
            # power at the antenna input
            print('Adding Pin antenna')
            self._df['Piin'] = 10**((Piin_dBm + 41.451 + 61 + 0.55 + cable_att_dB) / 10)/1e3
        else:
            self._df['Piin'] = 0 * self._df['Piin_raw']
       
        
    def raw_Pgen_to_Pgen(self):
        '''
        Process the generator input/reflected power raw data
        
        Electronic Cards:
         * Vi -> dBm : A * Vi + B
         * Vr -> dBm : A * Vr + B
        coupler attenutation:
         * Pi:  XX dB
         * Pr:  YY dB
        
        The result is in dBm --> Power in Watts
        
        '''      
        # Electronic card aquisition data from G.Lombard prev acquisition program
        # Pi
        #{2.1477,	1.0735, 	61.05}, # @ 48 MHz	
		#{2.1494, 	1.6246, 	61.04}, # @ 53 MHz	
		#{2.1513, 	2.0106, 	61.03},	# @ 55.5 MHz
        #{2.1540, 	2.5968, 	61.00}, # @ 57 MHz	
        #{2.1608, 	3.0142, 	60.97}, # @ 63 MHz	
        # Pr
        #{2.1802, 	1.2402, 	61.19},	# @ 48 MHz	  	
        #{2.1838, 	1.6224, 	61.16}, # @ 53 MHz	  	
        #{2.1853, 	1.7151, 	61.14}, # @ 55.5 MHz
        #{2.1841, 	2.1701, 	61.12}, # @ 57 MHz	  	
        #{2.1910, 	2.2478, 	61.09}, # @ 63 MHz	 
        
        # An additional 10 dB attenuator has been added the 19/04/2021
        # to correct the saturation seen in generator power measurement before
        if self.df['start_time'][0].date() >= np.datetime64('2021-04-19'):
            # 2021-04-20 12-13-29: -0.66 dB has been added to match the power request value
            # add_att_Pi_dB = 9.85 - 0.66
            # add_att_Pr_dB = 9.87
            #print('Adding additional 10dB attenuator')
            
            # 2021-04-21 new calibration of the full chain
            if self.df['start_time'][0] >= np.datetime64('2021-04-21 11:00:00'):
                add_att_Pi_dB = 0 + 0.2
                add_att_Pr_dB = 0 + 0.2
            else:
                add_att_Pi_dB = 0
                add_att_Pr_dB = 0
            print('New calibration Gen')
        else:
            # before 2021-04-21
            # add_att_Pi_dB = 0
            # add_att_Pr_dB = 0
            # 2021-04-21 new calibration of the full chain
            add_att_Pi_dB = -(9.85 - 0.66)
            add_att_Pr_dB = -9.87

        # self._df['Pig'] = 10**(((2.1513*self._df['Pig_raw'] + 2.0106) + 61.03 + add_att_Pi_dB)/10)/1e3
        # self._df['Prg'] = 10**(((2.1853*self._df['Prg_raw'] + 1.7151) + 61.14 + add_att_Pr_dB)/10)/1e3
        self._df['Pig'] = 10**(((2.1412*self._df['Pig_raw'] + 72.836) + add_att_Pi_dB)/10)/1e3
        self._df['Prg'] = 10**(((2.1819*self._df['Prg_raw'] + 73.239) + add_att_Pr_dB)/10)/1e3
        # Return Loss at generator
        self._df['RLG'] = 10*np.log10(self._df['Prg']/self._df['Pig'])
        
    def raw_Tc_to_Tc(self):
        '''
        Process thermocouple raw data
        
        The result is in degree C
        '''
        self._df['TC1'] = 21.665 * self._df['TC1_raw'] -23.048
        self._df['TC2'] = 21.665 * self._df['TC2_raw'] -23.048 
        self._df['TC3'] = 21.665 * self._df['TC3_raw'] -23.048 
        
    def raw_Vm_to_Pm(self):
        '''
        Vm1*32.113 - 30.531 : -> (A/B) in dB
        33 dB: attenuator
        
        The result is a power Pm in Watts
        '''
        if self.df['start_time'][0] < np.datetime64('2021-04-19 13:30:00'):
            print('Current probe configuration with reference on channel 1 only (3dB splitter)')
            self._df['Pm1'] = 10**(((-10 -(self._df['Vm1_raw']*32.113 - 30.531)) + 33)/10)/1e3
        else:
            print('Current probe configuration with common reference (no 3dB splitter)')
            self._df['Pm1'] = 10**(((-10 -(self._df['Vm1_raw']*32.113 - 30.531)) + 30)/10)/1e3
            self._df['Pm2'] = 10**(((-10 -(self._df['Vm2_raw']*32.113 - 30.531)) + 30)/10)/1e3
            self._df['Pm3'] = 10**(((-10 -(self._df['Vm3_raw']*32.113 - 30.531)) + 30)/10)/1e3
            self._df['Pm4'] = 10**(((-10 -(self._df['Vm4_raw']*32.113 - 30.531)) + 30)/10)/1e3
            self._df['Pm5'] = 10**(((-10 -(self._df['Vm5_raw']*32.113 - 30.531)) + 30)/10)/1e3
            self._df['Pm6'] = 10**(((-10 -(self._df['Vm6_raw']*32.113 - 30.531)) + 30)/10)/1e3


def find_shots_indices(array, threshold):
    """
    Returns the start and stop arrays indices corresponding to RF shot.

    Parameters
    ----------
    array : numpy array
        Array to threshold on
    threshold : float
        threshold to appy

    Returns
    -------
    idx_starts : list of int
    idx_stops : list of int
    """
    # indices of values above threshold
    idx_thres = np.nonzero(array > threshold)[0]
    if idx_thres.size > 0:  # not empty
        # find indices where we change the RF shot   
        idx_starts = np.append(idx_thres[0], idx_thres[1:][np.diff(idx_thres) > 1])
        
        idx_stops = np.append(idx_thres[0:-1][np.diff(idx_thres) > 1], idx_thres[-1])
 
        return idx_starts, idx_stops
    else:
        return None, None

def split_array(array, idx_starts, idx_stops):
    """
    Split an numerical array into sub-arrays according to start and stop indices.

    Parameters
    ----------
    array : numpy array
    idx_starts : list of int
    idx_stops : list of int

    Returns
    -------
    arrays : list of array
    """
    arrays = []    
    for idx_start, idx_stop in zip(idx_starts, idx_stops):
        arrays.append(array[idx_start:idx_stop])
    return arrays

def stats(subarray_list):
    """
    Extract the (mean, std, min, max) values of each subarrays

    Parameters
    ----------
    subarray_list : list of numpy array

    Returns
    -------
    stats : list of array

    """
    stats = []
    for arr in subarray_list:
        if arr.size > 0: # not empty
            stats.append([np.mean(arr), np.std(arr), np.min(arr), np.max(arr)])

    return stats

def create_resumed_parameters(files):
    """
    Return the resumed parameters (mean, std, min, max) of resonator data.

    Parameters
    ----------
    files : list
        list of data files

    Returns
    -------
    db : pd.DataFrame
        resumed data.

    """
    V1_stats = []
    V2_stats = []
    V3_stats = []
    V4_stats = []
    V5_stats = []
    V6_stats = []          
    Piin_stats = []
    Piout_stats = []
    Pig_stats = []
    Prg_stats = []
    Vac1_stats = []
    Vac2_stats = []
    TC1_stats = []
    TC2_stats = []
    TC3_stats = []
    freq_stats = []
    Pm1_stats = []
    Pm2_stats = []
    Pm3_stats = []
    Pm4_stats = []
    Pm5_stats = []
    Pm6_stats = []
            
    time_stats = []
    time_cur_stats = []
    pulse_lengths = []
    freqs_stats = []
    
    for file in tqdm(files):
        data = TWAdata(file)
        # find start and stop times of each RF pulses
        # smoothing data a bit to avoid counting breakdown as the stop of the pulse
        idx_starts, idx_stops = find_shots_indices(data.df['V1'].ewm(span = 10).mean().values, 0.1)
        
        if idx_starts is not None:

            times = split_array(data.df['time_absolute'].values, idx_starts, idx_stops)
            subV1s = split_array(data.df['V1'].values, idx_starts, idx_stops)
            subV2s = split_array(data.df['V2'].values, idx_starts, idx_stops)
            subV3s = split_array(data.df['V3'].values, idx_starts, idx_stops)
            subV4s = split_array(data.df['V4'].values, idx_starts, idx_stops)
            subV5s = split_array(data.df['V5'].values, idx_starts, idx_stops)
            subV6s = split_array(data.df['V6'].values, idx_starts, idx_stops)
            
            is_current_probe_data = True
            try:
                subPm1s = split_array(data.df['Pm1'].values, idx_starts, idx_stops)
                subPm2s = split_array(data.df['Pm2'].values, idx_starts, idx_stops)
                subPm3s = split_array(data.df['Pm3'].values, idx_starts, idx_stops)
                subPm4s = split_array(data.df['Pm4'].values, idx_starts, idx_stops)
                subPm5s = split_array(data.df['Pm5'].values, idx_starts, idx_stops)
                subPm6s = split_array(data.df['Pm6'].values, idx_starts, idx_stops)
            except KeyError as e:
                is_current_probe_data = False

            subPiin = split_array(data.df['Piin'].values, idx_starts, idx_stops)
            subPiout = split_array(data.df['Piout'].values, idx_starts, idx_stops)
            subPig = split_array(data.df['Pig'].values, idx_starts, idx_stops)
            subPrg = split_array(data.df['Prg'].values, idx_starts, idx_stops)            
            subVac1 = split_array(data.df['Vac1'].values, idx_starts, idx_stops)
            subVac2 = split_array(data.df['Vac2'].values, idx_starts, idx_stops)        
            subTC1 = split_array(data.df['TC1'].values, idx_starts, idx_stops)
            subTC2 = split_array(data.df['TC2'].values, idx_starts, idx_stops)
            subTC3 = split_array(data.df['TC3'].values, idx_starts, idx_stops)
            
            # calculate the pulse duration in seconds
            durations = []
            for idx, time in enumerate(idx_starts):
                durations.append((data.df['time_absolute'][idx_stops][idx] - data.df['time_absolute'][idx_starts][idx]).total_seconds())
                freqs_stats.append(data.fMHz)
            pulse_lengths.append(durations)

            # Append data
            time_stats.append([t.flatten()[0] for t in times if t.size > 0])
            
            V1_stats.append(stats(subV1s))
            V2_stats.append(stats(subV2s))
            V3_stats.append(stats(subV3s))
            V4_stats.append(stats(subV4s))
            V5_stats.append(stats(subV5s))
            V6_stats.append(stats(subV6s))

            if is_current_probe_data:
                Pm1_stats.append(stats(subPm1s))
                Pm2_stats.append(stats(subPm2s))
                Pm3_stats.append(stats(subPm3s))
                Pm4_stats.append(stats(subPm4s))
                Pm5_stats.append(stats(subPm5s))
                Pm6_stats.append(stats(subPm6s))
                time_cur_stats.append([t.flatten()[0] for t in times if t.size > 0])
                
            Piin_stats.append(stats(subPiin))
            Piout_stats.append(stats(subPiout))
            Pig_stats.append(stats(subPig))
            Prg_stats.append(stats(subPrg))
            Vac1_stats.append(stats(subVac1))
            Vac2_stats.append(stats(subVac2))
            TC1_stats.append(stats(subTC1))
            TC2_stats.append(stats(subTC2))
            TC3_stats.append(stats(subTC3))            

    times_mmm = np.hstack(np.array(time_stats, dtype=object))
    times_cur_mmm = np.hstack(np.array(time_cur_stats, dtype=object))
    freqs = np.hstack(np.array(freqs_stats, dtype=object))
    V1_mmm = np.vstack(np.array(V1_stats, dtype=object))
    V2_mmm = np.vstack(np.array(V2_stats, dtype=object))
    V3_mmm = np.vstack(np.array(V3_stats, dtype=object))
    V4_mmm = np.vstack(np.array(V4_stats, dtype=object))
    V5_mmm = np.vstack(np.array(V5_stats, dtype=object))
    V6_mmm = np.vstack(np.array(V6_stats, dtype=object))

    if is_current_probe_data:
        Pm1_mmm = np.vstack(np.array(Pm1_stats, dtype=object))
        Pm2_mmm = np.vstack(np.array(Pm2_stats, dtype=object))
        Pm3_mmm = np.vstack(np.array(Pm3_stats, dtype=object))
        Pm4_mmm = np.vstack(np.array(Pm4_stats, dtype=object))
        Pm5_mmm = np.vstack(np.array(Pm5_stats, dtype=object))
        Pm6_mmm = np.vstack(np.array(Pm6_stats, dtype=object))
    
    Pig_mmm = np.vstack(np.array(Pig_stats, dtype=object))
    Prg_mmm = np.vstack(np.array(Prg_stats, dtype=object))
    Piin_mmm = np.vstack(np.array(Piin_stats, dtype=object))
    Piout_mmm = np.vstack(np.array(Piout_stats, dtype=object))
    
    Vac1_mmm = np.vstack(np.array(Vac1_stats, dtype=object))
    Vac2_mmm = np.vstack(np.array(Vac2_stats, dtype=object))
    
    TC1_mmm = np.vstack(np.array(TC1_stats, dtype=object))
    TC2_mmm = np.vstack(np.array(TC2_stats, dtype=object))
    TC3_mmm = np.vstack(np.array(TC3_stats, dtype=object))
    
    pulse_lengths_mmm = np.hstack(np.array(pulse_lengths, dtype=object))
    # remove zero lengths pulse
    pulse_lengths_mmm = pulse_lengths_mmm[pulse_lengths_mmm != 0]
        
    db = pd.DataFrame(data={
        'V1_mean': V1_mmm[:,0], 'V1_std': V1_mmm[:,1], 'V1_min': V1_mmm[:,2], 'V1_max': V1_mmm[:,3],
        'V2_mean': V2_mmm[:,0], 'V2_std': V2_mmm[:,1], 'V2_min': V2_mmm[:,2], 'V2_max': V2_mmm[:,3],
        'V3_mean': V3_mmm[:,0], 'V3_std': V3_mmm[:,1], 'V3_min': V3_mmm[:,2], 'V3_max': V3_mmm[:,3],
        'V4_mean': V4_mmm[:,0], 'V4_std': V4_mmm[:,1], 'V4_min': V4_mmm[:,2], 'V4_max': V4_mmm[:,3],
        'V5_mean': V5_mmm[:,0], 'V5_std': V5_mmm[:,1], 'V5_min': V5_mmm[:,2], 'V5_max': V5_mmm[:,3],
        'V6_mean': V6_mmm[:,0], 'V6_std': V6_mmm[:,1], 'V6_min': V6_mmm[:,2], 'V6_max': V6_mmm[:,3],
        'Pig_mean': Pig_mmm[:,0], 'Pig_std': Pig_mmm[:,1], 'Pig_min': Pig_mmm[:,2], 'Pig_max': Pig_mmm[:,3],
        'Prg_mean': Prg_mmm[:,0], 'Prg_std': Prg_mmm[:,1], 'Prg_min': Prg_mmm[:,2], 'Prg_max': Prg_mmm[:,3],
        'Piin_mean': Piin_mmm[:,0], 'Piin_std': Piin_mmm[:,1], 'Piin_min': Piin_mmm[:,2], 'Piin_max': Piin_mmm[:,3],
        'Piout_mean': Piout_mmm[:,0], 'Piout_std': Piout_mmm[:,1], 'Piout_min': Piout_mmm[:,2], 'Piout_max': Piout_mmm[:,3],        
        'Vac1_mean': Vac1_mmm[:,0], 'Vac1_std': Vac1_mmm[:,1], 'Vac1_min': Vac1_mmm[:,2], 'Vac1_max': Vac1_mmm[:,3],
        'Vac2_mean': Vac2_mmm[:,0], 'Vac2_std': Vac2_mmm[:,1], 'Vac2_min': Vac2_mmm[:,2], 'Vac2_max': Vac2_mmm[:,3],
        'TC1_mean': TC1_mmm[:,0], 'TC1_std': TC1_mmm[:,1], 'TC1_min': TC1_mmm[:,2], 'TC1_max': TC1_mmm[:,3],
        'TC2_mean': TC2_mmm[:,0], 'TC2_std': TC2_mmm[:,1], 'TC2_min': TC2_mmm[:,2], 'TC2_max': TC2_mmm[:,3],
        'TC3_mean': TC3_mmm[:,0], 'TC3_std': TC3_mmm[:,1], 'TC3_min': TC3_mmm[:,2], 'TC3_max': TC3_mmm[:,3],        
        'pulse_length': pulse_lengths_mmm, 'freq': freqs
        }, index=pd.DatetimeIndex(data=times_mmm, yearfirst=True))
    if is_current_probe_data:
        db_cur = pd.DataFrame(data={
         'Pm1_mean': Pm1_mmm[:,0], 'Pm1_std': Pm1_mmm[:,1], 'Pm1_min': Pm1_mmm[:,2], 'Pm1_max': Pm1_mmm[:,3],
         'Pm2_mean': Pm2_mmm[:,0], 'Pm2_std': Pm2_mmm[:,1], 'Pm2_min': Pm2_mmm[:,2], 'Pm2_max': Pm2_mmm[:,3],
         'Pm3_mean': Pm3_mmm[:,0], 'Pm3_std': Pm3_mmm[:,1], 'Pm3_min': Pm3_mmm[:,2], 'Pm3_max': Pm3_mmm[:,3],
         'Pm4_mean': Pm4_mmm[:,0], 'Pm4_std': Pm4_mmm[:,1], 'Pm4_min': Pm4_mmm[:,2], 'Pm4_max': Pm4_mmm[:,3],
         'Pm5_mean': Pm5_mmm[:,0], 'Pm5_std': Pm5_mmm[:,1], 'Pm5_min': Pm5_mmm[:,2], 'Pm5_max': Pm5_mmm[:,3],
         'Pm6_mean': Pm6_mmm[:,0], 'Pm6_std': Pm6_mmm[:,1], 'Pm6_min': Pm6_mmm[:,2], 'Pm6_max': Pm6_mmm[:,3],        
        }, index=pd.DatetimeIndex(data=times_cur_mmm, yearfirst=True))

        db = pd.concat([db, db_cur], axis=1)
    # Create the date column from the index and create an index columns as well.
    db = db.reset_index().rename(columns={'index':'date'}).reset_index()
    return db
