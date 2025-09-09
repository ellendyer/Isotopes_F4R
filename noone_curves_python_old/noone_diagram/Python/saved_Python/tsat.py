### Translated IDL --> Python - CCD Jan 18, 2021 - needs numpy ...
#  Finds the (dewpoint) temperature given a saturated mass mixing ratio
#  (i.e., works backwards along the Clausias curve)
#  
#  PRESSURE IN PA
#  MIXING RATIO IN kg/kg
#  
#  David Noone <dcn@colorado.edu> - Sun Mar  2 09:42:31 MST 2008

# Translated from IDL function tsat,pressure,qsat
def tsat(pressure,qsat):
  from math import log
  epsqs = 0.62197                   # ratio of molecular weights
  esat = pressure/(epsqs/qsat + 1)  # Convert mixing ratio to evapor presure
  try:        # Ensure log(...) is in range
    loge = log(esat/611.2)      # Use the empirical formula to get dewpoint
  except:
    loge = float("NaN")        # on log error, return a NaN
    print "tsat: log(esat/611.2) error!"
    print "tsat: (pressure,qsat) = ", pressure,qsat
  tsat = 243.5*loge/(17.67 - loge) + 273.16	# in K
  return tsat
