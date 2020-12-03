#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import SCons.Util
from SCons.Script import Environment, Variables, ARGUMENTS, COMMAND_LINE_TARGETS

def wrappers_class(variables_cache_file):
    int_data = _internal_data(variables_cache_file)

    ext_methods = {
        'get_argument_from_cli' : lambda *args: get_argument_from_cli(int_data, args[0]),
        'get_option_from_cli' : lambda *args: get_option_from_cli(int_data, args[0]),
        'get_any_target_from_cli' : lambda: get_any_target_from_cli(int_data),
        'get_var_from_env' : lambda *args: get_var_from_env(int_data, args[0]),
        'replace_var_in_env' : lambda *args: replace_var_in_env(int_data, args[0], args[1]),
        'append_value_to_var_in_env' : lambda *args: append_value_to_var_in_env(int_data, args[0], args[1]),
        'read_vars_from_cache' : lambda *args: read_vars_from_cache(int_data, args[0]),
        'save_vars_to_cache' : lambda *args: save_vars_to_cache(int_data, args[0], args[1], variables_cache_file),
        'will_compile' : lambda *args: will_compile(int_data, args[0], args[1]),
        'will_install' : lambda *args: will_install(int_data, args[0], args[1])
    }
    return ext_methods

# ========== ALL THE FUNCTIONS BELOW ARE NOT INTENDED TO BE IMPORTED ==========

# ========== METHODS ==========

# External method
def get_argument_from_cli(int_data, argname):
    myvalue = int_data['arguments'].get(argname)
    return myvalue

# External method
def get_option_from_cli(int_data, optname):
    myvalue = int_data['env'].GetOption(optname)
    return myvalue

# External method
def get_any_target_from_cli(int_data):
    if int_data['command_line_targets']:
        return 1
    else:
        return 0

# External method
def get_var_from_env(int_data, varname):
    mylist = int_data['env'][varname]
    if mylist:
        myvalue = int_data['env'][varname][0]
    else:
        myvalue = ''
    return myvalue

# External method
def replace_var_in_env(int_data, key, value):
    replace_args = {}
    replace_args[key] = int_data['clvar'](value)
    int_data['env'].Replace(**replace_args)

# External method
def append_value_to_var_in_env(int_data, key, value):
    int_data['env'][key] = int_data['clvar'](value)
    # print('append_value_to_var_in_env after appending: ' + key + ' = ' + int_data['env'][key])

# External method
def read_vars_from_cache(int_data, descriptions):
    for varname, is_saved_to_cache_file in descriptions.items():
        print('Reading ' + varname + ' from cache as ' + is_saved_to_cache_file[0] + '...')
        int_data['scons_var_obj'].Add(is_saved_to_cache_file)
    # This adds new variables to Environment (doesn't rewrite it)
    # https://scons.org/doc/2.3.0/HTML/scons-user/x2445.html#AEN2504
    int_data['env'] = int_data['new_env_call'](variables = int_data['scons_var_obj'])

# External method
def save_vars_to_cache(int_data, descriptions, values, variables_cache_file):
    for varname, is_saved_to_cache_file in descriptions.items():
        print('Saving ' + varname + ' to cache as ' + is_saved_to_cache_file[0] + '...')
        value = values[varname]
        append_value_to_var_in_env(int_data, is_saved_to_cache_file[0], value)
    # This saves only variables from 'scons_var_obj', not all variables from 'env'
    # (here 'env' is the environment to get the option values from)
    # https://scons.org/doc/3.0.1/HTML/scons-api/SCons.Variables.Variables-class.html#Save
    # print('save_vars_to_cache: scons_var_obj HelpText:')
    # print(int_data['scons_var_obj'].GenerateHelpText(int_data['env']))
    int_data['scons_var_obj'].Save(variables_cache_file, int_data['env'])

# External method
def will_compile(int_data, compile_source, compile_target):
    target_for_default = int_data['env'].Program(target = compile_target, source = compile_source)
    int_data['env'].Default(target_for_default)
    print('will compile: target = ' + compile_target + ', source = ' + compile_source)

# External method
def will_install(int_data, install_source, install_target):
    target_for_default = int_data['env'].Install(dir = install_target, source = install_source)
    int_data['env'].Default(target_for_default)
    print('will install: dir = ' + install_target + ', source = ' + install_source)

# ========== (DATA) CONSTRUCTOR ==========

def _internal_data(variables_cache_file):
    mydata = {
        # 2 my own env variables are added in function read_vars_from_cache and then
        # their values are set in function save_vars_to_cache
        'env' : Environment(),

        'new_env_call': lambda **kwargs: Environment(**kwargs),

        # This is a SCons.Variables.Variables class object for reading from /
        # writing to the variables cache file
        # Changed by calling method "Add" in function read_vars_from_cache
        'scons_var_obj' : Variables(variables_cache_file),

        'arguments' : ARGUMENTS,
        'command_line_targets' : COMMAND_LINE_TARGETS,

        # A class for appending values to environment variables (as lists)
        'clvar' : SCons.Util.CLVar
    }
    return mydata
