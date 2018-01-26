#!/usr/bin/python
import myapi as api
import os

payables = []
receivables = []

def process(value, line):
    res = ''
    aux = value.split(' ')
    if line == 'account':
        res = aux[1].split('"')[1]
    else:
        res = aux[5].split('"')[1]
    return res

receivable = False
payable = False

current_path = os.getcwd()
file_list = api.get_file_list(current_path,['xml'])
for file in file_list:
    file_content = []
    with open(file) as f:
        file_content = f.readlines()
    for line in file_content:
        if '<field name="code">2.1.1.03.01</field>' in line:
            payable = True
            index = file_content.index(line)
        elif '<field name="code">1.1.2.02.03.06</field>' in line:
            receivable = True
            index = file_content.index(line)
        if '</record>' in line and (receivable or payable):
            index_record = file_content.index(line)
            tupla = (process(file_content[index-1],'account'),
                     process(file_content[index_record-1],'company'))
            if payable:
                payables.append(tupla)
            else:
                receivables.append(tupla)
            receivable = False
            payable = False

partners_list = []
p_list = []
with open('/home/eduardo/Escritorio/id_suppliers.txt') as f:
    p_list = f.readlines()

for partner in p_list:
    partners_list.append(partner.replace('\n',''))

xml_record = []
xml_record.append('<?xml version="1.0" encoding="UTF-8"?>\n')
xml_record.append(' <openerp>\n')
xml_record.append('     <data noupdate="1">\n')
count = 1
for partner in partners_list:
    for account in payables:
        record_id = 'property_payable_'+str(count)
        xml_record.append('        <record forcecreate="True" id="%s" model="ir.property">\n' % record_id)
        xml_record.append('             <field name="name">property_account_payable</field>\n')
        xml_record.append('             <field name="fields_id" search="[(\'model\',\'=\',\'res.partner\'),(\'name\',\'=\',\'property_account_payable\')]"/>\n')
        xml_record.append('             <field eval="\'account.account,\'+str(ref(\'%s\'))" model="account.account" name="value"/>\n' % account[0])
        xml_record.append('             <field eval="\'res.partner,\'+str(ref(\'%s\'))" model="res.partner" name="res_id"/>\n' % partner)
        xml_record.append('             <field name="company_id" ref="%s"/>\n' % account[1])
        xml_record.append('        </record>\n')
        count += 1
xml_record.append('     </data>\n')
xml_record.append('</openerp>\n')

with open('/home/eduardo/Escritorio/partners_payable_accounts.xml','w') as file:
    file.writelines(xml_record)

xml_record = []
xml_record.append('<?xml version="1.0" encoding="UTF-8"?>\n')
xml_record.append(' <openerp>\n')
xml_record.append('     <data noupdate="1">\n')
count = 1
for partner in partners_list:
    for account in receivables:
        record_id = 'property_receivable_'+str(count)
        xml_record.append('        <record forcecreate="True" id="%s" model="ir.property">\n' % record_id)
        xml_record.append('             <field name="name">property_account_receivable</field>\n')
        xml_record.append('             <field name="fields_id" search="[(\'model\',\'=\',\'res.partner\'),(\'name\',\'=\',\'property_account_receivable\')]"/>\n')
        xml_record.append('             <field eval="\'account.account,\'+str(ref(\'%s\'))" model="account.account" name="value"/>\n' % account[0])
        xml_record.append('             <field eval="\'res.partner,\'+str(ref(\'%s\'))" model="res.partner" name="res_id"/>\n' % partner)
        xml_record.append('             <field name="company_id" ref="%s"/>\n' % account[1])
        xml_record.append('        </record>\n')
        count += 1
xml_record.append('     </data>\n')
xml_record.append('</openerp>\n')

with open('/home/eduardo/Escritorio/partners_receivable_accounts.xml','w') as file:
    file.writelines(xml_record)
