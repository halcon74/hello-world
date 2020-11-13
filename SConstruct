env = Environment()

program_name = "Hello_World"
program_source = "src/main.cpp"

# default
program_destdir = "build"

print("checking for DESTDIR... (are we on Gentoo?)")
get_destdir = ARGUMENTS.get('DESTDIR')
if get_destdir:
    program_destdir = get_destdir
    print("DESTDIR found and will be used: " + program_destdir)
else:
    print("DESTDIR not found")
    print("checking for install_root... (are we on Debian/Ubuntu?)")
    get_install_root = ARGUMENTS.get('install_root')
    if get_install_root:
        program_destdir = get_install_root
        print("install_root found and will be used: " + program_destdir)
    else:
        print("install_root not found")
        print("default destination directory will be used: " + program_destdir)

if program_destdir.endswith('/'):
    program_target = program_destdir + program_name
else:
    program_target = program_destdir + "/" + program_name

print("Building: target = " + program_target + ", source = " + program_source)

target = env.Program(target=program_target, source=program_source)
Default(target)
