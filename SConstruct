#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict
import os

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

variables_cache_file = 'scons_variables_cache.conf'
variables_cache = Variables(variables_cache_file)

def _variables_cache_save(variables_cache):
    variables_cache.Update(env)
    variables_cache.Save('scache.conf', env)
    Help(variables_cache.GenerateHelpText(env))

def set_os_data(variables_cache, name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
    mydict = {}
    if not name:
        print('set_os_data: name argument is undefined or empty string')
        return mydict
    if not destdir:
        print('set_os_data: destdir argument is undefined or empty string')
        return mydict
    mydict['name'] = name
    mydict['destdir'] = destdir
    variables_cache.AddVariables(PathVariable('DESTDIR', 'intermediate install prefix', '', PathVariable.PathAccept))
    mydict['prefix'] = prefix
    variables_cache.AddVariables(PathVariable('PREFIX', 'install prefix', '/usr/local'))
    mydict['cpp_compiler'] = cpp_compiler
    mydict['cpp_compiler_flags'] = cpp_compiler_flags
    mydict['linker_flags'] = linker_flags
    _variables_cache_save(variables_cache)
    return mydict

supported_oses = OrderedDict()
# On each Operating System - its own set of variables
supported_oses['gentoo']=set_os_data(variables_cache, 'Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
supported_oses['debian']=set_os_data(variables_cache, 'Debian/Ubuntu',  'install_root')

program_builddir = 'build'
program_install_path = 'bin'

# Set in set_program_destdir()
detected_os = ''

def set_program_destdir(supported_oses, program_builddir):
    for key, nested_dict in supported_oses.items():
        this_destdir = nested_dict['destdir']
        print('checking for ' + this_destdir + '... (are we on ' + nested_dict['name'] + '?)')
        program_destdir = ARGUMENTS.get(this_destdir)
        if program_destdir:
            print(this_destdir + ' found and will be used: ' + program_destdir)
            global detected_os
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
    program_install_target = os.path.join(program_destdir, program_install_path)
    if detected_os:
        this_prefix = supported_oses[detected_os]['prefix']
        program_prefix = ARGUMENTS.get(this_prefix)
        if program_prefix:
            program_install_target = os.path.join(program_destdir, program_prefix, program_install_path)
            print(this_prefix + ' found and will be used: ' + program_prefix)
        else:
            print(this_prefix + ' not found for Operating System: ' + detected_os)
    else:
        print('no prefix will be used because Operating System was not detected')
    return program_install_target

program_build_target = os.path.join(program_builddir, program_name)
target = env.Program(target=program_build_target, source=program_source)
Default(target)
print('will build: target = ' + program_build_target + ', source = ' + program_source)

program_destdir = set_program_destdir(supported_oses, program_builddir)
program_install_target = set_program_install_target(program_destdir, program_install_path)
Alias("install", env.Install(dir=program_install_target, source=program_source))
print('will install: dir = ' + program_install_target + ', source = ' + program_source)


