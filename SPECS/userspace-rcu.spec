Name:           userspace-rcu
Version:        0.10.1
Release:        4%{?dist}
Summary:        RCU (read-copy-update) implementation in user-space

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://liburcu.org
Source0:        http://lttng.org/files/urcu/%{name}-%{version}.tar.bz2
Patch0:         regtest-without-bench.patch
BuildRequires:  pkgconfig
BuildRequires:  perl-Test-Harness
BuildRequires:  autoconf automake libtool
BuildRequires:  multilib-rpm-config

%description
This data synchronization library provides read-side access which scales
linearly with the number of cores. It does so by allowing multiples copies
of a given data structure to live at the same time, and by monitoring
the data structure accesses to detect grace periods after which memory
reclamation is possible.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
# Reinitialize libtool with the fedora version to remove Rpath
autoreconf -vif

%configure --disable-static
V=1 make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT%{_libdir}/*.la
# Replace arch-dependent header file with arch-independent stub (when needed).
%multilib_fix_c_header --file %{_includedir}/urcu/config.h


%check
make check
make regtest

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc ChangeLog LICENSE README.md gpl-2.0.txt lgpl-relicensing.txt lgpl-2.1.txt
%{_libdir}/*.so.*

%files devel
%doc %{_pkgdocdir}/examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/liburcu*.pc
%{_docdir}/%{name}/cds-api.md
%{_docdir}/%{name}/rcu-api.md
%{_docdir}/%{name}/solaris-build.md
%{_docdir}/%{name}/uatomic-api.md


%changelog
* Wed Feb 10 2021 Benjamin Marzinski <bmarzins@redhat.com> - 0.10.1-4
- Fix CI test package requirements
- Resolves: bz #1682555

* Fri Oct 04 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.10.1-3
- Replace arch-dependent /usr/include/urcu/config.h with arch-independent
  stub when needed. (bz #1853168)
- Added CI gating tests (bz #1682555)
- Resolves: bz #1682555, #1853168

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Michael Jeanson <mjeanson@efficios.com> - 0.10.1-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Michael Jeanson <mjeanson@efficios.com> - 0.10.0-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.3-1
- New upstream release

* Wed Jun 22 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.2-2
- Re-add rpath removing

* Tue Jun 21 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.2-1
- New upstream release
- Dropped aarch64 patch merged upstream

* Sun May 15 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.6-4
- Fix %%doc usage (#1001239)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Scott Tsai <scottt.tw@gmail.com> - 0.8.6-1
- New upstream release

* Sun Nov 02 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 0.8.5-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-3
- Use upstream patch for aarch64 (includes ppc64le too)

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-2
- Added AArch64 support

* Mon Feb 10 2014 Yannick Brosseau <yannick.brosseau@gmail.com> 0.8.1-1
- New upstream release

* Sat Jan 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.9-1
- Update to 0.7.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.7-1
- New upstream version

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.6-1
- New upstream version

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.5-1
- New upstream version 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.3-1
- New upstream version (#828716)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 26 2010 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.4.1-1
- new upstream version.

* Tue Oct 20 2009 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.2.4-1
- Initial revision.
