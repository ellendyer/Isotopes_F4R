;+
;
; Computes saturation specific humidity from input pressure and temperature
;
; Saturation is taken from the well known simple formula in Rogers and Yau.
;
; Returned value is between 0 and 1.
;
;
; PRESSURE IN PASCAL
; TEMPERATURE IN KELIN
;
;
; David Noone <dcn@colorado.edu> - Thu Jul 21 15:29:23 MDT 2005
;
;
function qsat,pressure,temperature
  epsqs = 0.62197       ; ratio of molecular weights
;
; Falg which equation to use
;
;eseq = 0		; Rogers and Yau
eseq = 1		; 10 pount empircal formula from CAM


if (eseq eq 0) then begin
;;;
;;; Set up coefficients for saturation vapour pressure
;;;
  tref = 273.0          ; reference temperature (freezing ) K
  eref = 610.71         ; es at reference temperature (Pa)
  cliq = 1.844e-4       ; "c" factor for liquid
  cice = 1.629e-4       ; "c" factor for ice
;;;
;;; Compute the saturation vapour pressure, and thus saturation mixing ratio
;;;
  cfac = cliq
  i = where(temperature lt tref)
  if (i[0] gt 0) then cfac(i) = cice
  es = (1.0/tref - 1.0/temperature) / cfac
  es = eref*exp(es)

endif


if (eseq eq 1) then begin
;
; This one as per CAM. Work in deg C.
; Better bahaved for crazy values.
;
  a0=6.107799961    
  a1=4.436518521e-01
  a2=1.428945805e-02
  a3=2.650648471e-04
  a4=3.031240396e-06
  a5=2.034080948e-08
  a6=6.136820929e-11

  b0=6.109177956    
  b1=5.034698970e-01
  b2=1.886013408e-02
  b3=4.176223716e-04
  b4=5.824720280e-06
  b5=4.838803174e-08
  b6=1.838826904e-10

  tc = temperature - 273.16

  i = where (tc gt 50. ) 
   if (i[0] gt -1) then tc[i] = 50.
  i = where (tc lt -50. ) 
   if (i[0] gt -1) then tc[i] = -50.
        

  es = tc		; array constructor
  i = where (tc ge 0.) 
  if (i[0] gt -1) then begin
   es[i] = 100.*(a0+tc[i]*(a1+tc[i]*(a2+tc[i]*(a3+tc[i]*(a4+tc[i]*(a5+tc[i]*a6))))))
  endif 

  i = where (tc lt 0.) 
  if (i[0] gt -1) then begin
    es[i] = 100.*(b0+tc[i]*(b1+tc[i]*(b2+tc[i]*(b3+tc[i]*(b4+tc[i]*(b5+tc[i]*b6))))))
  endif
endif
;
; Convert to final form
;
  qsat = epsqs*es/(pressure - es)
;
;;  humidity  = mixrat/qsat
;
  return, qsat
end

