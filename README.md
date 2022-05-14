# Digital-Modulation-Simulator
This project simulates different digital modulation technqiues and plots the resulting modulated signal using matplotlib. In the digital_modulation directory, there are two files digital_modulation and digital_modulation_gui. digital_modulation contains all the signal modulation and plotting code and _gui contains the GUI initialization code. The goal of the project was to gain a intuitive understanding of the different fundamental digital modulation techniques.

### **Supported Modulation Techniques**

|Modulation Technique|Description|
|------|------|
|Amplitude Shift Keying|Carrier signal on for 1 & off for 0|
|Frequency Shift Keying|Offset carrier signal by + offset for 1 and - offset for 0|
|Phase Shift Keying|Offset phase +0 deg for 1 and +180 deg for 0|
|Quadrature Phase Shift Keying|[QPSK Description](https://en.wikipedia.org/wiki/Phase-shift_keying#Quadrature_phase-shift_keying_(QPSK))*|
|Differential Phase Shift Keying|[DPSK Description](https://en.wikipedia.org/wiki/Phase-shift_keying#Differential_phase-shift_keying_(DPSK))*|
|Differential Quadrature Phase Shift Keying|Differnatial phase shift keying, but with qudature bit pairing*|
*There are more in-depth explinations in [digital_modulation/Digital_Modulation](asd)
### **GUI Preview**


|Inputs & Buttons    |Description
|-----------------   |------------------------------------------------------------------------------|
|Data Sequence       |Text Entry: The Sequences of 1's & 0's you wish to modulate                   |
|Carrier Frequency   |Text Entry: The frequency that you want the modulated signal to be centered at|
|Bit Rate            |Text Entry: The rate of the transmitted bits                                  |
|Frequency Offset    |Text Entry: The +/- offset applied to the carrier frequency (FSK)             |
|Modulation Technique|Dropdown: Select the desired modulation technique                             |
|Modulate            |Button: Plot the modulated data sequence and display the graph                |
