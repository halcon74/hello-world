#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

supported_oses = OrderedDict()
supported_oses['gentoo'] = {'name':'Gentoo', 'destdir':'DESTDIR'}
supported_oses['debian'] = {'name':'Debian/Ubuntu', 'destdir':'install_root'}

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
    if not program_destdir:
        program_destdir = default_program_destdir
        print('default destination directory will be used: ' + program_destdir)
        return program_destdir

program_destdir = set_program_destdir(supported_oses, default_program_destdir)

if program_destdir.endswith('/'):
    program_target = program_destdir + program_name
else:
    program_target = program_destdir + '/' + program_name

print('will build: target = ' + program_target + ', source = ' + program_source)

target = env.Program(target=program_target, source=program_source)
Default(target)
