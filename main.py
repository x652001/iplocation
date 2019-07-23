import requests
import sys

author = "Sam"
Edit_time = "2018/07/14"
version = "v1.5"

ip_tablenum = 18
info_tablenum = 26


###########
# InfoStr #
###########

# about the help
help_str="""
iplocation <ip> - check the ip's location
iplocation -a <ip_file> - check the ip's location of file
iplocation -h - this information
"""
# about this program
info="""
######################
# IP_Location_Finder #
######################
"""
print (info)

####################
# Master_Functions #
####################

# Get the IP's location
def get_location (ip):
    try:
        # Get ip if doesn't set
        if ip == "":
            ip_url = "https://ipinfo.io/ip"
            ip = requests.get(ip_url).text
            ip = ip.replace('\n','')
        #Get the location of this ip    
        geo_url = "https://ipinfo.io/"+ip+"/country"
        geo = requests.get(geo_url).text
        geo = geo.replace('\n','')

        #Check the GeoLocation ,if location is TW or SG ,set yellow print
        if geo == "TW" or geo == "SG":
            print ('\033[1;33m%s\033[1;m' %(ip.ljust(ip_tablenum)) +'\033[0;0m%s\033[0;m' %(geo))
            return
        print (ip.ljust(ip_tablenum)+geo)

    except requests.exceptions.ConnectionError:
        print(" - connection error")
        sys.exit()

    return

# Check the ip is availale
def chk_ip(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i,x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError as e:
            return False
    return True

# Read the file from host into mem
def readfile (location):
    try:
        print ("Loading the file".ljust(info_tablenum)+" : "+location+" - ",end="")
        ips = list()
        f = open(location,'r')
        for line in f.readlines():
            line = line.strip()
            ips.append(line)
        f.close()
        print("OK")
        return ips
    except FileNotFoundError:
        print("failed")
        print(" - No such file or directory")
        sys.exit()

# print the help_str from this code's head
def help():
    print (help_str)
    sys.exit()

# chk the ipinfo.io is alive
def chkconnection():
    print ("Version".ljust(info_tablenum)+" : "+version)
    print ("Soruce".ljust(info_tablenum)+" : ipinfo.io")
    print ("Check the connection".ljust(info_tablenum)+" : ",end="")
    try:
        res = requests.get("https://ipinfo.io/",timeout=3)
        print("OK")
    except requests.exceptions.ConnectionError:
        print("Failed")
        print(" - Connection Error")
        sys.exit()

# After get ip location from file,print the ip which is failed
def print_failip(ips):
    print ("")
    print ("Those IPs are failed")
    print ("==========================")
    for ip in ips:
        print (ip)
    return

# Creating Table and Print
def iplocation_table():
    print ("")
    print ("Starting check IP Location")
    print ("==========================")
    print ("IP".ljust(16)+"| Location")
    return

##################
# Slave Funtions #
##################

# Get IP location from file
# This function need master function :
# readfile,get_location,print_failip,iplocation table
def get_location_from_file(filename):
    #Load the file from host to mem
    try:
        ip_file = readfile(filename)
    except IndexError:
        help()
    iplocation_table()
    # Check the ip location one by one from file's string
    # If the string is empty ,just skip
    # If the string isn't empty but not ipaddr,save to the $fail_ips.
    for ip in ip_file:
        if ip == "":
            continue
        if chk_ip(ip) == False:
            fail_ips.append(str(ip))
            continue
        get_location(ip)
    # If the fail_ips have something , print the text tell user those are
    # invalid.
    if fail_ips :
        print_failip(fail_ips)
    print ("==========================")
    sys.exit()

# If the sys.argv is invalid ,tell user error
def invalid_option():
    print (" - This option is invalid : " +sys.argv[1])
    help()

#############
# Variables #
#############
fail_ips = []

############
# Starting #
############

# First Check the network is alive
chkconnection()

# If user dosen't type any argument , return the location from self
if len(sys.argv) < 2:
    iplocation_table()
    get_location("")
    sys.exit()

# If user type 1 argument like :
# iplocation -h        - print help
# iplocation -a        - print need filename
# iplocation 8.8.8.8   - get ip location for 8.8.8.8
# iplocation -(others) - invalid
# iplocation (others)  - invalid
if len(sys.argv) == 2:
    if sys.argv[1].startswith("-"):
        if sys.argv[1] == "-h":
            help()
        elif sys.argv[1] == "-a":
            print (" - You need type the filename")
            help()
        else:
            invalid_option()
    if chk_ip(sys.argv[1]) == False:
        print (" - "+sys.argv[1]+" is not IP")
        sys.exit()
    iplocation_table()
    get_location(sys.argv[1])

# If user type 2 argument like :
# iplocation -a <filename> - get iplocation from files
# iplocation -(others)     - invalid
# iplocation (others)      - invalid
if len(sys.argv) == 3:
    if sys.argv[1].startswith("-"):
        if sys.argv[1] == "-a":
            get_location_from_file(sys.argv[2])
        else:
            invalid_option()
    else:
        invalid_option()

if len(sys.argv) > 3:
    print (" - Too much options")
    sys.exit()

print ("")
