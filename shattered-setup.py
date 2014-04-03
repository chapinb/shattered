#!/usr/bin/env python3
##################################################################################
##                                                                              ##
##       _____ _       _   _                 _                                  ##
##      |   __| |_ ___| |_| |_ ___ ___ ___ _| |                                 ##
##      |__   |   | .'|  _|  _| -_|  _| -_| . |                                 ##
##      |_____|_|_|__,|_| |_| |___|_| |___|___| 				                        ##
##                                                                              ##
##                      					 									                           ##
## Special Thanks to Julie Desautels, Jon Rajewski, and the LCDI for the 		   ##
## research leading to the success of this script.                              ##
##                                                                              ##
## Copyright 2013, Chapin Bryce													                       ##
## This program is free software: you can redistribute it and/or modify         ##
## it under the terms of the GNU General Public License as published by         ##
## the Free Software Foundation, either version 3 of the License, or            ##
## any later version.    		                       							              ##
##                                                                              ##
## This program is distributed in the hope that it will be useful,              ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of               ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                ##
## GNU General Public License for more details.                                 ##
##                                                                              ##
## You should have received a copy of the GNU General Public License            ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>.        ##
##                                              								                ##
##################################################################################


#### Shattered Setup Script ####

"""
This script is designed to setup Shattered and the dependencies on the destination platform.
"""

import subprocess
import shutil
import zipfile

def shattered_linux ():
	stauts = 1
	print("Setting up Shattered...")
	
	## Define ADT Bundle wget command
	x = 1
	while x == 1:
		version = input("What is your OS Version: 32/64")
		if version == "32":
			wget_cmd = "sudo wget -O /usr/local/src/adt-bundle32.zip http://dl.google.com/android/adt/adt-bundle-linux-x86-20131030.zip"
			x = 0
		elif version == "64":
			wget_cmd = "sudo wget -O /usr/local/src/adt-bundle64.zip http://dl.google.com/android/adt/adt-bundle-linux-x86_64-20131030.zip"
			x = 0
		else:
			print("invalid OS type")
			x = 1
			
	##Download ADT Bundle
	try:
		subprocess.call([wget_cmd], shell=True)
	except:
		print("Error Downloading ADT Bundle. Please report to http://code.google.com/p/shattered/issues/")
		sys.exit(1)
	
	## Unzip adt bundle
	unzip_cmd = "sudo unzip /usr/local/src/adt-bundle64.zip -d /usr/local/src/"
	print("unzip command: " + unzip_cmd)
	try:
		subprocess.call([unzip_cmd], shell=True)
	except:
		print("Error unzipping. Please report to http://code.google.com/p/shattered/issues/")
		sys.exit(1)
	
	## Make adb global
	if version == "32":
		cp_cmd = "sudo cp /usr/local/src/adt-bundle-linux-x86-20131030/sdk/platform-tools/adb /usr/local/bin"
	elif version == "64":
		cp_cmd = "sudo cp /usr/local/src/adt-bundle-linux-x86_64-20131030/sdk/platform-tools/adb /usr/local/bin"
	else:
		print("Error with copying binaries. Please report to http://code.google.com/p/shattered/issues/")
	
	print("adb copy command: " + cp_cmd)
	
	try:
		subprocess.call([cp_cmd], shell=True)
	except:
		print("Error Setting Global Binaries. Please report to http://code.google.com/p/shattered/issues/")
		sys.exit(1)
	
	##Make shattered.py executable
	cp_cmd = "sudo cp shattered.py /usr/local/bin"
	
	print("shattered copy command: " + cp_cmd)
	
	try:
		subprocess.call([cp_cmd], shell=True)
		status = 0
	except:
		print("Error Creating Shattered Executable. Please report to http://code.google.com/p/shattered/issues/")
		sys.exit(1)
	
	return status
## Currently Shattered is only supported on Linux, will be ported to other platforms in near future
y = shattered_linux()
print("Done %r" % y)