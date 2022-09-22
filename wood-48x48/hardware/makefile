

fcch-7i96-dm556.pdf: fcch-7i96-dm556-controller-0.pdf fcch-7i96-dm556-controller-1.pdf fcch-7i96-dm556-wiring-0.pdf fcch-7i96-dm556-wiring-1.pdf
	pdfjam --paper letter $^ -o $@


fcch-7i96-dm556-controller-0.pdf: fcch-7i96-dm556-controller.dxf
	dwg2pdf.bat -center -monochrome -layer='0.*' -scale='1:4' -paper='Letter' -force -o $@ $<

fcch-7i96-dm556-controller-1.pdf: fcch-7i96-dm556-controller.dxf
	dwg2pdf.bat -center -monochrome -layer='1.*' -scale='1:4' -paper='Letter' -force -o $@ $<


fcch-7i96-dm556-wiring-0.pdf: fcch-7i96-dm556-wiring.dxf
	dwg2pdf.bat -center -grayscale -layer='0.*' -scale='1:7' -paper='Letter' -force -o $@ $<

fcch-7i96-dm556-wiring-1.pdf: fcch-7i96-dm556-wiring.dxf
	dwg2pdf.bat -center -grayscale -layer='1.*' -scale='1:7' -paper='Letter' -force -o $@ $<

.PHONY: clean
clean:
	rm -f *.pdf
