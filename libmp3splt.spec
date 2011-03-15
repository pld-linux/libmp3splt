#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	ltdl		# don't build ltdl
#
Summary:	Libraries for the mp3splt project
Summary(pl.UTF-8):	Biblioteki do projektu mp3splt
######		/home/users/duddits/rpm/rpm.groups: no such file
Name:		libmp3splt
Version:	0.6.1a
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/mp3splt/%{name}-%{version}.tar.gz
# Source0-md5:	a6a00d83e49adf27abb7a0cb0ea384a4
URL:		http://mp3splt.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libmad-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
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

%prep
%setup -q
# Avoid standard rpaths on lib64 archs:
sed -i -e 's|"/lib /usr/lib\b|"/%{_lib} %{_libdir}|' configure

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with ltdl}
	--with-ltdl-lib=%{_libdir} \
	--with-ltdl-include=%{_includedir} \
%endif
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libmp3splt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp3splt.so.0
%attr(755,root,root) %{_libdir}/%{name}/libsplt_mp3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libsplt_mp3.so.0
%attr(755,root,root) %{_libdir}/%{name}/libsplt_ogg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libsplt_ogg.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmp3splt.so
%{_libdir}/libmp3splt.la
%{_libdir}/%{name}/libsplt_mp3.so
%{_libdir}/%{name}/libsplt_mp3.la
%{_libdir}/%{name}/libsplt_ogg.so
%{_libdir}/%{name}/libsplt_ogg.la
%{_includedir}/libmp3splt
%{_aclocaldir}/mp3splt.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmp3splt.a
%{_libdir}/%{name}/libsplt_mp3.a
%{_libdir}/%{name}/libsplt_ogg.a
%endif
