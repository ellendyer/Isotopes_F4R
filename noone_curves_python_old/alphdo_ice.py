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
