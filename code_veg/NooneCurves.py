### Translated IDL --> Python - CCD January, 2021

# Some global imports, keyword values, global variable values

import numpy as np
import matplotlib.pyplot as plt
import sys         # Just to allow write to stderr, and exit ....
import xarray as xr

dump_parms = True  # set to False to prevent parameter dump at end

plot_file = '/Users/ellendyer/Documents/GitHub/Isotopes_F4R/plots/plot_noone_curves.png'    # default file name for plots

hdo=True
h218o=False
conventional=True
eff=False
noice=False
tfreeze=False
vh2ovhdo=False

# Some initial values for testing
del0 = -400.    # Try -360 ....
delp = -30. 
eta  = 0.995
hsrc = 0.80 
nn   = 1000     # It needs to be this large to get precision in the searches
pcld = 85000.
ps = 1000.e2                    # approximate surface pressure
q0   = 0.9 
qmin = 11.
tsrc = 300. 

#### ========== Function = alphdo_ice(...)
# Returns HDO equilibrium fractionation for HDO to ice
# fractionation is the parameter alpha in paper
# Translated from IDL function alphdo_ice, tk
# tk is temperature Kelvin
def alphdo_ice(tk):
  from math import exp   # This will also require sys somewhere
  a = 16288.
  b = 0.
  c = -9.34e-2
  alpeq = a/(tk*tk) + b/tk + c
  try:
    alpeq = exp(alpeq)          # Ensure exp(...) is in range
  except:
    alpeq = float("NaN")        # on exp error, return a NaN
    sys.stderr.write("alphdo_ice: exp(alpeq) error!\n")
    sys.stderr.write("alphdo_ice: tk,alpeq = %g , %g\n" %(tk,alpeq))
  return alpeq

#### ========== Function = alphdo_liq(...)
# Returns HDO equilibrium fractionation for HDO to liquid
# fractionation is the parameter alpha in paper
# Translated from IDL function alphdo_liq, tk
# tk is temperature Kelvin
def alphdo_liq(tk):
  from math import exp   # This will also require sys somewhere
  a = 24.844e+3
  b = -76.248
  c =  52.612e-3
  alpeq = a/(tk*tk) + b/tk + c
  try:
    alpeq = exp(alpeq)          # Ensure exp(...) is in range
  except:
    alpeq = float("NaN")        # on exp error, return a NaN
    sys.stderr.write("alphdo_liq: exp(alpeq) error!\n")
    sys.stderr.write("alphdo_liq: tk,alpeq = %g , %g\n" %(tk,alpeq))
  return alpeq

#### ========== Function = qsat(...)
# qsat.py from qsat.pro  .... CCD ....
# Computes saturation specific humidity from input pressure and temperature
# Saturation is taken from the well known simple formula in Rogers and Yau.
# Returned value is between 0 and 1.
# PRESSURE IN PASCAL
# TEMPERATURE IN KELVIN
# David Noone <dcn@colorado.edu> - Thu Jul 21 15:29:23 MDT 2005
#
def qsat(pressure,temperature) :
  from math import exp  # Since exp() only gets applied to a scalar
  epsqs = 0.62197       # ratio of molecular weights
#
# eseq = 0              # Rogers and Yau - Never used here - CCD
  eseq = 1              # 10 pount empircal formula from CAM

  if eseq == 0 :   # CCD: It would appear this block is never executed.
# Set up coefficients for saturation vapour pressure
    tref = 273.0          # reference temperature (freezing ) K
    eref = 610.71         # es at reference temperature (Pa)
    cliq = 1.844e-4       # "c" factor for liquid
    cice = 1.629e-4       # "c" factor for ice
#
# Compute the saturation vapour pressure, and thus saturation mixing ratio
#
    if temperature < tref : cfac = cice   # choose ice or liquid
    else: cfac = cliq
    es = (1.0/tref - 1.0/temperature) / cfac
    es = eref*exp(es)
# ===================== end block: if eseq == 0 =========================

  if eseq == 1 :
# This one as per CAM. Work in deg C. Better bahaved for crazy values.
#
    a0=6.107799961    
    a1=4.436518521e-01 ; a2=1.428945805e-02 ; a3=2.650648471e-04
    a4=3.031240396e-06 ; a5=2.034080948e-08 ; a6=6.136820929e-11

    b0=6.109177956    
    b1=5.034698970e-01 ; b2=1.886013408e-02 ; b3=4.176223716e-04
    b4=5.824720280e-06 ; b5=4.838803174e-08 ; b6=1.838826904e-10

    tc = temperature - 273.16
    if tc > 50. : tc = 50.      # Force tc to be in [-50,+50]
    if tc < -50. : tc = -50.

    if tc >= 0:                 # Select correct expression for es
      es = 100.*(a0+tc*(a1+tc*(a2+tc*(a3+tc*(a4+tc*(a5+tc*a6))))))
    if tc < 0:
      es = 100.*(b0+tc*(b1+tc*(b2+tc*(b3+tc*(b4+tc*(b5+tc*b6))))))
# ========================= end block: if eseq == 1 =====================

  qsat = epsqs*es/(pressure - es) # Convert to final form
  return qsat        #  humidity  = mixrat/qsat

#### ========== Function = tsat(...)
#  Finds the (dewpoint) temperature given a saturated mass mixing ratio
#  (i.e., works backwards along the Clausias curve)
#  
#  PRESSURE IN PA
#  MIXING RATIO IN kg/kg
#  
#  David Noone <dcn@colorado.edu> - Sun Mar  2 09:42:31 MST 2008
# Translated from IDL function tsat,pressure,qsat
def tsat(pressure,qsat):
  from math import log   # This will also require sys somewhere

  epsqs = 0.62197                   # ratio of molecular weights
  esat = pressure/(epsqs/qsat + 1)  # Convert mixing ratio to evapor presure
  try:                              # Ensure log(...) is in range
    loge = log(esat/611.2)      # Use the empirical formula to get dewpoint
  except:
    loge = float("NaN")        # on log error, return a NaN
    sys.stderr.write("tsat: log(esat/611.2) error!\n")
    sys.stderr.write("tsat: pressure,qsat = %g , %g\n" % (pressure,qsat))
  tsat = 243.5*loge/(17.67 - loge) + 273.16     # in K
  return tsat

#### ========== Function = isoeqlsat(...)
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

def isoeqlsat(q0,del0,q1,npts,pressure, \
              hdo=hdo,h218o=h218o,conventional=conventional):
# arrays qh2o and deld are returned and are available in caller through
#    (qh2o,deld) = isoeqlsat(q0,del0,q1,npts,pressure)

# Set the species (HDO by default)
#
  ispec = 0
  if hdo : ispec = 0
  if h218o : ispec = 1

#
# Set initial ratio from delta value
#
  if conventional:
    rat0 = del0/1000. + 1.                      # APPROXIMATE form
  else:
    rat0 = np.exp(del0/1000.)                   # LOG form
#
# Set up integration evolution - log variation in q
#
  qh2o = np.exp(np.log(q0) + np.log(q1/q0)*np.arange(npts,dtype=float)/(npts))

  qhdo = np.zeros(npts)   # just allocating an array(npts)

  qhdo[0] = rat0*q0          # Set value for first element
  for n in range(1,npts):    # Now build subsequent elements ...
#
# Get the dew point temperature
#
    qsat = 0.5*(qh2o[n-1] + qh2o[n])
    ttsat = tsat(pressure,qsat)
# NB: in IDL code it was tsat = tsat(...) but this cannot be used in
# Python where names are unique. I changed variable tsat to ttsat - CCD
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
    deld = (qhdo/qh2o - 1.)*1000.                       # APPROXIMATE form
  else:
    deld = np.log(qhdo/qh2o)*1000.                      # LOG form
  return (qh2o,deld)                      # return the two allocated arrays.

#### ========== Function = isomixline(...)
#
# Makes delD values (etc) under a mixing line assumtion (evaporation, etc)
#
# Works internally with HDO (isotope) specific humidity, and converts at 
# the end for output. Assumes discretization in 1/q for pretty plotting.
#
# David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
#

def isomixline(q0,del0,qs,dels,npts,eta,conventional=conventional):
# arrays qh2o and deld are returned and are available in caller through
#    (qh2o,deld) = isoeqlsat(q0,del0,q1,npts,pressure)
#
# Set initial ratios from input delta values
#
  if conventional:
    rat0 = del0/1000. + 1.                      # APPROXIMATE form
    rats = dels/1000. + 1.                      # APPROXIMATE form
  else:
    rat0 = np.exp(del0/1000.)                   # LOG form
    rats = np.exp(dels/1000.)                   # LOG form
#
# Set range of q values
#
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
# Finalize for output
#
  if conventional:
    deld = (qhdo/qh2o - 1.)*1000.                       # APPROXIMATE form
  else:
    deld = np.log(qhdo/qh2o)*1000.                      # LOG form
  return (qh2o,deld)                  # return the two allocated arrays.

#### ========== Function = isoraysat(...)
#
# Makes delD values (etc) under a rayleigh distillation
#
# Works internally with HDO of H218O (isotope) specific humidity, and converts
# at the end for output. Assumes discretization in log q for pretty plotting.
#
# This version takes alpha based on saturation (dewpoint) temperature.
# given the mixing ratio.
#  MIXING RATIO IN kg/kg
#  PRESSURE IN Pa
# This must be done setpwise along history to get temperature effect on alpha.
# David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
#

def isoraysat(q0,del0,q1,npts,pressure,hdo=hdo,h218o=h218o,eff=eff, \
      noice=noice,conventional=conventional,tfreeze=tfreeze,vh2ovhdo=vh2ovhdo):
# arrays qh2o,deld,rh2o,rdel are returned and are available in caller through
#    (qh2o,deld,rh2o,rdel) = isoraysat(q0,del0,q1,npts,pressure)
# If vh2ovhdo is True then array vdel can be obtained using
#    (qh2o,deld,rh2o,rdel,vdel) = isoraysat(q0,del0,q1,npts,pressure)


#
# Set freezing transition
#
  tfrz = 273.16
  if tfreeze : tfrz = tfreeze  # different tfrz passed in as tfreeze=value 
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
     rat0 = del0/1000. + 1.                     # conventional form
  else:
     rat0 = np.exp(del0/1000.)                  # LOG form

  qh2o = np.exp(np.log(q0) + np.log(q1/q0)*np.arange(npts,dtype=float)/npts)

  qhdo = np.zeros(npts)   # just allocating an array of npts zeros

  qhdo[0] = rat0*q0       # CCD: assign value to first element of qhdo
#
# Also save off the mass and composition of the preciptation
#
  rh2o = np.zeros(npts)   # just allocating an array(npts)
  rhdo = np.zeros(npts)   # just allocating an array(npts)
  if vh2ovhdo:
    vh2o = np.zeros(npts)   # just allocating an array(npts)
    vhdo = np.zeros(npts)   # just allocating an array(npts)
#
# Loop over points
#
# build rest of array after qhdo[0] which was assigned above
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
      if ispec == 0:              # Choose HDO alpha function
        alpha = alphdo_liq(ttsat)
      if ispec == 1:              # Choose H218O alpha function
        alpha = alp18o_liq(ttsat)
    else:                         # Choose ice alpha functions
      if ispec == 0:              # Choose HDO alpha function
        alpha = alphdo_ice(ttsat)
      if ispec == 1:              # Choose H218O alpha function
        alpha = alp18o_ice(ttsat)
    alpeq = alpha
#
# Make a correction for "eff" if optional eff is not False, but has a
# value. # (as per Noone, TES HUM, 2008)
#   
    if eff :      # NB: eff is passed as eff=value in function call
      f = eff
#     alpha = alpha / (alpha*(1.0-f) + f)       # fraction vapor CCD=??
      alpha = alpha / (f*(alpha-1.) + 1.)       # fraction retained
#
    qhdo[n] = qhdo[n-1]*(qh2o[n]/qh2o[n-1])**alpha
#
# Save the rain, i.e., the change
#
    rh2o[n] = qh2o[n-1] - qh2o[n]               # each increment
    rhdo[n] = qhdo[n-1] - qhdo[n]               # each increment
#;    rh2o[n] = qh2o[0] - qh2o[n]               # total - ever used?
#;    rhdo[n] = qhdo[0] - qhdo[n]               # total - ever used?
#
# Optionally output just the vapor (for f/=1)
#
  if vh2ovhdo and eff :
    vh2o[n] = (1-f)*qh2o[n]
    vhdo[n] = qhdo[n]/(1+alpeq*f/(1-f))
### end of for n in range(1,npts):      # Now build subsequent
#
# No rain in the zeroth step, so trim the array
#
  rh2o = rh2o[1:npts-1]
  rhdo = rhdo[1:npts-1]
#
# Put into final form for deta values
#
  if conventional:
    deld = (qhdo/qh2o - 1.)*1000.               # APPROXIMATE form
    rdel = (rhdo/rh2o - 1.)*1000.               # APPROXIMATE FORM (rain)
    if vh2ovhdo :
      vdel = (vhdo/vh2o - 1.)*1000.             # APPROXIMATE FORM (vapor only)
  else:
    deld = np.log(qhdo/qh2o)*1000.              # LOG form
    rdel = np.log(rhdo/rh2o)*1000.              # LOG form (rain)
    if vh2ovhdo :
      vdel = np.log(vhdo/vh2o)*1000.            # LOG form (vapor only)

  if vh2ovhdo:    # only if vdel (from vh2o,vhdo) needed
    return (qh2o,deld,rh2o,rdel,vdel)
  else :
    return (qh2o,deld,rh2o,rdel)

#### ========== Function = noone_curves(...)
#
# Plots the varierty of curves making up a "Noone diagram"
# This assumes you have already initialized a delta-q plot with axes in
# permil and VMR in mmol/mol (i.e., permil)
#
# INPUTS
#    tsrc       Temperature (K) of ocean source
#    q0         H2O vmr of dry end member
#    del0       delD of dry end member
#    delp=delp  delD of local precipitation/transpiration
#    hsrc=hsrc  humidity at evaporation source (sets dewpoint)
#    pcld=pcld  pressure at cloud level (Pa)
#    qmin=qmin  minimum H2O VMR for reevap curve
#    nn=nn      "Resolution" of curves (iterations)
#    eta=eta    kinetic fractionation (1 or 0.995 is defensibel)
#    /label     flag to add labels
#    /color     flag to make color (based on color table 40)
#
# OUTPUTS: none
#
# EXAMPLE: Still in IDL ... CCD
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

def noone_curves(tsrc,q0,del0):

# Keyword values assignment:
# delp=delp,hsrc=hsrc,pcld=pcld,qmin=qmin,nn=nn,eta=eta,label=label,color=color
# These should be handled in a simpler manner, probably by setting such
# things up in a file such as globals_iniits.py
#
# Set defaults
#
  ps = 1000.e2          # approximate surface pressure - CCD - Why set it here?
  v2m = (18./29.)       # converts pptv to mixing ratio
#
# Check to see if variables are initialized, and if not do it here.
# CCD: If variable named XYZ is defined anywhere, it will be in globals()
# CCD: This is to replace all the IDL if (n_elements(nn) eq 0) ...

  # List of variables that should have been assigned values
  must_be_set = ['del0','delp','eta','hsrc','nn','pcld','ps','q0','qmin','tsrc']
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
  qs =  1000*qsat(ps, tsrc)/v2m # source value (saturation specific humidity?)

  (qh2oevap,deldevap) = isomixline(q0,del0,qs,dels,nn,eta)
#
# Mix between high latitude and tropical super-depleted points
# 
  (qh2omix,deldmix) = isomixline(q0,del0,qs,delp,nn,eta)
#
# Find the location of the minimum element in the vector qh2oevap/qs - hsrc
# which gives the location in the vector qh2oevap/qs that is closest to
# hsrc in value. Assuming hsrc = 0.8 (80% RH) this will be the location of
# the 80% relative humidity point along this curve in the Noone diagram.

  i80 = np.argmin(np.abs(qh2oevap/qs - hsrc))
#
  q1 = qh2oevap[i80]
  del1 = deldevap[i80]

  (qh2oray,deldray,qh2ocld,deldcld) = \
            isoraysat(q1/1000.,del1,q0/1000.,nn,pcld)
  qh2oray = qh2oray*1000.
  qh2ocld = qh2ocld*1000.
#
# Re-evaporation curve (maximum amount for 2 stage process)
#
  (qh2orev,deldrev,qh2ocld2,deldcld2) = \
          isoraysat(q1/1000.,del1,qmin/1000,nn,pcld,eff=-1.0)
  qh2orev = qh2orev*1000.
  qh2ocld2= qh2ocld2*1000.
#
# Closed system, as per pseudo adiabatic process
#
# CCD: In original IDL code arg-1 and arg-3 were both q1/1000. -- Wrong!
# CCD: Change arg-3 to q0/1000.
  (qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q0/1000.,nn,pcld)
  qh2oeql = qh2oeql*1000.
#
# A bit of rayleigh from the freezing point
#
  qfrz = 1000*qsat(65000., 263.0)/v2m

# Find the location of the minimum element in the vector qh2oeql - qfrz
# which give the location in the vector qh2oeql that is closest to
# qfrz in value. This will be the location of where the pressure and
# temperature become 65000., 263.0 respectively

  ifrz = np.argmin(np.abs(qh2oeql - qfrz))

# CCD: In original IDL code arg-3 was q1/1000. This was wrong, since the
# CCD: curve is supposed to go from freezing down. Change arg-3 to q0/1000.
  (qh2oice,deldice,qh2osno,deldsno) = \
       isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q0/1000.,nn,pcld)
  qh2oice = qh2oice*1000.

  # Try some Matplotlib plots:

  plt.xlabel('q (mmol/mol)')

  plt.ylabel(r'$ \delta (o/oo) $')

#  # Plot vertical line where q --> q0
#  plt.plot([q0,q0],[-400.0,0.0],color='black',linestyle='dashed')
#
#  # Plot vertical line where q --> qfrz
#  plt.plot([qfrz,qfrz],[-400.0,0.0],color='black',linestyle='dashed')
#
#  # Plot vertical line where q --> q at 80% RH
#  plt.plot([q1,q1],[-400.0,0.0],color='black',linestyle='dashed')

  # Noone paper colour: Orange Solid
  # plt.plot(qh2oevap,deldevap,'-.y')
  plt.plot(qh2oevap,deldevap,color='teal',linestyle='solid',label='Mixing - Ocean Source')

  # Noone paper colour: Orange Dashed
  plt.plot(qh2omix,deldmix,color='teal',linestyle='dashed',label='Mixing - Transpiration Source')

  # Noone paper colour: Cyan Long-dashed
  plt.plot(qh2oeql,deldeql,color='black',linestyle='dashdot',label='Reversible moist adiabatic')

  # Noone paper colour: Cyan Solid
  plt.plot(qh2oray,deldray,color='black',linestyle='solid',label='Removal of water (Rayleigh)')

  # Noone paper colour: Cyan Dashed
  plt.plot(qh2oice,deldice,color='black',linestyle='dashed')

  # Noone paper colour: Magenta Solid
  plt.plot(qh2orev,deldrev,color='orange',linestyle='solid',label='Re-evaporation')
  


