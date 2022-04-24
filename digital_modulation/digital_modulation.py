#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : James Starks
# Created Date: 4/11
# ---------------------------------------------------------------------------
""" Built for EE5374 Final Course Project """
# ---------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
# ---------------------------------------------------------------------------

class Digital_Modulation():
  """
  Digital_Modulation: is a class that modulates digital values based on a set of
  input parameters. Currently ASK, FSK, PSK, QPSK, DPSK, and DQPSK digital modulation
  techniques are supported.
  """
  RESOLUTION=100 # Number of points in one period of the carrier frequency

  # Input data string is expected in binary
  def __init__(self, modulation_technique, data, fc, rs, fc_offset=0):
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
    self.data = list(data)
    self.data_len = len(self.data)

    self.fc_offset = fc_offset
    self.fc = fc
    self.rs = rs

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
    symbols = self.data_len + 1 if self.quadrature == True else self.data_len
    self.cycles_per_symbol = self.fc/self.rs
    stop = self.cycles_per_symbol*(1/self.fc)*symbols
    step = (1/self.fc) / self.RESOLUTION
    self.x = np.arange(0, stop, step)

  # Time stretch base band signal
  def setup_base_band(self, fill_values):
    """
    setup_base_band: stretches the data or phase values (based on the fill_values)
    so they match with the symbol/bit periods and can easily be converted to a sine
    wave.

    :param fill_values: values to be stretched to match the symbol periods
    """

    self.base_band = []
    for data in fill_values:
      modulated_bit =  np.full(int(self.cycles_per_symbol*self.RESOLUTION), fill_value=int(data)) # Stretch for one symbol period
      self.base_band = np.append(self.base_band, modulated_bit)

    self.base_band_len = len(self.base_band)

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
       11   |  +45 deg
       10   |  +135 deg
       00   |  +225 deg
       01   |  +315 deg
    Binary:
      Data  | Phase offset relative to carrier phase
       1    |  +0 deg
       0    |  +180 deg
    """
    self.phase_data = []
    if self.quadrature == True:
      for data in self.data:
        if data == "11": self.phase_data += [45]
        elif data == "10": self.phase_data += [135]
        elif data == "00": self.phase_data += [225]
        elif data == "01": self.phase_data += [315]
    else:
      for data in self.data:
        if data == "1": self.phase_data += [0]
        if data == "0": self.phase_data += [180]

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
      self.phase_data += [45] # Initial symbol period phase offset
      for i in range(0, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i]
        if   self.data[i] == "11": self.phase_data += [previous_symbol_phase] # Mod 360 to keep on unit circle
        elif self.data[i] == "10": self.phase_data += [(previous_symbol_phase + 90)  % 360]
        elif self.data[i] == "00": self.phase_data += [(previous_symbol_phase + 180) % 360]
        elif self.data[i] == "01": self.phase_data += [(previous_symbol_phase + 270) % 360]
    
    else:
      self.phase_data += [0] # Initial symbol period phase offset
      for i in range(1, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i-1]
        if   self.data[i] == "1": self.phase_data += [previous_symbol_phase]
        elif self.data[i] == "0": self.phase_data += [(previous_symbol_phase + 180) % 360]

    self.phase_data_len = self.data_len + 1 # +1 to account for initialization period

  # Amplitude shift keying
  def ask(self):
    """
    ask: generates the modulated signal using amplitude shift keying. The data stream
    is stretched so each bit fits one symbol period. The stretched data values are used
    to control if the carrier signal is one or off for each symbol period.
    """
    self.setup_base_band(self.data) # Stretch data 

    self.modulated_signal = []
    for i in range(0, self.base_band_len, 1):
      # If 1, the carrier freq is one, else it's off
      self.modulated_signal += [self.base_band[i] * np.sin(2*np.pi*self.fc*self.x[i])]
      
  # Frequency shift keying
  def fsk(self):
    """
    fsk: generates the modulated signal using frequency shift keying. The data stream
    is streched so each bit fits one symbol period. The stretched data values are then
    used to select the frequency offset, 1 -> +fc offset, 0 -> -fc offset. With the
    offset values the symbol periods calculated, it is added (or subtracted) to the
    carrier frequency for each time step to generate the modulated signal. Note: this
    approach really only works when the offset is integer multiples of fc and rs.
    """
    self.setup_base_band(self.data)

    self.modulated_signal = []
    for i in range(self.base_band_len):
      offset = self.fc_offset if self.base_band[i] == 1 else -self.fc_offset # select the offset
      self.modulated_signal += [np.sin(2*np.pi*(self.fc + offset)*self.x[i])]

  # Binary phase shift keying
  def psk(self):
    """
    psk: generates the modulated signal using phase shift keying. For phase shift
    keying, the phase data is computed first (in degrees), then pased to setup_base_band.
    These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_data()
    self.setup_base_band(self.phase_data)
    
    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Quaternary phase shift keying  
  def qpsk(self):
    """
    qpsk: generates the modulated signal using quadrature phase shift keying. For qpsk, the
    paired data bits are mapped to the appropriate phases, then stretched to fit each symbol
    period. These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_data()
    self.setup_base_band(self.phase_data)
    
    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Differential phase shift keying
  def dpsk(self):
    """
    dpsk: generates the modulated signal using differential phase shift keying. For dpsk, the
    phase data is generated based on the phase of the previous symbol depending on the current
    bit value. These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_differential()
    self.setup_base_band(self.phase_data)

    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Differntial quartenary shift keying
  def dqpsk(self):
    """
    dqpsk: generates the modulated signal using differential quadrature phase shift keying. The
    phase data is generated based on the phase of the previous symbol depending on the current
    symbol value. These phase values are then used to generate the modulated signal.
    """
    self.setup_phase_differential()
    self.setup_base_band(self.phase_data)

    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  def plot(self):
    """
    plot: assumes the modulation signal and time axis has been generated.
    """
    symbols = self.data_len + 1 if self.quadrature == True else self.data_len
    plt.title(f"{self.modulation_technique} Modulation, fc={self.fc}kHz, rs={self.rs}kHz")
    plt.ylabel("Amplitude (Volts)")
    plt.xlabel("Time(s)")
    plt.plot(self.x, self.modulated_signal)
    for i in range(symbols + 1): # Vertial lines at the edge of each symbol period
      plt.axvline(x=i*(self.x[1]*self.RESOLUTION*self.fc/self.rs), ls='--') # x[1] is the size of one time step assuming x[0] equals 0
    plt.show()
    plt.clf()


#------------------------Debugging------------------------
def main():
  mod = Digital_Modulation(modulation_technique="dqpsk", data="1100", fc=150E3, rs=25E3, fc_offset=50E3)
  mod.plot()

if __name__ == "__main__": main()
