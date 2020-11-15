#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

def set_os_data(dict, key, name, destdir='', cpp_compiler='', cpp_compiler_flags='', linker_flags='', prefix=''):
    dict[key] = {}
    dict[key]['name'] = name
    dict[key]['destdir'] = destdir
    dict[key]['cpp_compiler'] = cpp_compiler
    dict[key]['cpp_compiler_flags'] = cpp_compiler_flags
    dict[key]['linker_flags'] = linker_flags
    dict[key]['prefix'] = prefix
    return dict

supported_oses = OrderedDict()
supported_oses=set_os_data(supported_oses, 'gentoo', 'Gentoo',         'DESTDIR',      'CXX', 'CXXFLAGS', 'LDFLAGS', 'PREFIX')
supported_oses=set_os_data(supported_oses, 'debian', 'Debian/Ubuntu',  'install_root')

print('supported_oses_gentoo_name = ' + supported_oses['gentoo']['name'])

default_program_destdir = 'build'

def set_program_destdir(supported_oses, default_program_destdir):
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
    print('default destination directory will be used: ' + program_destdir)
    return program_destdir

def set_program_target(program_destdir, program_name):
    if program_destdir.endswith('/'):
        program_target = program_destdir + program_name
    else:
        program_target = program_destdir + '/' + program_name
    return program_target

program_destdir = set_program_destdir(supported_oses, default_program_destdir)
program_target = set_program_target(program_destdir, program_name)
print('will build: target = ' + program_target + ', source = ' + program_source)

target = env.Program(target=program_target, source=program_source)
Default(target)

Alias("install", env.Install(dir=program_destdir, source=program_source))
