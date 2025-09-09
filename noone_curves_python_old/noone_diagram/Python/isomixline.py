#
# Makes delD values (etc) under a mixing line assumtion (evaporation, etc)
#
# Works internally with HDO (isotope) specific humidity, and converts at 
# the end for output. Assumes discretization in 1/q for pretty plotting.
#
# David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
#
### CCD:: pro isomixline, q0,del0,qs,dels,npts,eta,qh2o,deld, $
### CCD::              conventional=conventional
### CCD: arguments 7 and 8 are names of two vectors which are actually
### CCD: allocated space here in isoeqlsat with findgen and fltarr

import numpy as np

# conventional must be defined in context of function
from globals import *		

def isomixline(q0,del0,qs,dels,npts,eta,conventional=conventional):

# The arguments, qh2o,deld, are each an array allocated in this function,
# and cannot be returned in the manner of IDL.
# Instead, these two must be returned in a tuple by the return statement
# of this function as in:  return (qh2o,deld)
# They can each be picked up in caller by:
#
#    (qh2o,deld) = isomixline(q0,del0,qs,dels,npts,eta)
#
#
# Set initial ratios from input delta values
#
  if conventional:
    rat0 = del0/1000. + 1.			# APPROXIMATE form
    rats = dels/1000. + 1.			# APPROXIMATE form
  else:
    rat0 = exp(del0/1000.)			# LOG form
    rats = exp(dels/1000.)			# LOG form

#
# Set range of q values
#
### CCD:: qh2o = (1/q0 + (1/qs-1/q0)*findgen(npts)/(npts-1))**(-1)
### CCD:: findgen(n) generates float array of n elements with each
### CCD:: element set to its own index as a float.

  qh2o = (1/q0 + (1/qs-1/q0)*np.arange(npts,dtype=float)/(npts-1))**(-1)
#
# Set the (evolving) flux factor
#
  hfac = (rats*qs - rat0*q0)/(qs-q0)**eta
#
# Solve the Noone equation
#
  qhdo = rats*qs - hfac*(qs - qh2o)**eta
#
# This will fail with a div zero for the end memeber, so overwrite by hand
#
  qh2o[npts-1] = qs
  qhdo[npts-1] = qs*rats
#
# Finalize for ourput
#
  if conventional:
    deld = (qhdo/qh2o - 1.)*1000.			# APPROXIMATE form
  else:
    deld = np.log(qhdo/qh2o)*1000.			# LOG form
  return (qh2o,deld)    # return the two allocated arrays.
