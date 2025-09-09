;+
;
; Makes delD values (etc) under a comple equillibrium (closed system)
;
; Works internally with HDO (isotope) specific humidity, and converts at 
; the end for output. Assumes discretization in log q for pretty plotting.
;
; This version takes alpha based on saturation (dewpoint) temperature.
; given the mixing ratio.
;
;  MIXING RATIO IN kg/kg
;  PRESSURE IN Pa
;
;
; This this mist be done setpwise along the history.
;
;
; David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
;
pro isoeqlsat, q0,del0,q1,npts,pressure,qh2o,deld,  $
         hdo=hdo,h218o=h218o,conventional=conventional

;
; Set the species (HDO by default)
;
  ispec = 0
  if (keyword_set(HDO)) then ispec = 0
  if (keyword_set(H218O)) then ispec = 1

   
;
; Set initial ratio from delta value
;
  if (keyword_set(conventional)) then begin
    rat0 = del0/1000. + 1.			; APPROXIMATE form
  endif else begin
    rat0 = exp(del0/1000.)			; LOG form
  endelse


;
; Set up integration evolution - log variation in q
;
  qh2o = exp(alog(q0) + alog(q1/q0)*findgen(npts)/npts)

  qhdo = fltarr(npts)
  qhdo[0] = rat0*q0
  for n = 1, npts-1 do begin
;
; Get the dew point temperature
;
    qsat = 0.5*(qh2o[n-1] + qh2o[n])
    tsat = tsat(pressure,qsat)
;
; Get the fractionation factor: Must ALWAYS be liquid
;
    case ispec of
      0: alpeq = alphdo_liq(tsat)
      1: alpeq = alp18o_liq(tsat)
    endcase

    qhdo[n] = qhdo[0]/(alpeq*(qh2o[0]/qh2o[n] - 1.) + 1.)
  endfor

;
; Convert output to delta
;
  if (keyword_set(conventional)) then begin
    deld = (qhdo/qh2o - 1)*1000.			; APPROXIMATE form
  endif else begin
    deld = alog(qhdo/qh2o)*1000.			; LOG form
  endelse
  return

end
