#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

def getFiles(path):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
                file_list.append(os.path.join(dirpath, filename))
    return file_list

def getRoute(name, files_path):
    for f in files_path:
        if name in f:
            return f

def getFileName(files_path):
    file_nopath_name =[]
    for f in files_path:
        file_nopath_name.append(f.split("/")[-1])
    return file_nopath_name

def find(path1, path2):
    files_list_path1 = getFiles(path1)
    files_list_path2 = getFiles(path2)
    names1 = getFileName(files_list_path1)
    names2 = getFileName(files_list_path2)
    duplicated = []
    for name in names1:
        if name in names2:
            duplicated.append(name)

    html_format =  """
        <html>
            <body>
                <table>
                  <tr>
                    <td>%s</td>
                    <td>%s</td>
                  </tr>
                  %s
                </table>
            </body>
        </html>
    """

    td_format = """
    <tr>
        <td>
            <img src="%s" width=300 height=400/>
            </br>
            <span style="font-size:10px">%s</span>
        </td>
        <td>
            <img src="%s" width=300 height=400/>
            </br>
            <span style="font-size:10px">%s</span>
        </td>
    </tr>
    """

    table_list = ""
    to_delete = []
    for dup in duplicated:
        route1 = getRoute(dup, files_list_path1)
        to_delete.append(route1+'\n')
        route2 = getRoute(dup, files_list_path2)
        table_list += td_format % (route1, route1, route2, route2)

    html = html_format % (path1, path2, table_list)

    with open('/home/eduardo/Escritorio/repetidos.html','w') as var:
        var.write(html)

    with open('/home/eduardo/Escritorio/repetidos-borrar.txt','w') as var:
        var.writelines(to_delete)

if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    #photos.py -p /home/edu asdas
    #args = ['-p','/home/eduardo','asdas']
    find(args[0], args[1])

