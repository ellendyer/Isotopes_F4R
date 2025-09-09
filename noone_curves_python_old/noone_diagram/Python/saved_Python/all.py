
# Global default settings of some keywords / flags and some initial
# values for global variables

hdo=True
h218o=False
conventional=True

eff=False
noice=False
tfreeze=False
vh2ovhdo=False

# Some initial values for testing
del0 = -400.
delp = -30. 
eta  = 0.995
hsrc = 0.80 
nn   = 20          # Make it small for testing ..   nn   = 1000 
pcld = 85000.
ps = 1000.e2			# approximate surface pressure
q0   = 0.9 
qmin = 11.
tsrc = 300. 
v2m = (18./29.)                 # converts pptv to mixing ratio
# Returns HDO equilibrium fractionation for HDO to ice
# fractionation is the parameter alpha in paper
#
# Translated from IDL function alphdo_ice, tk
# tk is temperature Kelvin
def alphdo_ice(tk):
  from math import exp
  a = 16288.
  b = 0.
  c = -9.34e-2
  alpeq = a/(tk*tk) + b/tk + c
  try:
    alpeq = exp(alpeq)          # Ensure exp(...) is in range
  except:
    alpeq = float("NaN")        # on exp error, return a NaN
    print "alphdo_ice: exp(alpeq) error!"
    print "alphdo_ice: tk,alpeq = ", tk,alpeq
  return alpeq
# Returns HDO equilibrium fractionation for HDO to liquid
# fractionation is the parameter alpha in paper
#
# Translated from IDL function alphdo_liq, tk
# tk is temperature Kelvin
def alphdo_liq(tk):
  from math import exp
  a = 24.844e+3
  b = -76.248
  c =  52.612e-3
  alpeq = a/(tk*tk) + b/tk + c
  try:
    alpeq = exp(alpeq)          # Ensure exp(...) is in range
  except:
    alpeq = float("NaN")        # on exp error, return a NaN
    print "alphdo_liq: exp(alpeq) error!"
    print "alphdo_liq: tk,alpeq = ", tk,alpeq
  return alpeq
# qsat.py from qsat.pro  .... CCD ....
# Computes saturation specific humidity from input pressure and temperature
# Saturation is taken from the well known simple formula in Rogers and Yau.
#
# Returned value is between 0 and 1.
#
# PRESSURE IN PASCAL
# TEMPERATURE IN KELVIN
#
# David Noone <dcn@colorado.edu> - Thu Jul 21 15:29:23 MDT 2005
#
def qsat(pressure,temperature) :

### CCD:: Function qsat(...) is only called from noone_curves.pro or python
### CCD:: equivalent, and there the two calls are:
### CCD:: 
### CCD::   qs =  1000*qsat(ps, tsrc)/v2m
### CCD:: where   ps = 1000.e2 and tsrc = 300. are both scalars
### CCD::   qfrz = 1000*qsat(65000., 263.0)/v2m
### CCD:: so qsat(...) is only ever called with scalar arguments.

  from math import exp  # Since exp() only gets applied to a scalar
  epsqs = 0.62197       # ratio of molecular weights
#
### CCD:: This eseq variable is totally local to qsat and looks like it just
### CCD:: selects a method of computing the result. eseq = 0 is never used.
# eseq = 0		# Rogers and Yau
  eseq = 1		# 10 pount empircal formula from CAM

  if eseq == 0 :   # CCD: It would appear this block is never executed.
# =======================================================================
# Set up coefficients for saturation vapour pressure
#
    tref = 273.0          # reference temperature (freezing ) K
    eref = 610.71         # es at reference temperature (Pa)
    cliq = 1.844e-4       # "c" factor for liquid
    cice = 1.629e-4       # "c" factor for ice
#
# Compute the saturation vapour pressure, and thus saturation mixing ratio
#
    cfac = cliq
### CCD::  The translation of where(temperature,...) depends on the
### CCD::  nature of temperture - is it a scalar ot an array?
### CCD::  i = where(temperature lt tref)

### CCD:: if (i[0] gt 0) then cfac(i) = cice
### CCD::  if i[0] > 0 : cfac(i) = cice
    if temperature < tref : cfac = cice
    es = (1.0/tref - 1.0/temperature) / cfac
    es = eref*exp(es)
# ===================== end block: if eseq == 0 =========================

  if eseq == 1 :
# =======================================================================
#
# This one as per CAM. Work in deg C. Better bahaved for crazy values.
#
    a0=6.107799961    
    a1=4.436518521e-01 ; a2=1.428945805e-02 ; a3=2.650648471e-04
    a4=3.031240396e-06 ; a5=2.034080948e-08 ; a6=6.136820929e-11

    b0=6.109177956    
    b1=5.034698970e-01 ; b2=1.886013408e-02 ; b3=4.176223716e-04
    b4=5.824720280e-06 ; b5=4.838803174e-08 ; b6=1.838826904e-10

    tc = temperature - 273.16

### CCD:: The nature of tc is same as temperature, since it is just shifted

### CCD::  The translation of where(tc,...) depends on the
### CCD::  nature of tc - is it a scalar ot an array?
### CCD::   i = where (tc gt 50. ) 
### CCD::  if (i[0] gt -1) then tc[i] = 50.
    if tc > 50. : tc = 50.

### CCD::  i = where (tc lt -50. ) 
### CCD::  if (i[0] gt -1) then tc[i] = -50.
### CCD::  if i[0] < -1 : tc[i] = -50.
    if tc < -50. : tc = -50.

### CCD::  What is this for?  es = tc		# array constructor
### CCD::  The translation of where(tc,...) depends on the
### CCD::  nature of tc - is it a scalar ot an array?
### CCD::  i = where (tc ge 0.) 
### CCD:: if (i[0] gt -1) then begin
### CCD::  es[i] = 100.*(a0+tc[i]*(a1+tc[i]*(a2+tc[i]*(a3+tc[i]*(a4+tc[i]*(a5+tc[i]*a6))))))
### CCD:: endif 
### CCD ::if i[0] > -1 :
    if tc >= 0:
      es = 100.*(a0+tc*(a1+tc*(a2+tc*(a3+tc*(a4+tc*(a5+tc*a6))))))

### CCD::  The translation of where(tc,...) depends on the
### CCD::  nature of tc - is it a scalar ot an array?
### CCD::  i = where (tc lt 0.) 
### CCD:: if (i[0] gt -1) then begin
### CCD::   es[i] = 100.*(b0+tc[i]*(b1+tc[i]*(b2+tc[i]*(b3+tc[i]*(b4+tc[i]*(b5+tc[i]*b6))))))
### CCD:: endif
### CCD::  if i[0] > -1 :
    if tc < 0:
      es = 100.*(b0+tc*(b1+tc*(b2+tc*(b3+tc*(b4+tc*(b5+tc*b6))))))
# ========================= end block: if eseq == 1 =====================

  qsat = epsqs*es/(pressure - es) # Convert to final form
  return qsat        #  humidity  = mixrat/qsat
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

from globals import *		

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
#### CCD::  Needs a lot of clarification .....
#####################################################################
### CCD:: Questions:
### CCD:: What is the variable called "i80" ????
### CCD:: What is the variable called "dum" ????
### CCD:: 
### CCD:: # if (n_elements(pcld) eq 0) then delp = 85000.
### CCD::   #***** CCD I think this is an error:
### CCD::   # if (n_elements(pcld) eq 0) then delp = 85000.
### CCD::   # It should assign value to pcld, not delp, as in:
### CCD::   # if (n_elements(pcld) eq 0) then pcld = 85000.
### CCD:: if 'pcld' not in globals():       pcld = 85000.
### CCD:: The original "noone_curves.pro" file seems to set not set pcld here
### CCD:: but to set delp to 85000, having just set delp to 0 in the previous
### CCD:: line. But maybe this is all moot, since everything seems to be set
### CCD:: explicitly. Maybe this piece of code that initializes things that
### CCD:: have never been set should just be eliminated. CCD ??????

#
# Plots the varierty of curves making up a "Noone diagram"
#
# This assumes you have already initialized a delta-q plot with axes in
# permil and VMR in mmol/mol (i.e., permil)
#
# INPUTS
#    tsrc	Temperature (K) of ocean source
#    q0		H2O vmr of dry end member
#    del0	delD of dry end member
#    delp=delp	delD of local precipitation/transpiration
#    hsrc=hsrc	humidity at evaporation source (sets dewpoint)
#    pcld=pcld	pressure at cloud level (Pa)
#    qmin=qmin	minimum H2O VMR for reevap curve
#    nn=nn	"Resolution" of curves (iterations)
#    eta=eta	kinetic fractionation (1 or 0.995 is defensibel)
#    /label	flag to add labels
#    /color	flag to make color (based on color table 40)
#
# OUTPUTS:
#    none
#
# EXAMPLE:
#
#  plot,[0,0],[0,0],/nodata, $
#     xrange=[0,38],xstyle=1,yrange=[-380,50],ystyle=1, $
#     xtitle='q (ppt)',ytitle='!9d!3 (permil)', $
#     charsize=1.3,xthick=2,ythick=2
#
#   nn   = 1000 
#   tsrc = 300. 
#   hsrc = 0.80 
#   q0   = 0.9 
#   del0 = -400.
#   delp = -30. 
#   eta  = 0.995
#   pcld = 85000.
#
#  noone_curves,tsrc,q0,del0,delp=delp,eta=eta,hsrc=hsrc,pcld=pcld, $
#         nn=nn,/color,/label
#
#  DEPENDENCIES:
#     (From David) QSAT,TSAT,ALPHDO_LIQ,ALPHDO_ICE,
#                  ISOMIXLINE,ISORAYSAT,ISOEQLSAT,
#     (Coyote library) SYMCAT
#
# David Noone <dcn@colorado.edu> - Mon Jul 27 09:52:07 MDT 2009
#
# ------------------------------------------------------------------------
###CCD:: pro noone_curves,tsrc,q0,del0,delp=delp,hsrc=hsrc,pcld=pcld, $
###CCD::          qmin=qmin,nn=nn,eta=eta,label=label,color=color

def noone_curves(tsrc,q0,del0):

# Keyword values assignment:
# delp=delp,hsrc=hsrc,pcld=pcld,qmin=qmin,nn=nn,eta=eta,label=label,color=color
# These should be handled in a simpler manner, probably by setting such
# things up in the file globals_iniits.py

  import sys         # Just to allow write to stderr, and exit ....
#
# Set defaults
#
  ps = 1000.e2			# approximate surface pressure
  v2m = (18./29.)                 # converts pptv to mixing ratio
#
# Check to see if variables are initialized, and if not do it here.
# CCD: If variable named XYZ is defined anywhere, it will be in globals()
# CCD: If we want to see if it is defined locally, change globals to locals
# CCD: This is to replace all the IDL if (n_elements(nn) eq 0) ...

  # List of variables that should have beeb assigned values
  must_be_set = ['del0','delp','eta','hsrc','nn','pcld', \
                  'ps','q0','qmin','tsrc','v2m']
  must_be_set.append('i80')     # i80 does not seem to be defined
  must_be_set.append('ifrz')    # ifrz does not seem to be defined
  count = 0
  for name in must_be_set:
    if name in globals():     # Check to see if each is defined somewhere
      count += 1
    else:
      sys.stderr.write("Variable %s without assigned value.\n" % name)
  if count < len(must_be_set):
    sys.stderr.write("Some variables have no initial values - exit!\n")
    sys.exit(1)

#
# Make a curve for evaporation
#
  dels = (1./alphdo_liq(tsrc) - 1)*1000.
  qs =  1000*qsat(ps, tsrc)/v2m	# source value (saturation specific humidity?)

### CCD::  isomixline,q0,del0,qs,dels,nn,eta,qh2oevap,deldevap

  (qh2oevap,deldevap) = isomixline(q0,del0,qs,dels,nn,eta)
#
# Mix between high latitude and tropical super-depleted points
# 
### CCD::  isomixline,q0,del0,qs,delp,nn,eta,qh2omix,deldmix

  (qh2omix,deldmix) = isomixline(q0,del0,qs,delp,nn,eta)
#
  dum = min(abs(qh2oevap/qs - hsrc), i80)
#
  q1 = qh2oevap[i80]
  del1 = deldevap[i80]

### CCD:: isoraysat,q1/1000.,del1,q0/1000.,nn,pcld, \
### CCD::                    qh2oray,deldray,qh2ocld,deldcld

  (qh2oray,deldray,qh2ocld,deldcld) = \
            isoraysat(q1/1000.,del1,q0/1000.,nn,pcld)
  qh2oray = qh2oray*1000.
  qh2ocld = qh2ocld*1000.
#
# Re-evaporation curve (maximum amount for 2 stage process)
#
### CCD::   eff = -1.0		# processed twice (reevaporation)
### CCD::   isoraysat,q1/1000.,del1,qmin/1000,nn,pcld,qh2orev,deldrev,qh2ocld2,deldcld2,eff=eff
  (qh2orev,deldrev,qh2ocld2,deldcld2) = \
          isoraysat(q1/1000.,del1,qmin/1000,nn,pcld,eff=-1.0)

  qh2orev = qh2orev*1000.
  qh2ocld2= qh2ocld2*1000.

#
# Closed system, as per pseudo adiabatic process
#
### CCD::  isoeqlsat,q1/1000.,del1,q1/1000.,nn,pcld,qh2oeql,deldeql
  (qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q1/1000.,nn,pcld)

  qh2oeql = qh2oeql*1000.

#
# A bit of rayleigh from the freezing point
#
  qfrz = 1000*qsat(65000., 263.0)/v2m
  dum = min(abs(qh2oeql - qfrz), ifrz)

### CCD::  isoraysat,qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000., \
                 nn,pcld,qh2oice,deldice,qh2osno,deldsno
  (qh2oice,deldice,qh2osno,deldsno) = \
         isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000.,nn,pcld)

  qh2oice = qh2oice*1000.

''' ************ if IDL_Plot: ***** The Rest of the File ***********
#
# Draw the lines
#

#  oplot,qh2oevap,deldevap,color=icol_evp,thick=mthk
#  if keyword_set(label) then $
#      xyouts,12,-94,"Mixing to ocean (evaporation)",orient=3.,charsize=0.8,color=icol_evp

#  oplot,qh2omix, deldmix,color=icol_evp,thick=mthk,linestyle=2
#  if keyword_set(label) then $
#      xyouts,15,-30,"Mixing to land source",orient=3.,charsize=0.8,color=icol_evp


#  oplot,qh2oeql ,deldeql ,color=icol_ray,thick=mthk,linestyle=5
#  if keyword_set(label) then $
#      xyouts,4.5,-165,"Moist adiabatic (f=0)",orient=15.,charsize=0.8,color=icol_ray

#  oplot,qh2oray ,deldray ,color=icol_ray,thick=mthk
#  if keyword_set(label) then begin
#      xyouts,8,-240,"Pseudoadiabatic (f=1)",orient=28.,charsize=0.8,color=icol_ray
#      xyouts,8,-260,"   (Rayleigh)",orient=28.,charsize=0.8,color=icol_ray
#  endif

  oplot,qh2oice ,deldice ,color=icol_ray,thick=mthk,linestyle=2
#  if keyword_set(label) then begin
#      xyouts,6,-310,"Ice condensation",orient=0,charsize=0.8,color=icol_ray
#      xyouts,6,-330,"   (Rayleigh)",orient=0,charsize=0.8,color=icol_ray
#      arrow,5.8,-300,2.8,-260,/data,thick=2
#  endif

  oplot,qh2orev ,deldrev ,color=icol_rev,thick=mthk
#  if keyword_set(label) then begin
#      xyouts,14,-260,"Remoistening (f=2)",orient=38.,charsize=0.8,color=icol_rev
#      xyouts,14,-290,"     (super-Rayleigh)",orient=38.,charsize=0.8,color=icol_rev
#  endif


  if (keyword_set(label)) then begin
    xyouts,5,-208,"(0<f<1)",orient=21.,charsize=0.8,color=icol_ray

    oplot,[0,200],[0,0],thick=2
    xyouts,4.3,7,'SMOW',charsize=0.6

    oplot,[qfrz,qfrz],[-1000,1000],thick=2,linestyle=2
    xyouts,2.7,-5,'Frost point',orient=-90.,charsize=0.6
    xyouts,1.7,-12,'(T=263K)',orient=-90.,charsize=0.6


    oplot,[qs,qs],[dels,dels],psym=1
    xyouts,qs-5,-115,"q!LS!N,!9d!3!LS!N",charsize=1.0

    oplot,[q0,q0],[del0,del0],psym=1,symsize=0.5
    oplot,[1,1],[-360,-360],psym=1
    xyouts,1,-350,"q!L0!N,!9d!3!L0!N",charsize=1.0

    xyouts,29,-102,'RH=80%', orient=-55,charsize=0.6

  endif
'''
