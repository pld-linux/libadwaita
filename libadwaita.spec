#
# Conditional_build:
%bcond_without	apidocs		# gi-doc API documentation
%bcond_without	static_libs	# static libraries

Summary:	Adwaita mobile widgets library
Summary(pl.UTF-8):	Biblioteka widżetów mobilnych Adwaita
Name:		libadwaita
Version:	1.6.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libadwaita/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	8c8fe1e64c361eb5a84d60f61147fbf9
URL:		https://gnome.pages.gitlab.gnome.org/libadwaita/
BuildRequires:	AppStream-devel
BuildRequires:	fribidi-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	gtk4-devel >= 4.15.2
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	sassc
BuildRequires:	tar >= 1:1.22
# vala with gtk4 bindings
BuildRequires:	vala >= 2:0.44
BuildRequires:	xz
Requires:	glib2 >= 1:2.76.0
Requires:	gtk4 >= 4.15.2
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
Requires:	fribidi-devel
Requires:	glib2-devel >= 1:2.76.0
Requires:	gtk4-devel >= 4.15.2

%description devel
Header files for Adwaita library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Adwaita.

%package static
Summary:	Static Adwaita library
Summary(pl.UTF-8):	Statyczna biblioteka Adwaita
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Adwaita library.

%description static -l pl.UTF-8
Statyczna biblioteka Adwaita.

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
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dexamples=false \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libadwaita-1 $RPM_BUILD_ROOT%{_gidocdir}
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
%attr(755,root,root) %{_libdir}/libadwaita-1-internal.so.0
%{_libdir}/girepository-1.0/Adw-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libadwaita-1.so
%attr(755,root,root) %{_libdir}/libadwaita-1-internal.so
%{_includedir}/libadwaita-1
%{_datadir}/gir-1.0/Adw-1.gir
%{_pkgconfigdir}/libadwaita-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libadwaita-1.a
%{_libdir}/libadwaita-1-internal.a
%endif

%files -n vala-libadwaita
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libadwaita-1.deps
%{_datadir}/vala/vapi/libadwaita-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libadwaita-1
%endif
