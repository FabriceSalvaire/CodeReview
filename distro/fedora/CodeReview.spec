%global pypi_name CodeReview

Name:           %{pypi_name}
Version:        0.3.6
Release:        1%{?dist}
Summary:        Application to perform code review on local Git repositories
License:        GPLv3
URL:            https://github.com/FabriceSalvaire/CodeReview
Source0:        https://files.pythonhosted.org/packages/source/C/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
#               https://github.com/FabriceSalvaire/% {pypi_name}/archive/% {version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

Requires:       python3-PyYAML
Requires:       python3-PyQt5
Requires:       python3-pygit2
Requires:       python3-pygments

%description
CodeReview provides two applications, 'diff-viewer', a standalone diff
viewer and 'pyqgit' a code reviewer for local Git repositories.

The main features of CodeReview are:

- display and browse the log and paches of a Git repository
- diff side by side using Patience algorithm
- watch for file system changes

Diff viewer features:

- stage/unstage file
- number of context lines
- font size
- line number mode
- align mode
- complete mode
- highlight mode

CodeReview is coded in Python 3 and use the Qt5 framework.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files
%{_bindir}/diff-viewer
%{_bindir}/pyqgit
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{_datadir}/%{pypi_name}/

%changelog
* Fri Dec 01 2017 Fabrice Salvaire - 0.3.6-1
- Initial package.
