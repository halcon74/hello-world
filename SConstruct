#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

def set_os_data(name='', destdir='', cpp_compiler='', cpp_compiler_flags='', linker_flags='', prefix=''):
    if not name:
        print('set_os_data: name argument is not defined')
        return mydict
    if not destdir:
        print('set_os_data: destdir argument is not defined')
        return mydict
    mydict = {}
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

def set_program_destdir(supported_oses, program_builddir):
    for key, nested_dict in supported_oses.items():
        this_destdir = nested_dict['destdir']
        print('checking for ' + this_destdir + '... (are we on ' + nested_dict['name'] + '?)')
        program_destdir = ARGUMENTS.get(this_destdir)
        if program_destdir:
            print(this_destdir + ' found and will be used: ' + program_destdir)
            return program_destdir
        else:
            print(this_destdir + ' not found')
    program_destdir = default_program_destdir
    print('program build directory will be used: ' + program_builddir)
    return program_destdir

def set_program_target(program_destdir, program_name):
    if program_destdir.endswith('/'):
        program_target = program_destdir + program_name
    else:
        program_target = program_destdir + '/' + program_name
    return program_target

program_target = set_program_target(program_builddir, program_name)
target = env.Program(target=program_target, source=program_source)
Default(target)
print('will build: target = ' + program_target + ', source = ' + program_builddir)

program_destdir = set_program_destdir(supported_oses, program_builddir)
Alias("install", env.Install(dir=program_destdir, source=program_source))
print('will install: dir = ' + program_destdir + ', source = ' + program_source)


