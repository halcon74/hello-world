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
# The name of this file is set in function helpers_class,
# variable int_obj['variables_cache_file'].
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

def helpers_class():

    int_obj = {}

    int_obj['paths_and_names'] = {
        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'compile_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World'
    }

    int_obj['variables_cache_file'] = 'scons_variables_cache.conf'

    def _define_vars_data_and_myown_env_variables(os_detected_at):
        supported_oses = OrderedDict()
        supported_oses = {
            'gentoo' : {
                'os_name' : 'Gentoo'
            },
            'debian' : {
                'os_name' : 'Debian/Ubuntu'
            }
        }
        vars_data = {
            # All that I add to env variables must be defined
            # in values of 'is_saved_to_cache_file' here
            'install_vars' : {
                'destdir' : {
                    'is_applied_to_scons_env' : '',
                    'is_saved_to_cache_file' : ('MYCACHEDDIR', \
                                    "cached 'dir' argument for " + \
                                    "int_obj['scons_objects']['env'].Install", ''),
                    'is_got_from_arguments' : {'gentoo' : 'DESTDIR', 'debian' : 'install_root'},
                    'is_post_processed_in_a_function' : 'reset_destdir'
                },
                'prefix' : {
                    'is_applied_to_scons_env' : '',
                    'is_saved_to_cache_file' : '',
                    'is_got_from_arguments' : {'gentoo' : 'PREFIX'},
                    'is_post_processed_in_a_function' : ''
                },
                'compile_target' : {
                    'is_applied_to_scons_env' : '',
                    'is_saved_to_cache_file' : ('MYCACHEDSOURCE', \
                                    "cached 'source' argument for " + \
                                    "int_obj['scons_objects']['env'].Install", ''),
                    'is_got_from_arguments' : '',
                    'is_post_processed_in_a_function' : ''
                }
            },
            'cpp_linker_vars' : {
                'cpp_compiler' : {
                    'is_applied_to_scons_env' : 'CXX',
                    'is_saved_to_cache_file' : '',
                    'is_got_from_arguments' : {'gentoo' : 'CXX'},
                    'is_post_processed_in_a_function' : ''
                },
                'cpp_compiler_flags' : {
                    'is_applied_to_scons_env' : 'CXXFLAGS',
                    'is_saved_to_cache_file' : '',
                    'is_got_from_arguments' : {'gentoo' : 'CXXFLAGS'},
                    'is_post_processed_in_a_function' : ''
                },
                'linker_flags' : {
                    'is_applied_to_scons_env' : 'LINKFLAGS',
                    'is_saved_to_cache_file' : '',
                    'is_got_from_arguments' : {'gentoo' : 'LDFLAGS'},
                    'is_post_processed_in_a_function' : ''
                },
                'source_full' : {
                    'is_applied_to_scons_env' : '',
                    'is_saved_to_cache_file' : '',
                    'is_got_from_arguments' : '',
                    'is_post_processed_in_a_function' : ''
                }
            }
        }

        def _populate_os_dict():
            for os_dict_key in supported_oses.keys():
                os_dict = supported_oses[os_dict_key]
                for vars_key in vars_data.keys():
                    vars_data_dict = vars_data[vars_key]
                    for var_key in vars_data_dict.keys():
                        os_var_dict = vars_data_dict[var_key]
                        if os_var_dict['is_got_from_arguments']:
                            for key in os_var_dict['is_got_from_arguments'].keys():
                                if key == os_dict_key:
                                    os_dict[var_key] = os_var_dict['is_got_from_arguments'][key]
                            if var_key == os_detected_at and os_dict[var_key] == '':
                                print('_populate_os_dict ERROR: ' + var_key + \
                                                                ' is empty for ' + os_dict_key)
                                sys.exit(1)
        _populate_os_dict()

        def _myown_env_variables_descriptions():
            myowndict = {}
            for vars_key in vars_data.keys():
                vars_data_dict = vars_data[vars_key]
                for var_key in vars_data_dict.keys():
                    os_var_dict = vars_data_dict[var_key]
                    if os_var_dict['is_saved_to_cache_file']:
                        myowndict[var_key] = os_var_dict['is_saved_to_cache_file']
            return myowndict
        myown_env_dict = _myown_env_variables_descriptions()
        return supported_oses, vars_data, myown_env_dict

    int_obj['os_detected_at'] = 'destdir'
    int_obj['supported_oses'], int_obj['vars_data'], int_obj['myown_env_variables'] = \
                            _define_vars_data_and_myown_env_variables(int_obj['os_detected_at'])

    int_obj['scons_objects'] = {
        # 2 my own env variables are added in function read_variables_cache and then
        # their values are set in function _save_variables_cache
        'env' : Environment(),

        # This is a SCons.Variables.Variables class object for reading from /
        # writing to the variables cache file
        # Changed by calling method "Add" in function read_variables_cache
        'scons_var_obj' : Variables(int_obj['variables_cache_file'])
    }

    int_obj['my_vars'] = {
        'source_full' : _myown_os_path_join(int_obj['paths_and_names']['source_path'], \
                                                int_obj['paths_and_names']['source_name']),
        'compile_target' : _myown_os_path_join(int_obj['paths_and_names']['compile_path'], \
                                                int_obj['paths_and_names']['binary_name'])
    }

    # Set in function _detect_os, by finding non-empty value of scons argument
    # which name is determined by variable int_obj['os_detected_at']:
    #   (see function _define_vars_data_and_myown_env_variables)
    #      if we found argument 'DESTDIR' with non-empty value, then,
    #         OS is detected as Gentoo,
    #      if we found argument 'install_root' with non-empty value, then,
    #         OS is detected as Debian/Ubuntu
    # I don't use special tools for detecting OS intentionally,
    # because I define OS here as a set of variables
    int_obj['detected_os'] = ''

    # Values are set in function get_vars
    int_obj['got_vars'] = {}

    # Internal method
    def _detect_os():
        if int_obj['detected_os']:
            print('re-detecting Operating System is not supported')
            sys.exit(1)
        for key, nested_dict in int_obj['supported_oses'].items():
            os_argname = nested_dict[int_obj['os_detected_at']]
            print('checking for ' + int_obj['os_detected_at'] + ' as ' + os_argname + \
                                            '... (are we on ' + nested_dict['os_name'] + '?)')
            os_argvalue = ARGUMENTS.get(os_argname)
            if os_argvalue:
                int_obj['detected_os'] = key
                print('detected Operating System: ' + int_obj['detected_os'])
                return 1
        print('Operating System not detected')
        print('If your Operating System is not supported, you can simulate one of ' + \
                        'supported OSes by passing parameters with names that it has')
        print('Parameter names that each of supported Operating Systems has, ' + \
                        'you can see them in function _define_vars_data_and_myown_env_variables')
        sys.exit(1)

    # Internal method
    def _get_from_os(argname):
        if int_obj['detected_os'] == '' and argname != int_obj['os_detected_at']:
            print('_get_from_os ERROR: when getting ' + argname + \
                                    ' value, OS should be already detected')
            sys.exit(1)
        if argname == int_obj['os_detected_at']:
            _detect_os()
        detected_os = int_obj['detected_os']
        this_os_argname = int_obj['supported_oses'][detected_os][argname]
        argvalue = ARGUMENTS.get(this_os_argname)
        if argvalue:
            print(argname + ' (' + this_os_argname + ' in ' + \
                    int_obj['supported_oses'][detected_os]['os_name'] + \
                    ') argument found: ' + argvalue)
            return argvalue
        print(argname + ' (' + this_os_argname + ' in ' + \
                    int_obj['supported_oses'][detected_os]['os_name'] + \
                    ') argument not found')
        return ''

    # Internal method, goes to post_process_funcs
    def _reset_destdir():
        print('initially, destdir is set for default value without prefix: ' + \
                                                            int_obj['got_vars']['destdir'])
        if 'prefix' in int_obj['got_vars'] and int_obj['got_vars']['prefix']:
            int_obj['got_vars']['destdir'] = _myown_os_path_join(\
                                    int_obj['got_vars']['destdir'], \
                                    int_obj['got_vars']['prefix'], \
                                    int_obj['paths_and_names']['install_path'])
            print('destdir is reset using prefix and install_path: ' + \
                                    int_obj['got_vars']['destdir'])

    # Contains internal methods
    post_process_funcs = {}
    post_process_funcs['reset_destdir'] = _reset_destdir

    # Internal method, uses post_process_funcs
    def _post_process(funcname):
        if funcname in post_process_funcs:
            post_process_funcs[funcname]()
        else:
            print('_post_process ERROR: function ' + funcname + ' is not defined')
            sys.exit(1)

    # Internal method
    def _launch_post_process(vars_name):
        for var_dict in int_obj['vars_data'][vars_name].values():
            is_post_processed_in_a_function_key = var_dict['is_post_processed_in_a_function']
            if is_post_processed_in_a_function_key:
                _post_process(is_post_processed_in_a_function_key)

    # External method (FACADE: _get_from_os | use int_obj['my_vars'])
    def get_vars(vars_name):
        for var_key, var_dict in int_obj['vars_data'][vars_name].items():
            if var_dict['is_got_from_arguments']:
                var_value = _get_from_os(var_key)
                if var_value:
                    int_obj['got_vars'][var_key] = var_value
            else:
                int_obj['got_vars'][var_key] = int_obj['my_vars'][var_key]
        _launch_post_process(vars_name)

    # External method
    def apply_vars(vars_name):
        for var_key, var_dict in int_obj['vars_data'][vars_name].items():
            is_applied_to_scons_env = var_dict['is_applied_to_scons_env']
            if is_applied_to_scons_env:
                replace_args = {}
                print('setting ' + is_applied_to_scons_env + ' to ' + int_obj['got_vars'][var_key])
                replace_args[is_applied_to_scons_env] = \
                                            SCons.Util.CLVar(int_obj['got_vars'][var_key])
                int_obj['scons_objects']['env'].Replace(**replace_args)

    # External method
    def get_myown_env_variable(usedname):
        varname = int_obj['myown_env_variables'][usedname][0]
        value = int_obj['scons_objects']['env'][varname]
        if value:
            return int_obj['scons_objects']['env'][varname][0]
        return int_obj['scons_objects']['env'][varname]

    # Internal method
    def _set_myown_env_variable(usedname, value):
        varname = int_obj['myown_env_variables'][usedname][0]
        int_obj['scons_objects']['env'][varname] = SCons.Util.CLVar(value)

    # External method
    def read_variables_cache():
        for varname, is_saved_to_cache_file in int_obj['myown_env_variables'].items():
            print('Reading ' + varname + ' from cache as ' + is_saved_to_cache_file[0] + '...')
            int_obj['scons_objects']['scons_var_obj'].Add(is_saved_to_cache_file)
        # This adds new variables to Environment (doesn't rewrite it)
        # https://scons.org/doc/2.3.0/HTML/scons-user/x2445.html#AEN2504
        int_obj['scons_objects']['env'] = Environment(variables = \
                                            int_obj['scons_objects']['scons_var_obj'])

    # External method
    def save_variables_cache():
        for varname, is_saved_to_cache_file in int_obj['myown_env_variables'].items():
            print('Saving ' + varname + ' to cache as ' + is_saved_to_cache_file[0] + '...')
            _set_myown_env_variable(varname, int_obj['got_vars'][varname])
        # This saves only variables from 'scons_var_obj', not all variables from 'env'
        # (here 'env' is the environment to get the option values from)
        # https://scons.org/doc/3.0.1/HTML/scons-api/SCons.Variables.Variables-class.html#Save
        int_obj['scons_objects']['scons_var_obj'].Save(int_obj['variables_cache_file'], \
                                                                    int_obj['scons_objects']['env'])

    # External method
    def program_compile():
        target = int_obj['scons_objects']['env'].Program(target = \
                                                int_obj['got_vars']['compile_target'], \
                                                source = int_obj['got_vars']['source_full'])
        Default(target)
        print('will compile: target = ' + int_obj['got_vars']['compile_target'] + \
                                                ', source = ' + int_obj['got_vars']['source_full'])

    # External method
    def program_install():
        target = int_obj['scons_objects']['env'].Install(dir = get_myown_env_variable('destdir'), \
                                        source = get_myown_env_variable('compile_target'))
        Default(target)
        print('will install: dir = ' + get_myown_env_variable('destdir') + \
                            ', source = ' + get_myown_env_variable('compile_target'))

    ext_obj = {}
    ext_obj['get_vars'] = get_vars
    ext_obj['apply_vars'] = apply_vars
    ext_obj['get_myown_env_variable'] = get_myown_env_variable
    ext_obj['read_variables_cache'] = read_variables_cache
    ext_obj['save_variables_cache'] = save_variables_cache
    ext_obj['program_compile'] = program_compile
    ext_obj['program_install'] = program_install
    return ext_obj

def get_and_save_variables_for_install(helpers_):
    print('getting and saving variables needed for install...')
    helpers_['get_vars']('install_vars')
    helpers_['save_variables_cache']()

def mycompile(helpers_):
    helpers_['get_vars']('cpp_linker_vars')
    helpers_['apply_vars']('cpp_linker_vars')
    helpers_['program_compile']()

def myinstall(helpers_):
    helpers_['program_install']()

helpers = helpers_class()

helpers['read_variables_cache']()

if helpers['get_myown_env_variable']('destdir') and \
            helpers['get_myown_env_variable']('compile_target'):
    print('variables for install retrieved successfully; no need for re-configuring!')
    install_passed = ARGUMENTS.get('INSTALL')
    if install_passed == '1':
        myinstall(helpers)
    else:
        print('will not install; this SConscript requires passing "INSTALL=1" ' + \
                                'in command-line arguments instead of "install" after them')
        mycompile(helpers)
else:
    print('variables for install not retrieved')
    get_and_save_variables_for_install(helpers)
    mycompile(helpers)
