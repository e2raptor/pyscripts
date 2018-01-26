#!/bin/sh
     
opcion=$1
param1=$2 
destino="/media/"
mia="EDU@R2"
upd="nod32v4.zip"
origen="/media/Datos/Install/Windows/update_nod32v4/"
 
if [ -z $param1 ]; then

	gcp --force --preserve=ownership $origen$upd $destino$mia
else
	gcp --force --preserve=ownership $origen$upd $destino$param1 
fi
echo "Copia terminada"
