#!/usr/bin/python
import sys


def sanitize(value):
    '''
    Se usa para crear strings comparables y que
    puedan ser usadas como ids. Ejemplo:
    CADENA != cadena
    '''
    return value
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


def compare(FILE_1, FILE_2):
    with open(FILE_1) as f1:
        list_1 = f1.readlines()
    with open(FILE_2) as f2:
        list_2 = f2.readlines()

    sanitized_list1 =[]
    sanitized_list2 =[]
    sanitized_list1.extend(sanitize(elem) for elem in list_1)
    sanitized_list2.extend(sanitize(elem) for elem in list_2)


    repeated_list1 = []
    repeated_list1_count = 0
    repeated_list2 = []
    repeated_list2_count = 0
    aux_rep_l1 = []
    aux_rep_l2 = []

    #Chequear por elementos repetidos en las propias listas
    for elem in sanitized_list1:
        print "Chequando: %s en %s" % (elem, FILE_1)
        count = sanitized_list1.count(elem)
        if count > 1:
            elem_rep = list_1[sanitized_list1.index(elem)]
            if elem_rep not in aux_rep_l1:
                #Guardo el elemento original
                aux_rep_l1.append(elem_rep)
                #Guardo el elemento con la cantidad de veces que se repite
                repeated_list1.append(elem_rep.replace('\n',' ('+str(count)+')\n'))
                repeated_list1_count += count
                repeated_list1_count -= 1


    for elem in sanitized_list2:
        print "Chequando: %s en %s" % (elem,FILE_2)
        count = sanitized_list2.count(elem)
        if count > 1:
            elem_rep = list_2[sanitized_list2.index(elem)]
            if elem_rep not in aux_rep_l2:
                aux_rep_l2.append(elem_rep)
                repeated_list2.append(elem_rep.replace('\n',' ('+str(count)+')\n'))
                repeated_list2_count += count

    only_in_file_1 = []
    only_in_file_2 = []
    in_both_files = []

    for elem in sanitized_list1:
        normal_elem = list_1[sanitized_list1.index(elem)]
        if elem not in sanitized_list2:
            # Si ya el elemento esta en la lista no lo vuelvo a poner
            if normal_elem not in only_in_file_1:
                only_in_file_1.append(normal_elem)
        else:
            if normal_elem not in in_both_files:
                in_both_files.append(normal_elem)

    for elem in sanitized_list2:
        normal_elem = list_2[sanitized_list2.index(elem)]
        if elem not in sanitized_list1:
            if normal_elem not in only_in_file_2:
                only_in_file_2.append(normal_elem)


    with open('Resultados-Comparacion.txt', 'w') as f:
        if repeated_list1:
            f.write('====================\n')
            message = 'ELEMENTOS REPETIDOS DENTRO DE %s (Total: %s) \n' % (FILE_1, str(repeated_list1_count))
            f.write(message)
            f.write('====================\n')
            f.writelines(repeated_list1)
            f.write('\n\n')

        if repeated_list2:
            f.write('====================\n')
            message = 'ELEMENTOS REPETIDOS DENTRO DE %s (Total: %s) \n' % (FILE_2, str(repeated_list2_count))
            f.write(message)
            f.write('====================\n')
            f.writelines(repeated_list2)
            f.write('\n\n')

        f.write('====================\n')
        f.write('SOLO EN '+FILE_1+'\n')
        f.write('====================\n')
        f.writelines(only_in_file_1)
        f.write('\n\n')
        f.write('====================\n')
        f.write('SOLO EN '+FILE_2+'\n')
        f.write('====================\n')
        f.writelines(only_in_file_2)
        f.write('\n\n')
        f.write('====================\n')
        f.write('EN AMBOS ARCHIVOS\n')
        f.write('====================\n')
        f.writelines(in_both_files)

if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    if len(args) == 2:
        compare(args[0], args[1])
    else:
        print 'Numero incorrecto de argumentos'
        print 'Uso: ./duplicados.py archivo1 archivo2'
