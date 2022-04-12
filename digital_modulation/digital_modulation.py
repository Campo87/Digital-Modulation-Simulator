import numpy as np
import matplotlib.pyplot as plt

class Modulation():
  RESOLUTION=100

  # Constructor
  # Input data string is expected in binary
  def __init__(self, modulation_technique, data, fc, rs):
    self.modulation_technique = modulation_technique
    self.data = np.asanyarray(list(data))
    self.data_len = len(self.data)

    self.fc = fc
    self.tc = 1/fc
    self.rs = rs
    self.ts = 1/rs

  # Differentiate for binary or bit pairs
  def differential(self, quartenary=False):
    if (quartenary is True): # quartenary encoded
      pass
    else: # binary encoded
      pass
  
  # Repackage data into bit pairs dtype string
  def pair_bits(self):
    # Make data stream even if odd number of bits
    if (self.data_len % 2 is 1):
      self.data = np.append(self.data, self.data[-1])

    paired_bits = []
    for i in range(0, self.data_len, 2):
      paired_bits.append(f"{self.data[i]}{self.data[i+1]}")

    self.data = np.asarray(paired_bits)
    self.data_len = len(self.data)
 
  # Time stretch base band signal
  def timescale_base_band_signal(self):
    base_band_signal = []
    for data in self.data:
      if data == "0" or data == "00": amp = 0
      elif data == "1" or data == "11": amp = 1
      elif data == "01": amp = 2
      elif data == "10": amp = 3

      base_band_signal = np.append(base_band_signal,
                                   np.full(int(self.cycles_per_symbol * self.RESOLUTION), fill_value=amp))

    self.base_band_signal = base_band_signal
      
  # Initialize time axis based on resolution, carrier frequency, and data rate
  def setup_timeaxis(self):
    self.cycles_per_symbol = self.fc/self.rs
    stop = self.cycles_per_symbol*self.tc*self.data_len
    step = self.tc / self.RESOLUTION
    self.x = np.arange(0, stop, step)

  # Amplitude shift keying
  def ask(self):
    pass

  # Frequency shift keying
  def fsk(self):
    pass
  
  # Phase shift keying
  def psk(self):
    pass

  # Quaternary phase shift keying  
  def qpsk(self):
    pass

  # Differential phase shift keying
  def dpsk(self):
    pass

  # Differntial quartenary shift keying
  def dqpsk(self):
    pass


#------------------------Debug------------------------
def main():
  mod = Modulation("qpsk", "11010", 150E3, 25E3)
  mod.pair_bits()  
  mod.setup_timeaxis()
  mod.timescale_base_band_signal()
  print(len(mod.x))
  print(len(mod.base_band_signal))


if __name__ == "__main__": main()
