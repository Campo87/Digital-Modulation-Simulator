#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : James Starks & Inioluwa Obisakin
# Created Date: 4/11/22
# ---------------------------------------------------------------------------
""" Built for EE5374 Final Course Project """
# ---------------------------------------------------------------------------
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter

# ---------------------------------------------------------------------------

class Digital_Modulation():
  """
  Digital_Modulation: is a class that modulates digital values based on a set of
  input parameters. Currently ASK, FSK, PSK, QPSK, DPSK, and DQPSK digital modulation
  techniques are supported.
  """
  RESOLUTION=100 # Number of points in one period of the carrier frequency

  def __init__(self, modulation_technique, data, fc, rb, fc_offset=0):
    """
    __init__: is the modulation class constructor

    :param modulation_technique: one of the supported modualtion techniques
    :param data: binary data to be encoded
    :param fc: carrier frequency
    :param rs: symbol/bit rate, depending on if a quadrature technique is choosen
    :param fc_offset: carrier frequency offset for fsk techniques

    """

    self.modulation_technique = modulation_technique.upper() # Force uppercase
    self.quadrature = True if self.modulation_technique.find('Q') != -1 else False # Quadrature flag
    self.differential = True if self.modulation_technique.find('D') != -1 else False # Differential flag
    self.data = list(data)
    self.data_len = len(self.data)

    self.fc_offset = fc_offset
    self.fc = fc
	
    self.rb = rb

    # Quadrature check
    if self.quadrature == True: self.pair_bits() # Pair bits
    self.setup_timeaxis()
    self.run() # Modulate

  def run(self):
    """
    run: allows the user to manually start the modulator
    """
    if   self.modulation_technique == "ASK":   self.ask()
    elif self.modulation_technique == "FSK":   self.fsk()
    elif self.modulation_technique == "PSK":   self.psk()
    elif self.modulation_technique == "QPSK":  self.qpsk()
    elif self.modulation_technique == "DPSK":  self.dpsk()
    elif self.modulation_technique == "DQPSK": self.dqpsk()

  def setup_timeaxis(self):
    """
    setup_timeaxis: sets up the time (x) axis values. x will be used throughout
    the class for generating the sine waves and plotting the modulated data.
    """
    # Add an extra symbol period for the initialization period for differential encoding
    self.symbols = self.data_len + 1 if self.differential == True else self.data_len
    self.cycles_per_bit = self.fc/self.rb
    # When using quadrature, the number of cycles per symbol is double the number of
    # cycles per bit (i.e. symbol_rate = bit_rate/2)
    self.cycles_per_symbol = self.cycles_per_bit * 2 if self.quadrature == 1 else self.cycles_per_bit
    stop = self.cycles_per_symbol*(1/self.fc)*self.symbols
    step = (1/self.fc) / self.RESOLUTION
    self.x = np.arange(0, stop, step)

  def pair_bits(self):
    """
    pair_bits: groups the data bits in pairs for quadrature modulation. If there are
    an odd number of bits, the last bit is extended. 
    """
    # Make data stream even if odd number of bits
    if (self.data_len % 2 == 1):
      self.data = np.append(self.data, self.data[-1])

    paired_bits = np.array([])
    for i in range(0, self.data_len, 2):
      paired_bits = np.append(paired_bits, f"{self.data[i]}{self.data[i+1]}")

    self.data = paired_bits
    self.data_len = len(self.data) # Data length changes

  def setup_phase_data(self):
    """
    setup_phase_data: compairs the bit pairs and fills a phase data list. Works with
    quadrature and binary phase shift keying.
    Quadrature:
      Data  | Phase offset relative to carrier phase
       11   |  +0   deg
       10   |  +90  deg
       00   |  +180 deg
       01   |  +270 deg
    Binary:
      Data  | Phase offset relative to carrier phase
       1    |  +0 deg
       0    |  +180 deg
    """
    self.phase_data = []
    if self.quadrature == True:
      for data in self.data:
        if data == "11": self.phase_data += [0]
        elif data == "10": self.phase_data += [90]
        elif data == "00": self.phase_data += [180]
        elif data == "01": self.phase_data += [270]
    else:
      for data in self.data:
        if data == "1": self.phase_data += [0]
        if data == "0": self.phase_data += [180]
    
    self.phase_data_len = len(self.phase_data)

  def setup_phase_differential(self):
    """
    setup_phase_differential: prepares the phase relative to the phase of the previous
    symbol. Works with quadrature and binary differntial phase shift keying.
    Quadrature:
      Data  | Phase offset relative to previous symbol phase
       11   |  +0 deg
       10   |  +90 deg
       00   |  +180 deg
       01   |  +270 deg
    Binary:
      Data  | Phase offset relative to previous symbol phase
       1    |  +0 deg
       0    |  +180 deg
    """
    self.phase_data = []
    if self.quadrature == True: # quartenary encoded
      self.phase_data += [0] # Initial symbol phase offset
      for i in range(0, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i]
        if   self.data[i] == "11": self.phase_data += [previous_symbol_phase] # Mod 360 to keep on unit circle
        elif self.data[i] == "10": self.phase_data += [(previous_symbol_phase + 90)  % 360]
        elif self.data[i] == "00": self.phase_data += [(previous_symbol_phase + 180) % 360]
        elif self.data[i] == "01": self.phase_data += [(previous_symbol_phase + 270) % 360]
    
    else:
      self.phase_data += [0] # Initial symbol period phase offset
      for i in range(0, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i]
        if   self.data[i] == "1": self.phase_data += [previous_symbol_phase]
        elif self.data[i] == "0": self.phase_data += [(previous_symbol_phase + 180) % 360]
    
    self.phase_data_len = len(self.phase_data) # +1 to account for initialization period

  def ask(self):
    """
    ask: generates the modulated signal using amplitude shift keying. Using data length
    as an large offset value, j selects the time slice associated with the symbol by 
    dividing the length of the total samples in the transmission by the data length. 
    These should be even values if integral multiples of the carrier and data rate are
    kept. The same technique is used in all the other modulation functions.
    """
    self.modulated_signal = []
    for i in range(0, self.data_len, 1):
      for j in range(0, len(self.x)//self.data_len, 1):
        t = self.x[i*(len(self.x)//self.data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [int(self.data[i]) * np.sin(2*np.pi*self.fc*t)]
  
  def fsk(self):
    """
    fsk: generates the modulated signal using frequency shift keying. The data values
    are then used to select the frequency offset, 1 -> +fc offset, 0 -> -fc offset.
    With the offset values the symbol periods calculated, it is added (or subtracted)
    to the carrier frequency for each time step to generate the modulated signal.
    Note: this approach really only works when the offset is integer multiples of
    fc and rb.
    """
    self.modulated_signal = []
    for i in range(0, self.data_len, 1):
      for j in range(0, len(self.x)//self.data_len, 1):
        offset = self.fc_offset if self.data[i] == "1" else -self.fc_offset # select the offset

        t = self.x[i*(len(self.x)//self.data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [np.sin(2*np.pi*(self.fc+offset)*t)]

  def psk(self):
    """
    psk: generates the modulated signal using phase shift keying. For phase shift
    keying, the phase data is computed first (in degrees), then applied to the sine
    function to generate the modulated signal.
    """
    self.setup_phase_data()
    
    self.modulated_signal = []
    for i in range(0, self.phase_data_len, 1):
      for j in range(0, len(self.x)//self.phase_data_len, 1):
        t = self.x[i*(len(self.x)//self.phase_data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [np.sin(2*np.pi*self.fc*t + np.deg2rad(self.phase_data[i]))]

  def qpsk(self):
    """
    qpsk: generates the modulated signal using quadrature phase shift keying. For qpsk, the
    paired data bits are mapped to the appropriate phases. These phase values are then used
    to generate the modulated signal.
    """
    self.setup_phase_data()

    self.modulated_signal = []
    for i in range(0, self.phase_data_len, 1):
      for j in range(0, len(self.x)//self.phase_data_len, 1):
        t = self.x[i*(len(self.x)//self.phase_data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [np.sin(2*np.pi*self.fc*t + np.deg2rad(self.phase_data[i]))]

  def dpsk(self):
    """
    dpsk: generates the modulated signal using differential phase shift keying. For dpsk, the
    phase data is generated based on the phase of the previous symbol depending on the current
    bit value. These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_differential()
    
    self.modulated_signal = []
    for i in range(0, self.phase_data_len, 1):
      for j in range(0, len(self.x)//self.phase_data_len, 1):
        t = self.x[i*(len(self.x)//self.phase_data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [np.sin(2*np.pi*self.fc*t + np.deg2rad(self.phase_data[i]))]

  def dqpsk(self):
    """
    dqpsk: generates the modulated signal using differential quadrature phase shift keying. The
    phase data is generated based on the phase of the previous symbol depending on the current
    symbol value. These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_differential()
    
    self.modulated_signal = []
    for i in range(0, self.phase_data_len, 1):
      for j in range(0, len(self.x)//self.phase_data_len, 1):
        t = self.x[i*(len(self.x)//self.phase_data_len)+j] # Map i and j to correct time slice in x
        self.modulated_signal += [np.sin(2*np.pi*self.fc*t + np.deg2rad(self.phase_data[i]))]

  def plot(self):
    """
    plot: assumes the modulation signal and time axis has been generated. If rb and fc aren't
    integral multiplies of each other, you will get mismatched shape errors in the plot function.
    """
     # Format data rate to symbols/second for quadrature
    eng_formatter_freq = EngFormatter(unit="Hz") # Engineering notation for Hz
    if self.quadrature == True:
      data_rate = f"Symbol Rate={eng_formatter_freq.format_eng(self.rb/2)}sps"
    else:
      data_rate = f"Bit Rate={eng_formatter_freq.format_eng(self.rb)}bps"
      
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(self.x, self.modulated_signal)

    eng_formatter_time = EngFormatter(unit="s") # Set engineering notation formatter for time
    fig.get_axes()[0].xaxis.set_major_formatter(eng_formatter_time)

    eng_formatter_amp = EngFormatter(unit="V") # Set engineering notation formatter for time
    fig.get_axes()[0].yaxis.set_major_formatter(eng_formatter_amp)

    plt.title(f"{self.modulation_technique} Modulation, Carrier Freq={eng_formatter_freq.format_eng(self.fc)}Hz, {data_rate}")
    for i in range(self.symbols + 1): # Vertial lines at the edge of each symbol period
      plt.axvline(x=i*(self.x[1]*self.RESOLUTION*self.cycles_per_symbol), color='grey', ls='--', alpha=0.5) # x[1] is the size of one time step assuming x[0] is 0
    plt.show()
    plt.clf()

#------------------------Debugging------------------------
def main():
  mod = Digital_Modulation(modulation_technique="FSK",data="1011",fc=150E3,rb=50E3,fc_offset=50E3)
  mod.plot()

if __name__ == "__main__": main()
