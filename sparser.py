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
    
    This script is built to parse artifacts from Google Glass in a forensic manner.
    
    Built at the LCDI at Champlain College. Learn More at http://lcdi.champlain.edu
    
    """

# Import Python
import os
import re
import sys

# Import Modules
from liblogcat import logcat_parser
from liblogcat import logcat_version
from libsqlite import sqlite_parser
from libsqlite import sqlite_version
from libprivatecache import pvtcache_version
from libprivatecache import pvtcache_sorter

def sparser_version():
    """
        This function prints the version of the code.
        """
    version = 20140226
    print("Shattered Parser version: ", version)


######### Main Program #########

os.popen("clear")
print("       _____ _       _   _                 _               ")
print("      |   __| |_ ___| |_| |_ ___ ___ ___ _| |              ")
print("      |__   |   | .'|  _|  _| -_|  _| -_| . |              ")
print("      |_____|_|_|__,|_| |_| |___|_| |___|___|           ")
print("             _____                     ")
print("            |  _  |___ ___ ___ ___ ___ ")
print("            |   __| .'|  _|_ -| -_|  _|")
print("            |__|  |__,|_| |___|___|_| \n ")

print("    Google Glass Forensic Tool\n\nBrought to you by:\nThe Leahy Center for Digital Investigation at Champlain College.\nLearn more at http://lcdi.champlain.edu \n\nCopyright 2013, Chapin Bryce \t GNU GLPv3\n")
print("Be sure to check http://code.google.com/p/shattered for frequent updates")

print("\n==================================================================\n")

print("This script does not require glass to be plugged in")
print("Please run this script on the same machine as the shattered output directory\n")

## Suite versions
print("Suite Versions\n--------------")
sparser_version()
logcat_version()
sqlite_version()
pvtcache_version()

print("\n==================================================================\n")


case_path = ""
print("Please enter full path and case folder")
case_path = input("ie. /home/user/Documents/shattered-20140226/ \n>>")

if os.path.exists(case_path):
    print("Case Directory Found")
else:
    print("Case Directory Not Found")
    sys.exit(0)

if case_path.endswith("/"):
    pass
else:
    case_path = case_path + "/"

parser_folder = case_path + "parser"
try:
    os.mkdir(parser_folder)
except:
    print("Failed Creating output folder. Does it exist already?")

fs_path = "No Data Dir Found"
for root, dirs, files in os.walk(case_path):

    for i in dirs:
        if i.startswith("fs-"):
            fs_path = i
if fs_path == "No Data Dir Found":
        print("No Data path, modules may not run correctly")
else:        
    print("File System Dump: " + fs_path + " Discovered")
    fs_path = case_path + "/" + fs_path + "/"

### Starting Logcat Parser ###
logcat_input = case_path + "logcat.txt"
logcat_output = parser_folder + "/" + "logcat_sparser.csv"

logcat_parser(logcat_input, logcat_output)

### Starting Timeline.db Parser ###

# Location of the database to process in the case folder
sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/timeline.db"

# names of the tables within the database
timelinedb_tables = ["timeline", "android_metadata", "entity", "pending_actions"]

#for loop to iterate each table in the database's table array
for database in timelinedb_tables:
    print("Processing timeline.db table: " + database)

    sqlite_outfile = parser_folder + "/timelinedb_" + database + "_sparser.csv"

    #Setup outfile & write header for each table in the database
    fout = open(sqlite_outfile, 'w')
    if database == "timeline":
        fout.write("_id,Creation Time,Modified Time,Display Time,Delivery Time,Expiration Time,Pin Time,Pin Score,Is Deleted,Sync Status,Sync Protocol,Bundle ID,Bundle Cover Status,Source,Protobuf Blob\n")
        fout.close()
    elif database == "android_metadata":
        fout.write("locale\n")
        fout.close()
    elif database == "entity":
        fout.write("_id,entityId,entityType,timelineId\n")
        fout.close()
    elif database == "pending_actions":
        fout.write("_id,timeline_id,action_type,payload\n")
        fout.close()
    else:
        print("Unexpected table in database")
        
    try:
        sqlite_parser(sqlite_infile, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database timeline.db")

### Starting entity.db Parser ###

sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/entity.db"

entitydb_tables = ["android_metadata", "entity"]

for database in entitydb_tables:
    print("Processing entity.db table: " + database)

    sqlite_outfile = parser_folder + "/entitydb_" + database + "_sparser.csv"

    #Setup outfile & write header
    fout = open(sqlite_outfile, 'w')
    if database == "entity":
        fout.write("_id,source,is_share_target,is_communication_target,can_hangout,share_priority,share_count,share_time,phone_number,secondary_phone_numbers,email,display_name,image_url,type,obfuscated_gaia_id,is_in_my_contacts,protobuf_blob\n")
        fout.close()
    elif database == "android_metadata":
        fout.write("locale\n")
        fout.close()
    else:
        print("Unexpected table in database")
        
    try:
        sqlite_parser(sqlite_infiles, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database entity.db")

### Starting homemenuitems.db Parser ###
sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/homemenuitems.db"

entitydb_tables = ["android_metadata", "usage_stats"]

for database in entitydb_tables:
    print("Processing homemenuitems.db table: " + database)

    sqlite_outfile = parser_folder + "/homemenuitemsdb_" + database + "_sparser.csv"

    #Setup outfile & write header
    fout = open(sqlite_outfile, 'w')
    if database == "usage_stats":
        fout.write("command_literal,install_time,last_used_time,usage_count\n")
        fout.close()
    elif database == "android_metadata":
        fout.write("locale\n")
        fout.close()
    else:
        print("Unexpected table in database")
        
    try:
        sqlite_parser(sqlite_infile, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database homemenuitems.db")

### Starting sync_window.db Parser ###
sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/sync_window.db"

entitydb_tables = ["android_metadata", "sync_window", "write_timestamp"]

for database in entitydb_tables:
    print("Processing sync_window.db table: " + database)

    sqlite_outfile = parser_folder + "/sync_window.db_" + database + "_sparser.csv"

    # Setup outfile & write header
    fout = open(sqlite_outfile, 'w')
    if database == "sync_window":
        fout.write("start_time,continuation_token\n")
        fout.close()
    elif database == "android_metadata":
        fout.write("locale\n")
        fout.close()
    elif database == "write_timestamp":
        fout.write("id,timestamp\n")
        fout.close()
    else:
        print("Unexpected table in database")
        
    try:
        sqlite_parser(sqlite_infile, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database sync_window.db")

### Starting webview.db Parser ###
sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/webview.db"

entitydb_tables = ["android_metadata", "formurl", "formdata", "password", "httpauth"]

for database in entitydb_tables:
    print("Processing webview.db table: " + database)

    sqlite_outfile = parser_folder + "/webview.db_" + database + "_sparser.csv"

    # Setup outfile & write header
    fout = open(sqlite_outfile, 'w')
    if database == "formurl":
        fout.write("_id,url\n")
        fout.close()
    elif database == "android_metadata":
        fout.write("locale\n")
        fout.close()
    elif database == "password":
        fout.write("_id,host,username,password\n")
        fout.close()
    elif database == "formdata":
        fout.write("_id,urlid,name,value\n")
        fout.close()
    elif database == "httpauth":
        fout.write("id,timestamp\n")
        fout.close()
    else:
        print("Unexpected table in database")
        
    try:
        sqlite_parser(sqlite_infile, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database webview.db")


### Starting webviewCookiesChromium.db Parser ###

sqlite_infile = fs_path + "data/data/com.google.glass.home/databases/webviewCookiesChromium.db"

entitydb_tables = ["cookies", "meta"]

for database in entitydb_tables:
    print("Processing webviewCookiesChromium.db table: " + database)

    sqlite_outfile = parser_folder + "/webviewCookiesChromium.db_" + database + "_sparser.csv"

    # Setup outfile & write header
    fout = open(sqlite_outfile, 'w')
    if database == "cookies":
        fout.write("creation_utc,host_key,name,value,path,expires_utc,secure,httponly,last_access_utc\n")
        fout.close()
    elif database == "meta":
        fout.write("key,value\n")
        fout.close()
    else:
        print("Unexpected table in database")

    try:
        sqlite_parser(sqlite_infile, sqlite_outfile, database)
    except:
        print("Unable to parse table " + database + " in database webviewCookiesChromium.db")

######################################
### Starting to sort private cache ###
######################################
pvtcache_input = fs_path + "data/private-cache/"
pvtcache_output = parser_folder + "/private-cache/"
pvtcache_sorter(pvtcache_input, pvtcache_output)
