# ELECTORAL_ROLL_PARSER

This project aims to create an API that recieves 4 parameters - NAME, AGE, FATHER'S/HUSBAND'S NAME AND STATE about a person and generates his/her family tree by aggregating imformation availbale in Indian Election Commision webisites - https://electoralsearch.in/ and https://nvsp.in/.


This directory contanins two important files
1. pdf_processing - This folder contains scripts to parse electoral rolls and works for any pdf in english language.

command to run - ./test.sh input_pdf_name name_of_the_person serial_number_of_the_person

test.sh is a bash file which takes 2 inputs as parameters - 
  1. The electoral roll pdf
  2. Name of the person th search
  3. Serial Number obtained from https://electoralsearch.in/
  
 It decrypts the pdf, makes it text parsable and runs the python script parser.py that uses dfs to generate family tree.
 
 
