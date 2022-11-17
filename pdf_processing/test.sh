#!/bin/sh

read input_file name ser_no

qpdf --decrypt $input_file out.pdf

ocrmypdf --pages $(( (ser_no / 31) + 2 )),$(( (ser_no / 31) + 3 )),$(( (ser_no / 31) + 4 )) out.pdf out.pdf

# ocrmypdf out.pdf out.pdf

python3 parser.py out.pdf $name $ser_no
