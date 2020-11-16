#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict
import os

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

def set_os_data(name='', destdir='', cpp_compiler='', cpp_compiler_flags='', linker_flags='', prefix=''):
    mydict = {}
    if not name:
        print('set_os_data: name argument is undefined or empty string')
        return mydict
    if not destdir:
        print('set_os_data: destdir argument is undefined or empty string')
        return mydict
    mydict['name'] = name
    mydict['destdir'] = destdir
    mydict['cpp_compiler'] = cpp_compiler
    mydict['cpp_compiler_flags'] = cpp_compiler_flags
    mydict['linker_flags'] = linker_flags
    mydict['prefix'] = prefix
    return mydict

supported_oses = OrderedDict()
supported_oses['gentoo']=set_os_data('Gentoo',         'DESTDIR',      'CXX', 'CXXFLAGS', 'LDFLAGS', 'PREFIX')
supported_oses['debian']=set_os_data('Debian/Ubuntu',  'install_root')

program_builddir = 'build'
program_install_path = 'bin'

# set in set_program_destdir()
global detected_os
detected_os = ''

def set_program_destdir(supported_oses, program_builddir):
    for key, nested_dict in supported_oses.items():
        this_destdir = nested_dict['destdir']
        print('checking for ' + this_destdir + '... (are we on ' + nested_dict['name'] + '?)')
        program_destdir = ARGUMENTS.get(this_destdir)
        if program_destdir:
            print(this_destdir + ' found and will be used: ' + program_destdir)
            detected_os = key
            print('detected Operating System: ' + detected_os)
            return program_destdir
        else:
            print(this_destdir + ' not found')
    program_destdir = program_builddir
    print('program build directory will be used: ' + program_builddir)
    print('Operating System not detected')
    return program_destdir

def set_program_install_target(program_destdir, program_install_path):
    if detected_os:
        prefix = supported_oses[detected_os]['prefix']
        print(prefix + ' found and will be used: ' + prefix)
        program_install_target = os.path.join(program_destdir, supported_oses[detected_os]['prefix'], program_install_path)
    else:
        print('no prefix will be used because Operating System was not detected')
        program_install_target = os.path.join(program_destdir, program_install_path)
    return program_install_target

build_target = os.path.join(program_builddir, program_name)
target = env.Program(target=build_target, source=program_source)
Default(target)
print('will build: target = ' + build_target + ', source = ' + program_source)

program_destdir = set_program_destdir(supported_oses, program_builddir)
program_install_target = set_program_install_target(program_destdir, program_install_path)
Alias("install", env.Install(dir=program_install_target, source=program_source))
print('will install: dir = ' + program_install_target + ', source = ' + program_source)


