#!/usr/bin/python

import sys
import commands as cmd 
import os

SCRIPT_NAME = 'gnote-shortcut.py'

def install():
	if not os.path.exists('/usr/bin/nt') and not os.path.exists('/usr/bin/nn') and not os.path.exists('/usr/bin/on'):
		if "root" in cmd.getoutput("whoami"):
			cwd = os.getcwd()
			os.chdir('/usr/bin')
			cmd.getoutput('ln -s '+cwd+'/'+SCRIPT_NAME+ ' nn')
			cmd.getoutput('ln -s '+cwd+'/'+SCRIPT_NAME+ ' nt')
			cmd.getoutput('ln -s '+cwd+'/'+SCRIPT_NAME+ ' on')
			os.chdir(cwd)
			print "Installation finished!"
		else:
			print 'Error!: You need root privileges to install this program'
	else:
		"This program is already installed."

def search_string(text):
	ss = 'tomboy --search '
	if not text:
		print 'No text to search'
	else:
		null = cmd.getoutput(ss+text[0])

def new_note(text):
	ss = 'tomboy --new-note'
	if not text:
		null = cmd.getoutput(ss)
	else:
		null = cmd.getoutput(ss+' '+text[0])

def open_note(text):	
	ss = 'tomboy --open-note'
	if not text:
		print 'No note to open'
	else:
		null = cmd.getoutput(ss+' '+text[0])


script, args = sys.argv[0], sys.argv[1:]

if 'install' in args:
	install()

if 'nn' in script:
	new_note(args)

if 'nt' in script:
	search_string(args)

if 'on' in script:
	open_note(args)

