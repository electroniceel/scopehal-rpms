# adapt commit id and commitdate to match the git version you want to build
%global commit fe86885ecafd0d16eb122f3212403d1d5a86e24e
%global commitdate 20170617

Summary: The Fastest Fourier Transform in the South
Name: ffts
Version: 0.9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Release: %{commitdate}.%{shortcommit}%{?dist}
License: BSD
URL: https://github.com/anthonix/ffts
Source: https://github.com/anthonix/ffts/archive/%{commit}/ffts-%{shortcommit}.tar.gz

# patch taken from https://github.com/anthonix/ffts/pull/76
Patch1: https://github.com/anthonix/ffts/commit/fcf4c5a809f49bf6c26b3654c6602de5c9e37760.patch

BuildRequires: cmake
BuildRequires: gcc

%package   devel
Summary:   The Fastest Fourier Transform in the South
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
The Fastest Fourier Transform in the South

%description devel
The Fastest Fourier Transform in the South

%prep
%setup -n ffts-%{commit}
%patch1 -p1

%build
%cmake -DGENERATE_POSITION_INDEPENDENT_CODE=ON -DENABLE_SHARED=ON
%cmake_build

%install
%cmake_install

# fix pkgconfig dir
mkdir -p  %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/usr/share/pkgconfig/ffts.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%license COPYRIGHT
%doc README.md
%{_libdir}/libffts.so.*

%files devel
%{_includedir}/ffts.h
%{_libdir}/libffts.a
%{_libdir}/libffts.so
%{_libdir}/pkgconfig/*.pc


