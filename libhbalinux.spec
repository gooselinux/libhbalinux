Name:           libhbalinux
Version:        1.0.10
Release:        1%{?dist}
Summary:        FC-HBAAPI implementation using scsi_transport_fc interfaces

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://www.open-fcoe.org
# This source was cloned from upstream git
# To get the tar package, just run:
# git clone git://open-fcoe.org/openfc/libhbalinux.git && cd libhbalinux
# git archive --prefix=libhbalinux-%{version}/ v%{version} > ../libhbalinux-%{version}.tar
# cd .. && gzip libhbalinux-%{version}.tar
Source0:        %{name}-%{version}.tar.gz
Patch0:         libhbalinux-1.0.9-conf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libhbaapi-devel libpciaccess-devel libtool automake
Requires:       libhbaapi

%description
SNIA HBAAPI vendor library built on top of the scsi_transport_fc interfaces

%prep
%setup -q
%patch0 -p1 -b .conf


%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.so' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
ORG=org.open-fcoe.libhbalinux
LIB=%{_libdir}/libhbalinux.so.2.0.2
STR="$ORG	$LIB"
CONF=%{_sysconfdir}/hba.conf
if test -f $CONF; then
  grep -E -q ^[[:space:]]*$ORG[[:space:]]+$LIB $CONF
  if test $? -ne 0; then
    echo $STR >> $CONF;
  fi
fi


%postun
/sbin/ldconfig
ORG=org.open-fcoe.libhbalinux
CONF=%{_sysconfdir}/hba.conf
if test -f $CONF; then
  grep -v $ORG $CONF > %{_sysconfdir}/hba.conf.new
  mv %{_sysconfdir}/hba.conf.new %{_sysconfdir}/hba.conf
fi


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/*.so.*


%changelog
* Mon May 24 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.10-1
- rebased to 1.0.10, bugfix release (see git changelog for more info)

* Wed Jan 13 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-2
- new tarball matching official 1.0.9 release (pulled from git)

* Fri Dec 04 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-20091204git
- rebased to the latest version in upstream git

* Thu Jul 30 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.8-1
- rebase of libhbalinux, spec file adjusted to match changes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 01 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-3
- replaced unofficial 1.0.7 source tarball with official one
- update of Makefile, part of it moved to postinstall section
  of spec file

* Tue Mar 31 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-2
- minor changes in spec file

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 1.0.7-1
- initial build

