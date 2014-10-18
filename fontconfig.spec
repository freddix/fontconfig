Summary:	Font configuration and customization tools
Name:		fontconfig
Version:	2.11.1
Release:	3
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{name}-%{version}.tar.gz
# Source0-md5:	e75e303b4f7756c2b16203a57ac87eba
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
# not really needed, makes bootstrap easier
#BuildRequires:	docbook-utils
#BuildRequires:	docbook-dtd41-sgml
#BuildRequires:	ed
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.
This package contains tools and documentation.

%package libs
Summary:	Font configuration and customization library
Group:		Development/Libraries

%description libs
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

%package devel
Summary:	Font configuration and customization library - development files
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files needed to develop programs that
use these fontconfig.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-docs		\
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{1,3,5},/var/cache/fontconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# enable lcdfilter and rgb by default
ln -s %{_datadir}/%{name}/conf.avail/10-lcd-filter.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/10-lcd-filter.conf
ln -s %{_datadir}/%{name}/conf.avail/10-sub-pixel-rgb.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/10-sub-pixel-rgb.conf

cp -f conf.d/README README.confd

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
HOME=/tmp %{_bindir}/fc-cache -r -s 2>/dev/null || :

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.confd
%attr(755,root,root) %{_bindir}/fc-*

%dir %{_sysconfdir}/fonts
%dir %{_sysconfdir}/fonts/conf.d

%config(noreplace) %verify(not link md5 mtime size) %{_sysconfdir}/fonts/conf.d/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/fonts.conf
%{_sysconfdir}/fonts/conf.d/README

%dir %{_datadir}/xml/%{name}
%{_datadir}/xml/%{name}/fonts.dtd

%dir %{_datadir}/fontconfig
%dir %{_datadir}/fontconfig/conf.avail
%{_datadir}/fontconfig/conf.avail/*.conf
/var/cache/fontconfig

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libfontconfig.so.?
%attr(755,root,root) %{_libdir}/libfontconfig.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/fontconfig-devel/*.html
%attr(755,root,root) %{_libdir}/libfontconfig.so
%{_includedir}/fontconfig
%{_pkgconfigdir}/fontconfig.pc

