#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# When this script is running for the first time with usual
# command-line arguments, like
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir"
# it performs COMPILE action
# and
# creates a variables-cache file.
#
# The name of this file is set in function populate_global_vars,
# for the dictionary key 'variables_cache_file'.
#
# With this file, no redundant actions (that are usually called
# 're-configuring' will be performed during the second and all the
# consequent runs (will be performed only populating global variables
# and reading variables cache).
#
# This file contains variables that are needed for INSTALL action only,
# not for COMPILE action.
#
# The COMPILE action can be done after creating this file as well;
# this file does not make any harm for it.
#
# Moreover, this file makes the consequent compiling runs faster,
# because the script will not try to get variables needed for
# INSTALL action and to save them in the variables-cache file.
#
# THE MOST IMPORTANT PART: this script does not contain an usual
# Alias "install", because I prefer to use command-line arguments
# instead of Aliases.
#
# For this reason, this script requires
# passing "INSTALL=1" IN command-line arguments
# instead of
# passing "install" AFTER command-line arguments
#
# That is, if you run
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" install
# the INSTALL action WILL NOT be performed.
#
# The INSTALL action WILL be performed
# if you run
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL="1"
#
# And, in conclusion:
# As the INSTALL action requires the variables-cache file,
# it will not be performed without this file.
#
# That is, if you run
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL="1"
# as the first run (or after deleting the variables-cache file)
# the script will be going to COMPILE, not to INSTALL (will print
# a message about it).
#
# IMHO, this algorithm is consistent enough.

from collections import OrderedDict

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
        # ['env']['PREFIX'] and ['env']['DESTDIR'] are set in function _set_env_prefix_and_destdir
        'env' : Environment(),
        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'compile_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World',
        # Set in function save_variables_for_install
        'supported_oses' : OrderedDict(),
        # Set in function _get_os_destdir_argvalue by finding non-empty value of a variable which name is set as OS's destdir
        'detected_os' : '',
        'variables_cache_file' : 'scons_variables_cache.conf'
    }
    mydict['source_full'] = _myown_os_path_join(mydict['source_path'], mydict['source_name'])
    mydict['compile_target'] = _myown_os_path_join(mydict['compile_path'], mydict['binary_name'])
    mydict['install_args'] = Variables(mydict['variables_cache_file'])
    return mydict

def _populate_os_dict(name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
    mydict = {}
    if not name:
        print('_populate_os_dict ERROR: name argument is undefined or empty string')
        return mydict
    if not destdir:
        print('_populate_os_dict ERROR: destdir argument is undefined or empty string')
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
    os_destdir_argvalue = global_vars['compile_path']
    print('program compile path used: ' + os_destdir_argvalue)
    print('Operating System not detected')
    return os_destdir_argvalue

def _set_env_prefix_and_destdir(global_vars):
    os_destdir_argvalue = _get_os_destdir_argvalue(global_vars)
    detected_os = global_vars['detected_os']
    global_vars['env']['DESTDIR'] = _myown_os_path_join(os_destdir_argvalue, global_vars['install_path'])
    print("until prefix is found, global_vars['env']['DESTDIR'] is set for default value without prefix: " + global_vars['env']['DESTDIR'])
    if detected_os:
        os_prefix_argname = global_vars['supported_oses'][detected_os]['prefix']
        os_prefix_argvalue = ARGUMENTS.get(os_prefix_argname)
        if os_prefix_argvalue:
            global_vars['env']['PREFIX'] = os_prefix_argvalue
            global_vars['env']['DESTDIR'] = _myown_os_path_join(os_destdir_argvalue, global_vars['env']['PREFIX'], global_vars['install_path'])
            print(os_prefix_argname + ' found and used: ' + global_vars['env']['PREFIX'] + "")
            print("global_vars['env']['DESTDIR'] is reset using prefix: " + global_vars['env']['DESTDIR'])
        else:
            print(os_prefix_argname + ' not found for Operating System: ' + detected_os)
    else:
        print('no prefix used because Operating System was not detected')

def read_variables_cache(global_vars):
    global_vars['install_args'].Add('MYDIR', "cached 'dir' argument for global_vars['env'].Install", '')
    global_vars['install_args'].Add('MYSOURCE', "cached 'source' argument for global_vars['env'].Install", '')
    global_vars['env'] = Environment(variables = global_vars['install_args'])

def _save_variables_cache(global_vars):
    global_vars['env']['MYDIR'] = global_vars['env']['DESTDIR']
    global_vars['env']['MYSOURCE'] = global_vars['compile_target']
    global_vars['install_args'].Save(global_vars['variables_cache_file'], global_vars['env'])

def save_variables_for_install(global_vars):
    print('will get and save variables needed for install')
    # On each Operating System - its own set of variables
    global_vars['supported_oses']['gentoo'] = _populate_os_dict('Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
    global_vars['supported_oses']['debian'] = _populate_os_dict('Debian/Ubuntu',  'install_root')
    _set_env_prefix_and_destdir(global_vars)
    _save_variables_cache(global_vars)

def compile(global_vars):
    target = global_vars['env'].Program(target = global_vars['compile_target'], source = global_vars['source_full'])
    Default(target)
    print('will compile: target = ' + global_vars['compile_target'] + ', source = ' + global_vars['source_full'])

def install(global_vars):
    target = global_vars['env'].Install(dir = global_vars['env']['MYDIR'], source = global_vars['env']['MYSOURCE'])
    Default(target)
    print('will install: dir = ' + global_vars['env']['MYDIR'] + ', source = ' + global_vars['env']['MYSOURCE'])

global_vars = populate_global_vars()
read_variables_cache(global_vars)

if global_vars['env']['MYDIR'] and global_vars['env']['MYSOURCE']:
    print('install_args retrieved successfully; no need for re-configuring!')
    install_passed = ARGUMENTS.get('INSTALL')
    if install_passed == '1':
        install(global_vars)
    else:
        print('will not install; this SConscript requires passing "INSTALL=1" in command-line arguments instead of "install" after them')
        compile(global_vars)
else:
    print('install_args not retrieved')
    save_variables_for_install(global_vars)
    compile(global_vars)
