Summary: This prints hello world test of rpm
Name: helloworld
Version: 1.0
Release: 1%{?dist}
License: GPL
Group: Application/System
Source0: helloworld-1.0.tar.gz
Buildroot: <dir>

%define debug_package %{nil}

%description
This package prints hello world

%prep
%setup

%build
make PREFIX=/usr %{?_smp_mflags}

%install
make install PREFIX=/usr DESTDIR=%{?buildroot}
cp %{?buildroot}/usr/bin/helloworld %{_bindir}  

%clean
rm -rf %{?buildroot}


%files
%{_bindir}/helloworld

%defattr(-,root,root,-)
