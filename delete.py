#!/usr/bin/python
eliminar = []
with open('resultados_comparacion.txt') as file:
    eliminar = file.readlines()


prductos_sup = []
prductos_sup_copy = []
with open('product_supplierinfo_data.xml') as file:
    productos_sup = file.readlines()

productos_sup_copy = productos_sup 

for e in eliminar:
    print 'Eliminando %s' % e
    for l in productos_sup:
        if e in l:
            pos = productos_sup.index(l)
            pos = pos - 4
            print 'Record: ' + productos_sup[pos]
            for x in xrange(6):
                productos_sup.pop(pos)

with open('productos_terminados.xml','w') as file:
    file.writelines(productos_sup)




