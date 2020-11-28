#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# See the comments in helpers.py

from helpers import helpers_class

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

if helpers['is_any_target_passed']():
    print('this SConsctruct does not support COMMAND_LINE_TARGETS')
    sys.exit(1)

if helpers['is_this_option_passed']('clean'):
    helpers['clean_targets']()
else:
    helpers['read_variables_cache']()

    if helpers['get_myown_env_variable']('destdir') and \
                helpers['get_myown_env_variable']('compile_target'):
        print('variables for install retrieved successfully; no need for re-configuring!')

        if helpers['is_install_argument_passed_and_1']():
            myinstall(helpers)
        else:
            print('will not install; this SConstruct requires passing "INSTALL=1" in ' + \
                            'ARGUMENTS instead of "install" in COMMAND_LINE_TARGETS')
            mycompile(helpers)
    else:
        print('variables for install not retrieved')
        get_and_save_variables_for_install(helpers)
        mycompile(helpers)
