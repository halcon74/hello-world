#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
An attempt to make a helper for building/installing
on different (*nix primarily) OSes via SCons "out-of-the-box"
(that is without (distro's) maintainer patches).



TL;DR

How to compile and install:

Example for Gentoo
scons -j2 PREFIX=/usr DESTDIR=/var/tmp/portage/app-misc/Hello_World-9999/image \
        CXX=x86_64-pc-linux-gnu-g++ CXXFLAGS="-O2 -march=native -pipe" \
        LDFLAGS="-Wl,-O1 -Wl,--as-needed"
scons -j2 PREFIX=/usr DESTDIR=/var/tmp/portage/app-misc/Hello_World-9999/image \
        CXX=x86_64-pc-linux-gnu-g++ CXXFLAGS="-O2 -march=native -pipe" \
        LDFLAGS="-Wl,-O1 -Wl,--as-needed" INSTALL=1

Example for Debian
scons prefix=/usr install_root=/home/user/hello-world-0.5.3/hello-world-0.5.3/debian/hello-world/usr \
        CXX=g++ CXXFLAGS="-g -O2 -fdebug-prefix-map=/home/user/hello-world-0.5.3/hello-world-0.5.3=. -fstack-protector-strong -Wformat -Werror=format-security" \
        LDFLAGS="-Wl,-z,relro"
scons prefix=/usr install_root=/home/user/hello-world-0.5.3/hello-world-0.5.3/debian/hello-world/usr \
        CXX=g++ CXXFLAGS="-g -O2 -fdebug-prefix-map=/home/user/hello-world-0.5.3/hello-world-0.5.3=. -fstack-protector-strong -Wformat -Werror=format-security" \
        LDFLAGS="-Wl,-z,relro" INSTALL=1



SEE ALSO

build_on/gentoo/1_prepare_to_build/var/db/repos/localrepo/app-misc/Hello_World/Hello_World-9999.ebuild
and
build_on/debian_buster/1_prepare_to_build/debian/rules



LONG VERSION

==Detecting OS==

This script is designed to detect Operating System it runs on
by the names of command-line arguments passed.

I don't use special tools for detecting OS intentionally,
because I define OS here as a set of variables, for:

- making similar installs on similar Linux distributions derived
from one distro;
- giving the user full freedom to simulate another OS if he wants to.

Currently, the detecting of OS is doing so:

in function _detect_os, by finding non-empty value of scons argument
which name is determined by variable int_obj['os_detected_at']:
    (see function _define_vars_data)
        if we found argument 'DESTDIR' with non-empty value, then,
            OS is detected as Gentoo,
        if we found argument 'install_root' with non-empty value, then,
            OS is detected as Debian/Ubuntu.

==Refusing COMMAND_LINE_TARGETS==

When this script is running for the first time with usual
command-line arguments, like
scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir"
it performs COMPILE action
and
creates a variables-cache file.

The name of this file is set in function helpers_class,
variable int_obj['variables_cache_file'].

With this file, no redundant actions (that are usually called
're-configuring') will be performed during the second and all the
consequent runs (will be performed only constructing the class
and reading variables cache).

This file contains variables that are needed for INSTALL action
only, not for COMPILE action.

The COMPILE action can be done after creating this file as well;
this file does not make any harm for it.

Moreover, this file makes the consequent compiling runs faster,
because the script will not try to get variables needed for
INSTALL action and to save them in the variables-cache file.

THE MOST IMPORTANT PART: this script does not contain an usual
target "install", because I prefer to use command-line arguments
instead of targets.

( Why? Because, when using targets, I always meet a "SCons magic"
that breaks the imperative logic that I am trying to implement here.
This approach has a negative consequence: I have to re-write manually the
functionality of cleaning targets (option -c, --clean).
So far, I'm getting it done... If you found a way to use targets and
at the same time to preserve the imperative logic, please let me know. )

For this reason, this script requires
passing "INSTALL=1" IN ARGUMENTS
instead of
passing "install" in COMMAND_LINE_TARGETS

That is, if you run
scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" install
the INSTALL action WILL NOT be performed.

The INSTALL action WILL be performed
if you run
scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL=1

And, in conclusion:
As the INSTALL action requires the variables-cache file,
it will not be performed without this file.

That is, if you run
scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir" INSTALL=1
as the first run (or after deleting the variables-cache file)
the script will be going to COMPILE (and to get and save the
variables needed for INSTALL), not to INSTALL.

IMHO, this algorithm is consistent enough.

A side effect of this algorithm:
you can run this script two times with "INSTALL=1"
(the first run will COMPILE, the second run will INSTALL)
:)
"""

from collections import OrderedDict
import os
import os.path
import re
import sys
import SCons.Util
from SCons.Script import Environment, Variables, ARGUMENTS, COMMAND_LINE_TARGETS

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

# If you are surprised that I call it a class:
# https://forums.gentoo.org/viewtopic-p-8527031.html#8527031
# (search string: "OOP, because perl") :)
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
    int_obj['scons_db_file'] = '.sconsign.dblite'

    def _define_vars_data(os_detected_at):
        supported_oses = OrderedDict()

        # Is populated further in function _populate_supported_oses
        supported_oses['gentoo'] = {
            'os_name' : 'Gentoo'
        }
        supported_oses['debian'] = {
            'os_name' : 'Debian/Ubuntu'
        }

        vars_data = {
            # All that I add to env variables must be defined
            # in values of 'is_saved_to_cache_file' here
            'install_vars' : OrderedDict(),
            'cpp_linker_vars' : {}
        }

        vars_data['install_vars']['destdir'] = {
                'is_got_from_arguments' : {'gentoo' : 'DESTDIR', 'debian' : 'install_root'},
                'is_applied_to_scons_env' : '',
                'is_saved_to_cache_file' : ('MYCACHEDDIR', \
                                "cached 'dir' argument for " + \
                                "int_obj['scons_objects']['env'].Install", ''),
                'is_post_processed_in_a_function' : 'reset_destdir'
        }
        vars_data['install_vars']['prefix'] = {
                'is_got_from_arguments' : {'gentoo' : 'PREFIX', 'debian' : 'prefix'},
                'is_applied_to_scons_env' : '',
                'is_saved_to_cache_file' : '',
                'is_post_processed_in_a_function' : ''
        }
        vars_data['install_vars']['compile_target'] = {
                'is_got_from_arguments' : '',
                'is_applied_to_scons_env' : '',
                'is_saved_to_cache_file' : ('MYCACHEDSOURCE', \
                                "cached 'source' argument for " + \
                                "int_obj['scons_objects']['env'].Install", ''),
                'is_post_processed_in_a_function' : ''
        }
        vars_data['cpp_linker_vars'] = {
            'cpp_compiler' : {
                'is_got_from_arguments' : {'gentoo' : 'CXX', 'debian' : 'CXX'},
                'is_applied_to_scons_env' : 'CXX',
                'is_saved_to_cache_file' : '',
                'is_post_processed_in_a_function' : ''
            },
            'cpp_compiler_flags' : {
                'is_got_from_arguments' : {'gentoo' : 'CXXFLAGS', 'debian' : 'CXXFLAGS'},
                'is_applied_to_scons_env' : 'CXXFLAGS',
                'is_saved_to_cache_file' : '',
                'is_post_processed_in_a_function' : ''
            },
            'linker_flags' : {
                'is_got_from_arguments' : {'gentoo' : 'LDFLAGS', 'debian' : 'LDFLAGS'},
                'is_applied_to_scons_env' : 'LINKFLAGS',
                'is_saved_to_cache_file' : '',
                'is_post_processed_in_a_function' : ''
            },
            'source_full' : {
                'is_got_from_arguments' : '',
                'is_applied_to_scons_env' : '',
                'is_saved_to_cache_file' : '',
                'is_post_processed_in_a_function' : ''
            }
        }

        # Is populated further in function _populate_myown_env_variables_descriptions
        myown_env_variables_descriptions = {}

        def _populate_supported_oses():
            for supported_oses_key in supported_oses:
                # Otherwise here is
                # "dictionary changed size during iteration" RuntimeError
                supported_oses_dict = supported_oses[supported_oses_key]
                for vars_key in vars_data:
                    vars_dict = vars_data[vars_key]
                    for var_key in vars_dict:
                        var_dict = vars_dict[var_key]
                        if var_dict['is_got_from_arguments']:
                            for key in var_dict['is_got_from_arguments']:
                                if key == supported_oses_key:
                                    # Otherwise here is
                                    # "dictionary changed size during iteration" RuntimeError
                                    supported_oses_dict[var_key] = \
                                                        var_dict['is_got_from_arguments'][key]
                            if var_key == os_detected_at and supported_oses_dict[var_key] == '':
                                print('_populate_supported_oses ERROR: ' + var_key + \
                                                        ' is empty for ' + supported_oses_key)
                                sys.exit(1)
        _populate_supported_oses()
        # Uncomment to look at the dictionary
        # print('supported_oses dictionary dump:')
        # print(supported_oses)

        def _populate_myown_env_variables_descriptions():
            for vars_key in vars_data:
                vars_data_dict = vars_data[vars_key]
                for var_key in vars_data_dict:
                    os_var_dict = vars_data_dict[var_key]
                    if os_var_dict['is_saved_to_cache_file']:
                        myown_env_variables_descriptions[var_key] = \
                                                        os_var_dict['is_saved_to_cache_file']
        _populate_myown_env_variables_descriptions()
        # Uncomment to look at the dictionary
        # print('myown_env_variables_descriptions dictionary dump:')
        # print(myown_env_variables_descriptions)

        return supported_oses, vars_data, myown_env_variables_descriptions

    int_obj['os_detected_at'] = 'destdir'
    int_obj['supported_oses'], int_obj['vars_data'], int_obj['myown_env_variables'] = \
                            _define_vars_data(int_obj['os_detected_at'])

    int_obj['scons_objects'] = {
        # 2 my own env variables are added in function read_variables_cache and then
        # their values are set in function _save_variables_cache
        'env' : Environment(),

        # This is a SCons.Variables.Variables class object for reading from /
        # writing to the variables cache file
        # Changed by calling method "Add" in function read_variables_cache
        'scons_var_obj' : Variables(int_obj['variables_cache_file']),

        'arguments' : ARGUMENTS,
        'command_line_targets' : COMMAND_LINE_TARGETS,

        # A class for appending values to environment variables (as lists)
        'clvar' : SCons.Util.CLVar
    }

    # These are "ready values" for variables not got from ARGUMENTS
    # (see FACADE in function get_vars)
    int_obj['my_vars'] = {
        'source_full' : _myown_os_path_join(int_obj['paths_and_names']['source_path'], \
                                                int_obj['paths_and_names']['source_name']),
        'compile_target' : _myown_os_path_join(int_obj['paths_and_names']['compile_path'], \
                                                int_obj['paths_and_names']['binary_name'])
    }

    # Set in function _detect_os
    int_obj['detected_os'] = ''

    # Values are set in function get_vars
    int_obj['got_vars'] = {}

    # Callbacks are called in external method clean_targets
    int_obj['targets_to_clean'] = (
        lambda: int_obj['scons_db_file'],
        lambda: _get_object_file(),
        lambda: int_obj['my_vars']['compile_target'],
        lambda: _get_install_target(),
        lambda: int_obj['variables_cache_file']
    )

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
                        'you can see them in function _define_vars_data')
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
            print('get_vars: ' + var_key)
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
                                            int_obj['scons_objects']['clvar'](int_obj['got_vars'][var_key])
                int_obj['scons_objects']['env'].Replace(**replace_args)

    # External method
    def get_myown_env_variable(usedname):
        varname = int_obj['myown_env_variables'][usedname][0]
        value = int_obj['scons_objects']['env'][varname]
        if value:
            return int_obj['scons_objects']['env'][varname][0]
        return ''

    # Internal method
    def _set_myown_env_variable(usedname, value):
        varname = int_obj['myown_env_variables'][usedname][0]
        int_obj['scons_objects']['env'][varname] = int_obj['scons_objects']['clvar'](value)

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
        int_obj['scons_objects']['env'].Default(target)
        print('will compile: target = ' + int_obj['got_vars']['compile_target'] + \
                                                ', source = ' + int_obj['got_vars']['source_full'])

    # External method
    def program_install():
        target = int_obj['scons_objects']['env'].Install(dir = get_myown_env_variable('destdir'), \
                                        source = get_myown_env_variable('compile_target'))
        int_obj['scons_objects']['env'].Default(target)
        print('will install: dir = ' + get_myown_env_variable('destdir') + \
                            ', source = ' + get_myown_env_variable('compile_target'))

    # External method
    def is_this_option_passed(option):
        return int_obj['scons_objects']['env'].GetOption(option)

    # Internal method
    def _is_this_argument_passed(argument):
        return int_obj['scons_objects']['arguments'].get(argument)

    # External method
    def is_install_argument_passed_and_1():
        got_argument = _is_this_argument_passed('INSTALL')
        if got_argument and got_argument == '1':
            return 1
        else:
            return 0

    # External method
    def is_any_target_passed():
        if int_obj['scons_objects']['command_line_targets']:
            return 1
        else:
            return 0

    # Internal method
    def _get_object_file():
        object_file = os.path.splitext(int_obj['my_vars']['source_full'])[0] + '.o'
        print('get_object_file: ' + object_file)
        return object_file

    # Internal method
    def _get_install_target():
        read_variables_cache()
        destdir = get_myown_env_variable('destdir')

        if destdir:
            install_target = _myown_os_path_join(destdir, \
                                                int_obj['paths_and_names']['binary_name'])

            print('get_install_target: ' + install_target)
            return install_target
        else:
            # See the comment for function clean_targets
            print('_get_install_target WARNING: cannot get destdir')
            return ''

    # External method
    # When cleaning, passing to scons whatever arguments (like DESTDIR=...) doesn't have any effect.
    def clean_targets():
        for callback in int_obj['targets_to_clean']:
            somepath = callback()

            # No directories should be deleted, only files
            if os.path.isfile(somepath):

                # No files outside the current directory should be deleted
                target_to_clean = os.path.relpath(somepath, start=os.curdir)

                if target_to_clean:
                    print('deleting target: ' + target_to_clean)
                    os.unlink(target_to_clean)
                else:
                    print('clean_targets WARNING: ' + target_to_clean + \
                                            ' seems to be OUTSIDE the current directory! not cleaned')
                    continue
            else:
                print('clean_targets WARNING: ' + somepath + ' is not file! not cleaned')
                continue

    ext_obj = {}
    ext_obj['get_vars'] = get_vars
    ext_obj['apply_vars'] = apply_vars
    ext_obj['get_myown_env_variable'] = get_myown_env_variable
    ext_obj['read_variables_cache'] = read_variables_cache
    ext_obj['save_variables_cache'] = save_variables_cache
    ext_obj['program_compile'] = program_compile
    ext_obj['program_install'] = program_install
    ext_obj['is_this_option_passed'] = is_this_option_passed
    ext_obj['is_install_argument_passed_and_1'] = is_install_argument_passed_and_1
    ext_obj['is_any_target_passed'] = is_any_target_passed
    ext_obj['clean_targets'] = clean_targets
    return ext_obj
