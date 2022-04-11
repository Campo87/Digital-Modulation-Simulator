import numpy as np


class Modulation():
  modulation_technique = ""
  data = ""
  data_len = 0
  bb_signal = []
  fc = []
  rb = 0

  # Constructor
  # Input data string is expected in binary
  def __init__(self, modulation_technique, data, fc, rb):
    self.modulation_technique = modulation_technique
    self.data = np.asanyarray(list(data))
    self.data_len = len(self.data)
    self.fc = fc
    self.rb = rb

  # Differentiate for binary or bit pairs
  def differential(self, quartenary=False):
    if (quartenary is True): # quartenary encoded
      pass
    else: # binary encoded
      pass
  
  # Repackage data into bit pairs dtype string
  def bit_pair(self):
    # Make data stream even if odd number of bits
    if (self.data_len % 2 is 1):
      self.data = np.append(self.data, self.data[-1])

    paired_bits = []
    for i in range(0, self.data_len, 2):
      paired_bits.append(f"{self.data[i]}{self.data[i+1]}")

    self.data = np.asarray(paired_bits)
    self.data_len = len(self.data)
 
  # Time stretch base band signal
  def stretch_bb(self):
    pass

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
  mod = Modulation("psk", "11010", 23, 23)
  print(f"{mod.data_len} {mod.data}")
  mod.bit_pair()
  print(f"{mod.data_len} {mod.data}")

if __name__ == "__main__": main()
