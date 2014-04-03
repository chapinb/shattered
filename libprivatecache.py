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
    
    This script is built to parse private_cache artifacts from Google Glass in a forensic manner.
    
    Built at the LCDI at Champlain College. Learn More at http://lcdi.champlain.edu
    
    """

import os, re, sys, shutil

def pvtcache_version():
    """
    This function prints the version of the code.
    """
    version = 20140320
    print("Shattered Parser version: ", version)

def pvtcache_sorter(case_path, parser_folder):

    input_dir = case_path
    outputdir = parser_folder

    #define file names - OBSOLETE
    #p_files = re.compile("^p\_")
    #gi_msg_files = re.compile("^gi_.*MESSAGES")
    #gi_small_files = re.compile('^gi_.*SMALL')
    #bs_files = re.compile('^bs\_')
    #h_files = re.compile('^h_')
    #i_files = re.compile('^i_')

    #Create output directory structures
    png_cache = outputdir + "png_cache/"
    icon_cache = png_cache + "icon_cache/"
    screenshot = png_cache + "screenshot/"
    thumbnail = png_cache + "thumbnail/"
    html_searches = outputdir + "html_searches/"
    other_cache = outputdir + "other_cache_files/"
    
    try:
        os.mkdir(outputdir)
        os.mkdir(png_cache)
        os.mkdir(icon_cache)
        os.mkdir(screenshot)
        os.mkdir(thumbnail)
        os.mkdir(other_cache)
        os.mkdir(html_searches)
    except:
        pass
        #add method to print and save errors - ie directory already exists

    #iterrate through the private-cache and scan/process files
    for root, dirs, files in os.walk(input_dir):
        #print("Root: ", root)
        #print("dirs: ", dirs)
        #print("Files: ", files)

        #Sort files within
        for item in files:
            
            if item[:3] == "bs_":
                    print("Item name: ", item," is an empty file")
                    src = input_dir + item
                    copier = other_cache + item
                    shutil.copy(src, copier)
            elif item[:2] == "p_":
                print("Item name: ", item," is a PNG picture")
                src = input_dir + item
                copier = png_cache + item + ".png"
                shutil.copy(src, copier)
            elif item[:3] == "gi_":
                if item[15:] == ".SMALL":
                    print("Item name: ", item," is a binary file")
                    src = input_dir + item
                    copier = other_cache + item
                    shutil.copy(src, copier)
                elif item[15:] == ".MESSAGES":
                    print("Item name: ", item," is a text file")
                    src = input_dir + item
                    copier = other_cache + item + ".txt"
                    shutil.copy(src, copier)
            elif item[:2] == "i_":
                print("Item name: ", item," is an icon file")
                src = input_dir + item
                copier = icon_cache + item + ".png"
                shutil.copy(src, copier)
            elif item[:2] == "h_":
                print("Item name: ", item," is an html file")
                src = input_dir + item
                copier = html_searches + item + ".html"
                shutil.copy(src, copier)
            elif item[:3] == "ss_":
                print("Item name: ", item," is an PNG screenshot")
                src = input_dir + item
                copier = screenshot + item
                shutil.copy(src, copier)
            elif item[:3] == "t__":
                print("Item name: ", item," is an MP4 thumbnail")
                src = input_dir + item
                copier = thumbnail + item
                shutil.copy(src, copier)
            elif item[:2] == "t_":
                if item[28:] == "mp4":
                    print("Item name: ", item," is an MP4 thumbnail")
                    src = input_dir + item
                    copier = thumbnail + item
                    shutil.copy(src, copier)
                else:
                    print("Item name: ", item," is an JPEG thumbnail")
                    src = input_dir + item
                    copier = thumbnail + item + ".jpeg"
                    shutil.copy(src, copier)

                
                
            #add in escape opportunity in case where a new file type arises
            else:
                print("Error: found unknown file type")
                print("Please report to code.google.com/p/shattered!")
                input("Press enter to continue or ^c to exit")

    print ("Completed Processing the private cache")






