#!/usr/bin/python

import commands
import optparse
import os
import sys

SCRIPT_NAME = 'delete_trash_files.py'
EXCLUDED_EXTENSIONS = ('pyc','xml~','py~','csv~','txt~','po~','txt~','yml~','conf~','config~','cfg~','c~','cpp~','h~','sh~','ini~','swp','.DS_Store','Thumbs.db')

def install():
	if not os.path.exists('/usr/bin/clean'):
		if "root" in commands.getoutput("whoami"):
			cwd = os.getcwd()
			os.chdir('/usr/bin')
			commands.getoutput('ln -s '+cwd+'/'+SCRIPT_NAME+ ' clean')
			os.chdir(cwd)
			print "Installation finished. Execute clean -h for help"
		else:
			print 'Error!: You need root privileges to install this program'
	else:
		"This program is already installed. Execute 'clean -h' for help"

def has_extension(filename):
    for excluded in EXCLUDED_EXTENSIONS:
        if '.'+excluded in filename:
            return True
    return False

def delete_trash_files(path_to_search='.'):
    to_delete = []
    for dirpath, dirnames, filenames in os.walk(path_to_search):
        for filename in filenames:
            if has_extension(filename):
                to_delete.append(os.path.join(dirpath,filename))
    if to_delete:
        for trash in to_delete:
            print "Archivo eliminado: " + trash 
            os.unlink(trash)
    else:
        print "No se han encontrado archivos basura"


if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    options = ('-i','-h')
    if args and args[0] not in options:
        print "Opcion desconocida. Solo -h para ver las extensiones y -i para instalar." 
    if not args:
        delete_trash_files()
    if args and args[0] == '-i':
        install()
    if args and args[0] == '-h':
        print "La archivos con las siguientes extensiones seran eliminados de manera recursiva en el dir actual:" 
        print ", ".join(EXCLUDED_EXTENSIONS)
