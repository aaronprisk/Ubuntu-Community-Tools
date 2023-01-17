#!/bin/python
# Ubuntu Planet Launchpad ID Checker
import sys
import requests
import urllib.request
from configparser import ConfigParser
from launchpadlib.launchpad import Launchpad

# Open Planet INI file
conf_url = "https://bazaar.launchpad.net/~planet-ubuntu/config/main/download/head:/config.ini"
urllib.request.urlretrieve(conf_url, "conf.ini")  
parser = ConfigParser(interpolation=None)
parser.read("conf.ini")

# Connect to Launchpad
launchpad = Launchpad.login_with('community-email-list-generator', 'production', version='devel')
people = launchpad.people

# Generate list of names and email addresses
print("Creating email lists...")
poslist = open("existing-id-list.txt", "w")
neglist = open("missing-id-list.txt", "w")

# Check each member of Planet Ubuntu config for a registered Launchpad account
print("Checking Launchpad for accounts that match Ubuntu Planet nicknames...")
for section in parser.sections():     
    for key, values,in parser.items(section):
        if key == 'nick':
            try:
                print("Checking user ID: " + values)
                user = people[values]
                print(user.preferred_email_address.email)
                poslist.write(user.preferred_email_address.email + '\n')
            except:
                print("User ID " + values + " not found in Launchpad")
                neglist.write(values + '\n')

# Close email list files
print("Check has completed. Generated lists saved to current working directory.")
poslist.close()
neglist.close()