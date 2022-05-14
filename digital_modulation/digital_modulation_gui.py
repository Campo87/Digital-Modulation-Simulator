#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : James Starks & Inioluwa Obisakin
# Created Date: 5/14/22
# ---------------------------------------------------------------------------
import tkinter as tk

import digital_modulation.digital_modulation as dm

# ---------------------------------------------------------------------------
window = tk.Tk()
window.title("Digital Modulation Simulator")
window.configure(background="black")
#window.geometry("170x230")
#window.maxsize(170,230)
#window.minsize(170,230)
# ---------------------------------------------------------------------------

class Digital_Modulation_GUI():
  '''
  Digital_Modulation_GUI: is class that wraps up the Digitial_Modulation class and
  facilitates easy access to that class via a GUI. The GUI provides a text entry 
  for the data sequence, carrier frequency, bit rate, and frequency offset, as well
  as a drop down menu for selecting supported modulation techniques.
  '''
  def __init__(self):
    '''
    __init__: is the constructor function that initializes the GUI. 
    '''
    # Setup Data Entry
    tk.Label(window, text="Data Sequence", bg="black", fg="white", font="none 12 bold").grid(row=0, column=0, sticky=tk.W)
    self.textentryDS = tk.Entry(window, width=20, bg="white")
    self.textentryDS.grid(row=0, column=1, sticky=tk.W)

    # Setup Carrier Frequency Entry
    tk.Label(window, text="Carrier Frequency", bg="black", fg="white", font="none 12 bold").grid(row=0, column=3, sticky=tk.W)
    self.textentryFC = tk.Entry(window, width=20, bg="white")
    self.textentryFC.grid(row=0, column=4, sticky=tk.W)

    # Setup Bit Rate Entry
    tk.Label(window, text="Bit Rate", bg="black", fg="white", font="none 12 bold").grid(row=1, column=0, sticky=tk.W)
    self.textentryBR = tk.Entry(window, width=20, bg="white")
    self.textentryBR.grid(row=1, column=1, sticky=tk.W)

    # Setup Frequency Offset Entry
    tk.Label(window, text="Frequency Offset", bg="black", fg="white", font="none 12 bold").grid(row=1, column=3, sticky=tk.W)
    self.textentryFR = tk.Entry(window, width=20, bg="white")
    self.textentryFR.grid(row=1, column=4, sticky=tk.W)
    self.textentryFR.insert(0, "0")

    # Setup Start Button
    button = tk.Button(window, text="Modulate", command=self.show).grid(row=3, column=2, sticky=tk.W)

    # Dropdown menu options
    mod_options = [
      "ASK",
      "FSK",
      "PSK",
      "DPSK",
      "QPSK",
      "DQPSK"
      ]

    # Datatype of menu text
    self.clicked = tk.StringVar()

    # initial menu text
    self.clicked.set( "ASK" )

    # Create Dropdown menu
    drop = tk.OptionMenu(window, self.clicked, *mod_options )
    drop.grid(row=2, column=0, sticky=tk.W)
    #drop.pack()

    window.mainloop()

  def show(self):
    '''
    show: is called when the Modulate button is clicked and calls the
    Digital_Modulation function.
    '''
    mod_tech = self.clicked.get()
    data = self.textentryDS.get()
    fc = float(self.textentryFC.get())
    rb = float(self.textentryBR.get())
    fc_off = float(self.textentryFR.get())
    self.mod = dm.Digital_Modulation(modulation_technique=mod_tech, data=data, fc=fc, rb=rb, fc_offset=fc_off)
    self.mod.plot()
