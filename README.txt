Author: Samuel Lehman
        13/12/2022
        Last modified: 4:04PM 12/13/2022

Project Title: Metadata Management
This project is project assignment 4 for CS457 Database Management Systems at the University of Nevada, Reno
This program allows for the creation of databases and tables similar to SQLite

Getting Started:
This document will help you get this program running on your local environment 

Prerequisites:
Python version 3.9.2
A unix operating system such as ubuntu or the linux subsystem for windows

System Design:
This program uses linux directories as databases and files as database tables

Built with/Implementation:
This program was written in Python
Its functionalities are creating, altering, and viewing databases and tables
This program uses if an for loops to achieve this 
This program also allows a user to preform joins on tables
In this program you can also lock files
Modules used in the program are:
os: to get file paths
sys: to get program arguments
subprocess: to run linux commands from the program
This program uses a custom made class called "SamQLTable" that provides
functionality to create and manipulate tables

How to run/test:
1) Open a linux virtual machine or use the linux subsystem for windows
2) change directory to where the files are installed
3) run the command "python3 samuellehman_pa4.py" to run the program without a test file
if you have a test file run the command "python3 samuellehman_pa4.py [test file]"
inside the program you can use "SamQLTable> [filename].sql" to run sql commands in 
a file in the program
It is recommended to use P1_test1.sql and P2_test1.sql in their respective terminals
then when inside the program on the respective terminals type "SamQLTable> P1_test2.sql"
and "SamQLTable> P2_test2.sql" 
or you can write in commands one at a time (not recommended)