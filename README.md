# ELECTORAL_ROLL_PARSER

This project aims to create an API that recieves 4 parameters - NAME, AGE, FATHER'S/HUSBAND'S NAME and STATE of a person and generates his/her family tree by aggregating imformation available in Indian Election Commision webisites - https://electoralsearch.in/ and https://nvsp.in/.


This directory contanins two important files.
1. pdf_processing - This folder contains scripts to parse electoral rolls and works for **any pdf in english language.**

command to run - ./test.sh

test.sh is a bash file which takes 3 inputs as parameters - 
  * The electoral roll pdf <input_pdf_name>
  * Name of the person to search (with underscores)
  * Serial Number obtained from https://electoralsearch.in/

Sample command:
> ./test.sh <br />
> file.pdf Manoj_Vassudev_Aeer 59
  
It decrypts the pdf, makes it text parsable and runs the python script parser.py that uses dfs to generate family tree.


2. postman hackathon/api.py - This is the actual flask api that currently works for the state of GOA.

Given the dynamic nature of the webiste of different states, it was too time consuming to design automated scripts separately for each one of them. So we decided to go with Goa as their webiste doesn't require captcha and so is easier to handle. However, our sellenium script to easily scalable to state any with few minor changes unique to every state's website.

 
 
