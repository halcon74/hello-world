Name: hello-world
Version: 0.7.1
Release: 1

Summary: Test program printing 'Hello World!' to STDOUT
License: GPL2+

BuildArch: x86_64

URL: https://github.com/halcon74/%{name}
Source0: https://github.com/halcon74/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: python3-scons
BuildRoot: ~/rpmbuild/

%description
Test program printing 'Hello World!' to STDOUT, that actually 
turned into an attempt to make a helper for building/installing 
on different (*nix primarily) OSes via SCons "out-of-the-box" 
(that is without (distro's) maintainer patches).

%define _build_id_links none

%define _BUILDROOT %{buildroot}
%define _PREFIX /usr
%define _CXX %{__cxx}
%define _CXXFLAGS %{build_cxxflags}
%define _LDFLAGS %{build_ldflags}
%define _RPM_SCONS_OPTIONS BUILDROOT=%{_BUILDROOT} PREFIX=%{_PREFIX} CXX=%{_CXX} CXXFLAGS='%{_CXXFLAGS}' LDFLAGS='%{_LDFLAGS}'
%define _RPM_SCONS_INSTALL_OPTIONS %{_RPM_SCONS_OPTIONS} INSTALL=1

%define _binary_name Hello_World

%prep

%setup -q

%build

scons-3 %{_RPM_SCONS_OPTIONS}

%install

mkdir -p %{_BUILDROOT}%{_PREFIX}
scons-3 %{_RPM_SCONS_INSTALL_OPTIONS}

%clean

scons-3 -c

%files
%{_bindir}/%{_binary_name}
%doc README.md
%doc docs/ToDo
%doc docs/used_sources

%changelog
* Fri Dec 18 2020 Alexey Mishustin <halcon@tuta.io> - 0.7.1-1
- Initial CentOS release.
