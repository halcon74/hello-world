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
# A side effect of this algorithm:
# you can run this script two times with "INSTALL=1"
# (the first run will COMPILE, the second run will INSTALL)
# :)
#
# ==========================================================

from collections import OrderedDict
import os.path
import re
import sys
import SCons.Util

# os.path.join drops all other parts when one part is an absolute path;
# os.path.normpath takes only one argument...
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

def _populate_os_data():
    mydict = {}
    mydict['supported_oses'] = OrderedDict()
    mydict['supported_oses'] = {
        'gentoo' : {
            'os_name' : 'Gentoo'
        },
        'debian' : {
            'os_name' : 'Debian/Ubuntu'
        }
    }
    mydict['os_vars'] = {
        'install_vars' : {
            'destdir' : {
                'required' : 'non-empty',
                'name_in_env' : '',
                'names_in_supported_oses' : {
                    'gentoo' : 'DESTDIR',
                    'debian' : 'install_root'
                }
            },
            'prefix' : {
                'required' : '',
                'name_in_env' : '',
                'names_in_supported_oses' : {
                    'gentoo' : 'PREFIX'
                }
            }
        },
        'cpp_linker_vars' : {
            'cpp_compiler' : {
                'required' : '',
                'name_in_env' : 'CXX',
                'names_in_supported_oses' : {
                    'gentoo' : 'CXX'
                }
            },
            'cpp_compiler_flags' : {
                'required' : '',
                'name_in_env' : 'CXXFLAGS',
                'names_in_supported_oses' : {
                    'gentoo' : 'CXXFLAGS'
                }
            },
            'linker_flags' : {
                'required' : '',
                'name_in_env' : 'LINKFLAGS',
                'names_in_supported_oses' : {
                    'gentoo' : 'LDFLAGS'
                }
            }
        }
    }
    def _populate_os_dict(supported_oses, os_vars):
        for os_dict_key, os_dict in supported_oses.items():
            for vars_dict_key, vars_dict in os_vars.items():
                for var_dict_key, var_dict in vars_dict.items():
                    for name_in_supported_oses_key, name_in_supported_oses in \
                                            var_dict['names_in_supported_oses'].items():
                        if name_in_supported_oses_key == os_dict_key:
                            os_dict[var_dict_key] = name_in_supported_oses
                    if var_dict['required'] == 'non-empty' and not os_dict[var_dict_key]:
                        print('_populate_os_dict ERROR: ' + var_dict_key + \
                                                        ' is empty for ' + os_dict_key)
                        sys.exit(1)
    _populate_os_dict(mydict['supported_oses'], mydict['os_vars'])
    return mydict

def _myown_env_variables_descriptions():
    mydict = {}
    mydict['cached_dir'] = ('MYCACHEDDIR', \
                            "cached 'dir' argument for global_vars['env'].Install", '')
    mydict['cached_source'] = ('MYCACHEDSOURCE', \
                            "cached 'source' argument for global_vars['env'].Install", '')
    return mydict

def populate_global_vars():
    mydict = {
        # 2 my own env variables are added in function read_variables_cache and then
        # their values are set in function _save_variables_cache
        'env' : Environment(),

        # All that I add to env variables must be defined in tuples here
        'myown_env_variables' : _myown_env_variables_descriptions(),

        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'compile_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World'
    }
    mydict['os_data'] = _populate_os_data()
    mydict['os_detected_at'] = 'destdir'

    # Set in function _detect_os, by finding non-empty value of scons argument
    # which name is determined by the key 'os_detected_at' above:
    #   (see function _populate_os_data)
    #      if we found argument 'DESTDIR' with non-empty value, then,
    #         OS is detected as Gentoo,
    #      if we found argument 'install_root' with non-empty value, then,
    #         OS is detected as Debian/Ubuntu
    # I don't use special tools for detecting OS intentionally,
    # because I define OS here as a set of variables
    mydict['detected_os'] = ''

    # Values are set in functions _get_prefix_and_destdir and _get_cpp_linker_vars
    mydict['got_arguments'] = {}

    mydict['variables_cache_file'] = 'scons_variables_cache.conf'
    mydict['source_full'] = _myown_os_path_join(mydict['source_path'], mydict['source_name'])
    mydict['compile_target'] = _myown_os_path_join(mydict['compile_path'], mydict['binary_name'])

    # This is a SCons.Variables.Variables class object for reading from /
    # writing to the variables cache file
    # Changed by calling method "Add" in function read_variables_cache
    mydict['scons_var_obj'] = Variables(mydict['variables_cache_file'])

    return mydict

def _detect_os(obj):
    if obj['detected_os']:
        print('re-detecting Operating System is not supported')
        sys.exit(1)
    for key, nested_dict in obj['os_data']['supported_oses'].items():
        os_detected_at = obj['os_detected_at']
        os_argname = nested_dict[os_detected_at]
        print('checking for ' + os_detected_at + ' as ' + os_argname + \
                                        '... (are we on ' + nested_dict['os_name'] + '?)')
        os_argvalue = ARGUMENTS.get(os_argname)
        if os_argvalue:
            obj['detected_os'] = key
            print('detected Operating System: ' + obj['detected_os'])
            return 1
    print('Operating System not detected')
    print('If your Operating System is not supported, you can simulate one of \
                            supported OSes by passing parameters with names that it has')
    print('Parameter names that each of supported Operating Systems has, \
                                    you can see them in function _populate_os_data')
    sys.exit(1)

def _get_argvalue(obj, argname):
    if obj['detected_os'] == '' and argname != obj['os_detected_at']:
        print('_get_argvalue ERROR: when getting ' + argname + \
                                ' value, OS should be already detected')
        sys.exit(1)
    if argname == obj['os_detected_at']:
        _detect_os(obj)
    detected_os = obj['detected_os']
    this_os_argname = obj['os_data']['supported_oses'][detected_os][argname]
    argvalue = ARGUMENTS.get(this_os_argname)
    if argvalue:
        print(argname + ' (' + this_os_argname + ' in ' + \
                obj['os_data']['supported_oses'][detected_os]['os_name'] + \
                ') argument found: ' + argvalue)
        return argvalue
    print(argname + ' (' + this_os_argname + ' in ' + \
                obj['os_data']['supported_oses'][detected_os]['os_name'] + \
                ') argument not found')
    return ''

def _get_prefix_and_destdir(obj):
    os_destdir_argvalue = _get_argvalue(obj, 'destdir')
    # No check 'if os_destdir_argvalue' here because if it is not 'true',
    # OS will not be defined and the script will exit in function _detect_os
    obj['got_arguments']['destdir'] = _myown_os_path_join(os_destdir_argvalue, \
                                                                obj['install_path'])
    print('until prefix is found, destdir is set for default value without prefix: ' + \
                                                    obj['got_arguments']['destdir'])
    os_prefix_argvalue = _get_argvalue(obj, 'prefix')
    if os_prefix_argvalue:
        obj['got_arguments']['prefix'] = os_prefix_argvalue
        obj['got_arguments']['destdir'] = _myown_os_path_join(os_destdir_argvalue, \
                            obj['got_arguments']['prefix'], obj['install_path'])
        print('destdir is reset using prefix: ' + obj['got_arguments']['destdir'])

def _get_cpp_linker_vars(obj):
    for key, mydict in obj['os_data']['os_vars']['cpp_linker_vars'].items():
        os_argvalue = _get_argvalue(obj, key)
        if os_argvalue:
            obj['got_arguments'][key] = os_argvalue

def _apply_cpp_linker_vars(obj):
    for key, mydict in obj['os_data']['os_vars']['cpp_linker_vars'].items():
        name_in_env = mydict['name_in_env']
        if name_in_env:
            pattern = re.compile("^[A-Z]+$")
            match = pattern.match(name_in_env)
            if not match:
                print('_apply_cpp_linker_vars ERROR: name_in_env contains forbidden characters')
                sys.exit(1)
            print('setting ' + name_in_env + ' to ' + obj['got_arguments'][key])
            # Replace's keyword (in 'keyword = value' syntax) can't be an expression
            evaling_string = "obj['env'].Replace(" + name_in_env + \
                                "= SCons.Util.CLVar(obj['got_arguments'][key]))"
            eval(evaling_string)

def get_myown_env_variable(obj, usedname):
    varname = obj['myown_env_variables'][usedname][0]
    return obj['env'][varname]

def _set_myown_env_variable(obj, usedname, value):
    varname = obj['myown_env_variables'][usedname][0]
    obj['env'][varname] = value

def read_variables_cache(obj):
    obj['scons_var_obj'].Add(obj['myown_env_variables']['cached_dir'])
    obj['scons_var_obj'].Add(obj['myown_env_variables']['cached_source'])

    # This adds new variables to Environment (doesn't rewrite it)
    # https://scons.org/doc/2.3.0/HTML/scons-user/x2445.html#AEN2504
    obj['env'] = Environment(variables = obj['scons_var_obj'])

def _save_variables_cache(obj):
    _set_myown_env_variable(obj, 'cached_dir', obj['got_arguments']['destdir'])
    _set_myown_env_variable(obj, 'cached_source', obj['compile_target'])

    # This saves only variables from 'scons_var_obj', not all variables from 'env'
    # (here 'env' is the environment to get the option values from)
    # https://scons.org/doc/3.0.1/HTML/scons-api/SCons.Variables.Variables-class.html#Save
    obj['scons_var_obj'].Save(obj['variables_cache_file'], obj['env'])

def get_and_save_variables_for_install(obj):
    print('getting and saving variables needed for install...')
    _get_prefix_and_destdir(obj)
    _save_variables_cache(obj)

def mycompile(obj):
    _get_cpp_linker_vars(obj)
    _apply_cpp_linker_vars(obj)
    target = obj['env'].Program(target = obj['compile_target'], \
                                            source = obj['source_full'])
    Default(target)
    print('will compile: target = ' + obj['compile_target'] + ', \
                                            source = ' + obj['source_full'])

def install(obj):
    target = obj['env'].Install(dir = get_myown_env_variable(obj, 'cached_dir'), \
                                    source = get_myown_env_variable(obj, 'cached_source'))
    Default(target)
    print('will install: dir = ' + get_myown_env_variable(obj, 'cached_dir') + \
                        ', source = ' + get_myown_env_variable(obj, 'cached_source'))

global_vars = populate_global_vars()

read_variables_cache(global_vars)

if get_myown_env_variable(global_vars, 'cached_dir') and \
            get_myown_env_variable(global_vars, 'cached_source'):
    print('variables for install retrieved successfully; no need for re-configuring!')
    install_passed = ARGUMENTS.get('INSTALL')
    if install_passed == '1':
        install(global_vars)
    else:
        print('will not install; this SConscript requires passing "INSTALL=1" \
                                in command-line arguments instead of "install" after them')
        mycompile(global_vars)
else:
    print('variables for install not retrieved')
    get_and_save_variables_for_install(global_vars)
    mycompile(global_vars)
