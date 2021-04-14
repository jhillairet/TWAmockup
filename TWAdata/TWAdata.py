import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile

class TWAdata():
  def __init__(tdms_path):
    tdms_file = TdmsFile.read("path_to_file.tdms")
      for group in tdms_file.groups():
          group_name = group.name
          for channel in group.channels():
              channel_name = channel.name
              # Access dictionary of properties:
              properties = channel.properties
              # Access numpy array of data for channel:
              data = channel[:]
              # Access a subset of data
              data_subset = channel[100:200]
