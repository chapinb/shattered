#!/usr/bin/env python3
##################################################################################
##                                                                              ##
##       _____ _       _   _                 _                                  ##
##      |   __| |_ ___| |_| |_ ___ ___ ___ _| |                                 ##
##      |__   |   | .'|  _|  _| -_|  _| -_| . |                                 ##
##      |_____|_|_|__,|_| |_| |___|_| |___|___| 				##
##                                                                              ##
##                      					 		##
## Special Thanks to Julie Desautels, Jon Rajewski, and the LCDI for the 	##
## research leading to the success of this script.                              ##
##                                                                              ##
## Copyright 2013, Chapin Bryce							##
## This program is free software: you can redistribute it and/or modify         ##
## it under the terms of the GNU General Public License as published by         ##
## the Free Software Foundation, either version 3 of the License, or            ##
## any later version.    		                       			##
##                                                                              ##
## This program is distributed in the hope that it will be useful,              ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of               ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                ##
## GNU General Public License for more details.                                 ##
##                                                                              ##
## You should have received a copy of the GNU General Public License            ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>.        ##
##                                              				##
##################################################################################

## Logcat Parser

"""
This module is designed to parse data within the logcat export from shattered.
Run as a standalone, the module will prompt for an input and output file.
The output format is in csv.

ie. $ python3 logcat_lib.py 

"""

import re
import os
import sys

def logcat_version():
    """
    Function for calling the version of the code
    """
    version = 20140213
    print("Logcat Parser version: ", version)

def logcat_parser(inputfile, outputfile):
    """
    This function parses the data from a logcat input file into csv format for easier reading.
    Can be run as standalone script (ie ./logcat_lib.py) or imported to another script.
    """
    
    logcat_version()
    print("Parsing Logcat File...")

    fin = open(inputfile, 'r')
    fout = open(outputfile, 'w')

    fout.write("Date, Time, PID, Level, Tag, Data")

    bucket = ""

    logname = re.compile(r'----*')
    metainfostart = re.compile(r'^\[ \d')
    metainfoend = re.compile(r'\]$')
    anytext = re.compile(r'.*')

    for line in fin:
        line = line.strip()
        if logname.findall(line):
            print("Processesing Log:    " + line)
            loginfo = "Processesing Log:    " + line
        elif metainfoend.findall(line) and metainfostart.findall(line):
            meta = line
            meta = logcat_meta(meta)
            fout.write(meta)
        elif anytext.findall(line):
            data = line
            data = data.strip()
            data = data.replace(",", " ")
            bucket = data
            fout.write(bucket)
                
        fout.flush()

    fout.close()

    print("####################\nLogcat Processing Complete\n####################")

def logcat_meta(meta): 
    """
    This function breaks down the meta data information to allow better sorting and
    filtering in CSV interpreters
    """

    meta_a = meta.split()

    date = meta_a[1]
    time = meta_a[2]
    pid = meta_a[3]
    service = meta_a[4]

    print("service" + service)
    service_a = service.split("/")
    level = service_a[0]
    tag = service_a[1]
    
    meta_out = "\n" + date + "," + time + "," + pid + "," + level + "," + tag + ","
    return meta_out



