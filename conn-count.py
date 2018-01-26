#!/usr/bin/python
from datetime import datetime
import pickle
import os
import commands as cmd
import optparse


SCRIPT_NAME = 'conn-count.py'


def install():
    if not os.path.exists('/usr/bin/cct'):
        if "root" in cmd.getoutput("whoami"):
            cwd = os.getcwd()
            os.chdir('/usr/bin')
            cmd.getoutput('ln -s ' + cwd + '/' + SCRIPT_NAME + ' cct')
            os.chdir(cwd)
            data = []
            log = open('log.pkl', 'wb')
            pickle.dump(data, log)
            log.close()
            print "Installation finished. Execute cc -h for help"
        else:
            print 'Error!: You need root privileges to install this program'
    else:
        "This program is already installed. Execute 'cct -h' for help"


def get_output():
    out = cmd.getoutput('tail /var/log/syslog')
    print out


def get_date():
    today = datetime.today()
    date, rest = str(today).split(' ')
    return date


def was_conected():
    return True


def timer():
    data = []
    segundos = 0
    started = False
    if not os.path.exists('start.pkl'):
        output = open('start.pkl', 'wb')
        start_time = datetime.today()
        pickle.dump(start_time, output)
        print ' Start time is:' +str(start_time)
        output.close()
        started = True
    else:
        end_time = datetime.today()
        print ' End time is:' +str(end_time)
        start_file = open('start.pkl', 'rb')
        start_time = pickle.load(start_file)
        start_file.close()
        os.unlink('start.pkl')
        total_time = end_time - start_time
        segundos = total_time.total_seconds()
        # print ' Segundos is:' +str(segundos)

    # d = {'2014-05-2':[2,34,53,123,55]}
    #data = [d1,d2,d3,d4]

    if was_conected() and not started:
        log = open('log.pkl', 'rb')
        data = pickle.load(log)
        log.close()
        if len(data) > 0:
            for dic in data:
                if dic.has_key(get_date()):
                    dic[get_date()].append(segundos)
                else:
                    dic[get_date()] = [segundos]
        else:
            d = {get_date(): [segundos]}
            data.append(d)
        log = open('log.pkl', 'wb')
        pickle.dump(data, log)
        log.close()



def format(time):
    time = int(time)
    if time < 10:
        time = '0'+str(time)
    else:
        time = str(time)
    return time


def get_correct_time(segundos):
    m_min = segundos / 60
    m_sec = segundos % 60

    h_hour = segundos / 60 / 60
    h_min = segundos / 60 %  60
    h_sec = segundos % 60

    minutos = '00:'+ format(str(int(round(m_min)))) +':'+format(str(int(round(m_sec))))
    horas =  format(str(int(round(h_hour)))) +':'+format(str(int(round(h_min)))) + ':'+format(str(int(round(h_sec))))
    seconds =  '00:00:'+format(str(int(round(segundos))))

    if  segundos  >= 3600:
        return horas
    if segundos >= 60:
        return minutos
    return seconds


def get_log():
    log = open('log.pkl', 'rb')
    data = pickle.load(log)
    log.close()
    if len(data) == 0:
        print 'No hay registros'
    else:
        print ' '
        total_time = 0
        for dic in data:
            print '---------------------------'
            print '|  Fecha: ' + dic.keys()[0]+' '
            print '---------------------------'
            total_date_time = 0
            for time in dic.values()[0]:
                print '|   -  ' + get_correct_time(time)
                total_date_time += time
                total_time += time
            print '|   Total dia: ' + get_correct_time(total_date_time)

    print '=========================='
    print '|   Total: ' + get_correct_time(total_time)
    print '=========================='


def clean_log():
    data = []
    log = open('log.pkl', 'wb')
    pickle.dump(data, log)
    log.close()


def main(string_to_find=False):
    p = optparse.OptionParser(
        description="cc - Conection counter. Searches a string in the files within a dir and its subdirs. Returns the name of the file, the line number and the line text where the string was found",
        prog="ft",
        version="1.0",
        usage="%prog -options [arguments]")

    p.add_option('--install', '-i', action="store_true", help='Install this program. Require root privileges')
    p.add_option('--st', '-s', action="store_true", help='Comienza/Detiene el contador')
    p.add_option('--log', '-l', action="store_true", help='Chequea  el log')
    p.add_option('--clean', '-c', action="store_true", help='Limpia el log')

    options, arguments = p.parse_args()
    opt_dict = options

    if options.install:
        install()

    elif options.log:
        get_log()

    elif options.st:
        timer()

    elif options.clean:
        clean_log()

    else:
        p.print_help()


if __name__ == '__main__':
    main()
    # timer()
    # null_out = cmd.getoutput("sleep 7")
    # timer()
    # timer()
    # null_out = cmd.getoutput("sleep 8")
    # timer()
