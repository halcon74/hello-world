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

def set_install_target(supported_oses, program_builddir):
    for key, nested_dict in supported_oses.items():
        this_destdir = nested_dict['destdir']
        print('checking for ' + this_destdir + '... (are we on ' + nested_dict['name'] + '?)')
        install_target = ARGUMENTS.get(this_destdir)
        if install_target:
            print(this_destdir + ' found and will be used: ' + install_target)
            return install_target
        else:
            print(this_destdir + ' not found')
    install_target = program_builddir
    print('program build directory will be used: ' + program_builddir)
    return install_target

build_target = os.path.join(program_builddir, program_name)
target = env.Program(target=build_target, source=program_source)
Default(target)
print('will build: target = ' + build_target + ', source = ' + program_source)

install_target = set_install_target(supported_oses, program_builddir)
Alias("install", env.Install(dir=install_target, source=program_source))
print('will install: dir = ' + install_target + ', source = ' + program_source)


