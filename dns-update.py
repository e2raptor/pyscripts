#!/usr/bin/python
from datetime import datetime
import os
import commands as cmd
import optparse
import sys


SCRIPT_NAME = 'dns-update.py'


def install():
    if not os.path.exists('/usr/bin/dns'):
        if "root" in cmd.getoutput("whoami"):
            cwd = os.getcwd()
            os.chdir('/usr/bin')
            cmd.getoutput('ln -s ' + cwd + '/' + SCRIPT_NAME + ' dns')
            os.chdir(cwd)
            print "Installation finished. Execute dns -h for help"
        else:
            print 'Error!: You need root privileges to install this program'
    else:
        "This program is already installed. Execute 'dns -h' for help"

def check_ip(ip):
	bytes = ip.split('.')
	if len(bytes) !=4:
		return False
	for byte in bytes:
		if len(byte) > 3:
			return False
		for num in byte:
			if num.isdigit():
				return False
	return True

def update_dns(name,ip):
	if "root" in cmd.getoutput("whoami"):
		if check_ip(ip):
			upd_line = ip+'	'+name+'\n'
			with open('/etc/hosts','w') as file:
				host_lines = file.readlines()
			for line in host_lines:
				if name in line:
					index = host_lines.index(line)
					host_lines.remove(line)
					host_lines.insert(index,upd_line)
			with open('/etc/hosts','w') as file:
				file.writelines(host_lines)
		else:
			"Not valid ip"

	else:
		print "You have not enough privileges to perform that action"		


def help():
	print "The utility is used like this:"
	print "dns name ip"
	print "Ex: dns edu_laptop 192.168.0.1"

if __name__ == '__main__':
	script, args = sys.argv[0], sys.argv[1:]
	if args:
		if args[0] == '-i':
			install()
		elif len(args) == 2:
			update_dns(args[0],args[1])
		else:
			print 'Only two parameters are required: name and ip'
	else:
		help()


		
	#search('asd',True)