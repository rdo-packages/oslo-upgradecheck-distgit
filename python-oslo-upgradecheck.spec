
%global sname oslo.upgradecheck
%global pypi_name oslo-upgradecheck


# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-%{pypi_name}
Version:          XXX
Release:          XXX
Summary:          Common code for writing OpenStack upgrade checks
License:          ASL 2.0
URL:              https://docs.openstack.org/oslo.upgradecheck/latest/
Source0:          https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz

BuildArch:        noarch

%description
This project contains the common code necessary for writing upgrade checks in OpenStack projects.

%package -n python%{pyver}-%{pypi_name}
Summary:          Common code for writing OpenStack upgrade checks

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr >= 2.0.0
BuildRequires:    python%{pyver}-oslo-config
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-prettytable
BuildRequires:    python%{pyver}-stestr

Requires:         python%{pyver}-babel >= 2.3.4
Requires:         python%{pyver}-oslo-config >= 5.2.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-prettytable >= 0.7.1

# Handle python2 exception
%if %{pyver} == 2
Requires:    python-enum34
%endif

%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

%description -n python%{pyver}-%{pypi_name}
This project contains the common code necessary for writing upgrade checks in OpenStack projects.

%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack oslo.upgradecheck library

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the OpenStack oslo.upgradecheck library.

%prep
%setup -q -n %{sname}-%{upstream_version}

rm -rf *.egg-info
rm -rf {,test-}requirements.txt

%build
%{pyver_build}

sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{pyver_install}

%check
export PYTHONPATH=.
stestr-%{pyver} run

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/oslo_upgradecheck
%{pyver_sitelib}/*.egg-info

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%changelog
