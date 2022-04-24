from email.mime import base
from re import X
from unittest import mock
from cv2 import phase
import numpy as np
import matplotlib.pyplot as plt

class Modulation():
  RESOLUTION=100 # Number of points in one period of the carrier frequency

  # Input data string is expected in binary
  def __init__(self, modulation_technique, data, fc, rs, fc_offset=0):
    self.modulation_technique = modulation_technique.upper()
    self.quadrature = True if self.modulation_technique.find('Q') != -1 else False
    self.data = list(data)
    self.data_len = len(self.data)

    self.fc_offset = fc_offset
    self.fc = fc
    self.rs = rs

    # Quadrature check
    if self.quadrature == True: self.pair_bits()
    self.setup_timeaxis()
    self.run()

  def run(self):
    if   self.modulation_technique == "ASK":   self.ask()
    elif self.modulation_technique == "FSK":   self.fsk()
    elif self.modulation_technique == "PSK":   self.psk()
    elif self.modulation_technique == "QPSK":  self.qpsk()
    elif self.modulation_technique == "DPSK":  self.dpsk()
    elif self.modulation_technique == "DQPSK": self.dqpsk()

  # Initialize time axis based on resolution, carrier frequency, and data rate
  def setup_timeaxis(self):
    symbols = self.data_len + 1 if self.quadrature == True else self.data_len
    self.cycles_per_symbol = self.fc/self.rs
    stop = self.cycles_per_symbol*(1/self.fc)*symbols
    step = (1/self.fc) / self.RESOLUTION
    self.x = np.arange(0, stop, step)

  # Time stretch base band signal
  def setup_base_band(self, fill_values):
    self.base_band = []

    for data in fill_values:
      modulated_bit =  np.full(int(self.cycles_per_symbol*self.RESOLUTION), fill_value=int(data))
      self.base_band = np.append(self.base_band, modulated_bit)

    self.base_band_len = len(self.base_band)

  # Repackage data into bit pairs dtype string
  def pair_bits(self):
    # Make data stream even if odd number of bits
    if (self.data_len % 2 == 1):
      self.data = np.append(self.data, self.data[-1])

    paired_bits = np.array([])
    for i in range(0, self.data_len, 2):
      paired_bits = np.append(paired_bits, f"{self.data[i]}{self.data[i+1]}")

    self.data = paired_bits
    self.data_len = len(self.data)

  # Setup phase data for non differntial modualtion
  def setup_phase_data(self):
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

  # Differentiate for binary or bit pairs
  def setup_phase_differential(self):
    self.phase_data = []
    if self.quadrature == True: # quartenary encoded
      self.phase_data += [45]
      for i in range(0, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i]
        if   self.data[i] == "11": self.phase_data += [previous_symbol_phase]
        elif self.data[i] == "10": self.phase_data += [(previous_symbol_phase + 90) % 360]
        elif self.data[i] == "00": self.phase_data += [(previous_symbol_phase + 180) % 360]
        elif self.data[i] == "01": self.phase_data += [(previous_symbol_phase + 270) % 360]
    
    else:
      self.phase_data += [0]
      for i in range(1, self.data_len, 1):
        previous_symbol_phase = self.phase_data[i-1]
        if   self.data[i] == "1": self.phase_data += [previous_symbol_phase]
        elif self.data[i] == "0": self.phase_data += [(previous_symbol_phase + 180) % 360]

    self.phase_data_len = self.data_len + 1
    print(self.phase_data)

  # Amplitude shift keying
  def ask(self):
    self.setup_base_band(self.data)

    self.modulated_signal = []
    for i in range(0, self.base_band_len, 1):
      self.modulated_signal += [self.base_band[i] * np.sin(2*np.pi*self.fc*self.x[i])]
      
  # Frequency shift keying
  def fsk(self):
    self.setup_base_band(self.data)

    self.modulated_signal = []
    for i in range(self.base_band_len):
      offset = self.fc_offset if self.base_band[i] == 1 else -self.fc_offset
      self.modulated_signal += [np.sin(2*np.pi*(self.fc + offset)*self.x[i])]

  # Binary phase shift keying
  def psk(self):
    self.setup_phase_data()
    self.setup_base_band(self.phase_data)
    
    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Quaternary phase shift keying  
  def qpsk(self):
    self.setup_phase_data()
    self.setup_base_band(self.phase_data)
    
    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Differential phase shift keying
  def dpsk(self):
    self.setup_phase_differential()
    self.setup_base_band(self.phase_data)

    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  # Differntial quartenary shift keying
  def dqpsk(self):
    self.setup_phase_differential()
    self.setup_base_band(self.phase_data)

    self.modulated_signal = []
    for i in range(0, len(self.base_band), 1):
      self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + np.deg2rad(self.base_band[i]))]

  def plot(self):
    symbols = self.data_len + 1 if self.quadrature == True else self.data_len
    plt.plot(self.x, self.modulated_signal)
    for i in range(symbols+1):
      plt.axvline(x=i*(self.x[1]*self.RESOLUTION*self.fc/self.rs), ls='--') # x[1] is the size of one time step assuming x[0] equals 0
    plt.show()
    plt.clf()


#------------------------Debug------------------------
def main():
  mod = Modulation(modulation_technique="dqpsk", data="1100", fc=150E3, rs=25E3, fc_offset=50E3)
  mod.plot()

if __name__ == "__main__": main()
