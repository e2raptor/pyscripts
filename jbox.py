#!/usr/bin/python
import os
import commands as cmd
import sys

BUILD_DIR = 'build'
JAR_DIR = 'build/jar'
CLASSES_DIR = 'build/classes'
SRC_DIR = 'src'

def ask_data():
    project_name = raw_input('Nombre del projecto: ')
    main_class = raw_input('Nombre de la main class: ')
    return create_box(project_name, main_class)

def create_box(project_name, main_class):
    os.mkdir(project_name)
    os.chdir(project_name)
    os.mkdir(SRC_DIR)
    os.makedirs(CLASSES_DIR)
    os.makedirs(JAR_DIR)
    main_path = '%s/%s.java' % (SRC_DIR, main_class)
    com = 'touch '+ main_path
    cmd.getoutput(com)
    with open(main_path,'w') as file:
        class_def = 'public class %s {\n\n' % main_class
        constructor_def = '\tpublic %s() {}\n' % main_class
        main_m1 = '\tpublic static void main(String[] args) {\n'
        main_m2 = '\t\tSystem.out.println("Hola mundo!");\n}\n'
        close_def = '\n\n}'
        file.write(class_def)
        file.write(constructor_def)
        file.write(main_m1)
        file.write(main_m2)
        file.write(close_def)
    XML_CODE = '''
    <project name="%s" basedir="." default="main">

        <property name="src.dir" value="%s"/>
        <property name="build.dir" value="%s"/>
        <property name="project.name" value="%s"/>
        <property name="classes.dir" value="${build.dir}/classes"/>
        <property name="jar.dir" value="${build.dir}/jar"/>
        <property name="main-class" value="%s"/>

        <target name="clean">
            <delete dir="${build.dir}"/>
        </target>
        
        <target name="compile">
            <mkdir dir="${classes.dir}"/>
            <javac srcdir="${src.dir}" destdir="${classes.dir}"/>
        </target>

        <target name="jar" depends="compile">
            <mkdir dir="${jar.dir}"/>
            <jar destfile="${jar.dir}/${project.name}.jar" basedir="${classes.dir}">
                <manifest>
                    <attribute name="Main-Class" value="${main-class}"/>
                </manifest>
            </jar>
        </target>

        <target name="run" depends="jar">
            <java jar="${jar.dir}/${project.name}.jar" fork="true"/>
        </target>

        <target name="clean-build" depends="clean,jar"/>

        <target name="main" depends="clean,run"/>

    </project>
    ''' % (project_name,SRC_DIR,BUILD_DIR,project_name,main_class)
    with open('build.xml','w') as file:
        file.write(XML_CODE)
    return project_name

if __name__ == '__main__':
    script, args = sys.argv[0], sys.argv[1:]
    if not args: 
        project_name = ask_data()
    else:
        project_name = create_box(args[0], args[1])
