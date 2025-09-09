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
