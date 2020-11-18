#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# ==========================================================
#
# TL;DR
#
# Supposing that these are your preferred arguments
# -j2 DESTDIR="/some/dir" PREFIX="/some/dir"
# just run
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir"
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL=1
#
# ==========================================================
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
# 're-configuring') will be performed during the second and all the
# consequent runs (will be performed only populating global variables
# and reading variables cache).
#
# This file contains variables that are needed for INSTALL action
# only, not for COMPILE action.
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
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL=1
#
# And, in conclusion:
# As the INSTALL action requires the variables-cache file,
# it will not be performed without this file.
#
# That is, if you run
# scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL=1
# as the first run (or after deleting the variables-cache file)
# the script will be going to COMPILE (and to get and save the
# variables needed for INSTALL), not to INSTALL.
#
# IMHO, this algorithm is consistent enough.
#
# ==========================================================

from collections import OrderedDict
import os
import re
import sys

# os.path.join drops all other parts when one part is an absolute path; os.path.normpath takes only one argument...
# In short, I haven't yet found the proper built-in function :)
def _myown_os_path_join(*paths):
    joined = ''
    for path in paths:
        pattern = re.compile("^[a-zA-Z0-9_." + os.path.sep + "-]+$")
        match = pattern.match(path)
        if not match:
            print('_myown_os_path_join ERROR: path contains forbidden character(s)')
            sys.exit(1)
        if joined.endswith('/') and path.startswith('/'):
            fixed = path[1:]
            path = fixed
        elif not joined.endswith('/') and not path.startswith('/') and joined != '':
            joined += '/'
        joined += path
    return joined

def _populate_os_dict(name='', destdir='', prefix='', cpp_compiler='', cpp_compiler_flags='', linker_flags=''):
    mydict = {}
    if not name:
        print('_populate_os_dict ERROR: name argument is undefined or empty string')
        sys.exit(1)
    if not destdir:
        print('_populate_os_dict ERROR: destdir argument is undefined or empty string')
        sys.exit(1)
    mydict['name'] = name
    mydict['destdir'] = destdir
    mydict['prefix'] = prefix
    mydict['cpp_compiler'] = cpp_compiler
    mydict['cpp_compiler_flags'] = cpp_compiler_flags
    mydict['linker_flags'] = linker_flags
    return mydict

def populate_global_vars():
    mydict = {
        # ['env']['prefix'] and ['env']['destdir'] are set in function _set_env_prefix_and_destdir
        'env' : Environment(),

        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'compile_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World',
        'supported_oses' : OrderedDict(),
        'os_detected_at' : 'destdir',

        # Set in function _detect_os, by finding non-empty value of scons argument which name is determined by the key 'os_detected_at' above:
        # destdir -> second argument of function _populate_os_dict ->
        #      if we found argument 'DESTDIR' with non-empty value, then, OS is detected as Gentoo,
        #      if we found argument 'install_root' with non-empty value, then, OS is detected as Debian/Ubuntu
        'detected_os' : '',

        'variables_cache_file' : 'scons_variables_cache.conf'
    }
    mydict['source_full'] = _myown_os_path_join(mydict['source_path'], mydict['source_name'])
    mydict['compile_target'] = _myown_os_path_join(mydict['compile_path'], mydict['binary_name'])

    # Operating System is defined as a set of variables
    mydict['supported_oses']['gentoo'] = _populate_os_dict('Gentoo',         'DESTDIR',      'PREFIX', 'CXX', 'CXXFLAGS', 'LDFLAGS')
    mydict['supported_oses']['debian'] = _populate_os_dict('Debian/Ubuntu',  'install_root')

    # Changed by calling method "Add" in function read_variables_cache
    mydict['install_args'] = Variables(mydict['variables_cache_file'])

    return mydict

def _detect_os(global_vars):
    for key, nested_dict in global_vars['supported_oses'].items():
        os_detected_at = global_vars['os_detected_at']
        os_argname = nested_dict[os_detected_at]
        print('checking for ' + os_detected_at + ' as ' + os_argname + '... (are we on ' + nested_dict['name'] + '?)')
        os_argvalue = ARGUMENTS.get(os_argname)
        if os_argvalue:
            global_vars['detected_os'] = key
            print('detected Operating System: ' + global_vars['detected_os'])
            return 1
    print('Operating System not detected')
    print('If your Operating System is not supported, you can simulate one of supported OSes by passing parameters with names that it has')
    print('Parameter names that each of supported Operating Systems has, you can see them in function populate_global_vars (calls to function _populate_os_dict)')
    sys.exit(1)

def _get_argvalue(global_vars, argname):
    if global_vars['detected_os'] == '' and argname != global_vars['os_detected_at']:
        print('_get_argvalue ERROR: when getting ' + argname + ' value, OS should be already detected')
        sys.exit(1)
    if (argname == global_vars['os_detected_at']):
        _detect_os(global_vars)
    detected_os = global_vars['detected_os']
    this_os_argname = global_vars['supported_oses'][detected_os][argname]
    argvalue = ARGUMENTS.get(this_os_argname)
    if argvalue:
        print(argname + ' (' + this_os_argname + ' in ' + global_vars['supported_oses'][detected_os]['name'] + ') argument found: ' + argvalue)
        return argvalue
    else:
        print(argname + ' (' + this_os_argname + ' in ' + global_vars['supported_oses'][detected_os]['name'] + ') argument not found')
        return ''

def _set_env_prefix_and_destdir(global_vars):
    os_destdir_argvalue = _get_argvalue(global_vars, 'destdir')
    # No check 'if os_destdir_argvalue' here because if it is not 'true', OS will not be defined and the script will exit in function _detect_os
    global_vars['env']['destdir'] = _myown_os_path_join(os_destdir_argvalue, global_vars['install_path'])
    print("until prefix is found, global_vars['env']['destdir'] is set for default value without prefix: " + global_vars['env']['destdir'])
    os_prefix_argvalue = _get_argvalue(global_vars, 'prefix')
    if os_prefix_argvalue:
        global_vars['env']['prefix'] = os_prefix_argvalue
        global_vars['env']['destdir'] = _myown_os_path_join(os_destdir_argvalue, global_vars['env']['prefix'], global_vars['install_path'])
        print("global_vars['env']['destdir'] is reset using prefix: " + global_vars['env']['destdir'])

def read_variables_cache(global_vars):
    global_vars['install_args'].Add('MYDIR', "cached 'dir' argument for global_vars['env'].Install", '')
    global_vars['install_args'].Add('MYSOURCE', "cached 'source' argument for global_vars['env'].Install", '')
    global_vars['env'] = Environment(variables = global_vars['install_args'])

def _save_variables_cache(global_vars):
    global_vars['env']['MYDIR'] = global_vars['env']['destdir']
    global_vars['env']['MYSOURCE'] = global_vars['compile_target']
    global_vars['install_args'].Save(global_vars['variables_cache_file'], global_vars['env'])

def get_and_save_variables_for_install(global_vars):
    print('getting and saving variables needed for install...')
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
    print('variables for install retrieved successfully; no need for re-configuring!')
    install_passed = ARGUMENTS.get('INSTALL')
    if install_passed == '1':
        install(global_vars)
    else:
        print('will not install; this SConscript requires passing "INSTALL=1" in command-line arguments instead of "install" after them')
        compile(global_vars)
else:
    print('variables for install not retrieved')
    get_and_save_variables_for_install(global_vars)
    compile(global_vars)
