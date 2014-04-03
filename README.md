Shattered
=========

#####*Google Glass Acquisition and Analysis Tool*

##Overview


Google Glass is a revolutionary technology capable of many mobile device functions including taking pictures and videos, pulling data from the internet, getting directions, and so much more. Essentially Glass is an extension of your mobile phone. 

With this much data being streamed in and out of glass, there must be data left behind. With Locard's principle in mind, we designed Shattered: Google Glass acquisition and processing tool. 

Learn more about the Shattered project at the Champlain College Senator Patrick Leahy Center for Digital Investigations (LCDI) Blog http://computerforensics.champlain.edu/blog

For additional research on Google Glass, visit http://chapinbryce.com & http://desautelsja.blogspot.com/

###Code

*The latest code is available at GitHub https://github.com/4n6kid/shattered*

Download the latest code via git:

    git clone https://github.com/4n6kid/shattered.git

###Dependencies

Use the Setup script located in the Source tab to download the latest dependencies.

*The setup script only works for debian based linux systems.*

####Manual Dependency Installation
Linux & OSX
____

Download the ADT (20131030) bundle from http://developer.android.com/sdk/index.html

Unzip the Android SDK and place the tool *adb* in `/usr/local/bin/`

Run the script by typing `./shattered.py`

*OSX does not run the md5sm at this time after zipping the .tar.gz*


Windows
____

*Running in Windows is very buggy at this stage. If possible use a debian virtual machine to run this code. More stability in future versions*

    git clone https://github.com/4n6kid/shattered.git
    
Download the ADT (20131030) bundle from http://developer.android.com/sdk/index.html

Unzip the Android SDK and place the tool *adb* in the same directory as shattered.py

Run the script by typing `./shattered.py`

###Developer Notes

Shattered is in its alpha stage. Please report any bugs or feature requests to the issues section of GitHub
