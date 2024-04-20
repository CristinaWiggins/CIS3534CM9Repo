#!/usr/bin/env python3
# Cristina Wiggins
# 04/20/2024
# Edited for Git lab
# GPA 8: Working With Files
# networkFileRW.py
# Update routers and switches;
# Read equipment from a file, write updates & errors to file

#---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error: Unable to import the JSON module.")

#---->>>> Create file constants for the file names; file constants can be reused
#         There are 2 files to read this program: equip_r.txt and equip_s.txt
#         There are 2 files to write in this program: updated.txt and invalid.txt
EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# Function to get a valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

# Function to get a valid IP address
def getValidIP(invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPAddresses.append(ipAddress)  # Record invalid IP address
                print(SORRY)
                break
        else:
            return ipAddress
            # Don't need to return invalidIPAddresses list - it's an object
        

def main():

    ##---->>>> Open files here
    try:
        with open(EQUIP_R_FILE) as f_r, open(EQUIP_S_FILE) as f_s:
            routers = json.load(f_r)
            switches = json.load(f_s)
    except FileNotFoundError:
        print("One or more equipment files not found.")
        return

    # Dictionaries
    ##---->>>> Read the routers and addresses into the router dictionary
    print("Network Equipment Inventory\n")
    print("\tEquipment Name\tIP Address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)

    ##---->>>> Read the switches and addresses into the switches dictionary
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    updated = {}
    invalidIPAddresses = []

    while True:
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            break
        
        new_ip = getValidIP(invalidIPAddresses)  # Pass invalidIPAddresses list

        if 'r' in device:
            routers[device] = new_ip
        else:
            switches[device] = new_ip

        updated[device] = new_ip
        print(f"{device} was updated; the new IP address is {new_ip}")

    # User finished updating devices
    print("\nSummary:")
    print("Number of devices updated:", len(updated))
    print("Number of invalid addresses attempted:", len(invalidIPAddresses))

    ##---->>>> Write the updated equipment dictionary to a file
    try:
        with open(UPDATED_FILE, 'w') as f_updated:
            json.dump(updated, f_updated, indent=4)
        print(f"\nContents of the two output files:")
        print(f"{UPDATED_FILE}: {updated}")
    except IOError:
        print("\nError writing to updated equipment file.")

    ##---->>>> Write the list of invalid addresses to a file
    try:
        with open(INVALID_FILE, 'w') as f_invalid:
            json.dump(invalidIPAddresses, f_invalid, indent=4)
        print(f"{INVALID_FILE}: {invalidIPAddresses}")
    except IOError:
        print("Error writing to invalid addresses file.")

# Top-level scope check
if __name__ == "__main__":
    main()
