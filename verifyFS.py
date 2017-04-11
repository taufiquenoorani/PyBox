#Program by Taufique

import clc
import paramiko
import sys
import time
import colorama

colorama.init()

#Color coding the output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Set credentials.  These are the same credentials used to login to the web UI (https://control.ctl.io)

clc.v1.SetCredentials("8ca3a7e4e7834882a443fa0c672c82d3","65l)inf2KKD-K7D(")

print bcolors.HEADER + bcolors.BOLD + "Verifying disk I/O errors" + bcolors.ENDC
# Read file
with open('C:/Users/taufique.noorani/Documents/clc/servers.txt', 'r') as servlist:
    for line in servlist:
	clclist = line.split()
        print "\n" + bcolors.UNDERLINE + str(clclist) + bcolors.ENDC
	
	#Get Credentials
	getCreds = clc.v1.Server.GetCredentials(servers=clclist,alias=None)
	creds = getCreds[0]['Password']

	#Get IP address
	getIp = clc.v1.Server.GetServerDetails(alias=None, servers=clclist)
	ipaddr = getIp[0]['IPAddress']

	#Login and touch the file
	#Setting parameters like host IP, username, and passwd
	HOST = ipaddr 
	USER = "root"
	PASS = creds
	#A function that logins and execute commands
	def fn():
		for ips in getIp:
  			#Connect to server
  			try:
				command = 'if [ -w {filename} ]; then echo OK!; else echo NOT OK; fi;'
        	                command = command.format(filename='/etc/passwd')
	                        client1=paramiko.SSHClient()
                	        #Add missing client key
                        	client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        	#connect to server
				client1.connect(HOST,username=USER,password=PASS,timeout=2)
			except Exception, e:
        			print bcolors.FAIL + "[-] Connection Failed. Probably Offline" + bcolors.ENDC
				continue
			#Gather commands and read the output from stdout
			try:
  				stdin, stdout, stderr = client1.exec_command(command)
				result = stdout.readline().rstrip()
  				print bcolors.OKGREEN + result + bcolors.ENDC
			except:
				print bcolors.FAIL + 'FAILED' + stderr.read() + bcolors.ENDC
  			client1.close()

	showOut = fn()
