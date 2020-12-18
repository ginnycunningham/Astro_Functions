#Written by Ginny Cunningham (06/2020)
#This function takes magnitude observations as input and converts them to flux density in units of mJy 
#Requires zero point flux density (f0), observation frequency (v), and extinction level (A) as known values 
  #f0 can be found via: http://astroweb.case.edu/ssm/ASTR620/mags.html
  #A can be found via: https://ned.ipac.caltech.edu/extinction_calculator?in_csys=Equatorial&in_equinox=J2000.0&obs_epoch=2000.0&ra=20%3A34%3A23.25&dec=%2B06%3A55%3A10.5

import numpy as np

def mag2fv(mags, magerr, f0, v, A, label): #uncorrected magnitude, magnitude error, zero point flux density, frequency [Hz], extinction [microns], instrument
	f = np.zeros(len(mags))
	f_err = np.zeros(len(mags))
	for x in range(len(f)):
		try: 
			mag = mags[x]
			err = magerr[x]
			f[x] = (f0 * 10**((float(mag)-A) / -2.5)) * 1000 #mJy
			f_err[x] = ((f0 * 10**(((float(mag)-A)-float(err)) / -2.5))) * 1000 - f[x] #mJy
		except ValueError: #in case of magnitude upper limits
			mag = mags[x][1:5]
			f[x] = (f0 * 10**((float(mag)-A) / -2.5)) * 1000 #mJy
	return f, f_err #in units of mJy
