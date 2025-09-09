;### Some conversion from IDL to Python done - see CCD ....
;+
;
; Makes delD values (etc) under a rayleigh distillation
;
; Works internally with HDO of H218O (isotope) specific humidity, and converts at 
; the end for output. Assumes discretization in log q for pretty plotting.
;
; This version takes alpha based on saturation (dewpoint) temperature.
; given the mixing ratio.
;
;  MIXING RATIO IN kg/kg
;  PRESSURE IN Pa
;
;
; This this mist be done setpwise along the history to get the temperature effect on alpha.
;
;
; David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
;
pro isoraysat, q0,del0,q1,npts,pressure,qh2o,deld,rh2o,rdel, $
         hdo=hdo,h218o=h218o,eff=eff,vaph2o=vh2o,vapdel=vdel,noice=noice, $
         conventional=conventional,tfreeze=tfreeze

;
; Set freezing transition
;
  tfrz = 273.16
  if (keyword_set(tfreeze)) then tfrz = tfreeze
;
; Set the species (HDO by default)
;
  ispec = 0
  if (keyword_set(HDO)) then ispec = 0
  if (keyword_set(H218O)) then ispec = 1

;
; Set initial ratio given the input delta value
;
  if (keyword_set(conventional)) then begin
     rat0 = del0/1000. + 1.			; conventional form
  endif else begin
     rat0 = exp(del0/1000.)			; LOG form
  endelse

  ; CCD:: qh2o = exp(alog(q0) + alog(q1/q0)*findgen(npts)/npts)
  ; CCD fair replacement, better to give dtype explicitly
  ; CCD change alog() to np.log()   natural logarithms
  qh2o = exp(np.log(q0) + np.log(q1/q0)*np.arange(npts,dtype=float)/(npts-1)

  ; CCD:: qhdo = fltarr(npts)
  ;CCD replace with qhdo = np.zreos(npts)   # just allocating an array(npts)
  qhdo = np.zreos(npts)   # just allocating an array(npts)

  qhdo[0] = rat0*q0
;
; Also save off the mass and composition of the preciptation
;
  ; CCD change fltarr() to np,zeros() ....
  ; CCD:: rh2o = fltarr(npts)
  rh2o = np.zeros(npts)
  ; CCD:: rhdo = fltarr(npts)
  rhdo = np.zeros(npts)

  ; CCD:: vh2o = fltarr(npts)
  vh2o = np.zeros(npts)
  ; CCD:: vhdo = fltarr(npts)
  vhdo = np.zeros(npts)
;
; Loop over points
;
  for n = 1, npts-1 do begin
;
; Get the dew point temperature
;
    qsat = 0.5*(qh2o[n-1] + qh2o[n])
    tsat = tsat(pressure,qsat)
;
; Get the fractionation factor, to ice if needed
;
    if (tsat gt tfrz or keyword_set(NOICE)) then begin
      case ispec of
       0: alpha = alphdo_liq(tsat)
       1: alpha = alp18o_liq(tsat)
      endcase
    endif else begin
      case ispec of
       0: alpha = alphdo_ice(tsat)
       1: alpha = alp18o_ice(tsat)
      endcase
    endelse
    alpeq = alpha
;
; Make a correction for "eff" if optional eff exists
; (as per Noone, TES HUM, 2008)
;   
    if (keyword_set(eff)) then begin
        f = eff			; not if eff = 0, then if = false
;        alpha = alpha / (alpha*(1.0-f) + f)	; fraction vapor
        alpha = alpha / (f*(alpha-1.) + 1.)	; fraction retained
    endif

;
    qhdo[n] = qhdo[n-1]*(qh2o[n]/qh2o[n-1])**alpha
;
; Save the rain, i.e., the change
;
    rh2o[n] = qh2o[n-1] - qh2o[n]		; each increment
    rhdo[n] = qhdo[n-1] - qhdo[n]		; each increment

;;    rh2o[n] = qh2o[0] - qh2o[n]		; total
;;    rhdo[n] = qhdo[0] - qhdo[n]		; total


;
; Optionally output just the vapor (for f/=1)
;
   if (keyword_set(vh2o) and keyword_set(eff)) then begin
     vh2o[n] = (1-f)*qh2o[n]
     vhdo[n] = qhdo[n]/(1+alpeq*f/(1-f))
   endif

  endfor
;
; No rain in the zeroth step, so trim the array
;
  rh2o = rh2o[1:npts-1]
  rhdo = rhdo[1:npts-1]
;
; Put into final form for deta values
;

  if (keyword_set(CONVENIONAL)) then begin
    deld = (qhdo/qh2o - 1.)*1000.			; APPROXIMATE form
    rdel = (rhdo/rh2o - 1.)*1000.			; APPROXIMATE FORM (rain)
    vdel = (vhdo/vh2o - 1.)*1000.			; APPROXIMATE FORM (vapor only)
  endif else begin
    deld = alog(qhdo/qh2o)*1000.			; LOG form
    rdel = alog(rhdo/rh2o)*1000.			; LOG form (rain)
    vdel = alog(vhdo/vh2o)*1000.			; LOG form (vapor only)
  ; CCD change alog() to np.log()   natural logarithms
    deld = np.log(qhdo/qh2o)*1000.			; LOG form
    rdel = np.log(rhdo/rh2o)*1000.			; LOG form (rain)
    vdel = np.log(vhdo/vh2o)*1000.			; LOG form (vapor only)
  endelse
  return
end
