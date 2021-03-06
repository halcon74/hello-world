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

Example for CentOS
scons-3 PREFIX=/usr BUILDROOT=/home/user/rpmbuild/BUILDROOT/hello-world-0.7.1-1.x86_64 \
	CXX=g++ 'CXXFLAGS=-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection' \
	'LDFLAGS=-Wl,-z,relro  -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld'

SEE ALSO

build_on/gentoo/1_prepare_to_build/var/db/repos/localrepo/app-misc/Hello_World/Hello_World-9999.ebuild
and
build_on/debian_buster/1_prepare_to_build/debian/rules
and
build_on/centos_stream/1_prepare_to_build/SPECS/hello-world.spec


LONG VERSION

==Detecting OS==

This script is designed to detect Operating System it runs on
by the names of command-line arguments passed.

I don't use special tools for detecting OS intentionally,
because I define OS here as a set of variables, for:

- making similar installs on similar Linux distributions derived
from one distro;

- giving the user full freedom to simulate another OS if he wants to;

- setting custom hooks in any class function for any OS as simple as
if int_data['detected_os'] == 'gentoo':
if int_data['detected_os'] == 'debian-based':
if int_data['detected_os'] == 'rpm-based':
...
(currently, there are no such hooks).

Currently, the detecting of OS is doing so:

in function _detect_os, by finding non-empty value of scons argument
which name is determined by variable int_data['os_detected_at']:
    (see function _define_vars_data)
        if we found argument 'DESTDIR' with non-empty value, then,
            OS is detected as Gentoo,
        if we found argument 'install_root' with non-empty value, then,
            OS is detected as Debian-based Distro.

==Refusing COMMAND_LINE_TARGETS==

When this script is running for the first time with usual
command-line arguments, like
scons -j2 DESTDIR="/some/dir" PREFIX="/some/dir"
it performs COMPILE action
and
creates a variables-cache file.

The name of this file is set in function helpers_class,
variable int_data['variables_cache_file'].

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

from wrappers import wrappers_class

def exit_err_1(message):
    print(message)
    sys.exit(1)

# os.path.join drops all other parts when one part is an absolute path;
# os.path.normpath takes only one argument...
# In short, I haven't yet found the proper built-in function :)
def myown_os_path_join(*paths):
    joined = ''
    for path in paths:
        pattern = re.compile("^[a-zA-Z0-9_." + os.path.sep + "-]+$")
        match = pattern.match(path)
        if not match:
            exit_err_1('myown_os_path_join ERROR: path contains forbidden character(s)')
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
def helpers_class(paths_and_names):
    int_data, post_process_funcs, targets_to_clean = _internal_data(paths_and_names)

    ext_methods = {
        'get_vars' : lambda *args: get_vars(int_data, post_process_funcs, args[0]),
        'apply_vars' : lambda *args: apply_vars(int_data, args[0]),
        'get_myown_env_variable' : lambda *args: get_myown_env_variable(int_data, args[0]),
        'read_variables_cache' : lambda: read_variables_cache(int_data),
        'save_variables_cache' : lambda: save_variables_cache(int_data),
        'program_compile' : lambda: program_compile(int_data),
        'program_install' : lambda: program_install(int_data),
        'is_this_option_passed' : lambda *args: is_this_option_passed(int_data, args[0]),
        'is_install_argument_passed_and_1' : lambda: is_install_argument_passed_and_1(int_data),
        'is_any_target_passed' : lambda: is_any_target_passed(int_data),
        'clean_targets' : lambda : clean_targets(targets_to_clean)
    }
    return ext_methods

# ========== ALL THE FUNCTIONS BELOW ARE NOT INTENDED TO BE IMPORTED ==========

# ========== METHODS ==========

# Internal method
def _detect_os(int_data):
    if int_data['detected_os']:
        exit_err_1('re-detecting Operating System is not supported')
    for key, nested_dict in int_data['supported_oses'].items():
        os_argname = nested_dict[int_data['os_detected_at']]
        print('checking for ' + int_data['os_detected_at'] + ' as ' + os_argname + \
                                        '... (are we on ' + nested_dict['os_name'] + '?)')
        os_argvalue = int_data['scons_wrappers']['get_argument_from_cli'](os_argname)
        if os_argvalue:
            int_data['detected_os'] = key
            print('detected Operating System: ' + int_data['detected_os'])
            return 1
    print('Operating System not detected')
    print('If your Operating System is not supported, you can simulate one of ' + \
                    'supported OSes by passing parameters with names that it has')
    exit_err_1('Parameter names that each of supported Operating Systems has, ' + \
                    'you can see them in function _define_vars_data')

# Internal method
def _get_from_os(int_data, argname):
    if int_data['detected_os'] == '' and argname != int_data['os_detected_at']:
        exit_err_1('_get_from_os ERROR: when getting ' + argname + \
                                ' value, OS should be already detected')
    if argname == int_data['os_detected_at']:
        _detect_os(int_data)
    detected_os = int_data['detected_os']
    this_os_argname = int_data['supported_oses'][detected_os][argname]
    argvalue = int_data['scons_wrappers']['get_argument_from_cli'](this_os_argname)
    if argvalue:
        print(argname + ' (' + this_os_argname + ' in ' + \
                int_data['supported_oses'][detected_os]['os_name'] + \
                ') argument found: ' + argvalue)
        return argvalue
    print(argname + ' (' + this_os_argname + ' in ' + \
                int_data['supported_oses'][detected_os]['os_name'] + \
                ') argument not found')
    return ''

# Internal method, goes to post_process_funcs
def _reset_destdir(int_data):
    print('initially, destdir is set for default value without prefix: ' + \
                                                        int_data['got_vars']['destdir'])
    if 'prefix' in int_data['got_vars'] and int_data['got_vars']['prefix']:
        int_data['got_vars']['destdir'] = myown_os_path_join(\
                                int_data['got_vars']['destdir'], \
                                int_data['got_vars']['prefix'], \
                                int_data['paths_and_names']['install_path'])
        print('destdir is reset using prefix and install_path: ' + \
                                int_data['got_vars']['destdir'])

# Internal method, uses post_process_funcs
def _launch_post_process(int_data, post_process_funcs, vars_name):
    for var_dict in int_data['vars_data'][vars_name].values():
        funcname = var_dict['is_post_processed_in_a_function']
        if funcname:
            if funcname in post_process_funcs:
                post_process_funcs[funcname]()
            else:
                exit_err_1('_launch_post_process ERROR: function ' + funcname + ' is not defined')

# External method (FACADE: _get_from_os | use int_data['my_vars'])
def get_vars(int_data, post_process_funcs, vars_name):
    for var_key, var_dict in int_data['vars_data'][vars_name].items():
        print('get_vars: ' + var_key)
        if var_dict['is_got_from_arguments']:
            var_value = _get_from_os(int_data, var_key)
            if var_value:
                int_data['got_vars'][var_key] = var_value
        else:
            int_data['got_vars'][var_key] = int_data['my_vars'][var_key]
    _launch_post_process(int_data, post_process_funcs, vars_name)

# External method
def apply_vars(int_data, vars_name):
    for var_key, var_dict in int_data['vars_data'][vars_name].items():
        is_applied_to_scons_env = var_dict['is_applied_to_scons_env']
        if is_applied_to_scons_env:
            myvalue = int_data['got_vars'][var_key]
            print('setting ' + is_applied_to_scons_env + ' to ' + myvalue)
            int_data['scons_wrappers']['replace_var_in_env'](is_applied_to_scons_env, myvalue)

# External method
def get_myown_env_variable(int_data, usedname):
    varname = int_data['myown_env_variables'][usedname][0]
    value = int_data['scons_wrappers']['get_var_from_env'](varname)
    return value

# Internal method
def _set_myown_env_variable(int_data, usedname, value):
    varname = int_data['myown_env_variables'][usedname][0]
    int_data['scons_wrappers']['append_value_to_var_in_env'](varname, value)

# External method
def read_variables_cache(int_data):
    descriptions = int_data['myown_env_variables']
    int_data['scons_wrappers']['read_vars_from_cache'](descriptions)

# External method
def save_variables_cache(int_data):
    descriptions = int_data['myown_env_variables']
    got_vars = int_data['got_vars']
    int_data['scons_wrappers']['save_vars_to_cache'](descriptions, got_vars)

# External method
def program_compile(int_data):
    compile_source = int_data['got_vars']['source_full']
    compile_target = int_data['got_vars']['compile_target']
    int_data['scons_wrappers']['will_compile'](compile_source, compile_target)

# External method
def program_install(int_data):
    install_source = get_myown_env_variable(int_data, 'compile_target')
    install_target = get_myown_env_variable(int_data, 'destdir')
    int_data['scons_wrappers']['will_install'](install_source, install_target)

# External method
def is_this_option_passed(int_data, option):
    value = int_data['scons_wrappers']['get_option_from_cli'](option)
    return value

# Internal method
def _is_this_argument_passed(int_data, argument):
    argvalue = int_data['scons_wrappers']['get_argument_from_cli'](argument)
    return argvalue

# External method
def is_install_argument_passed_and_1(int_data):
    got_argument = _is_this_argument_passed(int_data, 'INSTALL')
    if got_argument and got_argument == '1':
        return 1
    else:
        return 0

# External method
def is_any_target_passed(int_data):
    result = int_data['scons_wrappers']['get_any_target_from_cli']()
    return result

# Internal method
def _get_object_file(int_data):
    object_file = os.path.splitext(int_data['my_vars']['source_full'])[0] + '.o'
    print('get_object_file: ' + object_file)
    return object_file

# Internal method
def _get_install_target(int_data):
    read_variables_cache(int_data)
    destdir = get_myown_env_variable(int_data, 'destdir')

    if destdir:
        install_target = myown_os_path_join(destdir, \
                                            int_data['paths_and_names']['binary_name'])

        print('get_install_target: ' + install_target)
        return install_target
    else:
        # See the comment for function clean_targets
        print('_get_install_target WARNING: cannot get destdir')
        return ''

# External method
# When cleaning, passing to scons whatever arguments (like DESTDIR=...) doesn't have any effect.
def clean_targets(targets_to_clean):
    for callback in targets_to_clean:
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

# ========== (DATA) CONSTRUCTOR ==========

def _populate_supported_oses(vars_data, supported_oses, os_detected_at):
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
                        exit_err_1('_populate_supported_oses ERROR: ' + var_key + \
                                                ' is empty for ' + supported_oses_key)

def _populate_myown_env_variables_descriptions(vars_data, myown_env_variables_descriptions):
    for vars_key in vars_data:
        vars_data_dict = vars_data[vars_key]
        for var_key in vars_data_dict:
            os_var_dict = vars_data_dict[var_key]
            if os_var_dict['is_saved_to_cache_file']:
                myown_env_variables_descriptions[var_key] = \
                                                os_var_dict['is_saved_to_cache_file']

def _define_vars_data(os_detected_at):
    vars_data = {
        # All that I add to env variables must be defined
        # in values of 'is_saved_to_cache_file' here
        'install_vars' : OrderedDict(),
        'compile_vars' : {}
    }

    vars_data['install_vars']['destdir'] = {
            'is_got_from_arguments' : {'gentoo' : 'DESTDIR', 'debian-based' : 'install_root', 'rpm-based': 'BUILDROOT'},
            'is_applied_to_scons_env' : '',
            'is_saved_to_cache_file' : ('MYCACHEDDIR', \
                            "cached 'dir' argument for " + \
                            "env.Install", ''),
            'is_post_processed_in_a_function' : 'reset_destdir'
    }
    vars_data['install_vars']['prefix'] = {
            'is_got_from_arguments' : {'gentoo' : 'PREFIX', 'debian-based' : 'prefix', 'rpm-based': 'PREFIX'},
            'is_applied_to_scons_env' : '',
            'is_saved_to_cache_file' : '',
            'is_post_processed_in_a_function' : ''
    }
    vars_data['install_vars']['compile_target'] = {
            'is_got_from_arguments' : '',
            'is_applied_to_scons_env' : '',
            'is_saved_to_cache_file' : ('MYCACHEDSOURCE', \
                            "cached 'source' argument for " + \
                            "env.Install", ''),
            'is_post_processed_in_a_function' : ''
    }
    vars_data['compile_vars'] = {
        'cpp_compiler' : {
            'is_got_from_arguments' : {'gentoo' : 'CXX', 'debian-based' : 'CXX', 'rpm-based': 'CXX'},
            'is_applied_to_scons_env' : 'CXX',
            'is_saved_to_cache_file' : '',
            'is_post_processed_in_a_function' : ''
        },
        'cpp_compiler_flags' : {
            'is_got_from_arguments' : {'gentoo' : 'CXXFLAGS', 'debian-based' : 'CXXFLAGS', 'rpm-based': 'CXXFLAGS'},
            'is_applied_to_scons_env' : 'CXXFLAGS',
            'is_saved_to_cache_file' : '',
            'is_post_processed_in_a_function' : ''
        },
        'linker_flags' : {
            'is_got_from_arguments' : {'gentoo' : 'LDFLAGS', 'debian-based' : 'LDFLAGS', 'rpm-based': 'LDFLAGS'},
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

    supported_oses = OrderedDict()
    # Is populated further in function _populate_supported_oses
    supported_oses['gentoo'] = {
        'os_name' : 'Gentoo'
    }
    supported_oses['debian-based'] = {
        'os_name' : 'Debian-based Distro'
    }
    supported_oses['rpm-based'] = {
        'os_name' : 'RPM-based Distro'
    }
    _populate_supported_oses(vars_data, supported_oses, os_detected_at)
    # Uncomment to look at the dictionary
    # print('supported_oses dictionary dump:')
    # print(supported_oses)

    # Is populated further in function _populate_myown_env_variables_descriptions
    myown_env_variables_descriptions = {}
    _populate_myown_env_variables_descriptions(vars_data, myown_env_variables_descriptions)
    # Uncomment to look at the dictionary
    # print('myown_env_variables_descriptions dictionary dump:')
    # print(myown_env_variables_descriptions)

    return vars_data, supported_oses, myown_env_variables_descriptions

def _check_paths_and_names(paths_and_names, mandatory_pnn_keys):
    if not isinstance(paths_and_names, dict):
        exit_err_1('_check_paths_and_names ERROR: paths_and_names is not dictionary')
    for mandatory_key in mandatory_pnn_keys:
        if mandatory_key not in paths_and_names:
            exit_err_1('_check_paths_and_names ERROR: mandatory key ' + mandatory_key + ' not found in paths_and_names')
        if not paths_and_names[mandatory_key]:
            exit_err_1("_check_paths_and_names ERROR: paths_and_names['" + mandatory_key + "'] is false")
        if not isinstance(paths_and_names[mandatory_key], str):
            exit_err_1("_check_paths_and_names ERROR: paths_and_names['" + mandatory_key + "'] is not string")
    for pnn_key in paths_and_names:
        if not pnn_key in mandatory_pnn_keys:
            exit_err_1('_check_paths_and_names ERROR: paths_and_names key ' + pnn_key + ' is not supported')

def _internal_data(paths_and_names):
    mydata = {}

    mydata['mandatory_pnn_keys'] = ['source_path', 'source_name', 'compile_path', 'install_path', 'binary_name']
    _check_paths_and_names(paths_and_names, mydata['mandatory_pnn_keys'])
    mydata['paths_and_names'] = paths_and_names

    variables_cache_file = 'scons_variables_cache.conf'
    mydata['variables_cache_file'] = variables_cache_file
    mydata['scons_wrappers'] = wrappers_class(variables_cache_file)

    mydata['scons_db_file'] = '.sconsign.dblite'

    mydata['os_detected_at'] = 'destdir'
    mydata['vars_data'], mydata['supported_oses'], mydata['myown_env_variables'] = \
                            _define_vars_data(mydata['os_detected_at'])

    # These are "ready values" for variables not got from ARGUMENTS
    # (see FACADE in function get_vars)
    mydata['my_vars'] = {
        'source_full' : myown_os_path_join(mydata['paths_and_names']['source_path'], \
                                                mydata['paths_and_names']['source_name']),
        'compile_target' : myown_os_path_join(mydata['paths_and_names']['compile_path'], \
                                                mydata['paths_and_names']['binary_name'])
    }

    # Set in function _detect_os
    mydata['detected_os'] = ''

    # Values are set in function get_vars
    mydata['got_vars'] = {}

    # Contains internal methods that are called in internal method _launch_post_process
    post_process_funcs = {
        'reset_destdir' : lambda: _reset_destdir(mydata)
    }

    # Contains differents callbacks (including internal methods) that are called in external method clean_targets
    targets_to_clean = (
        lambda: mydata['scons_db_file'],
        lambda: _get_object_file(mydata),
        lambda: mydata['my_vars']['compile_target'],
        lambda: _get_install_target(mydata),
        lambda: mydata['variables_cache_file']
    )

    return mydata, post_process_funcs, targets_to_clean
