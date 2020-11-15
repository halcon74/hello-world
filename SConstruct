#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

default_destdir = 'build'

supported_oses = OrderedDict()
supported_oses['gentoo'] = {'name':'Gentoo', 'destdir':'DESTDIR'}
supported_oses['debian'] = {'name':'Debian/Ubuntu', 'destdir':'install_root'}

def set_program_destdir():
    global program_destdir
    is_destdir_arg_found = 0
    for key, nested_dict in supported_oses.items():
        this_destdir = nested_dict['destdir']
        print('checking for ' + this_destdir + '... (are we on ' + nested_dict['name'] + '?)')
        get_destdir = ARGUMENTS.get(this_destdir)
        if get_destdir:
            program_destdir = get_destdir
            print(this_destdir + ' found and will be used: ' + program_destdir)
            is_destdir_arg_found = 1
            break
        else:
            print(this_destdir + ' not found')
    if not is_destdir_arg_found:
        program_destdir = default_destdir
        print('default destination directory will be used: ' + program_destdir)

set_program_destdir()

if program_destdir.endswith('/'):
    program_target = program_destdir + program_name
else:
    program_target = program_destdir + '/' + program_name

print('Building: target = ' + program_target + ', source = ' + program_source)

target = env.Program(target=program_target, source=program_source)
Default(target)
