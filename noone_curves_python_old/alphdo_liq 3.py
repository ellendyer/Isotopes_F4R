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
