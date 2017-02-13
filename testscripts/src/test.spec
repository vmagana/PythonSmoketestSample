Summary: This prints hello world test of rpm
Name: test
Version:1
Release:1
Copyright:GPL
Group:Application/System
Source:test.cpp
BuildRoot:/home/victora
%description: This package prints hello world
%prep

%build
g++ -o ./test ./test.cpp
%install
./test

