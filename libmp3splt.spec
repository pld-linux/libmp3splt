#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Libraries for the mp3splt project
Summary(pl.UTF-8):	Biblioteki do projektu mp3splt
Name:		libmp3splt
Version:	0.9.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/mp3splt/%{name}-%{version}.tar.gz
# Source0-md5:	b9b9677ababf823e0739e5caff68aa86
Patch0:		ltdl.patch
Patch1:		%{name}-format_security.patch
URL:		http://mp3splt.sourceforge.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
BuildRequires:	flac-devel >= 1.2.1
BuildRequires:	gettext-devel >= 0.18.3
BuildRequires:	libid3tag-devel
BuildRequires:	libltdl-devel
BuildRequires:	libmad-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	pcre-devel >= 1.0
BuildRequires:	pkgconfig
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The mp3Splt project provides utilities to split mp3 and ogg files, by
selecting a begin and an end time position, without decoding. It is
very useful to split large mp3/ogg into smaller files, or to split
entire albums to obtain original tracks. To split an album, the split
points and filenames can be selected manually or automatically from
CDDB (internet or a local file), or from .cue files.

It supports automatic silence detection, which can be used to adjust
cddb/cue split points. It is also possible to extract tracks from
Mp3Wrap or AlbumWrap files in a few seconds.

%description -l pl.UTF-8
Projekt mp3Splt dostarcza narzędzi umożliwiających dzielenie plików w
formacie mp3 i ogg poprzez zaznaczenie pozycji początku i końca
dzielenia, bez potrzeby dekodowania. Dzielenie dużych plików mp3/ogg
na mniejsze części jest bardzo użyteczne, można w ten sposób dzielić
całe albumy by otrzymać oryginalne ścieżki. Żeby podzielić album
punkty podziału i nazwy plików mogą zostać wybrane ręcznie lub
automatycznie z wykorzystaniem CDDB (z Internetu lub lokalnie), albo z
plików .cue.

Projekt wspiera automatyczne wykrywanie ciszy, które może zostać
wykorzystane do ustawienia punktów podziału cddb/cue. Jest również
możliwe wyciągnięcie ścieżek z plików Mp3Wrap lub AlbumWrap w ciągu
kilku sekund.

%package devel
Summary:	Header files for libmp3splt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmp3splt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libmp3splt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmp3splt.

%package static
Summary:	Static libmp3splt library
Summary(pl.UTF-8):	Statyczna biblioteka libmp3splt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmp3splt library.

%description static -l pl.UTF-8
Statyczna biblioteka libmp3splt.

%package apidocs
Summary:	libmp3splt API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmp3splt
Group:		Documentation

%description apidocs
API and internal documentation for libmp3splt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmp3splt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
sed -i -e 's/fr_FR/fr/;s/de_DE/de/;' po/LINGUAS
mv po/de_DE.po po/de.po
mv po/fr_FR.po po/fr.po

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-flac \
	--enable-id3tag \
	--enable-mp3 \
	--enable-ogg \
	--enable-pcre \
	--with-ltdl-lib=%{_libdir} \
	--with-ltdl-include=%{_includedir} \
	%{!?with_static_libs:--disable-static}

%{__make}
%if %{with apidocs}
%{__make} -C doc doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmp3splt0/*.{a,la}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%find_lang libmp3splt0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libmp3splt0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libmp3splt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp3splt.so.0
%dir %{_libdir}/libmp3splt0
%attr(755,root,root) %{_libdir}/libmp3splt0/libsplt_flac.so
%attr(755,root,root) %{_libdir}/libmp3splt0/libsplt_mp3.so
%attr(755,root,root) %{_libdir}/libmp3splt0/libsplt_ogg.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmp3splt.so
%{_libdir}/libmp3splt.la
%{_includedir}/libmp3splt
%{_pkgconfigdir}/libmp3splt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmp3splt.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/doxygen/*
%endif
