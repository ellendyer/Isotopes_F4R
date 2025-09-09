### CCD::  This seems to work properly after correcting IDL code errors.
#####################################################################
### CCD:: # if (n_elements(pcld) eq 0) then delp = 85000.
### CCD::   #***** CCD I think this is an error:
### CCD::   # if (n_elements(pcld) eq 0) then delp = 85000.
### CCD::   # It should assign value to pcld, not delp, as in:
### CCD::   # if (n_elements(pcld) eq 0) then pcld = 85000.
### CCD:: if 'pcld' not in globals():       pcld = 85000.
### CCD:: The original "noone_curves.pro" file seems to set not set pcld here
### CCD:: but to set delp to 85000, having just set delp to 0 in the previous
### CCD:: line. Maybe this is moot, since everything seems to be set explicitly.
#
# Plots the varierty of curves making up a "Noone diagram"
#
### CCD: Simple way to run is noone_curves(tsrc,q0,del0)
#
# This assumes you have already initialized a delta-q plot with axes in
# permil and VMR in mmol/mol (i.e., permil)
#
# INPUTS
#    tsrc	Temperature (K) of ocean source
#    q0		H2O vmr of dry end member
#    del0	delD of dry end member
#    delp=delp	delD of local precipitation/transpiration
#    hsrc=hsrc	humidity at evaporation source (sets dewpoint)
#    pcld=pcld	pressure at cloud level (Pa)
#    qmin=qmin	minimum H2O VMR for reevap curve
#    nn=nn	"Resolution" of curves (iterations)
#    eta=eta	kinetic fractionation (1 or 0.995 is defensibel)
#    /label	flag to add labels
#    /color	flag to make color (based on color table 40)
#
# OUTPUTS:
#    none
#
# EXAMPLE:
#
#  plot,[0,0],[0,0],/nodata, $
#     xrange=[0,38],xstyle=1,yrange=[-380,50],ystyle=1, $
#     xtitle='q (ppt)',ytitle='!9d!3 (permil)', $
#     charsize=1.3,xthick=2,ythick=2
#
#   nn   = 1000 
#   tsrc = 300. 
#   hsrc = 0.80 
#   q0   = 0.9 
#   del0 = -400.
#   delp = -30. 
#   eta  = 0.995
#   pcld = 85000.
#
#  noone_curves,tsrc,q0,del0,delp=delp,eta=eta,hsrc=hsrc,pcld=pcld, $
#         nn=nn,/color,/label
#
#  DEPENDENCIES:
#     (From David) QSAT,TSAT,ALPHDO_LIQ,ALPHDO_ICE,
#                  ISOMIXLINE,ISORAYSAT,ISOEQLSAT,
#     (Coyote library) SYMCAT
#
# David Noone <dcn@colorado.edu> - Mon Jul 27 09:52:07 MDT 2009
#
# ------------------------------------------------------------------------
###CCD:: pro noone_curves,tsrc,q0,del0,delp=delp,hsrc=hsrc,pcld=pcld, $
###CCD::          qmin=qmin,nn=nn,eta=eta,label=label,color=color

def noone_curves(tsrc,q0,del0):

# Keyword values assignment:
# delp=delp,hsrc=hsrc,pcld=pcld,qmin=qmin,nn=nn,eta=eta,label=label,color=color
# These should be handled in a simpler manner, probably by setting such
# things up in the file globals_iniits.py

  import sys         # Just to allow write to stderr, and exit ....
#
# Set defaults
#
  ps = 1000.e2			# approximate surface pressure
  v2m = (18./29.)                 # converts pptv to mixing ratio
#
# Check to see if variables are initialized, and if not do it here.
# CCD: If variable named XYZ is defined anywhere, it will be in globals()
# CCD: If we want to see if it is defined locally, change globals to locals
# CCD: This is to replace all the IDL if (n_elements(nn) eq 0) ...

  # List of variables that should have beeb assigned values
  must_be_set = ['del0','delp','eta','hsrc','nn','pcld', \
                  'ps','q0','qmin','tsrc','v2m']
  count = 0
  for name in must_be_set:
    if name in globals():     # Check to see if each is defined somewhere
      count += 1
    else:
      sys.stderr.write("Variable %s without assigned value.\n" % name)
  if count < len(must_be_set):
    sys.stderr.write("Some variables have no initial values - exit!\n")
    sys.exit(1)

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
#
### CCD:: Find index of the element of vector qh2oevap/qs which is
### CCD:: closest to the value hsrc, and store that index in i80
### CCD::      dum = min(abs(qh2oevap/qs - hsrc), i80)
# Find the location of the minimum element in the vector qh2oevap/qs - hsrc
# which give the location in the vector qh2oevap/qs that is closest to
# hsrc in value. This will be the location of the 80% relative humidity
# point along this curve in the Noone diagram.

  i80 = np.argmin(np.abs(qh2oevap/qs - hsrc))    #**************************
  # print "*** i80 = ",i80

#
  q1 = qh2oevap[i80]
  del1 = deldevap[i80]

### CCD:: isoraysat,q1/1000.,del1,q0/1000.,nn,pcld, \
### CCD::                    qh2oray,deldray,qh2ocld,deldcld

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
### CCD::: (qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q1/1000.,nn,pcld)
### CCD:: But this is wrong!!!! Arg-3 needs to be q0/1000.
### CCD Change arg-3 from q1/1000 to q0/1000. If both arg-1 and arg-3 are
#  equal, then isoeqlsat returns a constant vector ... Wrong!
  (qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q0/1000.,nn,pcld)

  qh2oeql = qh2oeql*1000.
#
# A bit of rayleigh from the freezing point
#
  qfrz = 1000*qsat(65000., 263.0)/v2m

### CCD:: Find index of the element of vector qh2oeql which is
### CCD:: closest to the value qfrz, and store that index in ifrz
### CCD::      dum = min(abs(qh2oeql - qfrz), ifrz)
# Find the location of the minimum element in the vector qh2oeql - qfrz
# which give the location in the vector qh2oeql that is closest to
# qfrz in value. This will be the location of where the pressure and
# temperature become 65000., 263.0 respectively

  ifrz = np.argmin(np.abs(qh2oeql - qfrz))    #**************************
  # print "*** ifrz = ",ifrz

### CCD::  isoraysat,qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000., \
### CCD::              n,pcld,qh2oice,deldice,qh2osno,deldsno
### CCD::  (qh2oice,deldice,qh2osno,deldsno) = \
### CCD::      isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000.,nn,pcld)
### CCD:: But this is wrong!!!! Arg-3 needs to be q0/1000, not q1/1000.
### CCD:: Otherwise the calculated curve is not below freezing point!!!
  (qh2oice,deldice,qh2osno,deldsno) = \
       isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q0/1000.,nn,pcld)

  qh2oice = qh2oice*1000.

### CCD:: ==============================================================
  # Try some plots:

  import matplotlib.pyplot as plt

  plt.xlabel('q (mmol/mol)')

  plt.ylabel(r'$ \delta (o/oo) $')

  # Plot vertical line where q --> q0
  plt.plot([q0,q0],[-400.0,0.0],color='black',linestyle='dashed')

  # Plot vertical line where q --> qfrz
  plt.plot([qfrz,qfrz],[-400.0,0.0],color='black',linestyle='dashed')

  # Plot vertical line where q --> q at 80% RH
  plt.plot([q1,q1],[-400.0,0.0],color='black',linestyle='dashed')

  # Noone paper colour: Orange Solid
  # plt.plot(qh2oevap,deldevap,'-.y')
  plt.plot(qh2oevap,deldevap,color='orange',linestyle='solid')

  # Noone paper colour: Orange Dashed
  plt.plot(qh2omix,deldmix,color='orange',linestyle='dashed')

  # Noone paper colour: Cyan Long-dashed
  plt.plot(qh2oeql,deldeql,color='cyan',linestyle='dashdot')

  # Noone paper colour: Cyan Solid
  plt.plot(qh2oray,deldray,color='cyan',linestyle='solid')

  # Noone paper colour: Cyan Dashed
  plt.plot(qh2oice,deldice,color='cyan',linestyle='dashed')

  # Noone paper colour: Magenta Solid
  plt.plot(qh2orev,deldrev,color='magenta',linestyle='solid')

  # plt.show()
  plt.savefig('NooneCurves_python.pdf')

### CCD:: ==============================================================

''' ************ if IDL_Plot: ***** The Rest of the File ***********
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
'''
