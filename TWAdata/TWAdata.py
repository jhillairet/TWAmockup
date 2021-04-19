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

            # Post processing
            self.raw_TOS_to_TOS()
            self.raw_V_to_V()
            self.raw_vac_to_vac()
            self.raw_Piout_to_Piout()
            self.raw_Pgen_to_Pgen()
            self.raw_Tc_to_Tc()
            self.raw_Vm1_to_Pm1()

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
        
    def cable_calib(self, cable, fMHz):
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
                'cable_ext_3':{'a':17.44274311,'b':-896.839019},
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
        
    def raw_TOS_to_TOS(self):
        '''
        calibration for TOS (AD8302)

        Returns
        -------
        None.

        '''
        self._df['TOS'] = 32.824 * self._df['TOS_raw'] - 29.717

    def AD8310_calib(self, card, Vdc):
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
               'V7':{'a':40.851, 'b':-96.176},}
        
        return cards[card]['a'] * Vdc + cards[card]['b']
    
    def V_probe_calib(self, probe, fMHz):
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
    
    def dBm_to_Vrf(self, dBm):
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
        60 dB: Spinner coupler attenuation
        0.5 dB: cable loss
        
        The result is in dBm --> Power in Watts
        '''
        cable_att_dB = self.cable_calib('cable_Pout_FWD', self.fMHz)[0]
        Piout_dBm = self.AD8310_calib('V7', self._df['Piout_raw'])
        self._df['Piout'] = 10**((Piout_dBm + 42.645 + 61 + cable_att_dB) / 10)/1e3
        
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
            add_att_Pi_dB = 9.85
            add_att_Pr_dB = 9.87
            print('Adding additional 10dB attenuator')
        else:
            add_att_Pi_dB = 0
            add_att_Pr_dB = 0

        self._df['Pig'] = 10**(((2.1513*self._df['Pig_raw'] + 2.0106) + 61.03 + add_att_Pi_dB)/10)/1e3
        self._df['Prg'] = 10**(((2.1853*self._df['Prg_raw'] + 1.7151) + 61.14 + add_att_Pr_dB)/10)/1e3
        
    def raw_Tc_to_Tc(self):
        '''
        Process thermocouple raw data
        
        The result is in degree C
        '''
        self._df['TC1'] = 21.665 * self._df['TC1_raw'] -23.048
        self._df['TC2'] = 21.665 * self._df['TC2_raw'] -23.048 
        self._df['TC3'] = 21.665 * self._df['TC3_raw'] -23.048 
        
    def raw_Vm1_to_Pm1(self):
        '''
        Vm1*32.113 - 30.531 : -> (A/B) in dB
        33 dB: attenuator
        
        The result is a power Pm1 in Watts
        '''
        self._df['Pm1'] = 10**(((-10 -(self._df['Vm1_raw']*32.113 - 30.531)) + 33)/10)/1e3

