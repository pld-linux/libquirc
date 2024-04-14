#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	sdl		# SDL-based tools
#
Summary:	Library for extracting and decoding QR codes
Summary(pl.UTF-8):	Biblioteka do wydobywania i dekodowania kodów QR
Name:		libquirc
Version:	1.0.2
Release:	1
License:	ISC
Group:		Libraries
#Source0Download: https://github.com/evolation/libquirc/tags
Source0:	https://github.com/evolation/libquirc/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df67eaa474850cb7a0f7acd404a38417
Patch0:		%{name}-make.patch
URL:		https://github.com/evolation/libquirc
%if %{with sdl}
BuildRequires:	SDL-devel
BuildRequires:	SDL_gfx-devel
BuildRequires:	libjpeg-devel
BuildRequires:	pkgconfig
%endif
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QR codes are a type of high-density matrix barcodes, and quirc is a
library for extracting and decoding them from images.

%description -l pl.UTF-8
Kody QR to rodzaj macierzowych kodów paskowych wysokiej
rozdzielczości, a quirc to biblioteka do wydobywania ich z obrazów i
dekodowania.

%package devel
Summary:	Header files for quirc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki quirc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for quirc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki quirc.

%package static
Summary:	Static quirc library
Summary(pl.UTF-8):	Statyczna biblioteka quirc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static quirc library.

%description static -l pl.UTF-8
Statyczna biblioteka quirc.

%package tools
Summary:	Tools for QR codes using quirc library
Summary(pl.UTF-8):	Narzędzia do kodów QR wykorzystujące bibliotekę quirc
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description tools
Tools for QR codes using quirc library.

%description tools -l pl.UTF-8
Narzędzia do kodów QR wykorzystujące bibliotekę quirc.

%prep
%setup -q
%patch0 -p1

%build
%{__make} libquirc.so %{?with_static_libs:libquirc.a} %{?with_sdl:quirc-demo quirc-scanner} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -fPIC -Wall" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install libquirc.so.1.0 $RPM_BUILD_ROOT%{_libdir}
ln -sf libquirc.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libquirc.so
cp -p lib/quirc.h $RPM_BUILD_ROOT%{_includedir}
%if %{with static_libs}
cp -p libquirc.a $RPM_BUILD_ROOT%{_libdir}
%endif
%if %{with sdl}
install quirc-demo quirc-scanner $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libquirc.so.1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquirc.so
%{_includedir}/quirc.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libquirc.a
%endif

%if %{with sdl}
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/quirc-demo
%attr(755,root,root) %{_bindir}/quirc-scanner
%endif
