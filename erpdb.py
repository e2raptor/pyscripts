#!/usr/bin/env python
import psycopg2
from datetime import datetime
import sys
import pickle
import os
import commands as cmd
import optparse
import pprint
pp = pprint.pprint

SCRIPT_NAME = 'erpdb.py'
HOME_DIR = cmd.getoutput('echo $HOME')
DATA_FILE = HOME_DIR+'/.scripts_data/'+'erpdb.pkl'

def connect(params):
    database,user,password= params[0], params[1], False
    if len(params) == 3:
        password = params[2]
    conn_str = 'user=eduardo dbname='+database
    data = {'db':database,'user':user,'pass':password}
    save_data(data)

def db_on():
    data = load_data()
    if not data['db']:
        return False, False
    conn_str = 'dbname=%s user=%s' % (data['db'],data['user'])
    if data['pass']:
        conn_str = 'dbname=%s user=%s password=%s'% (data['db'],data['user'],data['pass'])
    connection = psycopg2.connect(conn_str)
    cr = connection.cursor()
    return data['db'], cr, connection

def db_off():
    data = load_data()
    db = data['db']
    data = {'db':False,'user':False,'pass':False}
    save_data(data)
    if db:
        print 'Connection closed with '+db
    else:
        print 'All conections are closed'

def convert_val(val,like=False):
    if not val.isdigit():
        if not like:
            val = "'"+val+"'"
        else:
             val = "'%"+val+"%'"
    return val

def create_query(params):
    model, wparams = params[0], params[1:]
    table = model.replace('.', '_')
    select = 'SELECT * FROM %s' % (table)
    where_list = []
    where = ''
    if wparams and wparams != '*':
        for p in wparams:
            add_join = False
            param = ''
            if '=' in p:
                wp,wv = p.split('=')
                param = wp+' = '+convert_val(wv)
                where_list.append(param)
                where_list.append('AND')
            if '+' in p:
                wp,wv = p.split('+')
                param = wp+' > '+convert_val(wv)
                where_list.append(param)
                where_list.append('AND')
            if '-' in p:
                wp,wv = p.split('-')
                param = wp+' < '+convert_val(wv)
                where_list.append(param)
                where_list.append('AND')
            elif '~' in p:
                wp,wv = p.split('~')
                param = wp+' like '+convert_val(wv,True)
                where_list.append(param)
                where_list.append('AND')
            elif p == 'o':
                param = 'OR'
                where_list.pop()
                where_list.append(param)
        where = ' WHERE'
        where_list.pop() #Delete the last AND
        for p in where_list:
            where = where +' '+p
    return select+where

def get(params):
    query = create_query(params)
    db,cr,connection = db_on()
    if not cr:
        print 'Not connection alive: Execute erpdb -c database'
    else:
        format = '| %-50s- %-60s |'
        cr.execute(query)
        cols = []
        for d in cr.description:
            cols.append(d[0])
        #print cols
        rows = cr.fetchall()
        if not rows:
            print '[%s] No record match the given criteria' % (db)
        else:
            print '***************************************************************************************************************'
            for t in rows:
                for pos in xrange(len(t)):
                    field = str(cols[pos])
                    value = str(t[pos])
                    if field not in ('create_uid','create_date','write_date','write_uid'):
                        if len(value) < 100:
                            if len(field) < 60:
                                print format % (field, value)
                print '***************************************************************************************************************'
        connection.close()

def save_data(data):
    handler = open(DATA_FILE, 'wb')
    pickle.dump(data, handler)
    handler.close()

def load_data():
    log = open(DATA_FILE, 'rb')
    data = pickle.load(log)
    log.close()
    return data

def show_database():
    data = load_data()
    if data['db']:
        print 'Opened database: '+data['db']
    else:
        print 'No open database'

def install():
    if not os.path.exists('/usr/bin/erpdb'):
        if "root" in cmd.getoutput("whoami"):
            cwd = os.getcwd()
            os.chdir('/usr/bin')
            cmd.getoutput('ln -s ' + cwd + '/' + SCRIPT_NAME + ' erpdb')
            os.chdir(HOME_DIR)
            if not os.path.exists(HOME_DIR+'/.scripts_data'):
                os.mkdir('.scripts_data')
            os.chdir(HOME_DIR+'/.scripts_data')
            data = {'db':False,'user':False,'pass':False}
            save_data(data)
            cmd.getoutput('chmod 777 '+DATA_FILE)
            os.chdir(cwd)
            print "Installation finished. Execute erpdb -h for help"
        else:
            print 'Error!: You need root privileges to install this program'
    else:
        "This program is already installed. Execute 'erpdb -h' for help"

def query(query):
    cr,connection = db_on()
    cr.execute(query)

def main():
    p = optparse.OptionParser(
        description=
            '''erpdb - Search data for a model/table in pgsql: erpdb model field1=val1 field2=val. Operators between field and val can be = (equal) ~ (like) + (bigger than >) - (lesser than < )

            ''',
                prog="erpdb",
                version="1.0",
                usage="%prog -options [arguments]")

    p.add_option('--install', '-i',action="store_true", help='Install this program. Require root privileges')
    p.add_option('--connect', '-c',action="store_true", help='Connect to a specified database: erpdb -c database user [password]')
    p.add_option('--close', '-x',action="store_true", help='Disconnect from database')
    p.add_option('--show', '-s',action="store_true", help='Show the open database')
    p.add_option('--query', '-q',action="store_true", help='Specify a query string')
    #p.add_option('--fields', '-f', action="store_true", help='Get the fields name for a model')

    options, arguments = p.parse_args()
    opt_dict = options

    if options.connect:
        connect(arguments)

    elif options.show:
        show_database()

    elif options.install:
        install()

    elif options.query:
        query(arguments[0])

    elif options.close:
        db_off()

    else:
        p.print_help()

if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    options = ('-i','--install','-c','--connect','-x','--close','-s','--show','-q','--query')
    if not args or args[0] in options:
        main()
    elif args[0] not in options:
        get(args)


