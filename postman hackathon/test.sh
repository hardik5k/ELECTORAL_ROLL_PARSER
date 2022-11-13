#!/bin/sh

read name ser_no
qpdf --decrypt file.pdf out.pdf

ocrmypdf --pages $(( (ser_no / 31) + 2 )),$(( (ser_no / 31) + 3 )),$(( (ser_no / 31) + 4 )) out.pdf out.pdf

# ocrmypdf out.pdf out.pdf

python3 output.py out.pdf $name $ser_no