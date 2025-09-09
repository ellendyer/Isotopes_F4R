;+
; Returns HDO equilibrium fractionation for HDO to ice
;
function alphdo_ice, tk
  a = 16288.
  b = 0.
  c = -9.34e-2
  alpeq = a/(tk*tk) + b/tk + c
  alpeq = exp(alpeq)
  return, alpeq
end

