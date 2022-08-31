Summary:	Static multicast routing for UNIX
Name:		smcroute
Version:	2.5.5
Release:	0.1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	https://github.com/troglobit/smcroute/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6ed58b4887ccb737687b584f5794c7ed
URL:		https://troglobit.com/projects/smcroute/
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SMCRoute is a daemon and command line tool to manipulate the multicast
routing table in the UNIX kernel.

SMCRoute can be used as an alternative to dynamic multicast routing
daemons like mrouted or pimd when (only) static multicast routes
should be maintained or no proper signalling exists.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/smcroute.d,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p smcroute.default $RPM_BUILD_ROOT/etc/sysconfig/smcroute

sed -i \
	-e 's@%{_docdir}/smcroute@%{_docdir}/%{name}-%{version}@' \
	-e 's@%{_sysconfdir}/default@/etc/sysconfig@' \
        $RPM_BUILD_ROOT%{systemdunitdir}/smcroute.service

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/smcroute

sed -e 's/^\([[:space:]]*[^#]\)/# \1/' smcroute.conf > $RPM_BUILD_ROOT%{_sysconfdir}/smcroute.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post smcroute.service

%preun
%systemd_preun smcroute.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smcroute.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/smcroute
%dir %{_sysconfdir}/smcroute.d
%attr(755,root,root) %{_sbindir}/smcroute
%attr(755,root,root) %{_sbindir}/smcroutectl
%attr(755,root,root) %{_sbindir}/smcrouted
%{systemdunitdir}/smcroute.service
%{_mandir}/man5/smcroute.conf.5*
%{_mandir}/man8/smcroutectl.8*
%{_mandir}/man8/smcrouted.8*
