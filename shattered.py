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

This script is built to acquire artifacts from Google Glass in a forensic manner.

Built at the LCDI at Champlain College. Learn More at http://lcdi.champlain.edu

"""

import _thread
import subprocess
import sys
import shutil
import os
import time

#Import Custom Modules
#from logcat_lib import *

def shattered_version():
    """
    This function prints the version of the code.
    """
    version = 201402192
    print("Shattered Aquisition version: ", version)

def adb_path():
	"""
		This function checks the installation of adb to ensure it is correctly enabled as an executable in a /bin directory
		
		If the check fails, it reccomends the user should run 'sudo ln -s adb /usr/local/bin/adb' to correct the issue
		
		Set this up!
	"""
	subprocess.call("adb root", shell=True)

def get_serialno():
	"""
		This command gathers the device serial number and saves it for use later, returning it out of the function
	"""
	sno_cmd = "adb get-serialno"
	sno = os.popen(sno_cmd).read()
	sno = sno.strip("\n")
	print(sno) 
	return sno

def prep_dir(outdir, sno):
	"""
		This funtion creats the necessary directories for information to be placed within the case directory.
		
		Needs to be updated to use os.mkdir instead of yet another subrocess command
	"""
	subprocess.call("mkdir %r" % outdir, shell=True)
	subprocess.call("mkdir %r/fs-%r" % (outdir,sno), shell=True)
	subprocess.call("mkdir %r/dumpsys" % outdir, shell=True)
	
	
def dumpsys(outdir):
	"""
		This function runs dumpsys commands for the services available on Glass
		
		To make updating the changing available services, use the array 'services' to make modifications
	"""
	outdir = outdir + "/dumpsys"
	services = ["SurfaceFlinger", "accessibility", "account", "activity", "alarm", "appwidget", "audio", "backup", "battery", "batteryinfo", "bluetooth", "bluetooth_a2dp", "clipboard", "connectivity", "content", "country_detector", "cpuinfo", "device_policy", "devicestoragemonitor", "diskstats", "drm.drmManager",
"dropbox", "entropy", "eye_gesture", "gfxinfo", "hardware", "hardware.dsswb", "head_gesture", "input_method", "location", "lockscreen", "media.audio_flinger", "media.audio_policy", "media.camera", "media.player", "meminfo", "mount", "netpolicy", "netstats", "network_management", "notification", "package",
"permission", "power", "samplingprofiler", "search", "sensorservice", "statusbar", "telephony.registry", "textservices", "throttle", "timeline", "uimode", "usagestats", "usb", "vibrator", "wallpaper", "wifi", "wifip2p", "window"]
	x = len(services)
	i = 0
	while i < x:
		dumpsys_cmd = "adb shell dumpsys " + services[i] + " | tee ./"+ outdir +"/dumpsys-" + services[i] + ".txt"
		subprocess.call([dumpsys_cmd], shell=True)
		i = i + 1
	

def sysinfo(outdir):
	"""
		This function runs a series of system tools on Glass
		
		To make updating the changing available tools, use the array 'information' to make modifications
	"""
        ##Removed dumpsys due to instability in logfile termination
	information = ["date", "df", "dmesg", "dumpstate", "id", "iptables","logcat", "lsof", "netcfg", "netstat", "mount", "pm", "printenv", "ps", "screencap", "service", "uptime"]
	o = len(information)
	u = 0
	while u < o:
                if information[u] == "logcat":
                    tool = "logcat -d -v long *:V"
                    outfile = "logcat"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    u = u + 1

                elif information[u] == "iptables":
                    tool = "iptables -L"
                    outfile = "iptables"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    u = u + 1
                    
                elif information[u] == "service":
                    tool = "service list"
                    outfile = "service-list"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    u = u + 1
                    
                elif information[u] == "pm":
                    tool = "pm list features"
                    outfile = "package_manager-list-features"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    
                    tool = "pm list permission-groups"
                    output = "package_manager-list-permission-groups"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    
                    tool = "pm list permissions -g -f"
                    output = "package_manager-list-permission-groups"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    
                    tool = "pm list libraries"
                    output = "package_manager-list-libraries"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)

                    tool = "pm list packages"
                    output = "package_manager-list-packages"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    
                    "pm get-install-location",
                    tool = "pm get-install-location"
                    output = "package_manager-get-install-location"
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    
                    u = u + 1

                else:
                    tool = information[u]
                    outfile = information[u]
                    
                    sysinfo_cmd = "adb shell " + tool + " | tee ./" + outdir + "/" + outfile + ".txt"
                    subprocess.call([sysinfo_cmd], shell=True)
                    u = u + 1


def fspull(outdir):
	"""
		This function runs a series of system tools on Glass
		
		To make updating the changing available tools, use the array 'information' to make modifications
		
		Excluded Directories:
			/proc
			/dev
	"""
	directory = ["/acct", "/cache", "/charger", "/config", "/d", "/data", "/default.prop", "/etc", "/init", "/init.goldfish.rc", "/init.omap4430.bt.rc", "/init.omap4430.rc", "/init.omap4430.usb.rc", "/init.rc", "/mnt", "/res", "/root", "/sbin", "/sdcard", "/sys", "/system", "/ueventd,goldfish.rc", "ueventd.omap4430.rc",
	"/ueventd.rc", "/vendor"]
	y = len(directory)
	t = 0
	while t < y:
		fspull_cmd = "adb pull " + directory[t] + " ./" + outdir  + directory[t]
		subprocess.call([fspull_cmd], shell=True)
		t = t + 1
		
def zip_it_up(outdir):
	##zipping
	subprocess.call("tar cfvz %r.tgz %r" % (outdir,outdir), shell=True)
	subprocess.call("md5sum %r.tgz | tee %r.md5.txt" % (outdir,outdir), shell=True)
	print ("Acquisition Complete!")
	
	
"""
	Clear the command window and prepare prompt the user with some basic information. 
"""
subprocess.call("clear")
print("       _____ _       _   _                 _               ")
print("      |   __| |_ ___| |_| |_ ___ ___ ___ _| |              ")
print("      |__   |   | .'|  _|  _| -_|  _| -_| . |              ")
print("      |_____|_|_|__,|_| |_| |___|_| |___|___| \n")
shattered_version()
print("      Google Glass Forensic Tool\n\nBrought to you by:\nThe Leahy Center for Digital Investigation at Champlain College\nLearn more at http://lcdi.champlain.edu\n\nSpecial Thanks to Julie Desautels and Jon Rajewski for the research leading to the success of this script. \n\nCopyright 2013, Chapin Bryce \t GNU GLPv3\n\n")
print("Be sure to check http://code.google.com/p/shattered for frequent updates\n\n")

adb_path()

input("Ensure the device is connected via USB and you you are using root\npress ENTER to continue")
print("\n==================================================================\n")
subprocess.call("adb devices", shell=True)
input("If the device is present, press enter to continue or ^c to cancel")


#setup output
datetime = time.strftime("%Y%m%d%H%M%S")
casename = input ("Enter a Case Name: \t")
outdir = casename + '-' + datetime
sno = get_serialno()
prep_dir(outdir, sno)
outdir_sno = outdir + "/fs-" + sno

#run modules
dumpsys(outdir)
sysinfo(outdir)
fspull(outdir_sno)
zip_it_up(outdir)


print("Shattered Completed")
