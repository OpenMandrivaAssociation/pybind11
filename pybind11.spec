%global debug_package %{nil}

Name:    pybind11
Version:	2.6.1
Release:	1
Summary: Seamless operability between C++11 and Python
License: BSD
URL:	 https://github.com/pybind/pybind11
Source0: https://github.com/pybind/pybind11/archive/v%{version}/%{name}-%{version}.tar.gz

# Don't use pip to get path to headers
#Patch1:  pybind11-2.2.3-nopip.patch

# Needed to build the python libraries
BuildRequires: python2-devel
BuildRequires: python2-setuptools

# Needed to build the python libraries
BuildRequires: python3-devel
BuildRequires: python-setuptools

BuildRequires: eigen3-devel
BuildRequires: gcc-c++
BuildRequires: cmake

%global base_description \
pybind11 is a lightweight header-only library that exposes C++ types \
in Python and vice versa, mainly to create Python bindings of existing \
C++ code.

%description
%{base_description}

%package devel
Summary:  Development headers for pybind11
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
Provides: %{name}-static = %{version}-%{release}
# For dir ownership
Requires: cmake

%description devel
%{base_description}

This package contains the development headers for pybind11.

%package -n     python2-%{name}
Summary:        %{summary}
Requires: %{name}-devel = %{version}-%{release}

%description -n python2-%{name}
%{base_description}

This package contains the Python 2 files.

%package -n     python-%{name}
Summary:        %{summary}

Requires: %{name}-devel = %{version}-%{release}

%description -n python-%{name}
%{base_description}

This package contains the Python 3 files.

%prep
%setup -q

%build
for py in python2 python3; do
    mkdir $py
    cd $py
    %cmake ../.. -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=%{_bindir}/$py -DPYBIND11_INSTALL=TRUE -DUSE_PYTHON_INCLUDE_DIR=FALSE -DPYBIND11_TEST=FALSE
    %make
    cd ../..
done

python2 setup.py build
python3 setup.py build

%check
#make -C python2 check %{?_smp_mflags}
#make -C python3 check %{?_smp_mflags}

%install
# Doesn't matter if both installs run
%make_install -C python2/build
%make_install -C python3/build
PYBIND11_USE_CMAKE=true python2 setup.py install --root %{buildroot} "--install-purelib" "%{python2_sitearch}"
PYBIND11_USE_CMAKE=true python3 setup.py install --root %{buildroot} "--install-purelib" "%{python3_sitearch}"

%files devel
%doc README.rst LICENSE
%{_bindir}/pybind11-config
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/

%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%{python2_sitearch}/%{name}-%{version}-py?.?.egg-info

%files -n python-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py?.?.egg-info
