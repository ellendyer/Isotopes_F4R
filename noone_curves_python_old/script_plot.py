from all import *

nn = 1000
print "Number of points, nn = ",nn

#
# Make a curve for evaporation
#
dels = (1./alphdo_liq(tsrc) - 1)*1000.
qs =  1000*qsat(ps, tsrc)/v2m	# source value (saturation specific humidity?)

### CCD::  isomixline,q0,del0,qs,dels,nn,eta,qh2oevap,deldevap

(qh2oevap,deldevap) = isomixline(q0,del0,qs,dels,nn,eta)
print "\n------"
print "*** Curve from isomixline: .........."
print "*** qh2oevap[0],deldevap[0] =",qh2oevap[0],deldevap[0]
print "*** qh2oevap[-1],deldevap[-1] =",qh2oevap[-1],deldevap[-1]

#
# Mix between high latitude and tropical super-depleted points
# 
### CCD::  isomixline,q0,del0,qs,delp,nn,eta,qh2omix,deldmix

(qh2omix,deldmix) = isomixline(q0,del0,qs,delp,nn,eta)
print "\n------"
print "*** Curve from isomixline: .........."
print "*** qh2omix[0],deldmix[0] =",qh2omix[0],deldmix[0]
print "*** qh2omix[-1],deldmix[-1] =",qh2omix[-1],deldmix[-1]

#
### CCD:: Find index of the element of vector qh2oevap/qs which is
### CCD:: closest to the value hsrc, and store that index in i80
### CCD::      dum = min(abs(qh2oevap/qs - hsrc), i80)
# Find the location of the minimum element in the array qh2oevap/qs - hsrc
# which give the location in the array qh2oevap/qs that is closest to
# hsrc in value. This will be the location of the 80% relative humidity
# point along this curve in the Noone diagram.

i80 = np.argmin(np.abs(qh2oevap/qs - hsrc))    #**************************
print "\n------"
print "*** i80 = ",i80
print "*** qh2oevap[i80] = ", qh2oevap[i80]
print "*** deldevap[i80] = ", deldevap[i80]
print "*** target value hsrc = ", hsrc
print "*** qh2oevap[i80]/qs = ", qh2oevap[i80]/qs

#
q1 = qh2oevap[i80]
del1 = deldevap[i80]

### CCD:: isoraysat,q1/1000.,del1,q0/1000.,nn,pcld, \
### CCD::                    qh2oray,deldray,qh2ocld,deldcld

(qh2oray,deldray,qh2ocld,deldcld) = \
          isoraysat(q1/1000.,del1,q0/1000.,nn,pcld)
qh2oray = qh2oray*1000.
qh2ocld = qh2ocld*1000.
print "\n------"
print "*** Curve(s) from isoraysat: .........."
print "*** qh2oray[0],deldray[0] =",qh2oray[0],deldray[0]
print "*** qh2oray[-1],deldray[-1] =",qh2oray[-1],deldray[-1]
print "---"
print "*** qh2ocld[0],deldcld[0] =",qh2ocld[0],deldcld[0]
print "*** qh2ocld[-1],deldcld[-1] =",qh2ocld[-1],deldcld[-1]


#
# Re-evaporation curve (maximum amount for 2 stage process)
#
### CCD::   eff = -1.0		# processed twice (reevaporation)
### CCD::   isoraysat,q1/1000.,del1,qmin/1000,nn,pcld,qh2orev,deldrev,qh2ocld2,deldcld2,eff=eff
(qh2orev,deldrev,qh2ocld2,deldcld2) = \
        isoraysat(q1/1000.,del1,qmin/1000,nn,pcld,eff=-1.0)

qh2orev = qh2orev*1000.
qh2ocld2= qh2ocld2*1000.
print "\n------"
print "*** Curve(s) from isoraysat: .........."
print "*** qh2orev[0],deldrev[0] =",qh2orev[0],deldrev[0]
print "*** qh2orev[-1],deldrev[-1] =",qh2orev[-1],deldrev[-1]
print "---"
print "*** qh2ocld2[0],deldcld2[0] =",qh2ocld2[0],deldcld2[0]
print "*** qh2ocld2[-1],deldcld2[-1] =",qh2ocld2[-1],deldcld2[-1]


#
# Closed system, as per pseudo adiabatic process
#
### CCD::  isoeqlsat,q1/1000.,del1,q1/1000.,nn,pcld,qh2oeql,deldeql
### CCD::: (qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q1/1000.,nn,pcld)
#  CCD Change arg-3 from q1/1000 to q0/1000. If both arg-1 and arg-3 are
#  equal, then isoeqlsat returns a constant vector ... Wrong!
(qh2oeql,deldeql) = isoeqlsat(q1/1000.,del1,q0/1000.,nn,pcld)

qh2oeql = qh2oeql*1000.
print "\n------"
print "*** Curve(s) from isoeqlsat: .........."
print "*** qh2oeql[0],deldeql[0] =",qh2oeql[0],deldeql[0]
print "*** qh2oeql[-1],deldeql[-1] =",qh2oeql[-1],deldeql[-1]

#
# A bit of rayleigh from the freezing point
#
qfrz = 1000*qsat(65000., 263.0)/v2m

### CCD:: Find index of the element of vector qh2oeql which is
### CCD:: closest to the value qfrz, and store that index in ifrz
### CCD::      dum = min(abs(qh2oeql - qfrz), ifrz)
# Find the location of the minimum element in the array qh2oeql - qfrz
# which give the location in the array qh2oeql that is closest to
# qfrz in value. This will be the location of where the pressure and
# temperature become 65000., 263.0 respectively

ifrz = np.argmin(np.abs(qh2oeql - qfrz))    #**************************
print "\n------"
print "*** ifrz = ",ifrz
print "*** qh2oeql[ifrz] = ", qh2oeql[ifrz]
print "*** deldeql[ifrz] = ", deldeql[ifrz]
print "*** target value qfrz = ", qfrz
print "*** qh2oeq[ifrz] = ", qh2oeql[ifrz]

### CCD::  isoraysat,qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000., \
### CCD::              n,pcld,qh2oice,deldice,qh2osno,deldsno
'''
(qh2oice,deldice,qh2osno,deldsno) = \
       isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q1/1000.,nn,pcld)
##### !!!! Arg-3 is NOT q1/1000., but q0/1000. !!!!
'''
(qh2oice,deldice,qh2osno,deldsno) = \
       isoraysat(qh2oeql[ifrz]/1000.,deldeql[ifrz],q0/1000.,nn,pcld)

qh2oice = qh2oice*1000.
print "\n------"
print "*** Curve(s) from isoraysat: .........."
print "*** qh2oice[0],deldice[0] =",qh2oice[0],deldice[0]
print "*** qh2oice[-1],deldice[-1] =",qh2oice[-1],deldice[-1]
print "---"
print "*** qh2osno[0],deldsno[0] =",qh2osno[0],deldsno[0]
print "*** qh2osno[-1],deldsno[-1] =",qh2osno[-1],deldsno[-1]

# Try some plots:

import matplotlib.pyplot as plt

plt.xlabel('q (mmol/mol)')

plt.ylabel(r'$ \delta (o/oo) $')

# Plot vertical line where q --> q0
plt.plot([q0,q0],[-400.0,0.0],':b')

# Plot vertical line where q --> qfrz
plt.plot([qfrz,qfrz],[-400.0,0.0],':b')

# Plot vertical line where q --> q at 80% RH
plt.plot([q1,q1],[-400.0,0.0],':b')

# Noone paper colour: Orange Solid
plt.plot(qh2oevap,deldevap,'-.y')

# Noone paper colour: Orange Dashed
plt.plot(qh2omix,deldmix,'--y')

# Noone paper colour: Cyan Long-dashed
plt.plot(qh2oeql,deldeql,'--c')

# Noone paper colour: Cyan Solid
plt.plot(qh2oray,deldray,'-.c')

# Noone paper colour: Cyan Dashed
plt.plot(qh2oice,deldice,'-.r')

# Noone paper colour: Magenta Solid
plt.plot(qh2orev,deldrev,'-m')

# plt.show()
plt.savefig('NooneCurves_python.pdf')

