;+
;
; Finds the (dewpoint) temperature given a saturated mass mixing ratio
; (i.e., works backwards along the Clausias curve)
;
; PRESSURE IN PA
; MIXING RATIO IN kg/kg
;
;
; David Noone <dcn@colorado.edu> - Sun Mar  2 09:42:31 MST 2008
;
;
function tsat,pressure,qsat
  epsqs = 0.62197       ; ratio of molecular weights
;
; Convert mixing ratio to evapor presure
;
  esat = pressure/(epsqs/qsat + 1)
;
; Use the empirical formula to get dewpoint
;
  loge = alog(esat/611.2)
  tsat = 243.5*loge/(17.67 - loge) + 273.16	; in K

  return, tsat
end

