#!/usr/bin/python

import commands
import optparse
import os
import sys

SCRIPT_NAME = 'find-text.py'
EXTENSIONS = (
    'py', 'xml', 'csv', 'po', 'txt', 'yml', 'conf', 'config', 'cfg', 'log', 'c', 'cpp', 'h', 'sh', 'ini', 'php', 'html',
    'pl')
EXCLUDED_EXTENSIONS = (
    'pyc', 'xml~', 'py~', 'csv~', 'txt~', 'po~', 'txt~', 'yml~', 'conf~', 'config~', 'cfg~', 'c~', 'cpp~', 'h~', 'sh~',
    'ini~', 'swp')

PATH = '/usr/local/bin'


def install():
    if not os.path.exists('/usr/local/bin/ft'):
        if "root" in commands.getoutput("whoami"):
            cwd = os.getcwd()
            # os.chdir('/usr/local/bin')
            cmd = "ln -s %s/%s /usr/local/bin/ft" %(cwd, SCRIPT_NAME)
            a = commands.getoutput(cmd)
            print(a)
            # os.chdir(cwd)
            print "Installation finished. Execute ft -h for help"
        else:
            print 'Error!: You need root privileges to install this program'
    else:
        "This program is already installed. Execute 'ft -h' for help"


def final_single_print(match, count):
    file = '(' + str(count) + ') ' + match['file'] + ' [' + str(match['line_number']) + ']'
    file_colored = '\033[1;35m' + file + ':\033[1;m'
    line_colored = '\033[1;36m' + match['line'] + '\n\033[1;m'
    print file_colored + match['line'] + '\n'


def final_print(matches):
    count = 1
    if len(matches) > 0:
        for match in matches:
            file = '(' + str(count) + ') ' + match['file'] + ' [' + str(match['line_number']) + ']'
            file_colored = '\033[1;35m' + file + ':\033[1;m'
            line_colored = '\033[1;36m' + match['line'] + '\n\033[1;m'
            # print file_colored +'  '+line_colored
            print file_colored + match['line'] + '\n'
            count += 1
        print '--------------------------------'
        print '  Total matches: ' + str(len(matches))
        print ''
    else:
        print 'No results were found'


def has_extension(filename, ext):
    for excluded in EXCLUDED_EXTENSIONS:
        if '.' + excluded in filename:
            return False
    if '.' + ext in filename:
        return True


def search(options_dict, wizzard=False):
    string_to_find = ''
    extensions = ''
    path_to_search = '.'
    if wizzard:
        string_to_find = raw_input('String to find: ')
        extensions = raw_input('File extension (Comma separated: Ej: xml,py,txt): ')
        path_to_search = raw_input('Path to search (Current dir by default): ')
    else:
        string_to_find = options_dict.string
        extensions = options_dict.extension
        path_to_search = options_dict.path

    if not path_to_search:
        path_to_search = '.'
        current_path = commands.getoutput('pwd')
    else:
        current_path = path_to_search

    extension_list = ()
    if extensions:
        extension_list = extensions.split(',')

    print ''
    print "Searching for matches of '\033[1;31m" + string_to_find + "\033[1;m' within \033[1;34m" + current_path + "\033[1;m"
    print ''

    files_list = []
    for dirpath, dirnames, filenames in os.walk(path_to_search):
        for filename in filenames:
            if extensions:
                for ext in extension_list:
                    if has_extension(filename, ext):
                        files_list.append(os.path.join(dirpath, filename))
            else:
                if '.pyc' not in filename:
                    files_list.append(os.path.join(dirpath, filename))

    matches = []
    finded = False
    count = 1
    for file in files_list:
        lines = []
        with open(file) as f:
            lines = f.readlines()
        for l in lines:
            match_elem = {}
            if string_to_find in l:
                match_elem['line_number'] = lines.index(l) + 1
                match_elem['file'] = file
                # l = l.replace(string_to_find,'\033[1;41m'+string_to_find+'\033[1;m\033[1;36m')
                l = l.replace(string_to_find, '\033[1;31m' + string_to_find + '\033[1;m')
                match_elem['line'] = l.strip()
                matches.append(match_elem)
                final_single_print(match_elem, count)
                count += 1
                finded = True
    if finded:
        print '--------------------------------'
        print '  Total matches: ' + str(len(matches))
        print ''
    else:
        print 'No results were found'
    # final_print(matches)


def main(string_to_find=False):
    p = optparse.OptionParser(
        description="ft - Find Text. Searches a string in the files within a dir and its subdirs. Returns the name of the file, the line number and the line text where the string was found",
        prog="ft",
        version="1.0",
        usage="%prog -options [arguments]")

    p.add_option('--install', '-i', action="store_true", help='Install this program. Require root privileges')
    p.add_option('--string', '-s', action="store",
                 help='String to find. This option can be skipped but STRING must be specified immediately after command. i.e: ft string')
    p.add_option('--extension', '-e', action="store",
                 help='Limits the search to files with EXTENSION. Extensions must be separated by comma in case of more than one: i.e: xml,py,txt. All by defaults')
    p.add_option('--path', '-p', action="store", help='Path to search. Current dir by default')
    p.add_option('--wizzard', '-w', action="store_true", help='Raises a wizzard to guide the search')

    options, arguments = p.parse_args()
    opt_dict = options

    if options.wizzard:
        search(options, True)

    elif options.install:
        install()

    elif string_to_find:
        options.string = string_to_find
        search(options)

    elif not options.string and not options.extension and not options.path and not options.wizzard and not string_to_find:
        p.print_help()

    else:
        search(options)


if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    options = ('-p', '--path', '-s', '--string', '-e', '--extension', '-i', '--install', '-w', '--wizzard')
    if not args or args[0] in options:
        main()
    elif args[0] not in options:
        main(args[0])

    #search('asd',True)

