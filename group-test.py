#!/usr/bin/python
'''
Este script es para probar el algoritmo de agrupamiento que utilice en el modulo
Compras de Cuenca para agrupar bajo distintos criterios las solicitudes de compras segun
el contenido de las lineas de requerimientos.
'''
import pprint


class objeto:
    def __init__(self, proveedor, dependencia, partida, naturaleza):
        self.codigo = proveedor + '-' + dependencia + '-' + partida + '-' + naturaleza
        self.proveedor = proveedor
        self.dependencia = dependencia
        self.partida = partida
        self.naturaleza = naturaleza

    def __str__(self):
        return self.codigo

def group_criteria(obj,criteria):
    value = False
    if criteria == 'supplier':
        value = obj.proveedor
    elif criteria == 'dependency':
        value = obj.dependencia
    elif criteria == 'budget':
        value = obj.partida
    elif criteria == 'nature':
        value = obj.naturaleza
    return value

def has_same_criteria_value(req_list, criteria):
    """
        :param cr: database cursor
        :param uid: current user id
        :param req_list: List of requirements lines
        :param criteria: supplier,dependency,budget,nature
        :rtype: True if all lines meet the same criteria

        Search for each line in the list, if they meet the same criteria value.
    """
    elem = group_criteria(req_list[0],criteria)
    for obj in req_list:
        valor = group_criteria(obj,criteria)
        if elem != valor:
            return False
    return True

def meet_criteria(candidate_request, condition):
    """
        :param cr: database cursor
        :param uid: current user id
        :param req_list: List of candidate requests
        :param criteria: supplier,dependency,budget,nature
        :rtype: True if all lines meet the same criteria

        Checks for each candidate_request (list of requirement lines) if they
        requirements lines meet the same value of group criteria
    """
    for elem in candidate_request:
        if not has_same_criteria_value(elem, condition):
            return False
    return True

def create_requests(purchase_requests, criteria):
    while not meet_criteria(purchase_requests, criteria):
        if has_same_criteria_value(purchase_requests[0], criteria):
            purchase_requests.append(purchase_requests[0])
            purchase_requests.remove(purchase_requests[0])
        else:
            purchases_requests_dict = create_requests_dict(purchase_requests[0], criteria)
            for elem in purchases_requests_dict.itervalues():
                purchase_requests.append(elem)
            purchase_requests.remove(purchase_requests[0])

def create_requests_dict(requirement_lines_list, condition):
    """
        :param cr: database cursor
        :param uid: current user id
        :param req_list: List of candidate requests
        :param criteria: supplier,dependency,budget,nature
        :rtype: dict with unique criteria keys and respective values

        Search the specified criteria value for each line, and group them below
        a key that represent all the lines for that criteria value.
    """
    key_list = []
    for line in requirement_lines_list:
        valor = group_criteria(line, condition)
        if valor not in key_list:
            key_list.append(valor)
    purchases_requests_dict = dict.fromkeys(key_list, False)

    for line in requirement_lines_list:
        valor = group_criteria(line, condition)
        tmp = []
        if not purchases_requests_dict[valor]:
            tmp.append(line)
            purchases_requests_dict[valor] = tmp
        else:
            purchases_requests_dict[valor].append(line)
    return purchases_requests_dict

ob1 = objeto('proveedor1', 'dependencia1', 'partida1', 'naturaleza1')
ob2 = objeto('proveedor1', 'dependencia2', 'partida1', 'naturaleza1')
ob3 = objeto('proveedor2', 'dependencia1', 'partida1', 'naturaleza2')
ob4 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza1')
ob5 = objeto('proveedor1', 'dependencia1', 'partida1', 'naturaleza1')
ob6 = objeto('proveedor2', 'dependencia2', 'partida2', 'naturaleza5')
ob7 = objeto('proveedor4', 'dependencia1', 'partida1', 'naturaleza1')
ob8 = objeto('proveedor5', 'dependencia3', 'partida1', 'naturaleza3')
ob9 = objeto('proveedor5', 'dependencia1', 'partida2', 'naturaleza1')
ob10 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob11 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob12 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob13 = objeto('proveedor3', 'dependencia9', 'partida1', 'naturaleza4')
ob14 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob15 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza1')
ob16 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob17 = objeto('proveedor2', 'dependencia2', 'partida2', 'naturaleza5')
ob18 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob19 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza4')
ob20 = objeto('proveedor3', 'dependencia1', 'partida1', 'naturaleza24')

lista_ob = [ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10, ob11, ob12, ob13, ob14, ob15, ob16, ob17, ob18, ob19, ob20,]
lista_ob = [lista_ob]

create_requests(lista_ob, 'supplier')
create_requests(lista_ob, 'dependency')
create_requests(lista_ob, 'budget')
create_requests(lista_ob, 'nature')

count = 1
for elem in lista_ob:
    print 'Solicitud '+str(count)
    count += 1
    for obj in elem:
        print obj
