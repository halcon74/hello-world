#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import OrderedDict

# env['PREFIX'] and env['DESTDIR'] are set in function set_env_prefix_and_destdir
env = Environment()

# os.path.join drops all other parts when one part is an absolute path; os.path.normpath takes only one argument...
# In short, I haven't yet found the proper built-in function :)
def _myown_os_path_join(*paths):
    joined = ''
    for path in paths:
        if joined.endswith('/') and path.startswith('/'):
            fixed = path[1:]
            path = fixed
        elif not joined.endswith('/') and not path.startswith('/') and joined != '':
            joined += '/'
        joined += path
    return joined

def populate_global_vars():
    mydict = {
        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'build_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World',
        'supported_oses' : OrderedDict(),
        # Set in function _get_os_destdir_argvalue by finding non-empty value of a variable which name is set as OS's destdir
        'detected_os' : ''
    }
    mydict['source_full'] = _myown_os_path_join(mydict['source_path'], mydict['source_name'])
    mydict['build_target'] = _myown_os_path_join(mydict['build_path'], mydict['binary_name'])
    return mydict

def populate_os_dict(name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
    mydict = {}
    if not name:
        print('populate_os_dict ERROR: name argument is undefined or empty string')
        return mydict
    if not destdir:
        print('populate_os_dict ERROR: destdir argument is undefined or empty string')
        return mydict
    mydict['name'] = name
    mydict['destdir'] = destdir
    mydict['prefix'] = prefix
    mydict['cpp_compiler'] = cpp_compiler
    mydict['cpp_compiler_flags'] = cpp_compiler_flags
    mydict['linker_flags'] = linker_flags
    return mydict

def _get_os_destdir_argvalue(global_vars):
    for key, nested_dict in global_vars['supported_oses'].items():
        os_destdir_argname = nested_dict['destdir']
        print('checking for ' + os_destdir_argname + '... (are we on ' + nested_dict['name'] + '?)')
        os_destdir_argvalue = ARGUMENTS.get(os_destdir_argname)
        if os_destdir_argvalue:
            print(os_destdir_argname + ' found and used: ' + os_destdir_argvalue)
            global_vars['detected_os'] = key
            print('detected Operating System: ' + global_vars['detected_os'])
            return os_destdir_argvalue
        else:
            print(os_destdir_argname + ' not found')
    os_destdir_argvalue = global_vars['build_path']
    print('program build path used: ' + os_destdir_argvalue)
    print('Operating System not detected')
    return os_destdir_argvalue

def set_env_prefix_and_destdir(global_vars):
    os_destdir_argvalue = _get_os_destdir_argvalue(global_vars)
    detected_os = global_vars['detected_os']
    env['DESTDIR'] = _myown_os_path_join(os_destdir_argvalue, global_vars['install_path'])
    print("until prefix is found, env['DESTDIR'] is set for default value without prefix: " + env['DESTDIR'])
    if detected_os:
        os_prefix_argname = global_vars['supported_oses'][detected_os]['prefix']
        os_prefix_argvalue = ARGUMENTS.get(os_prefix_argname)
        if os_prefix_argvalue:
            env['PREFIX'] = os_prefix_argvalue
            env['DESTDIR'] = _myown_os_path_join(os_destdir_argvalue, env['PREFIX'], global_vars['install_path'])
            print(os_prefix_argname + ' found and used: ' + env['PREFIX'] + "")
            print("env['DESTDIR'] is reset using prefix: " + env['DESTDIR'])
        else:
            print(os_prefix_argname + ' not found for Operating System: ' + detected_os)
    else:
        print('no prefix used because Operating System was not detected')

def populate_install_args(global_vars):
    install_args = {
        'dir' : env['DESTDIR'],
        'source' : global_vars['build_target']
    }
    return install_args

install_args_retrieved = ARGUMENTS.get('INSTALLARGS')
if install_args_retrieved:
    print('INSTALLARGS retrieved successfully; no need for re-configuring!')
    Alias("install", env.Install(dir = install_args_retrieved['dir'], source = install_args_retrieved['source']))
    print('will install: dir = ' + install_args_retrieved['dir'] + ', source = ' + install_args_retrieved['source'])
else:
    print('INSTALLARGS not retrieved; configuring...')
    global_vars = populate_global_vars()
    # On each Operating System - its own set of variables
    global_vars['supported_oses']['gentoo'] = populate_os_dict('Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
    global_vars['supported_oses']['debian'] = populate_os_dict('Debian/Ubuntu',  'install_root')

    target = env.Program(target = global_vars['build_target'], source = global_vars['source_full'])
    Default(target)
    print('will build: target = ' + global_vars['build_target'] + ', source = ' + global_vars['source_full'])

    set_env_prefix_and_destdir(global_vars)
    Alias("install", env.Install(dir = env['DESTDIR'], source = global_vars['build_target']))
    print('will install: dir = ' + env['DESTDIR'] + ', source = ' + global_vars['build_target'])
    install_args = populate_install_args(global_vars)
    Return('install_args')
