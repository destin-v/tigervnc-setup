# ------------------------------------------------------------------
# Description:  This script will install a virtual network server
#               on a remote machine (i.e. Amazon E2) and setup
#               TigerVNC as the forwarding server.  You need to run
#               this script from the server you plan to access.
#
# Usage:        > python setup-server
#
# Requirements: Ssh must already be setup between server and client.
#               Works on Ubuntu 18 and 20.  Not tested on any other
#               OS.
#
# Author:       William Li
# Date:         12-14-2021
# ------------------------------------------------------------------
from os import system

# update the package manager
system("sudo apt update")

# setup KDE Plasma (desktop environment)
# Select the KDE’s default sddm display manager and hit the OK button.
system("sudo apt install kubuntu-desktop")

# if you want to uninstall use the following command:
# system("sudo apt remove kubuntu-desktop --autoremove")

# setup virtual network server
system("sudo apt install tigervnc-standalone-server tigervnc-common")

# setup the VNC server
# you can choose to setup a password (can be empty)
system("vncserver")

# kill all opened ports by vncserver
system("vncserver -kill :*")

# copy the startup configuration file into .vnc directory
system("mkdir $HOME/.vnc")
system("cp xstartup $HOME/.vnc/")

# startup VNC server with xstartup settings
system("vncserver")
