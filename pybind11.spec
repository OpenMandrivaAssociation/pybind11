%global debug_package %{nil}

Name:    pybind11
Version:	2.13.5
Release:	1
Summary: Seamless operability between C++11 and Python
License: BSD
URL:	 https://github.com/pybind/pybind11
Source0: https://github.com/pybind/pybind11/archive/v%{version}/%{name}-%{version}.tar.gz

# Don't use pip to get path to headers
#Patch1:  pybind11-2.2.3-nopip.patch

# Needed to build the python libraries
BuildRequires: python-devel
BuildRequires: python-setuptools

BuildRequires: eigen3-devel
BuildRequires: cmake
BuildRequires: ninja

%global base_description \
pybind11 is a lightweight header-only library that exposes C++ types \
in Python and vice versa, mainly to create Python bindings of existing \
C++ code.

%description
%{base_description}

%package devel
Summary:  Development headers for pybind11

%description devel
%{base_description}

This package contains the development headers for pybind11.

%package -n     python-%{name}
Summary:        %{summary}

Requires: %{name}-devel = %{version}-%{release}

%description -n python-%{name}
%{base_description}

This package contains the Python 3 files.

%prep
%autosetup -p1

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DPYBIND11_INSTALL=TRUE -DUSE_PYTHON_INCLUDE_DIR=FALSE -DPYBIND11_TEST=FALSE -G Ninja
cd ..
python setup.py build

%install
%ninja_install -C build
PYBIND11_USE_CMAKE=true python setup.py install --root %{buildroot} "--install-purelib" "%{python3_sitearch}"

%files devel
%doc README.rst LICENSE
%{_bindir}/pybind11-config
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/
%{_datadir}/pkgconfig/pybind11.pc

%files -n python-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py*.egg-info
