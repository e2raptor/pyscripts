#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import commands

if len(sys.argv) > 1:
	value = sys.argv[1]
	if value == "On" or value == "Off":
		with open("/etc/php5/apache2/php.ini") as file:
			data = file.readlines()
		
		try:
			pos = data.index("display_errors = Off\n")
			succed_value = "display_errors = Off\n"
		except:
			pos = data.index("display_errors = On\n")
			succed_value = "display_errors = On\n"
	
		data.remove(succed_value)
		data.insert(pos,"display_errors = "+value+"\n")

		with open("/etc/php5/apache2/php.ini",'w') as file:
			file.writelines(data)
		
		print "PHP display_errors is "+value
		print "Reiniciando apache ..."
		nullout = commands.getoutput("service apache2 restart")
		print "Hecho"		
	else:
		print "Uso: phperror On/Off"
else:
	print "Uso: phperror On/Off"


