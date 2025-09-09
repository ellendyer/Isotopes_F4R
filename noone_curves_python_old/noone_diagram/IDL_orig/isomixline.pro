;+
;
; Makes delD values (etc) under a mixing line assumtion (evaporation, etc)
;
;
; Works internally with HDO (isotope) specific humidity, and converts at 
; the end for output. Assumes discretization in 1/q for pretty plotting.
;
; David Noone <dcn@colorado.edu> - Wed Dec 19 15:57:05 MST 2007
;
pro isomixline, q0,del0,qs,dels,npts,eta,qh2o,deld,conventional=conventional

;
; Set initial ratios from input delta values
;
  if (keyword_set(conventional)) then begin
    rat0 = del0/1000. + 1.			; APPROXIMATE form
    rats = dels/1000. + 1.			; APPROXIMATE form
  endif else begin
    rat0 = exp(del0/1000.)			; LOG form
    rats = exp(dels/1000.)			; LOG form
  endelse

;
; Set range of q values
;
  qh2o = (1/q0 + (1/qs-1/q0)*findgen(npts)/(npts-1))^(-1)
;
; Set the (evolving) flux factor
;
  hfac = (rats*qs - rat0*q0)/(qs-q0)^eta
;
; Solve the Noone equation
;
  qhdo = rats*qs - hfac*(qs - qh2o)^eta
;
; This will fail with a div zero for the end memeber, so overwrite by hand
;
  qh2o[npts-1] = qs
  qhdo[npts-1] = qs*rats
;
; Finalize for ourput
;
  if (keyword_set(conventional)) then begin
    deld = (qhdo/qh2o - 1.)*1000.			; APPROXIMATE form
  endif else begin
    deld = alog(qhdo/qh2o)*1000.			; LOG form
  endelse
  return
end
