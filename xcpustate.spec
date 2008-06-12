Summary:	An X Window System based CPU state monitor
Name:		xcpustate
Version:	2.9
Release:	%mkrel 2
License:	MIT-style
Group:		Monitoring
BuildRequires:	libx11-devel
BuildRequires:	libelf-devel
BuildRequires:	imake
BuildRequires:	libxt-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxmu-devel
URL:		ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/
Source0:	ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/%{name}-%{version}.tar.lzma
Source11:	%{name}16.png
Source12:	%{name}32.png
Source13:	%{name}48.png
Patch1:		xcpustate-2.5-alpha.patch
Patch2:		xcpustate-2.5-6.0.patch
Patch3:		xcpustate-2.9-missingheaders.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The xcpustate utility is an X Window System based monitor which shows
the amount of time that the CPU is spending in different states.  On a
Linux system, xcpustate displays a bar that indicates the amounts of idle,
user, nice and system time (from left to right) used by the CPU.

Install the xcpustate package if you'd like to use a horizontal bar style
CPU state monitor.

%prep
%setup -q
%patch2 -p1 -b .glibc
%patch3 -p1 -b .headers
%ifarch alpha
%patch1 -p1 -b .alpha
%endif


%build
xmkmf
%make CDEBUGFLAGS="$RPM_OPT_FLAGS" MANPATH=%_mandir

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} install.man MANPATH=%_mandir

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XCpuState
Comment=CPU load indicator
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=System;Monitor;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README
%attr(0755,root,root) %_bindir/xcpustate
%attr(0644,root,root) %_mandir/man1/xcpustate.1*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png

