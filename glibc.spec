%define glibcrelease 40
%define auxarches i586 i686 athlon sparcv9 alphaev6
%define prelinkarches i686 athlon alpha alphaev6
%define prelinkdate 20020617
Summary: The GNU libc libraries.
Name: glibc
Version: 2.2.5
Release: %{glibcrelease}
Copyright: LGPL
Group: System Environment/Libraries
Source: %{name}-%{version}.tar.bz2
Source2: ftp://people.redhat.com/jakub/prelink/prelink-%{prelinkdate}.tar.bz2
# In the source tarball the file diff-CYGNUS-to-REDHAT.patch contains all
# diffs applied by Red Hat to the current CVS version of glibc
Buildroot: %{_tmppath}/glibc-%{PACKAGE_VERSION}-root
Obsoletes: zoneinfo, libc-static, libc-devel, libc-profile, libc-headers,
Obsoletes:  linuxthreads, gencat, locale, ldconfig, locale-ja
Provides: ldconfig
Autoreq: false
Requires: glibc-common = %{version}-%{release}
%ifarch sparc
Obsoletes: libc
%endif
Prereq: basesystem
# This is for building auxiliary programs like memusage
# For initial glibc bootstraps it can be commented out
BuildPreReq: gd-devel libpng-devel zlib-devel
BuildPreReq: libelf >= 0.7.0-2
# This is to ensure that __frame_state_for exported by glibc
# will be compatible with egcs 1.x.y
BuildPreReq: gcc >= 2.96-84
Conflicts: rpm <= 4.0-0.65
Conflicts: glibc-devel < 2.2.3
Patch: glibc-kernel-2.4.patch
Patch2: glibc-2.2.5.patch
Patch3: glibc-2.2.5-security.patch
Patch4: glibc-2.2.5-getdents.patch
Patch5: glibc-2.2.5-xdr_array.patch
Patch6: glibc-2.2.5-calloc.patch
%ifarch ia64 sparc64 s390x
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%define enablemask [01].*|2.[0-3]*
%else
%define enablekernel 2.2.5
%ifarch i686 athlon
%define enablekernel2 2.4.1
%define enablemask [01].*|2.[0-3]*|2.4.0*
%else
%define enablemask [01].*|2.[0-1]*|2.2.[0-4]|2.2.[0-4][^0-9]*
%endif
%endif
%define __find_provides %{_builddir}/%{name}-%{version}/find_provides.sh

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
need to install the glibc-profile package.

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
Prereq: /sbin/chkconfig, /usr/sbin/useradd, /usr/sbin/userdel, sh-utils
Autoreq: true

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well. Note that you
can't use nscd with 2.0 kernels because of bugs in the kernel-side
thread support. Unfortunately, nscd happens to hit these bugs
particularly hard.

%package debug
Summary: Shared standard C libraries with debugging information
Group: Development/Libraries
Requires: glibc = %{version}-%{release}, glibc-devel = %{version}-%{release}
Autoreq: false

%description debug
The glibc-debug package contains shared standard C libraries
with debugging information.  You need this only if you want to step into
C library routines during debugging.
To use these libraries, you need to set LD_LIBRARY_PATH=%{_prefix}/%{_lib}/debug
in your environment before starting debugger.
If you want to see glibc source files during debugging, you should
rpm -i glibc-%{version}-%{release}.src.rpm
rpm -bp %{_specdir}/glibc.spec

If unsure if you need this, don't install this package.

%package debug-static
Summary: Static standard C libraries with debugging information
Group: Development/Libraries
Requires: glibc = %{version}-%{release}, glibc-devel = %{version}-%{release}
Autoreq: true

%description debug-static
The glibc-debug-static package contains static standard C libraries
with debugging information.  You need this only if you want to step into
C library routines during debugging programs statically linked against
one or more of the standard C libraries.
To use this debugging information, you need to link binaries
with -L%{_prefix}/%{_lib}/debug compiler option.
If you want to see glibc source files during debugging, you should
rpm -i glibc-%{version}-%{release}.src.rpm
rpm -bp %{_specdir}/glibc.spec

If unsure if you need this, don't install this package.

%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: glibc = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%prep
%setup -q
# If we are building enablekernel 2.x.y glibc on older kernel,
# we have to make sure no binaries compiled against that glibc
# are ever run
case `uname -r` in
%enablemask)
%patch -p1
;; esac
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

perl -pi -e 'm/PACKET.*1024/ and s/1024/65536/' \
  `find resolv glibc-compat -name \*.c`

%ifarch %{prelinkarches}
mkdir prelink
tar x --bzip2 -C prelink -f %{SOURCE2}
%endif

%ifarch armv4l sparc64 ia64 s390 s390x
rm -rf glibc-compat
%endif

# Waiting for explanation...
rm -f sysdeps/powerpc/memset.S

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;
cat > find_provides.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh

%build
rm -rf build-%{_target_cpu}-linux
mkdir build-%{_target_cpu}-linux ; cd build-%{_target_cpu}-linux
GCC=gcc
%ifarch %{ix86}
BuildFlags="-march=%{_target_cpu}"
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
%ifnarch ia64 s390 s390x
BuildFlags="$BuildFlags -freorder-blocks"
%endif
BuildFlags="$BuildFlags -DNDEBUG=1"
if gcc -v | grep -q 'gcc version 3'; then
  BuildFlags="$BuildFlags -finline-limit=2000"
fi
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
gcc -static -Os ../redhat/glibc_post_upgrade.c -o glibc_post_upgrade \
%ifarch i386
    -DARCH_386 '-DVERSION="%{version}"' '-DPVERSION="0.9"' \
%endif
    '-DGCONV_MODULES_CACHE="%{_prefix}/%{_lib}/gconv/gconv-modules.cache"'

%install
if [ -x /usr/bin/getconf ] ; then
  numprocs=$(/usr/bin/getconf _NPROCESSORS_ONLN)
  if [ $numprocs -eq 0 ]; then
    numprocs=1
  fi
else
  numprocs=1
fi
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install_root=$RPM_BUILD_ROOT install -C build-%{_target_cpu}-linux
%ifnarch %{auxarches}
cd build-%{_target_cpu}-linux && \
    make -j$numprocs install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
    cd ..
%endif

%ifarch i686 athlon
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
mkdir -p $RPM_BUILD_ROOT/lib/i686/
cp -a libc.so $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libc-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libc-*.so` $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libc.so.*`
cp -a math/libm.so $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libm-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libm-*.so` $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libm.so.*`
cp -a linuxthreads/libpthread.so $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libpthread-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libpthread-*.so` $RPM_BUILD_ROOT/lib/i686/`basename $RPM_BUILD_ROOT/lib/libpthread.so.*`
strip -R .comment $RPM_BUILD_ROOT/lib/{libc,libm,libpthread}-*.so
cd ..
%endif

%ifarch %{prelinkarches}
# Build prelink
cd prelink/prelink
%configure
make
cd ../..
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

# If librt.so is a symlink, change it into linker script
if [ -L $RPM_BUILD_ROOT%{_prefix}/%{_lib}/librt.so ]; then
  rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/librt.so
  LIBRTSO=`cd $RPM_BUILD_ROOT/%{_lib}; echo librt.so.*`
  LIBPTHREADSO=`cd $RPM_BUILD_ROOT/%{_lib}; echo libpthread.so.*`
  cat > $RPM_BUILD_ROOT%{_prefix}/%{_lib}/librt.so <<EOF
/* GNU ld script
   librt.so.1 needs libpthread.so.0 to come before libc.so.6*
   in search scope.  */
GROUP ( /%{_lib}/$LIBPTHREADSO /%{_lib}/$LIBRTSO )
EOF
fi

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

# Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache

# Install the upgrade program
install -m 700 build-%{_target_cpu}-linux/glibc_post_upgrade $RPM_BUILD_ROOT/usr/sbin/glibc_post_upgrade

# Strip binaries
strip -R .comment $RPM_BUILD_ROOT/sbin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/bin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/sbin/* || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/libexec/pt_chown || :
strip -R .comment $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/* || :

mkdir $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug
cp -a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug/
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug/*_p.a
cp -a $RPM_BUILD_ROOT/%{_lib}/lib*.so* $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug/
# Now strip debugging info from all static and shared libraries but
# those which will be in glibc-debug subpackage
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
for i in *.a; do
  if [ -f $i ]; then
    case "$i" in
    *_p.a) ;;
    *) strip -g -R .comment $i ;;
    esac
  fi
done
popd
%ifarch i686 athlon
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug/{libc,libm,libpthread}[-.]*.so*
cp -a $RPM_BUILD_ROOT/%{_lib}/i686/lib*.so* $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug/
%endif
pushd $RPM_BUILD_ROOT/%{_lib}
for i in *.so*; do
  if [ -f $i -a ! -L $i ]; then
    if [ "$i" = libc.so -o "$i" = librt.so ]; then
      :
%ifarch i686 athlon
    elif [ -f i686/$i ]; then
      strip -g -R .comment i686/$i
%endif
    else
      strip -g -R .comment $i
    fi
  fi
done
popd

%ifarch i686 athlon
# Prelink ld.so and libc.so
cd prelink
> prelink.conf
# For now disable prelinking of ld.so, as it breaks statically linked
# binaries built against non-NDEBUG old glibcs (assert unknown dynamic tag)
# prelink/src/prelink -c ./prelink.conf -C ./prelink.cache \
#  --mmap-region-start=0x40000000 $RPM_BUILD_ROOT/%{_lib}/ld-*.so
prelink/src/prelink --reloc-only=0x42000000 \
  $RPM_BUILD_ROOT/%{_lib}/i686/libc-*.so
cd ..
%endif
%ifarch alpha alphaev6
# Prelink ld.so and libc.so
cd prelink
> prelink.conf
# For now disable prelinking of ld.so, as it breaks statically linked
# binaries built against non-NDEBUG old glibcs (assert unknown dynamic tag)
# prelink/src/prelink -c ./prelink.conf -C ./prelink.cache \
#  --mmap-region-start=0x0000020000000000 $RPM_BUILD_ROOT/%{_lib}/ld-*.so
prelink/src/prelink --reloc-only=0x0000020010000000 \
  $RPM_BUILD_ROOT/%{_lib}/libc-*.so
cd ..
%endif

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# Hardlink identical locale files together
%ifnarch %{auxarches}
gcc -O2 -o build-%{_target_cpu}-linux/hardlink redhat/hardlink.c
build-%{_target_cpu}-linux/hardlink -vc $RPM_BUILD_ROOT%{_prefix}/lib/locale
%endif

# BUILD THE FILE LIST
find $RPM_BUILD_ROOT -type f -or -type l |
	sed -e 's|.*/etc|%config &|' \
	    -e 's|.*/gconv/gconv-modules$|%verify(not md5 size mtime) %config(noreplace) &|' \
	    -e 's|.*/gconv/gconv-modules.cache|%verify(not md5 size mtime) &|' \
	    -e '/debug/d' > rpm.filelist.in
for n in %{_prefix}/share %{_prefix}/include %{_prefix}/lib/locale; do 
    find ${RPM_BUILD_ROOT}${n} -type d | \
	grep -v '%{_prefix}/share$' | \
	grep -v '\(%{_mandir}\|%{_infodir}\)' | \
	sed "s/^/%dir /" >> rpm.filelist.in
done

# primary filelist
SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
# rpm does not handle %lang() tagged files hardlinked together accross
# languages very well, temporarily disable
# LIB_LANG=''
sed -e "s|$RPM_BUILD_ROOT||" -e "$LIB_LANG" -e "$SHARE_LANG" < rpm.filelist.in |
	grep -v '/etc/\(localtime\|nsswitch.conf\|ld.so.conf\)'  | \
	grep -v '/%{_lib}/lib\(pcprofile\|memusage\).so' | \
	grep -v 'bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\)' | \
	sort > rpm.filelist

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}
for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
  cp -a $i $i.tmp
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_prefix}/%{_lib}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_prefix}/%{_lib}/libmemusage.so~' \
    $i.tmp > $i
  chmod 755 $i; rm -f $i.tmp
done

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

%ifnarch %{auxarches}
grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/lib/locale' < rpm.filelist >> common.filelist
grep '%{_prefix}/libexec' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist >> common.filelist
%endif

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/bin' < rpm.filelist.full |
	grep -v '%{_prefix}/lib/locale' |
	grep -v '%{_prefix}/libexec' | 
	grep -v '%{_prefix}/sbin/[^gi]' |
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

echo ====================TESTING=========================
cd build-%{_target_cpu}-linux
make -j$numprocs -k check PARALLELMFLAGS=-s || :
cd ..
%ifarch i686 athlon
echo ====================TESTING OPTIMIZED===============
cd build-%{_target_cpu}-linux2.4
make -j$numprocs -k check PARALLELMFLAGS=-s || :
cd ..
%endif
echo ====================TESTING END=====================

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

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

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
%ifarch i686 athlon
%dir /lib/i686
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB README.libm
%doc hesiod/README.hesiod

%files debug
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/debug
%{_prefix}/%{_lib}/debug/*.so*

%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f profile.filelist profile
%defattr(-,root,root)

%files utils
%defattr(-,root,root)
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace

%files debug-static
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/debug
%{_prefix}/%{_lib}/debug/*.a

%files -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%config /etc/rc.d/init.d/nscd
%{_prefix}/sbin/nscd
%endif

%changelog
* Mon Sep  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-40
- fix resolver buffer overflows

* Wed Aug  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-39
- fix the calloc patch so that calloc (131072, 0) doesn't
  crash

* Thu Aug  1 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-38
- fix xdr_array buffer overflow
- fix calloc overflow (both patches by Solar Designer)
- getdents fix for LSB conformance

* Tue Jul  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-37
- fix buffer overflows in getnetby* (if nsswitch.conf
  network: line includes dns) and gethostby* for apps compiled
  against glibc 2.0.

* Tue Jun 18 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-36
- fix nice return value
- fix __moddi3 (#65612, #65695)
- export get*ent_r@@GLIBC_2.1.2 symbols (#66278)
- update prelink to fix prelink -r on alpha

* Mon Apr 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-34
- add relocation dependencies even for weak symbols (#63422)
- stricter check_fds check for suid/sgid binaries
- run make check at %%install time

* Sat Apr 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-33
- handle Dec 31 1969 in mktime for timezones west of GMT (#63369)
- back out do-lookup.h change (#63261, #63305)
- use "memory" clobber instead all the fancy stuff in i386/i686/bits/string.h
  since lots of compilers break on it
- fix sparc build with gcc 3.1
- fix spec file for athlon

* Tue Apr  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-32
- fix debugging of threaded apps (#62804)
- fix DST for Estonia (#61494)
- document that pthread_mutexattr_?etkind_np are deprecated
  and pthread_mutexattr_?ettype should be used instead in man
  pages (#61485)
- fix libSegFault.so undefined externals

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-31
- temporarily disable prelinking ld.so, as some statically linked
  binaries linked against debugging versions of old glibcs die on it
  (#62352)
- fix <semaphore.h> for -std=c99 (#62516)
- fix ether_ntohost segfault (#62397)
- remove in glibc_post_upgrade on i386 all /lib/i686/libc-*.so,
  /lib/i686/libm-*.so and /lib/i686/libpthread-*.so, not just current
  version (#61633)
- prelink -r on alpha too

* Thu Mar 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-30
- update GB18030 iconv module (Yu Shao)

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-29
- features.h fix

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-28
- update from CVS
  - fix nscd with huge groups
  - fix nis to not close fds it shouldn't
- rebuilt against newer glibc-kernheaders to use the correct
  PATH_MAX
- handle .athlon.rpm glibc the same way as .i686.rpm
- add a couple of .ISO-8859-15 locales (#61922)
- readd temporarily currencies which were superceeded by Euro
  into the list of accepted currencies by localedef to make
  standard conformance testsuites happy
- temporarily moved __libc_waitpid back to make Sun JDK happy
- use old malloc code
- prelink i686/athlon ld.so and prelink -r i686/athlon libc.so

* Thu Mar 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-27
- update from CVS
  - fix DST handling for southern hemisphere (#60747)
  - fix daylight setting for tzset (#59951)
  - fix ftime (#60350)
  - fix nice return value
  - fix a malloc segfault
- temporarily moved __libc_wait, __libc_fork and __libc_stack_end
  back to what they used to be exported at
- censorship (#60758)

* Thu Feb 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-26
- update from CVS
- use __attribute__((visibility(...))) if supported, use _rtld_local
  for ld.so only objects
- provide libc's own __{,u}{div,mod}di3

* Wed Feb 27 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-25
- switch back to 2.2.5, mmap stdio needs work

* Mon Feb 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-8
- fix two other mmap stdio bugs (#60228)

* Thu Feb 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-7
- fix yet another mmap stdio bug (#60145)

* Tue Feb 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-6
- fix mmap stdio bug (seen on ld as File truncated error, #60043)
- apply Andreas Schwab's fix for pthread sigwait
- remove /lib/i686/ libraries in glibc_post_upgrade when
  performing i386 glibc install

* Thu Feb 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-5
- update to CVS
- added glibc-utils subpackage
- disable autoreq in glibc-debug
- readd %%lang() to locale files

* Fri Feb  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-4
- update to CVS
- move glibc private symbols to GLIBC_PRIVATE symbol version

* Wed Jan  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-3
- fix a sqrt bug on alpha which caused SHN_UNDEF $__full_ieee754_sqrt..ng
  symbol in libm

* Tue Jan  8 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-2
- add debug-static package

* Mon Dec 31 2001 Jakub Jelinek <jakub@redhat.com> 2.2.90-1
- update from CVS
- remove -D__USE_STRING_INLINES
- add debug subpackage to trim glibc and glibc-devel size

* Wed Oct  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-19
- fix strsep

* Fri Sep 28 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-18
- fix a ld.so bug with duplicate searchlists in l_scope
- fix erfcl(-inf)
- turn /usr/lib/librt.so into linker script

* Wed Sep 26 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-17
- fix a ld.so lookup bug after lots of dlopen calls
- fix CMSG_DATA for non-gcc non-ISOC99 compilers (#53984)
- prelinking support for Sparc64

* Fri Sep 21 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-16
- update from CVS to fix DT_SYMBOLIC
- prelinking support for Alpha and Sparc

* Tue Sep 18 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-15
- update from CVS
  - linuxthreads now retries if -1/EINTR is returned from
    reading or writing to thread manager pipe (#43742)
- use DT_FILTER in librt.so (#53394)
  - update glibc prelink patch so that it handles filters
- fix timer_* with SIGEV_NONE (#53494)
- make glibc_post_upgrade work on PPC (patch from Franz Sirl)

* Mon Sep 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-14
- fix build on sparc32
- 2.2.4-13 build for some reason missed some locales
  on alpha/ia64

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-13
- fix iconvconfig

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-12
- add fam to /etc/rpc (#52863)
- fix <inttypes.h> for C++ (#52960)
- fix perror

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-11
- fix strnlen(x, -1)

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-10
- doh, <bits/libc-lock.h> should only define __libc_rwlock_t
  if __USE_UNIX98.

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-9
- fix bits/libc-lock.h so that gcc can compile
- fix s390 build

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-8
- kill stale library symlinks in ldconfig (#52350)
- fix inttypes.h for G++ < 3.0
- use DT_REL*COUNT

* Wed Aug 22 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-7
- fix strnlen on IA-64 (#50077)

* Thu Aug 16 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-6
- glibc 2.2.4 final
- fix -lpthread -static (#51672)

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-5
- doh, include libio/tst-swscanf.c

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-4
- don't crash on catclose(-1)
- fix wscanf %[] handling
- fix return value from swprintf
- handle year + %U/%W week + week day in strptime

* Thu Aug  9 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-3
- update from CVS to
  - fix strcoll (#50548)
  - fix seekdir (#51132)
  - fix memusage (#50606)
- don't make gconv-modules.cache %%config file, just don't verify
  its content.

* Mon Aug  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix strtod and *scanf (#50723, #50724)

* Sat Aug  4 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix iconv cache handling
- glibc should not own %{_infodir}, %{_mandir} nor %{_mandir}/man3 (#50673)
- add gconv-modules.cache as emtpy config file (#50699)
- only run iconvconfig if /usr is mounted read-write (#50667)

* Wed Jul 25 2001 Jakub Jelinek <jakub@redhat.com>
- move iconvconfig from glibc-common into glibc subpackage,
  call it from glibc_post_upgrade instead of common's post.

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com>
- turn off debugging printouts in iconvconfig

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix IA-32 makecontext
  - make fflush(0) thread-safe (#46446)

* Mon Jul 23 2001 Jakub Jelinek <jakub@redhat.com>
- adjust prelinking DT_* and SHT_* values in elf.h
- update from CVS
  - iconv cache
  - make iconv work in SUID/SGID programs (#34611)

* Fri Jul 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - kill non-pic code in libm.so
  - fix getdate
  - fix some locales (#49402)
- rebuilt with binutils-2.11.90.0.8-5 to place .interp section
  properly in libBrokenLocale.so, libNoVersion.so and libanl.so
- add floating stacks on IA-64, Alpha, Sparc (#49308)

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com>
- make /lib/i686 directory owned by glibc*.i686.rpm

* Mon Jul  9 2001 Jakub Jelinek <jakub@redhat.com>
- remove rquota.[hx] headers which are now provided by quota (#47141)
- add prelinking patch

* Thu Jul  5 2001 Jakub Jelinek <jakub@redhat.com>
- require sh-utils for nscd

* Mon Jun 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS (#43681, #43350, #44663, #45685)
- fix ro_RO bug (#44644)

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
