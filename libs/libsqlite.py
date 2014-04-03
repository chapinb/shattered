#!/usr/bin/env python3
##################################################################################
##                                                                              ##
##       _____ _       _   _                 _                                  ##
##      |   __| |_ ___| |_| |_ ___ ___ ___ _| |                                 ##
##      |__   |   | .'|  _|  _| -_|  _| -_| . |                                 ##
##      |_____|_|_|__,|_| |_| |___|_| |___|___| 				                ##
##                                                                              ##
##                      					 									##
## Special Thanks to Julie Desautels, Jon Rajewski, and the LCDI for the 		##
## research leading to the success of this script.                              ##
##                                                                              ##
## Copyright 2013, Chapin Bryce													##
## This program is free software: you can redistribute it and/or modify         ##
## it under the terms of the GNU General Public License as published by         ##
## the Free Software Foundation, either version 3 of the License, or            ##
## any later version.    		                       							##
##                                                                              ##
## This program is distributed in the hope that it will be useful,              ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of               ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                ##
## GNU General Public License for more details.                                 ##
##                                                                              ##
## You should have received a copy of the GNU General Public License            ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>.        ##
##                                              								##
##################################################################################

"""@package Shattered
    
    This script is built to parse sqlite artifacts from Google Glass in a forensic manner.
    
    Built at the LCDI at Champlain College. Learn More at http://lcdi.champlain.edu
    
    """
import sqlite3

def sqlite_version():
    """
    This function prints the version of the code.
    """
    version = 20140312
    print("SQLite Parser version: ", version)
    
def sqlite_parser(infile, outfile, database):

    conn = sqlite3.connect(infile)
    #   conn.text_factory = str ## my current (failed) attempt to resolve this
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM " + database)

    fout = open(outfile, 'a')

    for row in data:
      row = str(row)
      row = row + "\n"
      fout.write(row)
      fout.flush()
    fout.close()

    
