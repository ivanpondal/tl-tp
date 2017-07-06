.PHONY: all clean cleanall

all: tl-tp-informe.pdf

%.pdf: %.tex
	pdflatex $<
	pdflatex $<

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.synctex.gz

cleanall:
	rm -f tl-tp-informe.pdf
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.synctex.gz
