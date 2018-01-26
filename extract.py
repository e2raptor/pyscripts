#!/usr/bin/python
import myapi

csv_lines = []
with open('partners.csv') as file:
    csv_lines = file.readlines()

class Record(object):
    """docstring for Record"""
    def __init__(self, center_id,company,inst,ced_ruc,db_id,name,person,id_type,customer,supplier,employee,taxpayer_type,active):
        self.center_id = center_id.replace('\n','')
        self.company = company.replace('\n','')
        self.inst = inst.replace('\n','')
        self.ced_ruc = ced_ruc.replace('\n','')
        self.db_id = db_id.replace('\n','')
        self.person = person.replace('\n','')
        self.id_type = id_type.replace('\n','')
        if self.id_type == 'cedula' or id_type=='CEDULA':
            self._check_cedula()
        if self.id_type == 'ruc' or id_type=='RUC':
            self._check_ruc()
        self.check_ced_ruc()
        self.name = name.replace('\n','')
        self.customer = "SI"
        self.supplier = "NO"
        self.employee = "NO"
        if customer == '0':
            self.customer = 'NO'
        if supplier == "1":
            self.supplier = "SI"
        if employee == "1":
            self.employee = "SI"
        self.taxpayer_type = taxpayer_type.replace('\n','')
        self.active = active.replace('\n','')

    def check_ced_ruc(self):
        if id_type == 'cedula' or id_type == 'pasaporte':
            self.person = ''
        if self.id_type == 'ruc':
            str_id = str(self.ced_ruc)
            if str_id[2] == '6':
                self.person = '06'
            elif str_id[2] == '9':
                self.person = '09'
            else:
                self.person = ''

    def _check_cedula(self):
        identificador = self.ced_ruc
        ultimos = identificador[10:13]
        #if len(identificador) == 13 and not ultimos == '001':
        if len(identificador) == 13 and ultimos == '000':
            self.ced_ruc = self.ced_ruc+'-BAD_CED-1'
            return False
        else:
            if len(identificador) < 10:
                if len(identificador) == 9:
                    # Le agrego 0 pero continuo comprobandolo
                    self.ced_ruc = '0'+self.ced_ruc
                    identificador = self.ced_ruc
                else:
                    self.ced_ruc = 'BAD_CED-1'
                    return False
        #Los primeros dos digitos corresponden al codigo de la provincia
        prov = identificador[0:2]
        provincia = int(prov)
        if provincia < 1 or provincia > 24:
            self.ced_ruc ='BAD_CED-3'
            return False

        coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        cedula = identificador[:9]
        suma = 0
        for c in cedula:
            val = int(c) * coef.pop()
            suma += val > 9 and val - 9 or val
        result = 10 - ((suma % 10) != 0 and suma % 10 or 10)
        if result == int(identificador[9:10]):
            return True
        else:
            self.ced_ruc ='BAD_CED-4'
            return False

    def _check_ruc(self):
        ruc = self.ced_ruc
        if not len(ruc) == 13:
            if len(ruc) == 12:
                self.ced_ruc = '0'+self.ced_ruc
                ruc = self.ced_ruc
            elif len(ruc) == 10:
                self.ced_ruc += '001'
                ruc = self.ced_ruc
            else:
                self.ced_ruc = 'BAD_RUC-1'
                return False

        suma = 0
        residuo = 0
        pri = False
        pub = False
        nat = False
        numeroProvincias = 24
        modulo = 11

        #Los primeros dos digitos corresponden al codigo de la provincia
        prov = ruc[0:2]
        provincia = int(prov)
        if provincia < 1 or provincia > numeroProvincias:
            self.ced_ruc = 'BAD_RUC-2'
            return False
        #alert('El codigo de la provincia (dos primeros digitos) es invalido');
        numero = ruc
        #Aqui almacenamos los digitos de la cedula en variables.
        d1 = int(numero[0])
        d2 = int(numero[1])
        d3 = int(numero[2])
        d4 = int(numero[3])
        d5 = int(numero[4])
        d6 = int(numero[5])
        d7 = int(numero[6])
        d8 = int(numero[7])
        d9 = int(numero[8])
        d10 = int(numero[9])

        #El tercer digito es:
        #9 para sociedades privadas y extranjeros (Persona Juridica)
        #6 para sociedades publicas
        #menor que 6 (0,1,2,3,4,5) para personas naturales

        if d3 == 7 or d3 == 8:
            self.ced_ruc = 'BAD_RUC-3'
            return False

        #Solo para personas naturales (modulo 10)
        if d3 < 6:
         nat = True
         p1 = d1 * 2
         if p1 >= 10:
             p1 -= 9
         p2 = d2 * 1
         if p2 >= 10:
             p2 -= 9
         p3 = d3 * 2
         if p3 >= 10:
             p3 -= 9
         p4 = d4 * 1
         if p4 >= 10:
             p4 -= 9
         p5 = d5 * 2
         if p5 >= 10:
             p5 -= 9
         p6 = d6 * 1
         if p6 >= 10:
             p6 -= 9
         p7 = d7 * 2
         if p7 >= 10:
             p7 -= 9
         p8 = d8 * 1
         if p8 >= 10:
             p8 -= 9
         p9 = d9 * 2
         if p9 >= 10:
             p9 -= 9
         modulo = 10

        #Solo para sociedades publicas (modulo 11)
        #Aqui el digito verficador esta en la posicion 9, en las otras 2 en la pos. 10
        elif d3 == 6:
         pub = True
         p1 = d1 * 3
         p2 = d2 * 2
         p3 = d3 * 7
         p4 = d4 * 6
         p5 = d5 * 5
         p6 = d6 * 4
         p7 = d7 * 3
         p8 = d8 * 2
         p9 = 0

        #Solo para entidades privadas (modulo 11)
        elif d3 == 9:
         pri = True
         p1 = d1 * 4
         p2 = d2 * 3
         p3 = d3 * 2
         p4 = d4 * 7
         p5 = d5 * 6
         p6 = d6 * 5
         p7 = d7 * 4
         p8 = d8 * 3
         p9 = d9 * 2

        suma = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
        residuo = suma % modulo

        #Si residuo=0, dig.ver.=0, caso contrario 10 - residuo
        if residuo == 0:
            digitoVerificador = 0
        else:
            digitoVerificador = modulo - residuo

        #ahora se compara el elemento de la posicion 10 con el dig. verificador
        if pub == True:
            if digitoVerificador != d9:
                self.ced_ruc = 'BAD_RUC-4'
                return False
            #alert('El ruc de la empresa del sector publico es incorrecto.');

            # los ultimos digitos no podran ser 0000 para las Instituciones publicas
            ultimo = numero[9] + numero[10] + numero[11] + numero[12]
            if ultimo == '0000':
                self.ced_ruc = 'BAD_RUC-5'
                return False
            #El ruc de las empresas del sector publico terminan con 0001
            #if ultimo != '0001':
            #    return False
            #alert('El ruc de la empresa del sector publico debe terminar con 0001');
        elif pri == True:
            if digitoVerificador != d10:
                self.ced_ruc = 'BAD_RUC-6'
                return False
                #alert('El ruc de la empresa del sector privado es incorrecto.')
            last = numero[10] + numero[11] + numero[12]
            #Los 3 ultimos digitos no podran ser 000 para las personas juridicas
            if last == '000':
                return False
                self.ced_ruc = 'BAD_RUC-7'
                #alert('El ruc de la empresa del sector privado debe terminar con 001')
        elif nat == True:
            if digitoVerificador != d10:
                self.ced_ruc = 'BAD_RUC-8'
                return False
                #alert('El numero de cedula de la persona natural es incorrecto.');
            last2 = numero[10] + numero[11] + numero[12]
            if len(numero) > 10 and last2 == '000':
                self.ced_ruc = 'BAD_RUC-9'
                return False
                #alert('El ruc de la persona natural debe terminar con 001');

        return True

suppliers_objs = []
customer_objs = []
employee_obj = []

#Centro_ID,Compania,Instituto,CedulaRUC,Database_ID,Nombre Representante,Persona,Tipo ID,Cliente,Proveedor,Empleado,Tipos de Contribuyentes,Activo
print 'Procesando csv.... go and take a cofee'
for rec_line in csv_lines:
    recorded = False
    #center_id,company,inst,ced_ruc,db_id,name,person,id_type,customer,supplier,employee,taxpayer_type,active = rec_line.split(',')
    name,id_type,ced_ruc= rec_line.split(':')
    #Parche temporal para los ruc de 9 digitos
    if len(ced_ruc) == 9:
        if ced_ruc[0] > 2:
            ced_ruc = '0'+ced_ruc
    print name
    #rec = Record(center_id,company,inst,ced_ruc,db_id,name,person,id_type,customer,supplier,employee,taxpayer_type,active)
    rec = Record('x','x','x',ced_ruc,'x',name,'x',id_type,'x','x','x','x','x')
    if rec.supplier == 'NO' and rec.employee == 'NO':
        name = rec.name.replace(' ','')
        name = myapi.sanitize(name)
        for elem in customer_objs:
            elem_name = elem.name.replace(' ','')
            elem_name = myapi.sanitize(elem_name)
            if elem_name == name:
                recorded = True
        if not recorded:
            customer_objs.append(rec)

lineal_customers_list = []

#lineal_customers_list.append('No.,Nombre Representante, Centro Educativo,Persona,Tipo ID,Cedula/RUC, Cliente, Proveedor, Empleado ,Tipos de Contribuyentes\n')
lineal_customers_list.append('No.,Nombre, Persona,Tipo ID,Cedula/RUC, Tipos de Contribuyentes\n')
count = 1
for c in customer_objs:
    line = '%s:%s:%s:%s\n' % (str(count), c.name, c.id_type, c.ced_ruc)
    line = '%s:%s:%s:%s\n' % (str(count), c.name, c.id_type, c.ced_ruc)
    count += 1
    lineal_customers_list.append(line)

with open('partners_modificados.csv','w') as file:
    file.writelines(lineal_customers_list)















