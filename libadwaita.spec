#
# Conditional_build:
%bcond_without	apidocs	# gtk-doc API documentation

Summary:	Adwaita mobile widgets library
Summary(pl.UTF-8):	Biblioteka widżetów mobilnych Adwaita
Name:		libadwaita
# meson.build /version:
Version:	1.1.0
# not released yet
%define	gitref	f7e47528c90a44066922ff998e4499af8c85554f
%define	snap	20210507
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.gnome.org/GNOME/libadwaita/-/tags
Source0:	https://gitlab.gnome.org/GNOME/libadwaita/-/archive/%{gitref}/%{name}-%{gitref}.tar.bz2
# Source0-md5:	ce86720130cad4e74ff3111cd62ae22b
URL:		https://gitlab.gnome.org/GNOME/libadwaita
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
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
