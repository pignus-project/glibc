%define glibcrelease 11
%define auxarches i586 i686 athlon sparcv9 alphaev6
Summary: The GNU libc libraries.
Name: glibc
Version: 2.2.3
Release: %{glibcrelease}
Copyright: LGPL
Group: System Environment/Libraries
Source: %{name}-%{version}.tar.bz2
# In the source tarball the file diff-CYGNUS-to-REDHAT.patch contains all
# diffs applied by Red Hat to the current CVS version of glibc
Buildroot: %{_tmppath}/glibc-%{PACKAGE_VERSION}-root
Obsoletes: zoneinfo, libc-static, libc-devel, libc-profile, libc-headers,
Obsoletes:  linuxthreads, gencat, locale, ldconfig, locale-ja
Provides: ldconfig
Autoreq: false
Requires: glibc-common = %{version}-%{release}
%ifarch alpha
Provides: ld.so.2
%else
%endif
%ifarch sparc
Obsoletes: libc
%endif
Prereq: basesystem
# This is for building auxiliary programs like memusage
# For initial glibc bootstraps it can be commented out
BuildPreReq: gd-devel libpng-devel zlib-devel
%ifarch ix86 sparc sparcv9 alpha alphaev6
# This is to ensure that __frame_state_for exported by glibc
# will be compatible with egcs 1.x.y
BuildPreReq: gcc >= 2.96-84
%endif
%ifarch ia64
# Earlier gcc's die compiling glibc
BuildPreReq: gcc >= 2.96-82
%endif
Conflicts: rpm <= 4.0-0.65
Conflicts: glibc-devel < 2.2.3
Patch: glibc-kernel-2.4.patch
%ifarch ia64 sparc64 s390x
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%define enablemask [01].*|2.[0-3]*
%else
%define enablekernel 2.2.5
%ifarch i686
%define enablekernel2 2.4.1
%define enablemask [01].*|2.[0-3]*|2.4.0*
%else
%define enablemask [01].*|2.[0-1]*|2.2.[0-4]*
%endif
%endif

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%package devel
Summary: Header and object files for development using standard C libraries.
Group: Development/Libraries
Conflicts: texinfo < 3.11
Prereq: /sbin/install-info
Obsoletes: libc-debug, libc-headers, libc-devel, linuxthreads-devel
Obsoletes: glibc-debug
Prereq: kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}
%ifarch x86
# Earlier gcc's had atexit reference in crtendS.o, which does not
# work with this glibc where atexit is in libc_nonshared.a
Conflicts: gcc < 2.96-79
%endif
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

%package common
Summary: Common binaries and locale data for glibc
Conflicts: %{name} < %{version}
Conflicts: %{name} > %{version} 
Autoreq: false
Group: System Environment/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support and timezone
databases.

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
# If we are building enablekernel 2.x.y glibc on older kernel,
# we have to make sure no binaries compiled against that glibc
# are ever run
case `uname -r` in
%enablemask)
%patch -p1
;; esac

%ifarch armv4l sparc64 ia64 s390 s390x
rm -rf glibc-compat
%endif

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

%build
rm -rf build-%{_target_cpu}-linux
mkdir build-%{_target_cpu}-linux ; cd build-%{_target_cpu}-linux
GCC=gcc
%ifarch %{ix86}
BuildFlags="-march=%{_target_cpu} -D__USE_STRING_INLINES -fstrict-aliasing"
%endif
%ifarch alphaev6
BuildFlags="-mcpu=ev6"
%endif
%ifarch sparc
BuildFlags="-fcall-used-g7"
GCC="gcc -m32"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g7"
GCC="gcc -m32"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g7"
GCC="gcc -m64"
%endif
# Temporarily don't do this on ia64 and s390
%ifnarch ia64 s390 s390x
BuildFlags="$BuildFlags -freorder-blocks"
%endif
BuildFlags="$BuildFlags -DNDEBUG=1"
EnableKernel="--enable-kernel=%{enablekernel}"
%ifarch %{auxarches}
EnableKernel="$EnableKernel --disable-profile"
%endif
echo "$BuildFlags" > ../BuildFlags
CC="$GCC" CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
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

%ifarch i686
rm -rf build-%{_target_cpu}-linux2.4
mkdir build-%{_target_cpu}-linux2.4 ; cd build-%{_target_cpu}-linux2.4
GCC=gcc
BuildFlags=`cat ../BuildFlags`
EnableKernel="--enable-kernel=%{enablekernel2} --disable-profile"
CC="$GCC" CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
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
mkdir -p $RPM_BUILD_ROOT/lib/%{_target_cpu}/
cp -a libc.so $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libc-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libc-*.so` $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libc.so.*`
cp -a math/libm.so $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libm-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libm-*.so` $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libm.so.*`
cp -a linuxthreads/libpthread.so $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libpthread-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libpthread-*.so` $RPM_BUILD_ROOT/lib/%{_target_cpu}/`basename $RPM_BUILD_ROOT/lib/libpthread.so.*`
strip -R .comment $RPM_BUILD_ROOT/lib/{libc,libm,libpthread}-*.so
cd ..
%endif

# compatibility hack: this locale has vanished from glibc, but some other
# programs are still using it. Normally we would handle it in the %pre
# section but with glibc that is simply not an option
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/locale/ru_RU/LC_MESSAGES

# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*
%ifarch sparc64 ia64 s390 s390x
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

# Hardlink identical locale files together
gcc -O2 -o build-%{_target_cpu}-linux/hardlink redhat/hardlink.c
build-%{_target_cpu}-linux/hardlink -vc $RPM_BUILD_ROOT%{_prefix}/lib/locale

# BUILD THE FILE LIST
find $RPM_BUILD_ROOT -type f -or -type l |
	sed -e 's|.*/etc|%config &|' \
	    -e 's|.*/gconv/gconv-modules|%verify(not md5 size mtime) %config(noreplace) &|' > rpm.filelist.in
for n in %{_prefix}/share %{_prefix}/include %{_prefix}/lib/locale; do 
    find ${RPM_BUILD_ROOT}${n} -type d | \
	grep -v '%{_prefix}/share$' | \
	sed "s/^/%dir /" >> rpm.filelist.in
done

# primary filelist
SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
# rpm does not handle %lang() tagged files hardlinked together accross
# languages very well, temporarily disable
LIB_LANG=''
sed -e "s|$RPM_BUILD_ROOT||" -e "$LIB_LANG" -e "$SHARE_LANG" < rpm.filelist.in |
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
	
grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/lib/locale' < rpm.filelist >> common.filelist
grep '%{_prefix}/libexec' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^g]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist >> common.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/bin' < rpm.filelist.full |
	grep -v '%{_prefix}/lib/locale' |
	grep -v '%{_prefix}/libexec' | 
	grep -v '%{_prefix}/sbin/[^g]' |
	grep -v '%{_prefix}/share' > rpm.filelist

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
%doc COPYING COPYING.LIB README.template README.libm
%doc hesiod/README.hesiod

%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f profile.filelist profile
%defattr(-,root,root)

%files -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%config /etc/rc.d/init.d/nscd
%{_prefix}/sbin/nscd
%endif

%changelog
* Wed Jun  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix a bunch of math bugs (#43210, #43345, #43346, #43347, #43348, #43355)
- make rpc headers -ansi compilable (#42390)
- remove alphaev6 optimized memcpy, since there are still far too many
  broken apps which call memcpy where they should call memmove
- update from CVS to (among other things):
  - fix tanhl bug (#43352)

* Tue May 22 2001 Jakub Jelinek <jakub@redhat.com>
- fix #include <signal.h> with -D_XOPEN_SOURCE=500 on ia64 (#35968)
- fix a dlclose reldeps handling bug
- some more profiling fixes
- fix tgmath.h

* Thu May 17 2001 Jakub Jelinek <jakub@redhat.com>
- make ldconfig more quiet
- fix LD_PROFILE on i686 (#41030)

* Wed May 16 2001 Jakub Jelinek <jakub@redhat.com>
- fix the hardlink program, so that it really catches all files with
  identical content
- add a s390x clone fix

* Wed May 16 2001 Jakub Jelinek <jakub@redhat.com>
- fix rpc for non-threaded apps using svc_fdset and similar variables (#40409)
- fix nss compatibility DSO versions for alphaev6
- add a hardlink program instead of the shell 3x for plus cmp -s/link
  which takes a lot of time during build
- rework BuildPreReq and Conflicts with gcc, so that
  it applies only where it has to

* Fri May 11 2001 Jakub Jelinek <jakub@redhat.com>
- fix locale name of ja_JP in UTF-8 (#39783)
- fix re_search_2 (#40244)
- fix memusage script (#39138, #39823)
- fix dlsym(RTLD_NEXT, ) from main program (#39803)
- fix xtrace script (#39609)
- make glibc conflict with glibc-devel 2.2.2 and below (to make sure
  libc_nonshared.a has atexit)
- fix getconf LFS_CFLAGS on 64bitters
- recompile with gcc-2.96-84 or above to fix binary compatibility problem
  with __frame_state_for function (#37933)

* Fri Apr 27 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.3 release
  - fix strcoll (#36539)
- add BuildPreReqs (#36378)

* Wed Apr 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix sparc64, ia64
  - fix some locale syntax errors (#35982)

* Wed Apr 18 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Wed Apr 11 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr  6 2001 Jakub Jelinek <jakub@redhat.com>
- support even 2.4.0 kernels on ia64, sparc64 and s390x
- include UTF-8 locales
- make gconv-modules %%config(noreplace)

* Fri Mar 23 2001 Jakub Jelinek <jakub@redhat.com>
- back out sunrpc changes

* Wed Mar 21 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build
  - fix pthread_getattr_np

* Fri Mar 16 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - run atexit() registered functions at dlclose time if they are in shared
    libraries (#28625)
  - add pthread_getattr_np API to make JVM folks happy

* Wed Mar 14 2001 Jakub Jelinek <jakub@redhat.com>
- require 2.4.1 instead of 2.4.0 on platforms where it required 2.4 kernel
- fix ldd behaviour on unresolved symbols
- remove nonsensical ldconfig warning, update osversion for the most
  recent library with the same soname in the same directory instead (#31703)
- apply selected patches from CVS
- s390x spec file changes from Florian La Roche

* Wed Mar  7 2001 Jakub Jelinek <jakub@redhat.com>
- fix gencat (#30894)
- fix ldconfig changes from yesterday, fix LD_ASSUME_KERNEL handling

* Tue Mar  6 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
- make pthread_attr_setstacksize consistent before and after pthread manager
  is started (#28194)
- pass back struct sigcontext from pthread signal wrapper (on ia32 only so
  far, #28493)
- on i686 ship both --enable-kernel 2.2.5 and 2.4.0 libc/libm/libpthread,
  make ld.so pick the right one

* Sat Feb 17 2001 Preston Brown <pbrown@redhat.com>
- glib-common doesn't require glibc, until we can figure out how to get out of dependency hell.

* Sat Feb 17 2001 Jakub Jelinek <jakub@redhat.com>
- make glibc require particular version of glibc-common
  and glibc-common prerequire glibc.

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.2 release
  - fix regex REG_ICASE bug seen in ksymoops

* Sat Feb 10 2001 Jakub Jelinek <jakub@redhat.com>
- fix regexec leaking memory (#26864)

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build with gnupro
  - make regex 64bit clean
  - fix tgmath make check failures on alpha

* Tue Feb  6 2001 Jakub Jelinek <jakub@redhat.com>
- update again for ia64 DF_1_INITFIRST

* Fri Feb  2 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix getaddrinfo (#25437)
  - support DF_1_INITFIRST (#25029)

* Wed Jan 24 2001 Jakub Jelinek <jakub@redhat.com>
- build all auxiliary arches with --enablekernel 2.4.0, those wanting
  to run 2.2 kernels can downgrade to the base architecture glibc.

* Sat Jan 20 2001 Jakub Jelinek <jakub@redhat.com>
- remove %%lang() flags from %%{_prefix}/lib/locale files temporarily

* Sun Jan 14 2001 Jakub Jelinek <jakub@redhat.com>
- update to 2.2.1 final
  - fix a pthread_kill_other_threads_np breakage (#23966)
  - make static binaries using dlopen work on ia64 again
- fix a typo in glibc-common group

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- devel requires glibc = %%{version}
- noreplace /etc/nscd.conf

* Wed Jan 10 2001 Jakub Jelinek <jakub@redhat.com>
- some more security fixes:
  - don't look up LD_PRELOAD libs in cache for SUID apps
    (because that bypasses SUID bit checking on the library)
  - place output files for profiling SUID apps into /var/profile,
    use O_NOFOLLOW for them
  - add checks for $MEMUSAGE_OUTPUT and $SEGFAULT_OUTPUT_NAME
- hardlink identical locale files together
- add %%lang() tags to locale stuff
- remove ko_KR.utf8 for now, it is provided by locale-utf8 package

* Mon Jan  8 2001 Jakub Jelinek <jakub@redhat.com>
- add glibc-common subpackage
- fix alphaev6 memcpy (#22494)
- fix sys/cdefs.h (#22908)
- don't define stdin/stdout/stderr as macros for -traditional (#22913)
- work around a bug in IBM JDK (#22932, #23012)
- fix pmap_unset when network is down (#23176)
- move nscd in rc.d before netfs on shutdown
- fix $RESOLV_HOST_CONF in SUID apps (#23562)

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ftw and nftw

* Wed Dec 13 2000 Jakub Jelinek <jakub@redhat.com>
- fix fcvt (#22184)
- ldd /lib/ld-linux.so.2 is not crashing any longer again (#22197)
- fix gencat

* Mon Dec 11 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha htonl and alphaev6 stpcpy

* Sat Dec  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - fix getnameinfo (#21934)
  - don't stomp on memory in rpath handling (#21544)
  - fix setlocale (#21507)
- fix libNoVersion.so.1 loading code (#21579)
- use auxarches define in spec file for auxiliary
  architectures (#21219)
- remove /usr/share directory from filelist (#21218)

* Sun Nov 19 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix getaddrinfo

* Fri Nov 17 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix freopen
- remove all alpha workarounds, not needed anymore

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix dladdr bug on alpha/sparc32/sparc64
- fix Makefiles so that they run static tests properly

* Tue Nov 14 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix ldconfig

* Thu Nov  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to glibc 2.2 release

* Mon Nov  6 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - export __sysconf@@GLIBC_2.2 (#20417)

* Fri Nov  3 2000 Jakub Jelinek <jakub@redhat.com>
- merge to 2.1.97

* Mon Oct 30 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS, including:
  - fix WORD_BIT/LONG_BIT definition in limits.h (#19088)
  - fix hesiod (#19375)
  - set LC_MESSAGES in zic/zdump for proper error message output (#19495)
  - fix LFS fcntl when used with non-LFS aware kernels (#19730)

* Thu Oct 19 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha semctl (#19199)
- update to CVS, including:
  - fix glibc headers for Compaq non-gcc compilers
  - fix locale alias handling code (#18832)
  - fix rexec on little endian machines (#18886)
- started writing changelog again

* Thu Aug 10 2000 Adrian Havill <havill@redhat.com>
- added ja ujis alias for backwards compatibility
