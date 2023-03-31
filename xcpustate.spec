%define debug_package %{nil}

Summary:	An X Window System based CPU state monitor
Name:		xcpustate
Version:	2.9
Release:	20
License:	MIT-style
Group:		Monitoring
URL:		ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/
Source0:	ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/%{name}-%{version}.tar.lzma
Source11:	%{name}16.png
Source12:	%{name}32.png
Source13:	%{name}48.png
BuildRequires:	imake
BuildRequires:	elfutils-devel
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	tirpc-devel
Patch1:		xcpustate-2.5-alpha.patch
Patch2:		xcpustate-2.5-6.0.patch
Patch3:		xcpustate-2.9-missingheaders.patch

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
%make CDEBUGFLAGS="%{optflags}" MANPATH=%{_mandir} SYS_LIBRARIES="-ltirpc"

%install
%{makeinstall_std} install.man MANPATH=%{_mandir}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%files
%defattr(-,root,root,0755)
%doc README
%attr(0755,root,root) %_bindir/xcpustate
%attr(0644,root,root) %_mandir/man1/xcpustate.1*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png

