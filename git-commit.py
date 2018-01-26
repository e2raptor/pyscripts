#!/usr/bin/python
from datetime import datetime
import sys
import pickle
import os
import commands as cmd
import optparse

SCRIPT_NAME = 'git-commit.py'
HOME_DIR = cmd.getoutput('echo $HOME')
DATA_FILE = HOME_DIR+'/.scripts_data/'+'gcommit.pkl'


def install():
    if not os.path.exists('/usr/bin/gcommit'):
        if "root" in cmd.getoutput("whoami"):
            cwd = os.getcwd()
            os.chdir('/usr/bin')
            cmd.getoutput('ln -s ' + cwd + '/' + SCRIPT_NAME + ' gcommit')
            os.chdir(HOME_DIR)
            if not os.path.exists(HOME_DIR+'.scripts_data'):
            	os.mkdir('.scripts_data')
            data = []
            save_data(data)        
            cmd.getoutput('chmod 777 '+DATA_FILE)               
            os.chdir(cwd)
            print "Installation finished. Execute gcommit -h for help"
        else:
            print 'Error!: You need root privileges to install this program'
    else:
        "This program is already installed. Execute 'gcommit -h' for help"


def save_data(data):
	handler = open(DATA_FILE, 'wb')
	pickle.dump(data, handler)
	handler.close()	

def load_data():
	log = open(DATA_FILE, 'rb')
	data = pickle.load(log)
	log.close()	
	return data

def get_prefix():
	prefix = False
	cwd = os.getcwd()
	data = load_data()
	if data:
		for d in data:
			if cwd == d[0]:
				prefix = d[1]
	return prefix

def set_prefix(prefix):
	cwd = os.getcwd()
	d = (cwd,prefix.strip())
	assigned = False
	data = load_data()
	for dt in data:
		if dt[0] == cwd:
			print "El directorio tiene asignado el prefijo: '"+dt[1]+"'"
			assigned = True
	if not assigned:
		data.append(d)
		save_data(data)

def remove_prefix():
	cwd = os.getcwd()
	data = load_data()
	if data:
		for d in data:
			if cwd == d[0]:
				data.remove(d)
	save_data(data)
	return True

def execute_commit(message,option_a):
	prefix = get_prefix()
	if prefix:	
		message = prefix+' '+message
	git_cmd = "git commit"
	options_cmd = ' -am '
	if not option_a:
		options_cmd = ' -m '
	command = git_cmd+options_cmd+"'"+message+"'"
	print 'Ejecutando: '+command
	print cmd.getoutput(command)
	# print command

def do_commit(message,option_a=True):
	final = False
	for m in message:
		if not final:
			final = m
		else:
			final = final+' '+m
	execute_commit(final,option_a)	

def set_message():
	message = raw_input('Mensaje del commit: ')
	execute_commit(message,True)

def show_prefixes():
	data = load_data()
	print 'Prefijos usados y sus directorios:'
	if not data:
		print 'No hay prefijos directorios con prefijos configurados'
	for d in data:
		print d[1]+' '+d[0]



def main(message_only=False):

	p = optparse.OptionParser(
        description=
        """Equivale a git commit -am 'mensaje'. Permite especificar prefijos para commits en directorios 
especificos, de manera tal que no haga falta recordar luego poner dicho prefijo en el mensaje. 
Ademas se puede poner el mensaje del commit sin comillas y sin las opciones -am.
           """,
        prog="gcommit",
        version="1.0",
        usage="%prog -options [arguments]")

	p.add_option('--install', '-i', action="store_true", help='Install this program. Require root privileges')
	p.add_option('--remove', '-r', action="store_true", help='Obtiene del repo (equivale al pull)')
	p.add_option('--show', '-s', action="store_true", help='Obtiene del repo (equivale al pull)')
	p.add_option('--message', '-m', action="store_true", help='Indica que solo use la opcion -m en vez de -am')
	p.add_option('--prefix', '-p', action="store_true", help='Indica un prefijo para los commits de este directorio')


	options, arguments = p.parse_args()
	opt_dict = options

	if not message_only:
		if options.install:
			install()

		elif options.prefix:
			set_prefix(arguments[0])

		elif options.show:
			show_prefixes()

		elif options.remove:
			remove_prefix()

		elif options.message:
			do_commit(arguments,False)

	else:
		do_commit(message_only)

if __name__ == '__main__':
	script, args = sys.argv[0], sys.argv[1:]
	options = ( '-i','--install',
				'-r','--add-dir',
				'-p','--del-dir',
				'-s','--show',
				'-m','--message')
	if not args:
		set_message()
	elif args[0] in options:
		main()
	elif args[0] not in options:
		main(args)

