# File name: save.plt - saves a Gnuplot plot as a PostScript file
# to save the current plot as a postscript file issue the commands:
#  gnuplot>   load 'saveplot'
#  gnuplot>   !mv my-plot.ps another-file.ps
set size 1.0, 0.6
set terminal postscript portrait enhanced mono dashed lw 1 "Helvetica" 14 
set output "qh2odeldmix_evap.ps"

plot "qh2odeldmix.dat" using 1:2 w l, "qh2odeldevap.dat" using 1:2 w l

set terminal x11
set size 1.0, 1.0
replot
   

