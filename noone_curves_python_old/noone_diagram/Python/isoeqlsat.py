#
# Makes delD values (etc) under a comple equillibrium (closed system)
#
# Works internally with HDO (isotope) specific humidity, and converts at 
# the end for output. Assumes discretization in log q for pretty plotting.
#
# This version takes alpha based on saturation (dewpoint) temperature.
# given the mixing ratio.
#
#  MIXING RATIO IN kg/kg
#  PRESSURE IN Pa
#
# This this mist be done setpwise along the history.
#
# David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
#
### CCD:: pro isoeqlsat, q0,del0,q1,npts,pressure,qh2o,deld,  $
### CCD::          hdo=hdo,h218o=h218o,conventional=conventional
### CCD: arguments 6 and 7 are names of two vectors which are actually
### CCD: allocated space here in isoeqlsat with findgen and fltarr

import numpy as np

from tsat import tsat
from alphdo_liq import alphdo_liq

# hdo,h218o, and conventional must be defined in context of function
from globals import *		

def isoeqlsat(q0,del0,q1,npts,pressure, \
              hdo=hdo,h218o=h218o,conventional=conventional):
# The arguments qh2o,deld, each an array allocated in this function,
# cannot be returned in the manner of IDL.
# Instead, these two must be returned in a tuple by the return statement
# of this function as in:  return (qh2o,deld)
# They can each be picked up in caller by:
#
#    (qh2o,deld) = isoeqlsat(q0,del0,q1,npts,pressure)
#
# Set the species (HDO by default)
#
  ispec = 0
  if hdo : ispec = 0
  if h218o : ispec = 1
  ### CCD: if (keyword_set(HDO)) then ispec = 0
  ### CCD: if (keyword_set(H218O)) then ispec = 1
   
#
# Set initial ratio from delta value
#
  if conventional:
    rat0 = del0/1000. + 1.			# APPROXIMATE form
  else:
    rat0 = np.exp(del0/1000.)			# LOG form

#
# Set up integration evolution - log variation in q
#

### CCD:: qh2o = exp(alog(q0) + alog(q1/q0)*findgen(npts)/npts)
### CCD:: findgen(n) generates float array of n elements with each
### CCD:: element set to its own index as a float.

  qh2o = np.exp(np.log(q0) + np.log(q1/q0)*np.arange(npts,dtype=float)/(npts))

### CCD:: qhdo = fltarr(npts)  replace with np,zeros(npts)
  qhdo = np.zeros(npts)   # just allocating an array(npts)

  qhdo[0] = rat0*q0          # Set value for first element
  for n in range(1,npts):    # Now build subsequent elements ...
#
# Get the dew point temperature
#
    qsat = 0.5*(qh2o[n-1] + qh2o[n])
    ttsat = tsat(pressure,qsat)
# NB: in IDL code it was tsat = tsat(...) but this cannot be used in
# Python since it is more precise. I changed variable tsat to ttsat - CCD
#
# Get the fractionation factor: Must ALWAYS be liquid
#
    if ispec == 0:   # Choose which alp...liq function, see alp...liq.pro
      alpeq = alphdo_liq(ttsat)
    if ispec == 1:
      alpeq = alp18o_liq(ttsat)

    qhdo[n] = qhdo[0]/(alpeq*(qh2o[0]/qh2o[n] - 1.) + 1.)
#
# Convert output to delta
#

  if conventional:
    deld = (qhdo/qh2o - 1.)*1000.			# APPROXIMATE form
  else:
    deld = np.log(qhdo/qh2o)*1000.			# LOG form
  return (qh2o,deld)    # return the two allocated arrays.
