#!/usr/bin/python
import sys

"""
Este script lo hice cuando necsite procesar un catalogo de partners donde habian partners repetidos. Primero se usa el script
para detectar duplicados, luego con el resultado y el csv de los partners este script genera dos ficheros csv: 

El primer fichero contendra todas las tuplas de los partners no repetidos
El segundo contendra las tuplas unicas de los repetidos, o sea a lo mejor hay un partner que aparece repetido porque en una 
tupla es cliente y en la otra es proveedor, en este caso ambas tuplas apareceran, pero si hay dos tuplas con el mismo partner 
y ademas son exactamente iguales, solo aparecera una de ellas.
"""

def sanitize(value):
    '''
    Se usa para crear strings comparables y que
    puedan ser usadas como ids. Ejemplo:
    CADENA != cadena
    '''
    value = value.strip()
    value = value.replace('\xc3\x81', 'A')
    value = value.replace('\xc3\x89', 'E')
    value = value.replace('\xc3\x8d', 'I')
    value = value.replace('\xc3\x93', 'O')
    value = value.replace('\xc3\x9a', 'U')
    value = value.replace('\xc3\x91', 'N')
    value = value.replace('\xc3\xa1', 'a')
    value = value.replace('\xc3\xa9', 'e')
    value = value.replace('\xc3\xad', 'i')
    value = value.replace('\xc3\xb3', 'o')
    value = value.replace('\xc3\xba', 'u')
    value = value.replace('\xc3\xb1', 'n')
    value = value.lower()
    value = value.replace('.', '_')
    value = value.replace(' ', '_')
    value = value.replace('\n', '')
    value = value.replace('&', 'and')
    return value



def main(f_1, f_2):
    file_1 = []
    file_2= []
    repeated_dic = {}
    not_repeated = []
    with open(f_1) as file:
        file_1 = file.readlines()
    with open(f_2) as file:
        file_2 = file.readlines()
    sanitized_f1 = [sanitize(name) for name in file_1]

    for register in file_2:
        name = register.split(':')[1]
        print "Processing: %s" % name
        name = sanitize(name)
        if name in sanitized_f1:
            if not name in repeated_dic: 
                repeated_dic[name] = [register]
            else:
                if register not in repeated_dic[name]:
                    repeated_dic[name].append(register)
        else:
            not_repeated.append(register)

    # Save the not repeated
    with open('Not repeated.csv','w') as file:
        file.writelines(not_repeated)


    repeated_list = []
    for key in repeated_dic:
        repeated_list.extend(repeated_dic[key])

    # Save the repeated
    with open('Repeated.csv','w') as file:
        file.writelines(repeated_list)


if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    if len(args) == 2:
        main(args[0], args[1])
    else:
        print 'Numero incorrecto de argumentos'
        print 'Uso: ./split_tuples.py archivo1 archivo2'
