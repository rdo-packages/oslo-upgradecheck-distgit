%global sname oslo.upgradecheck
%global pypi_name oslo-upgradecheck
%global with_doc 1


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This project contains the common code necessary for writing upgrade checks in OpenStack projects.

Name:             python-%{pypi_name}
Version:          XXX
Release:          XXX
Summary:          Common code for writing OpenStack upgrade checks
License:          ASL 2.0
URL:              https://docs.openstack.org/oslo.upgradecheck/latest/
Source0:          https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:          Common code for writing OpenStack upgrade checks

BuildRequires:    python3-devel
BuildRequires:    python3-pbr >= 2.0.0
BuildRequires:    python3-oslo-config
BuildRequires:    python3-oslotest
BuildRequires:    python3-prettytable
BuildRequires:    python3-stestr

Requires:         python3-oslo-config >= 5.2.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-prettytable >= 0.7.1


%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack oslo.upgradecheck library

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the OpenStack oslo.upgradecheck library.
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

rm -rf *.egg-info
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
export PYTHONPATH=.
PYTHON=%{__python3} stestr-3 run

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/oslo_upgradecheck
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
