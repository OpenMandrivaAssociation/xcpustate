Summary:	An X Window System based CPU state monitor
Name:		xcpustate
Version:	2.5
Release:	%mkrel 23
License:	MIT-style
Group:		Monitoring
BuildRequires:	libx11-devel libelf-devel imake
BuildRequires:	libxt-devel libxaw-devel libxmu-devel
URL:		ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/

Source0:	ftp://ftp.cs.toronto.edu/pub/jdd/xcpustate/%{name}-%{version}.tar.bz2
Source11:	%{name}16.png
Source12:	%{name}32.png
Source13:	%{name}48.png
Patch0:		xcpustate-%{version}-nlist.patch
Patch1:		xcpustate-%{version}-alpha.patch
Patch2:		xcpustate-%{version}-6.0.patch
Patch3:		%{name}-libelf.patch

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
%patch0 -p1 -b .nlist
%patch2 -p1 -b .glibc
%patch3 -p1 -b .libelf
%ifarch alpha
%patch1 -p1 -b .alpha
%endif


%build
xmkmf
%make CDEBUGFLAGS="$RPM_OPT_FLAGS" MANPATH=%_mandir

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} install.man MANPATH=%_mandir

install -m 755 -d $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(xcpustate):\
        needs="X11"\
        section="Applications/Monitoring"\
        title="Xcpustate"\
        longtitle="Cpu load indicator"\
        command="/usr/bin/xcpustate"\
        icon="xcpustate.png"\
        xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Xcpustate
Comment=Cpu load indicator
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Monitoring
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README
%attr(0755,root,root) %_bindir/xcpustate
%attr(0644,root,root) %_mandir/man1/xcpustate.1x*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

