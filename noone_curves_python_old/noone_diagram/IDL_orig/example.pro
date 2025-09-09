;
; Example of how to make a graph using David's set of curves
;
; David Noone <dcn@colorado.edu> - Mon Jul 27 09:11:40 MDT 2009
;
; ------------------------------------------------------------------------

;
; Read/create your isotope data. H2O is in VMR in paers per thousand
;
qh2otes = [   5.,  15.,   8.,  10.]
deldtes = [-200.,-100.,-250.,-150.]


;
; Start a plot - notice the X axis is H2O in VMR
;
!p.multi= 0
set_plot,'PS'
device,filename='noone_diagram.ps'
device,xsize=6,ysize=6,xoffset=0.5,yoffset=0.5,/inches
device,/color,bits=8
!p.font = 1
device,set_font="Helvetica",/tt_font
loadct,40
;
  plot,[0,0],[0,0],/nodata, $
     xrange=[0,38],xstyle=1,yrange=[-380,50],ystyle=1, $
     xtitle='q (ppt)',ytitle='!9d!3 (permil)', $
     charsize=1.3,xthick=2,ythick=2

;
; Plot your data
;
  oplot,qh2otes,deldtes,psym=1

;
; Overlay David's curves.
;
   nn   = 1000				; curve "resolution" (optional)
   tsrc	= 300.				; temperature (K) of ocean source water
   hsrc = 0.80				; humidity at source (to set dew point)
   q0   = 0.9				; dry end point for mixing model
   del0 = -400.				; isotopic composition at q0
   delp = -30.				; delta value of local precip (transpiration)
   eta  = 0.995				; kinetic fractionation (optional)
   pcld = 85000.			; pressure of clouds (Pa)


   noone_curves,tsrc,q0,del0,delp=delp,eta=eta,hsrc=hsrc,pcld=pcld, $
         nn=nn,/color,/label


;
; Finish the plot
;
device,/close
set_plot,'x'
!p.multi=0

end




