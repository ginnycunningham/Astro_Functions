#Written by Ginny Cunningham (05/2020)
#Function to convert raw count rates from Swift XRT to flux density
#The input data file is the basic light curve from https://www.swift.ac.uk/xrt_curves/
  #Usually only the photon counting mode is required, not window timing mode
#Requires spectral information for the photon index (gamma), unabsorbed counts-to-flux conversion (ct_flux [erg cm-2 cts-1]), and frequency range (va to vb [keV])

import pandas as pd
import numpy as np

def xrt_convert(data_file, ct_flux, gamma, va, vb, v): #input data file, counts-to-flux conversion, photon index, start observing frequncy, end observing frequency, frequency to convert to [keV]
	beta = 1-gamma
	counts = pd.read_csv(data_file, sep="\t", header=0)
	flux = counts['ctrt_ps'] * ct_flux #erg cm-2 s-1 (va-vb keV)
	fluxerr = counts['ctrt_uerr'] * ct_flux
	t = counts['dt'] #seconds

	fv = flux * (1+beta) / v * ((vb/v)**(1+beta) - (va/v)**(1+beta))**(-1) #erg cm-2 s-1 keV-1 #integrate over flux
	fverr = ((flux+fluxerr) * (1+beta) / v * ((vb/v)**(1+beta) - (va/v)**(1+beta))**(-1)) - fv
	keV2hz = 2.417989242e17  # hz / keV
	fv_jy = fv * 1e23 / (keV2hz) #Jy
	fv_jy_err = fverr * 1e23 / (keV2hz)
	return t, fv_jy, fv_jy_err #s, Jy, Jy
