all:
	pdflatex --shell-escape praca
	bibtex praca
	pdflatex --shell-escape praca
	pdflatex --shell-escape praca

clean:
	rm *.aux *.bbl *.blg *.log *.out *.toc *.dvi svg-inkscape _minted-praca -r