# .SPEC-file to package RPMs for Fedora

Summary: Software library containing FFT functions written in OpenCL
Name: clFFT
Version: 2.12.2
Release: 1%{?dist}

License: ASL 2.0
URL: https://github.com/clMathLibraries/clFFT
Source: https://github.com/clMathLibraries/clFFT/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# man page copied from debian package
Source1: clFFT-client.1

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: boost-devel
BuildRequires: opencl-headers
BuildRequires: ocl-icd-devel

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description
The clFFT library is an open source OpenCL library implementation of
discrete Fast Fourier Transforms. The library:

- provides a fast and accurate platform for calculating discrete FFTs.
- works on CPU or GPU backends.
- supports in-place or out-of-place transforms.
- supports 1D, 2D, and 3D transforms with a batch size that can be
  greater than 1.
- supports planar (real and complex components in separate arrays) and
  interleaved (real and complex components as a pair contiguous in
  memory) formats.
- supports dimension lengths that can be any combination of powers of
  2, 3, 5, 7, 11 and 13.
- Supports single and double precision floating point formats.

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
cd src
%cmake \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DBoost_USE_STATIC_LIBS=OFF \
    -DBUILD_RUNTIME=ON \
    -DBUILD_CLIENT=ON \
    -DBUILD_TEST=OFF \
    -DBUILD_LOADLIBRARIES=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_CALLBACK_CLIENT=ON
%cmake_build

%install
cd src
%cmake_install

# remove version number from the client executable
mv -f %{buildroot}%{_bindir}/clFFT-client-%{version} %{buildroot}%{_bindir}/clFFT-client

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/clFFT-client.1

%ldconfig_scriptlets

%files
%license LICENSE NOTICE
%doc CHANGELOG README.md ReleaseNotes.txt
%doc docs/*
%{_libdir}/*.so.*
%{_bindir}/clFFT-client
%{_mandir}/man*/*.1*

%files devel
%doc docs/*
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/cmake/clFFT/*.cmake
