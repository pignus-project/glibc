%define linux24 0
%define glibcrelease 2
Summary: The GNU libc libraries.
Name: glibc
Version: 2.1.95
%if %{linux24}
Release: %{glibcrelease}.2.4
%else
Release: %{glibcrelease}
%endif
Copyright: LGPL
Group: System Environment/Libraries
Source: %{name}-%{version}.tar.gz
# In the source tarball the file diff-CYGNUS-to-REDHAT.patch contains all
# diffs applied by Red Hat to the current CVS version of glibc
Buildroot: /var/tmp/glibc-%{PACKAGE_VERSION}-root
Obsoletes: zoneinfo, libc-static, libc-devel, libc-profile, libc-headers,
Obsoletes:  linuxthreads, gencat, locale, ldconfig, locale-ja
Provides: ldconfig
Autoreq: false
%ifarch alpha
Provides: ld.so.2
%else
%endif
%ifarch sparc
Obsoletes: libc
%endif
Prereq: basesystem
Conflicts: rpm <= 4.0-0.65
Patch: glibc-kernel-2.4.patch
%if %{linux24}
ExcludeArch: ia64
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%else
%ifarch ia64
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%else
%ifarch sparc64
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%else
%define enablekernel 2.2.5
%endif
%endif
%endif

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support and timezone databases.

%package devel
Summary: Header and object files for development using standard C libraries.
Group: Development/Libraries
Conflicts: texinfo < 3.11
Prereq: /sbin/install-info
Obsoletes: libc-debug, libc-headers, libc-devel, linuxthreads-devel
Obsoletes: glibc-debug
Prereq: kernel-headers
Requires: kernel-headers >= 2.2.1
Autoreq: true

%description devel
The glibc-devel package contains the header and object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header and object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package profile
Summary: The GNU libc libraries, including support for gprof profiling.
Group: Development/Libraries
Obsoletes: libc-profile
Autoreq: true

%description profile
The glibc-profile package includes the GNU libc libraries and support
for profiling using the gprof program.  Profiling is analyzing a
program's functions to see how much CPU time they use and determining
which functions are calling other functions during execution.  To use
gprof to profile a program, your program needs to use the GNU libc
libraries included in glibc-profile (instead of the standard GNU libc
libraries included in the glibc package).

If you are going to use the gprof program to profile a program, you'll
need to install the glibc-profile program.

%package -n nscd
Summary: A Name Service Caching Daemon (nscd).
Group: System Environment/Daemons
Conflicts: kernel < 2.2.0
Prereq: /sbin/chkconfig, /usr/sbin/useradd, /usr/sbin/userdel
Autoreq: true

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well. Note that you
can't use nscd with 2.0 kernels because of bugs in the kernel-side
thread support. Unfortunately, nscd happens to hit these bugs
particularly hard.

Install nscd if you need a name service lookup caching daemon, and
you're not using a version 2.0 kernel.

%prep
%setup -q
%if %{linux24}
# If we are building enablekernel 2.4.0 glibc on older kernel,
# we have to make sure no binaries compiled against that glibc
# are ever run
case `uname -r` in
[01].*|2.[0-3]*)
%patch -p1
;; esac
%endif
 
%ifarch armv4l sparc64 ia64
rm -rf glibc-compat
%endif

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

%build
rm -rf build-%{_target_cpu}-linux
mkdir build-%{_target_cpu}-linux ; cd build-%{_target_cpu}-linux
%ifarch %{ix86}
BuildFlags="-march=%{_target_cpu} -D__USE_STRING_INLINES -fstrict-aliasing"
%endif
%ifarch alphaev6
BuildFlags="-mcpu=ev6"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g7"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g7"
%endif
# Temporarily don't do this on ia64
%ifnarch ia64
BuildFlags="$BuildFlags -freorder-blocks -DNDEBUG=1"
%endif
EnableKernel="--enable-kernel=%{enablekernel}"
%if %{linux24}
EnableKernel="$EnableKernel --disable-profile"
%else
%ifarch i586 i686 athlon sparcv9 alphaev6 ia64
EnableKernel="$EnableKernel --disable-profile"
%endif
%endif
CC=gcc CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
	--enable-add-ons=yes --without-cvs $EnableKernel \
	%{_target_cpu}-redhat-linux
if [ -x /usr/bin/getconf ] ; then
  numprocs=$(/usr/bin/getconf _NPROCESSORS_ONLN)
  if [ $numprocs -eq 0 ]; then
    numprocs=1
  fi
else
  numprocs=1
fi
make -j$numprocs -r CFLAGS="$BuildFlags -g -O3" PARALLELMFLAGS=-s
gcc -static -Os ../redhat/glibc_post_upgrade.c -o glibc_post_upgrade

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install_root=$RPM_BUILD_ROOT install -C build-%{_target_cpu}-linux
cd build-%{_target_cpu}-linux && \
    make install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
    cd ..

# compatibility hack: this locale has vanished from glibc, but some other
# programs are still using it. Normally we would handle it in the %pre
# section but with glibc that is simply not an option
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/locale/ru_RU/LC_MESSAGES

# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*
%ifarch sparc64 ia64
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*
%endif

# the man pages for the linuxthreads require special attention
make -C linuxthreads/man
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -m 0644 linuxthreads/man/*.3thr $RPM_BUILD_ROOT%{_mandir}/man3
gzip -9nvf $RPM_BUILD_ROOT%{_mandir}/man3/*

if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
    mkdir -p $RPM_BUILD_ROOT%{_infodir}
    mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
    rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libbsd.a

install -m 644 redhat/nsswitch.conf $RPM_BUILD_ROOT/etc/nsswitch.conf

# Take care of setuids
# -- new security review sez that this shouldn't be needed anymore
#chmod 755 $RPM_BUILD_ROOT%{_prefix}/libexec/pt_chown

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 nscd/nscd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd

# Don't include ld.so.cache
rm -f $RPM_BUILD_ROOT/etc/ld.so.cache

# Include ld.so.conf
> $RPM_BUILD_ROOT/etc/ld.so.conf
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf

# Install the upgrade program
install -m 700 build-%{_target_cpu}-linux/glibc_post_upgrade $RPM_BUILD_ROOT/usr/sbin/glibc_post_upgrade

# Strip binaries
strip -R .comment $RPM_BUILD_ROOT/sbin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/bin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/sbin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/libexec/pt_chown || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/* || :

# BUILD THE FILE LIST
find $RPM_BUILD_ROOT -type f -or -type l |
	sed -e 's|.*/etc|%config &|' -e 's|.*/gconv/gconv-modules|%config &|' > rpm.filelist.in
for n in %{_prefix}/share %{_prefix}/include %{_prefix}/lib/locale; do 
    find ${RPM_BUILD_ROOT}${n} -type d | \
	grep -v '^%{_prefix}/share$' | \
	sed "s/^/%dir /" >> rpm.filelist.in
done

# primary filelist
sed "s|$RPM_BUILD_ROOT||" < rpm.filelist.in | 
	grep -v '/etc/localtime'  | \
	grep -v '/etc/nsswitch.conf'  | \
	grep -v '/etc/ld.so.conf'  | \
	sort > rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*_p\.a' < rpm.filelist > profile.filelist || :
egrep "(%{_prefix}/include)|(%{_infodir})" < rpm.filelist | 
	grep -v %{_infodir}/dir > devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/%{_lib}/lib.*_p.a' rpm.filelist.full | 
	egrep -v "(%{_prefix}/include)|(%{_infodir})" > rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.so' < rpm.filelist >> devel.filelist
grep '%{_mandir}' < rpm.filelist >> devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist.full |
	grep -v '%{_prefix}/%{_lib}/.*\.o' |
	grep -v '%{_prefix}/%{_lib}/lib.*\.so'|
	grep -v '%{_mandir}' | 
	grep -v 'nscd' > rpm.filelist

# /etc/localtime - we're proud of our timezone
rm -f $RPM_BUILD_ROOT/etc/localtime
cp -f $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime
#ln -sf ..%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime

# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp ChangeLog* documentation
gzip -9 documentation/ChangeLog*

%post -p /usr/sbin/glibc_post_upgrade

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir

%pre devel
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
    rm -f %{_prefix}/include/scsi
fi

%preun devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir
fi

%pre -n nscd
/usr/sbin/useradd -M -o -r -d / -s /bin/false \
	-c "NSCD Daemon" -u 28 nscd > /dev/null 2>&1 || :

%post -n nscd
/sbin/chkconfig --add nscd

%preun -n nscd
if [ $1 = 0 ] ; then
    service nscd stop > /dev/null 2>&1
    /sbin/chkconfig --del nscd
fi

%postun -n nscd
if [ $1 = 0 ] ; then
    /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
if [ "$1" -ge "1" ]; then
    service nscd condrestart > /dev/null 2>&1 || :
fi

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB
%doc documentation/* README.template README.libm
%doc hesiod/README.hesiod

%if !%{linux24}
%ifnarch sparcv9 i586 i686 athlon alphaev6
%files -f devel.filelist devel
%defattr(-,root,root)

%ifnarch ia64
%files -f profile.filelist profile
%defattr(-,root,root)
%endif

%files -n nscd
%defattr(-,root,root)
%config /etc/nscd.conf
/etc/rc.d/init.d/nscd
%{_prefix}/sbin/nscd
%endif
%endif

%changelog
* Thu Oct 19 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha semctl (#19199)
- update to CVS, including:
  - fix glibc headers for Compaq non-gcc compilers
  - fix locale alias handling code (#18832)
  - fix rexec on little endian machines (#18886)
- started writing changelog again
