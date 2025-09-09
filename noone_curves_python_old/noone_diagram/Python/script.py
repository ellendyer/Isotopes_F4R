# This is just some lines grabbed from noone_curves.py at some stage,
# just to test the operation of things. It was used to generate sokme of
# the data arrays that I plotted.

#
# Make a curve for evaporation
#
dels = (1./alphdo_liq(tsrc) - 1)*1000.
qs =  1000*qsat(ps, tsrc)/v2m	# source value (saturation specific humidity?)

### CCD::  isomixline,q0,del0,qs,dels,nn,eta,qh2oevap,deldevap
(qh2oevap,deldevap) = isomixline(q0,del0,qs,dels,nn,eta)
#
# Mix between high latitude and tropical super-depleted points
# 
### CCD::  isomixline,q0,del0,qs,delp,nn,eta,qh2omix,deldmix
(qh2omix,deldmix) = isomixline(q0,del0,qs,delp,nn,eta)
###
### CCD:: COMPLETE KLUDGE, since I don't know what i80 is!!!!!
i80 = len(qh2omix)/3    # **** COMPLETE KLUDGE !!!!!!
#
### CCD:: I do not know what this is!!!  dum = min(abs(qh2oevap/qs - hsrc), i80)
#
q1 = qh2oevap[i80]
del1 = deldevap[i80]

### CCD::  isoraysat,q1/1000.,del1,q0/1000.,nn,pcld,qh2oray,deldray,qh2ocld,deldcld
(qh2oray,deldray,qh2ocld,deldcld) = \
	isoraysat(q1/1000.,del1,q0/1000.,nn,pcld)

qh2oray = qh2oray*1000.
qh2ocld = qh2ocld*1000.
#
# Re-evaporation curve (maximum amount for 2 stage process)
#
### CCD::   eff = -1.0		# processed twice (reevaporation)
### CCD::   isoraysat,q1/1000.,del1,qmin/1000,nn,pcld,qh2orev,deldrev,qh2ocld2,deldcld2,eff=eff

(qh2orev,deldrev,qh2ocld2,deldcld2) = \
      isoraysat(q1/1000.,del1,qmin/1000,nn,pcld,eff=-1.0)

qh2orev = qh2orev*1000.
qh2ocld2= qh2ocld2*1000.

#
# Closed system, as per pseudo adiabatic process
#
### CCD::  isoeqlsat,q1/1000.,del1,q1/1000.,nn,pcld,qh2oeql,deldeql
(qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q1/1000.,nn,pcld)

qh2oeql = qh2oeql*1000.

#
# A bit of rayleigh from the freezing point
#
qfrz = 1000*qsat(65000., 263.0)/v2m
### CCD:: I do not know what this is!!! dum = min(abs(qh2oeql - qfrz), ifrz)
### CCD:: I do not know what ifrz is !!!!!!!!!!!!!!!!!
ifrz = len(qh2oeql)/3             # **** COMPLETE KLUDGE !!!!!!

### CCD::  isoraysat,qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000.,nn,pcld,qh2oice,deldice,qh2osno,deldsno
(qh2oice,deldice,qh2osno,deldsno) = \
     isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000.,nn,pcld)

qh2oice = qh2oice*1000.

#
# Draw the lines
#

#  oplot,qh2oevap,deldevap,color=icol_evp,thick=mthk
#  if keyword_set(label) then $
#      xyouts,12,-94,"Mixing to ocean (evaporation)",orient=3.,charsize=0.8,color=icol_evp

#  oplot,qh2omix, deldmix,color=icol_evp,thick=mthk,linestyle=2
#  if keyword_set(label) then $
#      xyouts,15,-30,"Mixing to land source",orient=3.,charsize=0.8,color=icol_evp


#  oplot,qh2oeql ,deldeql ,color=icol_ray,thick=mthk,linestyle=5
#  if keyword_set(label) then $
#      xyouts,4.5,-165,"Moist adiabatic (f=0)",orient=15.,charsize=0.8,color=icol_ray

#  oplot,qh2oray ,deldray ,color=icol_ray,thick=mthk
#  if keyword_set(label) then begin
#      xyouts,8,-240,"Pseudoadiabatic (f=1)",orient=28.,charsize=0.8,color=icol_ray
#      xyouts,8,-260,"   (Rayleigh)",orient=28.,charsize=0.8,color=icol_ray
#  endif

  oplot,qh2oice ,deldice ,color=icol_ray,thick=mthk,linestyle=2
#  if keyword_set(label) then begin
#      xyouts,6,-310,"Ice condensation",orient=0,charsize=0.8,color=icol_ray
#      xyouts,6,-330,"   (Rayleigh)",orient=0,charsize=0.8,color=icol_ray
#      arrow,5.8,-300,2.8,-260,/data,thick=2
#  endif

  oplot,qh2orev ,deldrev ,color=icol_rev,thick=mthk
#  if keyword_set(label) then begin
#      xyouts,14,-260,"Remoistening (f=2)",orient=38.,charsize=0.8,color=icol_rev
#      xyouts,14,-290,"     (super-Rayleigh)",orient=38.,charsize=0.8,color=icol_rev
#  endif

'''
  if (keyword_set(label)) then begin
    xyouts,5,-208,"(0<f<1)",orient=21.,charsize=0.8,color=icol_ray

    oplot,[0,200],[0,0],thick=2
    xyouts,4.3,7,'SMOW',charsize=0.6

    oplot,[qfrz,qfrz],[-1000,1000],thick=2,linestyle=2
    xyouts,2.7,-5,'Frost point',orient=-90.,charsize=0.6
    xyouts,1.7,-12,'(T=263K)',orient=-90.,charsize=0.6


    oplot,[qs,qs],[dels,dels],psym=1
    xyouts,qs-5,-115,"q!LS!N,!9d!3!LS!N",charsize=1.0

    oplot,[q0,q0],[del0,del0],psym=1,symsize=0.5
    oplot,[1,1],[-360,-360],psym=1
    xyouts,1,-350,"q!L0!N,!9d!3!L0!N",charsize=1.0

    xyouts,29,-102,'RH=80%', orient=-55,charsize=0.6

  endif
end
'''
