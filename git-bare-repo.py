#!/usr/bin/python

import os
import commands as cmd
import sys

SCRIPT_NAME = 'create-repo.py'
DEFAULT_PATH = '/var/repositorio/'
FOLDERS = ('sb','vertiente','localizacion','cuenca','fealegria','bohemia','helpdesk','petrolera','siati')
GIT = [
# SANTA BARBARA
('sb','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/sb/solt-sbep2_src'),
# VERTIENTE
('vertiente','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/vertiente/solt-vz_cont_src'),
('vertiente','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/vertiente/solt-vz_rrhh_src'),
# LOCALIZACION
('localizacion','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/localizacion/fuente/solt_ec_cont_src'),
('localizacion','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/localizacion/fuente/solt_ec_rrhh_src'),
# FE Y ALEGRIA
('fealegria','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/fealegria/solt-fya_src'),
# BOHEMIA
('bohemia','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/bohemia/fuente/'),
# CUENCA
('cuenca','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/cuenca/solt-cuenca-src/'),
# HELPDESK
('helpdesk','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/helpdesk/fuente/solt-hel_src/'),
# PETROLERA
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-gd_src/'),
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-pet_src/'),
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-qual_src/'),
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-mtto_src/'),
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-prod_src/'),
('petrolera','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/petrolera/solt-we_src/'),
# SIATI
('siati','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/siati/addons-extra/'),
('siati','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/siati/addons-local/'),
('siati','git clone --bare /home/yaima/Documentos/Estudio/OpenERP/General/Repos/siati/localization_l10n_ec/'),
]

def install():
	if not os.path.exists('/usr/bin/gitrep'):
		if "root" in cmd.getoutput("whoami"):
			cwd = os.getcwd()
			os.chdir('/usr/bin')
			cmd.getoutput('ln -s '+cwd+'/'+SCRIPT_NAME+ ' gitrep')
			os.chdir(cwd)
			print "Instalacion terminada. Ejecuta sudo gitrep para crear los bares"
		else:
			print 'Error!: Necesitas permisos de sudo para instalar esta utilidad'
	else:
		print "Ya este programa esta instalado."

def create_repo_skeleton(path):
	if path[-1] != '/':
		path = path + '/'
	if os.path.exists(path):
		cmd.getoutput('sudo rm '+path+' -r')
	os.mkdir(path)
	os.chdir(path)
	cmd.getoutput('echo "Nodata" >> .nodata')
	for folder in FOLDERS:
		os.mkdir(folder)
		os.chdir(folder)
		cmd.getoutput('echo "Nodata" >> .nodata')	
		os.chdir('..')
	print cmd.getoutput('chmod 775 '+path+' -R')

def clone(path, folder, command):
	os.chdir(path+folder)
	print cmd.getoutput(command)


def clone_all(path):
	for line in GIT_TEST:
		clone(path,line[0],line[1])

if __name__ == '__main__':
	script, args = sys.argv[0], sys.argv[1:]
	if args and args[0] == '--install':
		install()
	else: 
		print 'Indique la ruta a crear del repo (por defecto en /var/repositorio/)'
		path = raw_input('La ruta debe terminar con /: ')
		if not path:
			path = DEFAULT_PATH
		create_repo_skeleton(path)
		clone_all(path)




















