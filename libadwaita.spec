#
# Conditional_build:
%bcond_without	apidocs	# gtk-doc API documentation

Summary:	Adwaita mobile widgets library
Summary(pl.UTF-8):	Biblioteka widżetów mobilnych Adwaita
Name:		libadwaita
# meson.build /version:
# (now it's 1.0.0-alpha.2, but keep 1.1.0 to avoid epoch bumps)
Version:	1.1.0
# not released yet
%define	gitref	810ff7937a299e4822074bfa1381bec910535823
%define	snap	20210927
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.gnome.org/GNOME/libadwaita/-/tags
Source0:	https://gitlab.gnome.org/GNOME/libadwaita/-/archive/%{gitref}/%{name}-%{gitref}.tar.bz2
# Source0-md5:	4eb4e19ae41154851c4204b93baab478
URL:		https://gitlab.gnome.org/GNOME/libadwaita
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sassc
# vala with gtk4 bindings
BuildRequires:	vala >= 2:0.44
Requires:	glib2 >= 1:2.44
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of the Adwaita library is to help with developing UI for
mobile devices using GTK/GNOME.

%description -l pl.UTF-8
Celem biblioteki Adwaita jest pomoc przy tworzeniu interfejsów
użytkownika dla urządzeń przenośnych przy użyciu GTK/GNOME.

%package devel
Summary:	Header files for Adwaita library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Adwaita
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk4-devel >= 4.0

%description devel
Header files for Adwaita library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Adwaita.

%package -n vala-libadwaita
Summary:	Vala API for Adwaita library
Summary(pl.UTF-8):	API języka Vala do biblioteki Adwaita
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.44

%description -n vala-libadwaita
Vala API for Adwaita library.

%description -n vala-libadwaita -l pl.UTF-8
API języka Vala do biblioteki Adwaita.

%package apidocs
Summary:	API documentation for Adwaita library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Adwaita
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Adwaita library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Adwaita.

%prep
%setup -q -n %{name}-%{gitref}

%build
%meson build \
	-Dexamples=false \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libadwaita-1 $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libadwaita-1.so.0
%{_libdir}/girepository-1.0/Adw-1.typelib
# should belong to gtk4?
%dir %{_libdir}/gtk-4.0/inspector
%attr(755,root,root) %{_libdir}/gtk-4.0/inspector/libadwaita-inspector-module1.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libadwaita-1.so
%{_includedir}/libadwaita-1
%{_datadir}/gir-1.0/Adw-1.gir
%{_pkgconfigdir}/libadwaita-1.pc

%files -n vala-libadwaita
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libadwaita-1.deps
%{_datadir}/vala/vapi/libadwaita-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libadwaita-1
%endif
