 #!/usr/bin/python
 
account_list = []
match_dict = {}
lines = []
with open('accounts.txt') as file:
    lines = file.readlines()

def remove_endl(n):
    return n.replace('\n','')

account_list = map(remove_endl, lines)
parent_dict = {}

# This code is for getting the parent to each account
num_code = 1
for parent in account_list:
    parent = parent.split(';')[0]
    parent_dots = parent.count('.')
    for acc in account_list:
        acc = acc.split(';')[0]
        acc_dots = acc.count('.') - 1
        if acc != parent:
            if parent in acc and parent_dots == acc_dots:
                if not parent in parent_dict:
                    parent_dict[parent] = [acc]
                else:
                    if acc not in parent_dict[parent]:
                        parent_dict[parent].append(acc)
                match_dict[acc] = {'parent':parent, 
                                    'name':'', 
                                    'type':'', 
                                    'user_type':'', 
                                    'parent_code':False,
                                    'num_code':str(num_code)+'V2'}
                num_code += 1

#Set the parent code alias
for parent in parent_dict:
    parent_code = parent
    if parent.count('.') > 2:
        parent_code = match_dict[parent]['num_code']
    for child in parent_dict[parent]:
        match_dict[child]['parent_code'] = parent_code

# And this one is to set the name based on the parent name
'''
2 dots = Parent name
3 dots = Aux.1
4 dots = Aux.2
5 dots = Aux.3
'''

#Get those who are view
for acc in match_dict:
    # Si esta en los padres es vista:
    if parent_dict.get(acc,False):
        match_dict[acc]['type']='Vista'
    else:
        parent_code = acc.split('.')
        if parent_code[0] == '124' and parent_code[1]=='83':
            match_dict[acc]['type']='Por cobrar'
        elif parent_code[0] == '124' and parent_code[1]=='85':
            match_dict[acc]['type']='Por cobrar'
        elif parent_code[0] == '224' and parent_code[1]=='83':
            match_dict[acc]['type']='Por pagar'
        elif parent_code[0] == '224' and parent_code[1]=='85':
            match_dict[acc]['type']='Por pagar'
        else:
            match_dict[acc]['type']='Regular'


for acc in account_list:
    parent, name = acc.split(';')
    parent_dots = parent.count('.')
    # Get the childs
    if parent in parent_dict:
        for child in parent_dict[parent]:
            if child+';' in account_list:
                index = account_list.index(child+';')
                account_list[index] = child+';'+name
                if parent_dots == 2:
                    match_dict[child]['name'] = name+' - Auxiliar 1'
                if parent_dots == 3:
                    match_dict[child]['name'] = name+' - Auxiliar 2'
                if parent_dots == 4:
                    match_dict[child]['name'] = name+' - Auxiliar 3'


final_list = []
codes = [code for code in match_dict]
codes = sorted(codes)
for code in codes:
    line = '%s;%s;%s;%s;%s;%s\n' %\
            (
            match_dict[code]['parent_code'], 
            match_dict[code]['parent'], 
            code, 
            match_dict[code]['num_code'], 
            match_dict[code]['name'], 
            match_dict[code]['type'])
    final_list.append(line)

with open('parents_match.csv','w') as file:
    file.writelines(final_list)
