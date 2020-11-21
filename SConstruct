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

def helpers_class():

    paths_and_names = {
        'source_path' : 'src',
        'source_name' : 'main.cpp',
        'compile_path' : 'build',
        'install_path' : 'bin',
        'binary_name' : 'Hello_World'
    }

    def _define_os_data_and_myown_env_variables(os_detected_at):
        os_dict = {}
        os_dict['supported_oses'] = OrderedDict()
        os_dict['supported_oses'] = {
            'gentoo' : {
                'os_name' : 'Gentoo'
            },
            'debian' : {
                'os_name' : 'Debian/Ubuntu'
            }
        }
        os_dict['os_vars'] = {
            'install_vars' : {
                'destdir' : {
                    'name_in_env' : '',
                    'var_goes_to_cache' : 'cached_dir',
                    'scons_add_tuple' : ('MYCACHEDDIR', \
                                    "cached 'dir' argument for obj['env'].Install", ''),
                    'get_from_os' : 1,
                    'names_in_oses' : {
                        'gentoo' : 'DESTDIR',
                        'debian' : 'install_root'
                    },
                    'post_processing' : 'reset_destdir'
                },
                'prefix' : {
                    'name_in_env' : '',
                    'var_goes_to_cache' : '',
                    'get_from_os' : 1,
                    'names_in_oses' : {
                        'gentoo' : 'PREFIX'
                    },
                    'post_processing' : ''
                },
                'compile_target' : {
                    'name_in_env' : '',
                    'var_goes_to_cache' : 'cached_source',
                    'scons_add_tuple' : ('MYCACHEDSOURCE', \
                                    "cached 'source' argument for obj['env'].Install", ''),
                    'get_from_os' : 0,
                    'post_processing' : ''
                }
            },
            'cpp_linker_vars' : {
                'cpp_compiler' : {
                    'name_in_env' : 'CXX',
                    'var_goes_to_cache' : '',
                    'get_from_os' : 1,
                    'names_in_oses' : {
                        'gentoo' : 'CXX'
                    },
                    'post_processing' : ''
                },
                'cpp_compiler_flags' : {
                    'name_in_env' : 'CXXFLAGS',
                    'var_goes_to_cache' : '',
                    'get_from_os' : 1,
                    'names_in_oses' : {
                        'gentoo' : 'CXXFLAGS'
                    },
                    'post_processing' : ''
                },
                'linker_flags' : {
                    'name_in_env' : 'LINKFLAGS',
                    'var_goes_to_cache' : '',
                    'get_from_os' : 1,
                    'names_in_oses' : {
                        'gentoo' : 'LDFLAGS'
                    },
                    'post_processing' : ''
                }
            }
        }

        def _populate_os_dict(supported_oses, os_vars):
            for os_dict_key in supported_oses.keys():
                os_dict = supported_oses[os_dict_key]
                for vars_key in os_vars.keys():
                    os_vars_dict = os_vars[vars_key]
                    for var_key in os_vars_dict.keys():
                        os_var_dict = os_vars_dict[var_key]
                        if os_var_dict['get_from_os']:
                            for key in os_var_dict['names_in_oses'].keys():
                                if key == os_dict_key:
                                    os_dict[var_key] = os_var_dict['names_in_oses'][key]
                            if var_key == os_detected_at and os_dict[var_key] == '':
                                print('_populate_os_dict ERROR: ' + var_key + \
                                                                ' is empty for ' + os_dict_key)
                                sys.exit(1)
        _populate_os_dict(os_dict['supported_oses'], os_dict['os_vars'])

        def _myown_env_variables_descriptions(os_vars):
            myowndict = {}
            for vars_key in os_vars.keys():
                os_vars_dict = os_vars[vars_key]
                for var_key in os_vars_dict.keys():
                    os_var_dict = os_vars_dict[var_key]
                    var_goes_to_cache = os_var_dict['var_goes_to_cache']
                    if var_goes_to_cache:
                        myowndict[var_goes_to_cache] = os_var_dict['scons_add_tuple']
            return myowndict
        myown_env_dict = _myown_env_variables_descriptions(os_dict['os_vars'])
        return os_dict, myown_env_dict

    os_detected_at = 'destdir'
    os_data, myown_env_variables = _define_os_data_and_myown_env_variables(os_detected_at)

    obj = {}

    # 2 my own env variables are added in function read_variables_cache and then
    # their values are set in function _save_variables_cache
    obj['env'] = Environment()

    # All that I add to env variables must be defined in tuples here
    obj['myown_env_variables'] = myown_env_variables

    obj['source_full'] = _myown_os_path_join(paths_and_names['source_path'], paths_and_names['source_name'])
    obj['compile_target'] = _myown_os_path_join(paths_and_names['compile_path'], paths_and_names['binary_name'])

    obj['os_data'] = os_data

    obj['my_vars'] = {}
    obj['my_vars']['compile_target'] = obj['compile_target']

    # Set in function _detect_os, by finding non-empty value of scons argument
    # which name is determined by variable 'os_detected_at' above:
    #   (see function _define_os_data_and_myown_env_variables)
    #      if we found argument 'DESTDIR' with non-empty value, then,
    #         OS is detected as Gentoo,
    #      if we found argument 'install_root' with non-empty value, then,
    #         OS is detected as Debian/Ubuntu
    # I don't use special tools for detecting OS intentionally,
    # because I define OS here as a set of variables
    obj['detected_os'] = ''

    # Values are set in functions _get_prefix_and_destdir and _get_cpp_linker_vars
    obj['got_vars'] = {}

    obj['variables_cache_file'] = 'scons_variables_cache.conf'

    # This is a SCons.Variables.Variables class object for reading from /
    # writing to the variables cache file
    # Changed by calling method "Add" in function read_variables_cache
    obj['scons_var_obj'] = Variables(obj['variables_cache_file'])

    # Internal method
    def _detect_os(self):
        if self['detected_os']:
            print('re-detecting Operating System is not supported')
            sys.exit(1)
        for key, nested_dict in self['os_data']['supported_oses'].items():
            os_argname = nested_dict[os_detected_at]
            print('checking for ' + os_detected_at + ' as ' + os_argname + \
                                            '... (are we on ' + nested_dict['os_name'] + '?)')
            os_argvalue = ARGUMENTS.get(os_argname)
            if os_argvalue:
                self['detected_os'] = key
                print('detected Operating System: ' + self['detected_os'])
                return 1
        print('Operating System not detected')
        print('If your Operating System is not supported, you can simulate one of \
                                supported OSes by passing parameters with names that it has')
        print('Parameter names that each of supported Operating Systems has, \
                                        you can see them in function _define_os_data_and_myown_env_variables')
        sys.exit(1)

    # Internal method
    def _get_from_os(self, argname):
        if self['detected_os'] == '' and argname != os_detected_at:
            print('_get_from_os ERROR: when getting ' + argname + \
                                    ' value, OS should be already detected')
            sys.exit(1)
        if argname == os_detected_at:
            _detect_os(self)
        detected_os = self['detected_os']
        this_os_argname = self['os_data']['supported_oses'][detected_os][argname]
        argvalue = ARGUMENTS.get(this_os_argname)
        if argvalue:
            print(argname + ' (' + this_os_argname + ' in ' + \
                    self['os_data']['supported_oses'][detected_os]['os_name'] + \
                    ') argument found: ' + argvalue)
            return argvalue
        print(argname + ' (' + this_os_argname + ' in ' + \
                    self['os_data']['supported_oses'][detected_os]['os_name'] + \
                    ') argument not found')
        return ''

    # Internal method, goes to post_process_funcs
    def _reset_destdir(self):
        print('until prefix is found, destdir is set for default value without prefix: ' + \
                                                            self['got_vars']['destdir'])
        if 'prefix' in self['got_vars'] and self['got_vars']['prefix']:
            self['got_vars']['destdir'] = _myown_os_path_join(\
                                            self['got_vars']['destdir'], \
                                            self['got_vars']['prefix'], paths_and_names['install_path'])
            print('destdir is reset using prefix and install_path: ' + self['got_vars']['destdir'])

    # Contains internal methods
    post_process_funcs = {}
    post_process_funcs['reset_destdir'] = _reset_destdir

    # Internal method, uses post_process_funcs
    def _post_process(self, funcname):
        if funcname in post_process_funcs:
            post_process_funcs[funcname](self)
        else:
            print('_post_process ERROR: function ' + funcname + ' is not defined')
            sys.exit(1)

    # Internal method
    def _launch_post_process(self, vars_name):
        os_vars = self['os_data']['os_vars']
        for vars_key in os_vars.keys():
            if vars_key == vars_name:
                os_vars_dict = os_vars[vars_key]
                for var_key in os_vars_dict.keys():
                    os_var_dict = os_vars_dict[var_key]
                    post_processing_key = os_var_dict['post_processing']
                    if post_processing_key:
                        _post_process(self, post_processing_key)

    # External method (FACADE: _get_from_os | use obj['my_vars'])
    def get_vars(vars_name):
        self = obj
        os_vars = self['os_data']['os_vars']
        for vars_key in os_vars.keys():
            if vars_key == vars_name:
                os_vars_dict = os_vars[vars_key]
                for var_key in os_vars_dict.keys():
                    os_var_dict = os_vars_dict[var_key]
                    if os_var_dict['get_from_os']:
                        var_value = _get_from_os(self, var_key)
                        if var_value:
                            self['got_vars'][var_key] = var_value
                    else:
                        self['got_vars'][var_key] = self['my_vars']
        _launch_post_process(self, vars_name)

    obj['get_vars'] = get_vars
    return obj

def _get_prefix_and_destdir(obj):
    obj['get_vars']('install_vars')

def _get_cpp_linker_vars(obj):
    obj['get_vars']('cpp_linker_vars')

def _apply_cpp_linker_vars(obj):
    for key, mydict in obj['os_data']['os_vars']['cpp_linker_vars'].items():
        name_in_env = mydict['name_in_env']
        if name_in_env:
            replace_args = {}
            print('setting ' + name_in_env + ' to ' + obj['got_vars'][key])
            replace_args[name_in_env] = SCons.Util.CLVar(obj['got_vars'][key])
            obj['env'].Replace(**replace_args)

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
    _set_myown_env_variable(obj, 'cached_dir', obj['got_vars']['destdir'])
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
    print('will compile: target = ' + obj['compile_target'] + \
                                            ', source = ' + obj['source_full'])

def myinstall(obj):
    target = obj['env'].Install(dir = get_myown_env_variable(obj, 'cached_dir'), \
                                    source = get_myown_env_variable(obj, 'cached_source'))
    Default(target)
    print('will install: dir = ' + get_myown_env_variable(obj, 'cached_dir') + \
                        ', source = ' + get_myown_env_variable(obj, 'cached_source'))

helpers = helpers_class()

read_variables_cache(helpers)

if get_myown_env_variable(helpers, 'cached_dir') and \
            get_myown_env_variable(helpers, 'cached_source'):
    print('variables for install retrieved successfully; no need for re-configuring!')
    install_passed = ARGUMENTS.get('INSTALL')
    if install_passed == '1':
        myinstall(helpers)
    else:
        print('will not install; this SConscript requires passing "INSTALL=1" \
                                in command-line arguments instead of "install" after them')
        mycompile(helpers)
else:
    print('variables for install not retrieved')
    get_and_save_variables_for_install(helpers)
    mycompile(helpers)
