# adapt commit id and commitdate to match the git version you want to build
%global commit ceb14ffbcde5158e55acb34c4561b982a6a23fbb
%global commitdate 20210602

# then download and build like this
# (you need an rpmbuild dir, can be created with rpmdev-setuptree)
#
# GIT_COMMIT= ## insert commit id defined above here ##
# cp scopehal-apps.spec $HOME/rpmbuild/SPECS
# git clone --recurse-submodules https://github.com/azonenberg/scopehal-apps.git scopehal-apps-${GIT_COMMIT:0:7}
# tar cvzf $HOME/rpmbuild/SOURCES/scopehal-apps-${GIT_COMMIT:0:7}.tar.gz scopehal-apps-${GIT_COMMIT:0:7}
# cd $HOME/rpmbuild
# rpmbuild -ba SPECS/scopehal-apps.spec

Summary: glscopeclient and other client applications for libscopehal
Name: scopehal-apps

# No official release yet, just a git repo
# The first official release is planned to be called 0.1. Stay below that so that upgrading will work
Version: 0.0.99
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Release: %{commitdate}.%{shortcommit}%{?dist}

License: BSD
URL: https://github.com/azonenberg/scopehal-apps
Source: scopehal-apps-%{shortcommit}.tar.gz

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: ffts-devel
BuildRequires: gtkmm30-devel
BuildRequires: glew-devel
BuildRequires: libglvnd-devel
BuildRequires: libsigc++20-devel
BuildRequires: yaml-cpp-devel
BuildRequires: opencl-headers
BuildRequires: catch-devel
BuildRequires: ocl-icd-devel
BuildRequires: clFFT-devel

%if 0%{?fedora}
# necessary for building the documentation
BuildRequires: texlive
BuildRequires: texlive-makecell
BuildRequires: texlive-inconsolata
BuildRequires: texlive-newtx
BuildRequires: texlive-ec
BuildRequires: texlive-geometry
BuildRequires: texlive-placeins
BuildRequires: texlive-paralist
BuildRequires: texlive-colortbl
BuildRequires: texlive-koma-script
BuildRequires: texlive-float
BuildRequires: texlive-upquote
%endif

%package   -n glscopeclient
Summary:   User interface and signal analysis tool for oscilloscopes and logic analyzers
Requires:  scopehal-libs = %{version}-%{release}

%package   -n scopehal-libs
Summary:   Libraries required by scopehal-apps

%description
glscopeclient and other client applications for libscopehal

%description -n glscopeclient
User interface and signal analysis tool for oscilloscopes and logic analyzers

%description -n scopehal-libs
Libraries required by scopehal-apps

%prep
%setup -n scopehal-apps-%{shortcommit}

%build
%if 0%{?fedora}
%define docbuild -DBUILD_DOCS=ON
%else
# EL/EPEL doesn't have some texlive packages required to build the documentation
# so disable building the documentation there
%define docbuild -DBUILD_DOCS=OFF
%endif

%cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON %{docbuild}
%cmake_build

%install
%cmake_install

# if to include the documentation depends on a conditional
# this requires a workaround with a list file, the list file always must contain at least one file
%define DOC_FILES %{_sourcedir}/doc_files.list
echo "%doc README.md" >%{DOC_FILES}

%if 0%{?fedora}
# fix up doc path to Fedora default
mkdir -p %{buildroot}%{_docdir}
mv %{buildroot}/usr/doc/glscopeclient %{buildroot}%{_docdir}/glscopeclient

# include the pdf in the package
echo "%{_docdir}/glscopeclient/glscopeclient-manual.pdf" >>%{DOC_FILES}
%endif

# scopehal-apps is just a common source package, no output so no files section
#%files

%files -n glscopeclient -f %{DOC_FILES}
%license LICENSE
%{_bindir}/glscopeclient
%{_datadir}/glscopeclient/*
%{_datadir}/applications/glscopeclient.desktop  

%files -n scopehal-libs
%license LICENSE
%{_libdir}/lib*.so
