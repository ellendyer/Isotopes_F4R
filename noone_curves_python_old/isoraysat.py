#
# Makes delD values (etc) under a rayleigh distillation
#
# Works internally with HDO of H218O (isotope) specific humidity, and converts
# at the end for output. Assumes discretization in log q for pretty plotting.
#
# This version takes alpha based on saturation (dewpoint) temperature.
# given the mixing ratio.
#
#  MIXING RATIO IN kg/kg
#  PRESSURE IN Pa
#
# This must be done setpwise along history to get temperature effect on alpha.
#
# David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
#
### CCD:: pro isoraysat, q0,del0,q1,npts,pressure,qh2o,deld,rh2o,rdel, $
### CCD::          hdo=hdo,h218o=h218o,eff=eff,vaph2o=vh2o,vapdel=vdel, $
### CCD::          noice=noice,conventional=conventional,tfreeze=tfreeze

import numpy as np

# NB: hdo,h218o,eff,noice,conventional,tfreeze,vh2ovhdo must be
#    defined in the context of the function definition

from globals_inits import *

from tsat import tsat
from alphdo_liq import alphdo_liq
from alphdo_ice import alphdo_ice

def isoraysat(q0,del0,q1,npts,pressure,hdo=hdo,h218o=h218o,eff=eff, \
      noice=noice,conventional=conventional,tfreeze=tfreeze,vh2ovhdo=vh2ovhdo):

# The arguments qh2o,deld,rh2o,rdel, each an array allocated in this function,
# cannot be returned in the manner of IDL.
# Instead, these four must be returned in a tuple by the return statement
# of this function as in:  return (qh2o,deld,rh2o,rdel)
# They can each be picked up in caller by:
#
#    (qh2o,deld,rh2o,rdel) = isoraysat(q0,del0,q1,npts,pressure)
#
# the arguments that are passed in to function are: q0,del0,q1,npts,pressure

### CCD:: ORIGINAL keyword arguments:
### CCD::    hdo=hdo,h218o=h218o,eff=eff,vaph2o=vh2o,vapdel=vdel,
### CCD::    noice=noice,conventional=conventional,tfreeze=tfreeze
### CCD::   **** These need clarification: vaph2o=vh2o,vapdel=vdel

### CCD:: REVISED keyword arguments:
### CCD::    hdo=hdo,h218o=h218o,eff=eff,noice=noice,
### CCD::    conventional=conventional,tfreeze=tfreeze,vh2ovhdo=vh2ovhdo
### CCD::    Note new keyword vh2ovhdo sort of replaces the two
### CCD::    keywords vaph2o=vh2o,vapdel=vdel. vh2ovhdo implies create
### CCD::    and use the two arrays vhso and vhdo to handle vapor.
#
# Set freezing transition
#
  tfrz = 273.16
  if tfreeze : tfrz = tfreeze
#
# Set the species (HDO by default)
#
  ispec = 0
  if hdo : ispec = 0
  if h218o : ispec = 1
#
# Set initial ratio given the input delta value
#
  if conventional:
     rat0 = del0/1000. + 1.			# conventional form
  else:
     rat0 = np.exp(del0/1000.)			# LOG form

###CCD:: was: qh2o = exp(alog(q0) + alog(q1/q0)*findgen(npts)/npts)
  qh2o = np.exp(np.log(q0) + np.log(q1/q0)*np.arange(npts,dtype=float)/npts)

### CCD:: was: qhdo = fltarr(npts)
  qhdo = np.zeros(npts)   # just allocating an array of npts zeros

  qhdo[0] = rat0*q0       # CCD: assign value to first element of qhdo
#
# Also save off the mass and composition of the preciptation
#
### CCD:: was: rh2o = fltarr(npts)
  rh2o = np.zeros(npts)   # just allocating an array(npts)
### CCD:: was: rhdo = fltarr(npts)
  rhdo = np.zeros(npts)   # just allocating an array(npts)

  if vh2ovhdo:
    vh2o = np.zeros(npts)   # just allocating an array(npts)
    vhdo = np.zeros(npts)   # just allocating an array(npts)
#
# Loop over points
#
  # build rest of array after qhdo[0] which as assigned above
  for n in range(1,npts):
#
# Get the dew point temperature
#
    qsat = 0.5*(qh2o[n-1] + qh2o[n])
    ttsat = tsat(pressure,qsat)
# NB: in IDL code it was tsat = tsat(...) but this cannot be used in
# Python since it is more precise. I changed variable tsat to ttsat - CCD
#
# Get the fractionation factor, to ice if needed
#
    if ttsat > tfrz or noice :    # Choose liquid alpha functions
      if ispec == 0:             # Choose HDO alpha function
        alpha = alphdo_liq(ttsat)
      if ispec == 1:             # Choose H218O alpha function
        alpha = alp18o_liq(ttsat)
    else:                        # Choose ice alpha functions
      if ispec == 0:             # Choose HDO alpha function
        alpha = alphdo_ice(ttsat)
      if ispec == 1:             # Choose H218O alpha function
        alpha = alp18o_ice(ttsat)

    alpeq = alpha
#
# Make a correction for "eff" if optional eff exists
# (as per Noone, TES HUM, 2008)
#   
    if eff :
      f = eff
#     alpha = alpha / (alpha*(1.0-f) + f)	# fraction vapor CCD=??
      alpha = alpha / (f*(alpha-1.) + 1.)	# fraction retained
#
    qhdo[n] = qhdo[n-1]*(qh2o[n]/qh2o[n-1])**alpha
#
# Save the rain, i.e., the change
#
    rh2o[n] = qh2o[n-1] - qh2o[n]		# each increment
    rhdo[n] = qhdo[n-1] - qhdo[n]		# each increment

#;    rh2o[n] = qh2o[0] - qh2o[n]		# total
#;    rhdo[n] = qhdo[0] - qhdo[n]		# total

#
# Optionally output just the vapor (for f/=1)
#
  if vh2ovhdo and eff :
    vh2o[n] = (1-f)*qh2o[n]
    vhdo[n] = qhdo[n]/(1+alpeq*f/(1-f))

  ### end for n in range(1,npts):      # Now build subsequent
#
# No rain in the zeroth step, so trim the array
#
  rh2o = rh2o[1:npts-1]
  rhdo = rhdo[1:npts-1]
  # CCD get some information ....
  # print "rhdo = ", rhdo
  # print "rh2o = ", rh2o
#
# Put into final form for deta values
#
  if conventional:
    deld = (qhdo/qh2o - 1.)*1000.		# APPROXIMATE form
    rdel = (rhdo/rh2o - 1.)*1000.		# APPROXIMATE FORM (rain)
    if vh2ovhdo :
      vdel = (vhdo/vh2o - 1.)*1000.		# APPROXIMATE FORM (vapor only)
  else:
    deld = np.log(qhdo/qh2o)*1000.		# LOG form
    rdel = np.log(rhdo/rh2o)*1000.		# LOG form (rain)
    if vh2ovhdo :
      vdel = np.log(vhdo/vh2o)*1000.		# LOG form (vapor only)

  if vh2ovhdo: # only if vdel (from vh2o,vhdo) needed
    return (qh2o,deld,rh2o,rdel,vdel)
  else :
    return (qh2o,deld,rh2o,rdel)
