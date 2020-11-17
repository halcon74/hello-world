#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

# env['PREFIX'] and env['DESTDIR'] are set in function set_program_install_target
env = Environment()

program_name = 'Hello_World'
program_source = 'src/main.cpp'
program_builddir = 'build'
program_install_path = 'bin'

# Set in function _get_os_destdir_argvalue
detected_os = ''

# os.path.join drops all other parts when one part is an absolute path; os.path.normpath takes only one argument...
# In short, I haven't yet found the proper built-in function :)
def os_path_join(*paths):
    joined = ''
    for path in paths:
        if joined.endswith('/') and path.startswith('/'):
            fixed = path[1:]
            path = fixed
        elif not joined.endswith('/') and not path.startswith('/') and joined != '':
            joined += '/'
        joined += path
    return joined

def set_os_dict(name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
    mydict = {}
    if not name:
        print('set_os_dict: name argument is undefined or empty string')
        return mydict
    if not destdir:
        print('set_os_dict: destdir argument is undefined or empty string')
        return mydict
    mydict['name'] = name
    mydict['destdir'] = destdir
    mydict['prefix'] = prefix
    mydict['cpp_compiler'] = cpp_compiler
    mydict['cpp_compiler_flags'] = cpp_compiler_flags
    mydict['linker_flags'] = linker_flags
    return mydict

def _get_os_destdir_argvalue(supported_oses, program_builddir):
    for key, nested_dict in supported_oses.items():
        os_destdir_argname = nested_dict['destdir']
        print('checking for ' + os_destdir_argname + '... (are we on ' + nested_dict['name'] + '?)')
        os_destdir_argvalue = ARGUMENTS.get(os_destdir_argname)
        if os_destdir_argvalue:
            print(os_destdir_argname + ' found and will be used: ' + os_destdir_argvalue)
            global detected_os
            detected_os = key
            print('detected Operating System: ' + detected_os)
            return os_destdir_argvalue
        else:
            print(os_destdir_argname + ' not found')
    os_destdir_argvalue = program_builddir
    print('program build directory will be used: ' + os_destdir_argvalue)
    print('Operating System not detected')
    return os_destdir_argvalue

def set_program_install_target(supported_oses, program_builddir, program_install_path):
    os_destdir_argvalue = _get_os_destdir_argvalue(supported_oses, program_builddir)
    env['DESTDIR'] = os_path_join(os_destdir_argvalue, program_install_path)
    if detected_os:
        os_prefix_argname = supported_oses[detected_os]['prefix']
        os_prefix_argvalue = ARGUMENTS.get(os_prefix_argname)
        if os_prefix_argvalue:
            env['PREFIX'] = os_prefix_argvalue
            env['DESTDIR'] = os_path_join(os_destdir_argvalue, os_prefix_argvalue, program_install_path)
            print(os_prefix_argname + ' found and will be used: ' + env['PREFIX'])
        else:
            print(os_prefix_argname + ' not found for Operating System: ' + detected_os)
    else:
        print('no prefix will be used because Operating System was not detected')

supported_oses = OrderedDict()
# On each Operating System - its own set of variables
supported_oses['gentoo']=set_os_dict('Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
supported_oses['debian']=set_os_dict('Debian/Ubuntu',  'install_root')

program_build_target = os_path_join(program_builddir, program_name)
target = env.Program(target=program_build_target, source=program_source)
Default(target)
print('will build: target = ' + program_build_target + ', source = ' + program_source)

set_program_install_target(supported_oses, program_builddir, program_install_path)
Alias("install", env.Install(dir=env['DESTDIR'], source=program_build_target))
print('will install: dir = ' + env['DESTDIR'] + ', source = ' + program_build_target)
