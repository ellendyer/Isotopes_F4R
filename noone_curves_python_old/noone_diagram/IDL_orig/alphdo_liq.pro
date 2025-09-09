;+
; Returns HDO equilibrium fractionation for HDO to liquid
;
function alphdo_liq, tk
  a = 24.844e+3
  b = -76.248
  c =  52.612e-3
  alpeq = a/(tk*tk) + b/tk + c
  alpeq = exp(alpeq)
  return, alpeq
end

