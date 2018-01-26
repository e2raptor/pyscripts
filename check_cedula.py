#!/usr/bin/python

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

def check_cedula(identificador):
    ident = int(identificador)
    ultimos = identificador[10:13]
    #if len(identificador) == 13 and not ultimos == '001':
    if len(identificador) == 13 and ultimos == '000':
        return False
    else:
        if len(identificador) < 10:
            return 'A'
    #Los primeros dos digitos corresponden al codigo de la provincia
    prov = identificador[0:2]
    provincia = int(prov)
    if provincia < 1 or provincia > 24:
        return False

    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    cedula = identificador[:9]
    suma = 0
    for c in cedula:
        val = int(c) * coef.pop()
        suma += val > 9 and val - 9 or val
    result = 10 - ((suma % 10) != 0 and suma % 10 or 10)
    if result == int(identificador[9:10]):
        return 'OK' 
    else:
        return result

lines = []
with open('cedulas.txt') as file:
    lines = file.readlines()

bad_ceds = []
for ced in lines:
    result = check_cedula(sanitize(ced))
    if result != 'OK':
        final =  sanitize(ced)+' result:'+str(result)+'\n'
        print final
        bad_ceds.append(final)

with open('bad_cedulas.txt','w') as file:
    file.writelines(bad_ceds)

