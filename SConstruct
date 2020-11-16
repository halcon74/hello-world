#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'

variables_cache_file = 'scons_variables_cache.conf'
variables_cache = Variables(variables_cache_file)

def os_path_concat(*paths):
    joined = ''
    for path in paths:
        if joined.endswith('/') and path.startswith('/'):
            fixed = path[1:]
            path = fixed
        elif not joined.endswith('/') and not path.startswith('/') and joined != '':
            joined += '/'
        joined += path
    return joined

def variables_cache_save(env, variables_cache, variables_cache_file):
    variables_cache.Update(env)
    variables_cache.Save(variables_cache_file, env)
    Help(variables_cache.GenerateHelpText(env))

def set_os_data(name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
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
    return mydict

supported_oses = OrderedDict()
# On each Operating System - its own set of variables
supported_oses['gentoo']=set_os_data('Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
supported_oses['debian']=set_os_data('Debian/Ubuntu',  'install_root')
variables_cache_save(env, variables_cache, variables_cache_file)

program_builddir = 'build'
program_install_path = 'bin'

# Set in _set_program_destdir()
detected_os = ''

def _set_program_destdir(supported_oses, program_builddir):
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

def set_program_install_target(supported_oses, program_builddir, program_install_path):
    program_destdir = _set_program_destdir(supported_oses, program_builddir)
    env['DESTDIR'] = os_path_concat(program_destdir, program_install_path)
    if detected_os:
        this_prefix = supported_oses[detected_os]['prefix']
        program_prefix = ARGUMENTS.get(this_prefix)
        if program_prefix:
            env['PREFIX'] = program_prefix
            env['DESTDIR'] = os_path_concat(program_destdir, program_prefix, program_install_path)
            print(this_prefix + ' found and will be used: ' + env['PREFIX'])
        else:
            print(this_prefix + ' not found for Operating System: ' + detected_os)
    else:
        print('no prefix will be used because Operating System was not detected')

program_build_target = os_path_concat(program_builddir, program_name)
target = env.Program(target=program_build_target, source=program_source)
Default(target)
print('will build: target = ' + program_build_target + ', source = ' + program_source)

set_program_install_target(supported_oses, program_builddir, program_install_path)
print('will install: dir = ' + env['DESTDIR'] + ', source = ' + program_build_target)

Alias("install", env.Install(dir=env['DESTDIR'], source=program_build_target))
