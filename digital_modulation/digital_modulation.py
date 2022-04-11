import numpy as np


class Modulation():
  modulation_technique = ""
  bb_signal = []
  fc = []
  rb = 0

  # Constructor
  def __init__(self, modulation_technique, bb_signal, fc, rb):
    self.modulation_technique = modulation_technique
    self.bb_signal = bb_signal
    self.fc = fc
    self.rb = rb

  # Differentiate for binary or bit pairs
  def differential(self, quartenary=False):
    if (quartenary is True):
      pass
    else:
      pass
  
  # Repackage data into bit pairs
  def bit_pair(self):
    pass
 
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



def main():
  pass

if __name__ == "__main__": main()
