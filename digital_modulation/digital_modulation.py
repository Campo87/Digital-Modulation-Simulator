import numpy as np
import matplotlib.pyplot as plt

class Modulation():
  RESOLUTION=100

  # Constructor
  # Input data string is expected in binary
  def __init__(self, modulation_technique, data, fc, rs, fc_offset=0):
    self.modulation_technique = modulation_technique.upper()
    self.data = np.asanyarray(list(data))
    self.data_len = len(self.data)

    self.fc_offset = fc_offset
    self.fc = fc
    self.tc = 1/fc
    self.rs = rs
    self.ts = 1/rs

    self.setup_timeaxis()

  # Initialize time axis based on resolution, carrier frequency, and data rate
  def setup_timeaxis(self):
    self.cycles_per_symbol = self.fc/self.rs
    stop = self.cycles_per_symbol*self.tc*self.data_len
    step = self.tc / self.RESOLUTION
    self.x = np.arange(0, stop, step)

  def generate_carrier_signal(self, fc):
    self.carrier_signal = np.sin(2*np.pi*fc*self.x)

  # Time stretch base band signal
  def timescale_base_band_signal(self):
    base_band_signal = []
    for data in self.data:
      if data == "0" or data == "11": amp = 0
      elif data == "1" or data == "10": amp = 1
      elif data == "00": amp = 2 # quartenary encoded signals are extended
      elif data == "01": amp = 3
      else: amp = -1 # Used for PSK

      base_band_signal = np.append(base_band_signal,
                                   np.full(int(self.cycles_per_symbol * self.RESOLUTION), fill_value=amp))

    self.base_band_signal = base_band_signal
  
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

  # Differentiate for binary or bit pairs
  def phase_differentiate(self, quartenary=False):
    if (quartenary == True): # quartenary encoded
      self.data = np.insert(self.data, 0, "45")
      self.data_len += 1

      for i in range(1, self.data_len, 1):
        previous_symbol_phase = int(self.data[i-1])
        if  (self.data[i] == "11"): self.data[i] = previous_symbol_phase
        elif(self.data[i] == "10"): self.data[i] = (previous_symbol_phase + 90) % 360
        elif(self.data[i] == "00"): self.data[i] = (previous_symbol_phase + 180) % 360
        elif(self.data[i] == "01"): self.data[i] = (previous_symbol_phase + 270) % 360

    else: # binary encoded
      # Initial data
      self.data = np.insert(self.data, 0, "0")
      # 0 - 0 deg offset
      # 1 - 180 deg offset
      for i in range(1, self.data_len, 1):
        if(self.data[i] == "1"):
          self.data[i] = self.data[i-1]
        elif(self.data[i] == "0"):
          self.data[i] = "1" if self.data[i-1] == "0" else "0"

  # Amplitude shift keying
  def ask(self):
    self.generate_carrier_signal(fc=self.fc)
    self.timescale_base_band_signal()
    self.modulated_signal = [self.base_band_signal[i] * self.carrier_signal[i] for i in range(len(self.base_band_signal))]


  # Frequency shift keying
  def fsk(self):
    self.generate_carrier_signal(fc=self.fc + self.fc_offset)
    self.timescale_base_band_signal()
    fc_upper = [self.base_band_signal[i] * self.carrier_signal[i] for i in range(len(self.base_band_signal))]

    for i in range(0, self.data_len, 1):
      self.data[i] = "0" if self.data[i] == "1" else "1"

    self.generate_carrier_signal(fc=self.fc - self.fc_offset)
    self.timescale_base_band_signal()
    fc_lower = [self.base_band_signal[i] * self.carrier_signal[i] for i in range(len(self.base_band_signal))]

    self.modulated_signal = [fc_upper[i] + fc_lower[i] for i in range(len(fc_upper))]
  
  # Binary phase shift keying
  def psk(self):
    self.generate_carrier_signal(fc=self.fc)

    for i in range(0, self.data_len, 1):
      self.data[i] = "-1" if self.data[i] == "0" else "1"

    self.timescale_base_band_signal()
    self.modulated_signal = [self.base_band_signal[i] * self.carrier_signal[i] for i in range(len(self.base_band_signal))]



  # Quaternary phase shift keying  
  def qpsk(self):
    self.pair_bits()
    self.generate_carrier_signal(fc=self.fc)
    self.timescale_base_band_signal()
    
    self.modulated_signal = []
    for i in range(0, len(self.base_band_signal), 1):
      if self.base_band_signal[i] == 0: self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] +  np.pi/4)]
      if self.base_band_signal[i] == 1: self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + 3*np.pi/4)]
      if self.base_band_signal[i] == 2: self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + 5*np.pi/4)]
      if self.base_band_signal[i] == 3: self.modulated_signal += [np.sin(2*np.pi*self.fc*self.x[i] + 7*np.pi/4)]


  # Differential phase shift keying
  def dpsk(self):
    pass

  # Differntial quartenary shift keying
  def dqpsk(self):
    pass

  def plot(self):
    plt.plot(self.modulated_signal)
    plt.show()
    plt.clf()


#------------------------Debug------------------------
def main():
  mod = Modulation(modulation_technique="fsk", data="111000101100", fc=500E3, rs=25E3, fc_offset=100E3)
  mod.pair_bits()
  mod.differential(quartenary=True)
  print(mod.data)

if __name__ == "__main__": main()
