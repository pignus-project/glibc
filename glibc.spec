%define glibcrelease 4.80.8
%define auxarches i586 i686 athlon sparcv9 alphaev6
%define prelinkarches i686 athlon alpha alphaev6
%define nptlarches noarch
%define withtlsarches noarch
%define _unpackaged_files_terminate_build 0
%define glibcdate 20030312
Summary: The GNU libc libraries.
Name: glibc
Version: 2.3.2
Release: %{glibcrelease}
Copyright: LGPL
Group: System Environment/Libraries
Source0: %{name}-%{version}-%{glibcdate}.tar.bz2
Source1: %{name}-redhat-%{glibcdate}.tar.bz2
Source2: nptl-%{glibcdate}.tar.bz2
Patch0: %{name}-redhat.patch
Patch1: glibc-Versions.patch
Patch2: glibc-compat.patch
Patch3: glibc-add-ons.patch
Patch4: glibc-dl-i686.patch
Patch5: glibc-__fork.patch
Patch6: glibc-i386-uid32.patch
Patch7: glibc-sshd-condrestart.patch
Patch8: glibc-notls.patch
Patch9: glibc-pthread-sigsuspend.patch
Patch10: glibc-lt-pthread-atfork.patch
Patch11: glibc-errno-plt.patch
Patch12: glibc-pthread-version.patch
Patch13: glibc-misc.patch
Patch14: glibc-getgrouplist.patch
Patch15: glibc-nscd-lockup.patch
Patch16: glibc-ua-collation.patch
Patch17: glibc-perror.patch
Patch18: glibc-ldconfig-whitespace.patch
Patch19: glibc-strxfrm.patch
Patch20: glibc-localedef-time.patch
Patch21: glibc-getaddrinfo.patch
Patch22: glibc-libio-compat.patch
Patch23: glibc-cxa-finalize.patch
Patch24: glibc-sprintf.patch
Patch25: glibc-seteuid.patch
Patch26: glibc-ldconfig-order.patch
Patch27: glibc-i686-i386-upgrade.patch
Patch28: glibc-errno-stderr.patch
Patch29: glibc-i386-sysdep-cancel.patch
Patch30: glibc-important-hwcaps.patch
Patch31: glibc-dlopen-exec.patch
Patch32: glibc-glob-lnk.patch
Patch33: glibc-glob-brace-escape.patch
Patch34: glibc-reverse-ipv6.patch
Patch35: glibc-sprof.patch
Patch36: glibc-locale-be64.patch
Patch37: glibc-pthread-cond-timedwait.patch
Patch38: glibc-lt-sigaction.patch
Patch39: glibc-stdio-compat.patch
Patch40: glibc-uselocale.patch
Patch41: glibc-ftw.patch

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
%ifarch %{prelinkarches}
BuildPreReq: prelink >= 0.2.0-5
%endif
# This is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildPreReq: gcc >= 3.2
Conflicts: rpm <= 4.0-0.65
Conflicts: glibc-devel < 2.2.3
%ifarch ia64 sparc64 s390x
Conflicts: kernel < 2.4.0
%define enablekernel 2.4.0
%else
%define enablekernel 2.2.5
%ifarch i686 athlon
%define enablekernelltfs 2.4.1
%endif
%endif
%ifarch %{nptlarches}
%define enablekernelnptl 2.4.20
BuildRequires: binutils >= 2.13.90.0.16-5
BuildRequires: gcc >= 3.2.1-5
%endif
%if "%{_enable_debug_packages}" == "1"
BuildPreReq: elfutils >= 0.72
BuildPreReq: rpm >= 4.2-0.56
%endif
%define __find_provides %{_builddir}/%{name}-%{version}-%{glibcdate}/find_provides.sh
%define __find_requires %{_builddir}/%{name}-%{version}-%{glibcdate}/find_requires.sh

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
Conflicts: binutils < 2.13.90.0.2-2
Prereq: /sbin/install-info
Obsoletes: libc-debug, libc-headers, libc-devel, linuxthreads-devel
Prereq: kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}
%ifarch %{ix86}
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

%package -n nptl-devel
Summary: Header files and static libraries for development using NPTL library.
Group: Development/Libraries
Requires: glibc-devel = %{version}-%{release}
Autoreq: true

%description -n nptl-devel
The nptl-devel package contains the header and object files necessary
for developing programs which use the NPTL library (and either need
NPTL specific header files or want to link against NPTL statically).

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
Autoprov: false

%description debug
The glibc-debug package contains shared standard C libraries
with debugging information.  You need this only if you want to step into
C library routines during debugging.
To use these libraries, you need to set LD_LIBRARY_PATH=%{_prefix}/%{_lib}/debug
in your environment before starting debugger.
If you want to see glibc source files during debugging, you should
rpm -i glibc-%{version}-%{release}.src.rpm
rpm -bp /usr/src/redhat/SPECS/glibc.spec

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
rpm -bp /usr/src/redhat/SPECS/glibc.spec

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

%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}-%{glibcdate} -a1 -a2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1

%ifnarch %{ix86} alpha alphaev6 sparc sparcv9
rm -rf glibc-compat
%endif

# A lot of programs still misuse memcpy when they have to use
# memmove. The memcpy implementation below is not tolerant at
# all.
rm -f sysdeps/alpha/alphaev6/memcpy.S

# For 8.0 errata glibc, don't support {INIT,PREINIT,FINI}_ARRAY,
# because that requires a newer binutils
perl -pi -e 's/libc_cv_initfinit_array=yes/libc_cv_initfinit_array=no/' \
  configure.in configure

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;
cat > find_provides.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh
cat > find_requires.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-requires | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_requires.sh
touch `find . -name configure`

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
BuildFlags="-fcall-used-g6"
GCC="gcc -m32"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g6"
GCC="gcc -m32"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g6"
GCC="gcc -m64"
%endif
BuildFlags="$BuildFlags -DNDEBUG=1"
if gcc -v 2>&1 | grep -q 'gcc version 3'; then
  BuildFlags="$BuildFlags -finline-limit=2000"
fi
EnableKernel="--enable-kernel=%{enablekernel}"
echo "$BuildFlags" > ../BuildFlags
AddOns=`cd .. && echo */configure | sed -e 's!/configure!!g;s!\(linuxthreads\|nptl\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`
echo "$AddOns" > ../AddOns
Pthreads=linuxthreads
%ifarch %{withtlsarches}
WithTls="--with-tls --without-__thread"
%else
WithTls="--without-tls --without-__thread"
%endif
CC="$GCC" CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
	--enable-add-ons=$Pthreads$AddOns --without-cvs $EnableKernel \
	--with-headers=%{_prefix}/include \
	$WithTls --build %{_target_cpu}-redhat-linux --host %{_target_cpu}-redhat-linux
if [ -x /usr/bin/getconf ] ; then
  numprocs=$(/usr/bin/getconf _NPROCESSORS_ONLN)
  if [ $numprocs -eq 0 ]; then
    numprocs=1
  fi
else
  numprocs=1
fi
make -j$numprocs -r CFLAGS="$BuildFlags -g -O3" PARALLELMFLAGS=-s
gcc -static -L. -Os ../redhat/glibc_post_upgrade.c -o glibc_post_upgrade \
%ifarch i386
    -DARCH_386 '-DVERSION="%{version}"' \
    '-DPVERSION="'`sed 's/^linuxthreads-\([0-9.]*\) .*$/\1/' ../linuxthreads/Banner`'"' \
%endif
    '-DGCONV_MODULES_CACHE="%{_prefix}/%{_lib}/gconv/gconv-modules.cache"'
mkdir sed
cd sed
CFLAGS="$BuildFlags -g -O2" ../../redhat/sed-3.02/configure
make -j$numprocs
cd ..

%install
# hack
unset LD_ASSUME_KERNEL || :

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
make -j1 install_root=$RPM_BUILD_ROOT install -C build-%{_target_cpu}-linux PARALLELMFLAGS=-s
%ifnarch %{auxarches}
cd build-%{_target_cpu}-linux && \
    make -j$numprocs install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
    cd ..
%endif

SubDir=

%ifarch i686 athlon
rm -rf build-%{_target_cpu}-linuxltfs
mkdir build-%{_target_cpu}-linuxltfs ; cd build-%{_target_cpu}-linuxltfs
GCC=gcc
BuildFlags=`cat ../BuildFlags`
AddOns=`cat ../AddOns`
EnableKernel="--enable-kernel=%{enablekernelltfs} --disable-profile"
Pthreads=linuxthreads
SubDir=i686
%ifarch %{withtlsarches}
WithTls="--with-tls --without-__thread"
%else
WithTls="--without-tls --without-__thread"
%endif
CC="$GCC" CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
	--enable-add-ons=$Pthreads,$AddOns --without-cvs $EnableKernel \
	--with-headers=%{_prefix}/include \
	$WithTls --build %{_target_cpu}-redhat-linux --host %{_target_cpu}-redhat-linux
make -j$numprocs -r CFLAGS="$BuildFlags -g -O3" PARALLELMFLAGS=-s
mkdir -p $RPM_BUILD_ROOT/lib/$SubDir/
cp -a libc.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libc-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libc-*.so` $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libc.so.*`
cp -a math/libm.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libm-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libm-*.so` $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libm.so.*`
cp -a $Pthreads/libpthread.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libpthread-*.so`
pushd $RPM_BUILD_ROOT/lib/$SubDir
ln -sf libpthread-*.so `basename $RPM_BUILD_ROOT/lib/libpthread.so.*`
strip -R .comment $RPM_BUILD_ROOT/lib/{libc,libm}-*.so
strip -g -R .comment $RPM_BUILD_ROOT/lib/libpthread-*.so
popd

mkdir sed
cd sed
CFLAGS="$BuildFlags -g -O2" ../../redhat/sed-3.02/configure
make -j$numprocs
cd ..
cd ..
%endif

%ifarch %{nptlarches}
rm -rf build-%{_target_cpu}-linuxnptl
mkdir build-%{_target_cpu}-linuxnptl ; cd build-%{_target_cpu}-linuxnptl
GCC=gcc
BuildFlags=`cat ../BuildFlags`
AddOns=`cat ../AddOns`
EnableKernel="--enable-kernel=%{enablekernelnptl} --disable-profile"
Pthreads=nptl
WithTls="--with-tls --with-__thread"
SubDir=tls
CC="$GCC" CFLAGS="$BuildFlags -g -O3" ../configure --prefix=%{_prefix} \
	--enable-add-ons=$Pthreads$AddOns --without-cvs $EnableKernel \
	--with-headers=%{_prefix}/include \
	$WithTls --build %{_target_cpu}-redhat-linux --host %{_target_cpu}-redhat-linux
make -j$numprocs -r CFLAGS="$BuildFlags -g -O3" PARALLELMFLAGS=-s
mkdir -p $RPM_BUILD_ROOT/lib/$SubDir/
cp -a libc.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libc-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libc-*.so` $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libc.so.*`
cp -a math/libm.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libm-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libm-*.so` $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libm.so.*`
cp -a $Pthreads/libpthread.so $RPM_BUILD_ROOT/lib/$SubDir/libpthread-`awk '{ print $2 }' ../$Pthreads/Banner`.so
pushd $RPM_BUILD_ROOT/lib/$SubDir
ln -sf libpthread-*.so `basename $RPM_BUILD_ROOT/lib/libpthread.so.*`
popd

cp -a ${Pthreads}_db/libthread_db.so $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libthread_db-*.so`
ln -sf `basename $RPM_BUILD_ROOT/lib/libthread_db-*.so` $RPM_BUILD_ROOT/lib/$SubDir/`basename $RPM_BUILD_ROOT/lib/libthread_db.so.*`
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}/nptl
cp -a libc.a nptl/libpthread.a nptl/libpthread_nonshared.a \
  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/nptl/
sed "s| /lib/| /lib/$SubDir/|" $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libc.so \
  > $RPM_BUILD_ROOT%{_prefix}/%{_lib}/nptl/libc.so
sed "s|^GROUP (.*)|GROUP ( /lib/$SubDir/"`basename $RPM_BUILD_ROOT/lib/libpthread.so.*`' %{_prefix}/%{_lib}/nptl/libpthread_nonshared.a )|' \
  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libc.so \
  > $RPM_BUILD_ROOT%{_prefix}/%{_lib}/nptl/libpthread.so
strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/nptl/*.a
mkdir -p $RPM_BUILD_ROOT/nptl $RPM_BUILD_ROOT%{_prefix}/include/nptl
make -j1 install_root=$RPM_BUILD_ROOT/nptl install-headers PARALLELMFLAGS=-s
pushd $RPM_BUILD_ROOT/nptl%{_prefix}/include
  for i in `find . -type f`; do
    if ! [ -f $RPM_BUILD_ROOT%{_prefix}/include/$i ] \
       || ! cmp -s $i $RPM_BUILD_ROOT%{_prefix}/include/$i; then
      mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/nptl/`dirname $i`
      cp -a $i $RPM_BUILD_ROOT%{_prefix}/include/nptl/$i
    fi
  done
popd
rm -rf $RPM_BUILD_ROOT/nptl

mkdir sed
cd sed
CFLAGS="$BuildFlags -g -O2" ../../redhat/sed-3.02/configure
make -j$numprocs
cd ..
cd ..
%endif

# compatibility hack: this locale has vanished from glibc, but some other
# programs are still using it. Normally we would handle it in the %pre
# section but with glibc that is simply not an option
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/locale/ru_RU/LC_MESSAGES

# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*
%ifnarch %{ix86} alpha alphaev6 sparc sparcv9
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
    if [ "$i" = libc.so -o "$i" = libpthread.so ]; then
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
> prelink.conf
# For now disable prelinking of ld.so, as it breaks statically linked
# binaries built against non-NDEBUG old glibcs (assert unknown dynamic tag)
# /usr/sbin/prelink -c ./prelink.conf -C ./prelink.cache \
#  --mmap-region-start=0x40000000 $RPM_BUILD_ROOT/%{_lib}/ld-*.so
/usr/sbin/prelink --reloc-only=0x42000000 $RPM_BUILD_ROOT/%{_lib}/$SubDir/libc-*.so
%endif
%ifarch alpha alphaev6
# Prelink ld.so and libc.so
> prelink.conf
# For now disable prelinking of ld.so, as it breaks statically linked
# binaries built against non-NDEBUG old glibcs (assert unknown dynamic tag)
# /usr/sbin/prelink -c ./prelink.conf -C ./prelink.cache \
# --mmap-region-start=0x0000020000000000 $RPM_BUILD_ROOT/%{_lib}/ld-*.so
/usr/sbin/prelink --reloc-only=0x0000020010000000 $RPM_BUILD_ROOT/%{_lib}/$SubDir/libc-*.so
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
	    -e '/%{_lib}\/debug/d' > rpm.filelist.in
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
	grep -v %{_prefix}/include/nptl |
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
	grep -v '%{_prefix}/%{_lib}/nptl' |
	grep -v '%{_mandir}' | 
	grep -v 'nscd' > rpm.filelist

grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/lib/locale' < rpm.filelist >> common.filelist
grep '%{_prefix}/libexec' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist >> common.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/bin' < rpm.filelist.full |
	grep -v '%{_prefix}/lib/locale' |
	grep -v '%{_prefix}/libexec' | 
	grep -v '%{_prefix}/sbin/[^gi]' |
	grep -v '%{_prefix}/share' > rpm.filelist

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
echo '%{_prefix}/sbin/nscd' > nscd.filelist

cat > utils.filelist <<EOF
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

# /etc/localtime - we're proud of our timezone
rm -f $RPM_BUILD_ROOT/etc/localtime
cp -f $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime
#ln -sf ..%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime

cd redhat
gcc -Os -static -o build-locale-archive build-locale-archive.c \
  ../build-%{_target_cpu}-linux/locale/locarchive.o \
  ../build-%{_target_cpu}-linux/locale/md5.o \
  -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
  -L../build-%{_target_cpu}-linux
install -m 700 build-locale-archive $RPM_BUILD_ROOT/usr/sbin/build-locale-archive
cd ..

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

%ifarch s390x
# Compatibility symlink
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/lib/ld64.so.1
%endif

echo ====================TESTING=========================
cd build-%{_target_cpu}-linux
make -j$numprocs -k check PARALLELMFLAGS=-s || :
make -j$numprocs -C sed check || :
cd ..
%ifarch i686 athlon
echo ====================TESTING LINUXTHREADS FS=========
cd build-%{_target_cpu}-linuxltfs
make -j$numprocs -k check PARALLELMFLAGS=-s || :
make -j$numprocs -C sed check || :
cd ..
%endif
%ifarch %{nptlarches}
echo ====================TESTING NPTL====================
cd build-%{_target_cpu}-linuxnptl
make -j$numprocs -k check PARALLELMFLAGS=-s || :
make -j$numprocs -C sed check || :
cd ..
%endif
echo ====================TESTING END=====================

%post -p /usr/sbin/glibc_post_upgrade

%postun -p /sbin/ldconfig

%post common -p /usr/sbin/build-locale-archive

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
/usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
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
%ifarch %{nptlarches}
%dir /lib/tls
%endif
%ifarch i686 athlon
%dir /lib/i686
%endif
%ifarch s390x
%dir /lib
/lib/ld64.so.1
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB README.libm LICENSES
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

%files -f utils.filelist utils
%defattr(-,root,root)

%files debug-static
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/debug
%{_prefix}/%{_lib}/debug/*.a

%files -f nscd.filelist -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%config /etc/rc.d/init.d/nscd
%endif

%ifarch %{nptlarches}
%files -n nptl-devel
%defattr(-,root,root)
%{_prefix}/include/nptl
%{_prefix}/%{_lib}/nptl
%endif

%changelog
* Wed Nov  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.8
- fix ftw fd leak

* Wed Nov  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.7
- fix linuxthreads sigaction (#108634)
- fix uselocale (LC_GLOBAL_LOCALE)
- fix sprof (#103727)
- prevent dlopening of executables
- fix glob with GLOB_BRACE and without GLOB_NOESCAPE
- fix locale printing of word values on 64-bit big-endian arches
  (#107846)
- fix getnameinfo and getaddrinfo with reverse IPv6 lookups
  (#101261)
- add pthread_cond_timedwait stubs to libc.so (#102709)
- fix getgrouplist (#101691)
- avoid nscd lockups when using LDAP (#54697)
- fix Ukrainian collation (#83973)
- fix perror (#85994)
- allow whitespace in ld.so.conf (#86032)
- fix strxfrm (#88409)
- fix LC_CTIME localedef creation (#88978)
- fix getaddrinfo memory leaks (#89448)
- fix stdio glibc 2.0 compatibility (#90077)
- fix __cxa_finalize (#90301)
- fix sprintf (#90987)
- fix seteuid/setegid (#91567)
- search system library directories in ldconfig after ld.so.conf defined
  ones (#98966)
- avoid segfaults when "upgrading" from i686 to i386 rpm (#88456)
- issue warning about broken binaries using errno/h_errno on stderr,
  not stdout (#97814)
- fix pause, close and fsync cancel type restoring (#105348)
- fix important hwcaps computation

* Mon Apr  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.6
- fix register_printf_function (#88052)
- fix double free with fopen using ccs= (#88056)
- fix potential access below $esp in {set,swap}context (#88093)
- fix buffer underrun in gencat -H (#88099)
- avoid using unitialized variable in tst-tgmath (#88101)
- fix gammal (#88104)
- fix iconv -c
- fix xdr_string (PR libc/4999)

* Sat Apr  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.5
- make sure all calls to __errno_location() and __h_errno_location()
  jump through .plt to make older wine happy
- fix linuxthreads confstr (_CS_GNU_LIBPTHREAD_VERSION, ...)

* Wed Apr  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.4
- pthread_mutex_lock etc. should not be cancellation points (#87656)
- add pthread_atfork to libpthread.a
- only strip debug info not .symtab/.strtab in /lib/libpthread-*.so

* Fri Mar 28 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.3
- if in __i686__ build "" AT_PLATFORM is seen, assume "i686".

* Wed Mar 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80.1
- backout a hwcap fix to work around a kernel bug with AT_PLATFORM (#86359)
- execute service sshd condrestart in glibc %%post if not inside
  chroot and initscripts, sshd and bash are already installed (#86339);
  restarting of all other applications is on the user (easiest is reboot
  or telinit 1; telinit 5, but this cannot be done from glibc %%post).
- put __ctype_b etc. back into libc.a for the errata (#86465)
- export __fork@GLIBC_2.0 from libc.so.6 again (#86437, #86468)
- fix uid32/gid32 support in LD_ASSUME_KERNEL=2.2.5 libc (#86534)
- build glibc-compat and c_stubs add-ons, for glibc 2.0 compatibility

* Wed Mar 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4.80
- build as 8.0 errata
  - turn compatibility only symbols which are referenced in libc.so's
    relocations back into @@ symvers, as otherwise statically linked
    RHL 8 apps segfault when doing NSS or iconv
  - move __libc_fork, __libc_stack_end, __libc_wait and __libc_waitpid
    from GLIBC_PRIVATE symver for the errata
  - remove {INIT,PREINIT,FINI}_ARRAY support, since it requires
    binutils changes
  - don't build NPTL libraries
  - strip libraries and binaries, recreate glibc-debug-static
    subpackage

* Wed Mar 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-10
- update from CVS

* Tue Mar 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-9
- update from CVS
- fix glibc-debug description (#85111)
- make librt.so a symlink again, not linker script

* Tue Mar  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-8
- update from CVS
- remove the workarounds for broken software accessing GLIBC_PRIVATE
  symbols

* Mon Mar  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-7
- update from CVS

* Sun Mar  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-6
- fix TLS IE/LE model handling in dlopened libraries
  on TCB_AT_TP arches

* Thu Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-5
- update from CVS

* Tue Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4
- update from CVS

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-3
- update from CVS
- only warn about errno, h_errno or _res for binaries, never
  libraries
- rebuilt with gcc-3.2.2-4 to use direct %gs TLS access insn sequences

* Sun Feb 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-2
- update from CVS

* Sat Feb 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-1
- update from CVS

* Thu Feb 20 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-51
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-50
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-49
- update from CVS
- remove nisplus and nis from the default nsswitch.conf (#67401, #9952)

* Tue Feb 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-48
- update from CVS

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-47
- update from CVS

* Fri Feb 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-46
- update from CVS
  - pthread_cond* NPTL fixes, new NPTL testcases

* Thu Feb 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-45
- update from CVS
- include also linuxthreads FLOATING_STACKS libs on i686 and athlon:
  LD_ASSUME_KERNEL=2.2.5 to LD_ASSUME_KERNEL=2.4.0 is non-FLOATING_STACKS lt,
  LD_ASSUME_KERNEL=2.4.1 to LD_ASSUME_KERNEL=2.4.19 is FLOATING_STACKS lt,
  later is NPTL
- enable TLS on alpha/alphaev6
- add BuildPreReq: /usr/bin/readlink

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-44
- update from CVS
  - pthread_once fix

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-43
- update from CVS
- vfork fix on s390
- rebuilt with binutils 2.13.90.0.18-5 so that accesses to errno
  don't bind locally (#83325)

* Thu Feb 06 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-42
- update from CVS
- fix pthread_create after vfork+exec in linuxthreads

* Wed Feb 05 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-41
- update from CVS

* Thu Jan 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-40
- update from CVS

* Wed Jan 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-39
- update from CVS
- enable TLS on s390{,x} and sparc{,v9}

* Fri Jan 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-38
- update from CVS
- initialize __environ in glibc_post_upgrade to empty array,
  so that it is not NULL
- compat symlink for s390x /lib/ld64.so.1
- enable glibc-profile on x86-64
- only include libNoVersion.so on IA-32, Alpha and Sparc 32-bit

* Thu Jan 16 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-37
- update from CVS
  - nscd fixes, *scanf fix
- fix %%nptlarches noarch build (#81909)
- IA-64 TLS fixes

* Tue Jan 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-36
- update from CVS
- rework -debuginfo subpackage, add -debuginfo-common
  subpackage on IA-32, Alpha and Sparc (ie. auxiliary arches)
- fix vfork in libc.a on PPC32, Alpha, Sparc
- fix libio locks in linuxthreads libc.so if libpthread.so
  is dlopened later (#81374)

* Mon Jan 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-35
- update from CVS
  - dlclose bugfixes
- fix NPTL libpthread.a
- fix glibc_post_upgrade on several arches

* Sat Jan 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-34
- update from CVS
- TLS support on IA-64

* Wed Jan  8 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-33
- fix vfork in linuxthreads (#81377, #81363)

* Tue Jan  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-32
- update from CVS
- don't use TLS libs if kernel doesn't set AT_SYSINFO
  (#80921, #81212)
- add ntp_adjtime on alpha (#79996)
- fix nptl_db (#81116)

* Sun Jan  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-31
- update from CVS
- support all architectures again

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-30
- fix condvar compatibility wrappers
- add ugly hack to use non-TLS libs if a binary is seen
  to have errno, h_errno or _res symbols in .dynsym

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-29
- update from CVS
  - fixes for new condvar

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-28
- new NPTL condvar implementation plus related linuxthreads
  symbol versioning updates

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-27
- update from CVS
- fix #include <sys/stat.h> with -D_BSD_SOURCE or without
  feature set macros
- make *sigaction, sigwait and raise the same between
  -lpthread -lc and -lc -lpthread in linuxthreads builds

* Tue Dec 31 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-26
- fix dlclose

* Sun Dec 29 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-25
- enable sysenter by default for now
- fix endless loop in ldconfig

* Sat Dec 28 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-24
- update from CVS

* Fri Dec 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-23
- update from CVS
  - fix ptmalloc_init after clearenv (#80370)

* Sun Dec 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-22
- update from CVS
- add IA-64 back
- move TLS libraries from /lib/i686 to /lib/tls

* Thu Dec 19 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-21
- system(3) fix for linuxthreads
- don't segfault in pthread_attr_init from libc.so
- add cancellation tests from nptl to linuxthreads

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-20
- fix up lists of exported symbols + their versions
  from the libraries

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-19
- fix --with-tls --enable-kernel=2.2.5 libc on IA-32

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-18
- update from CVS
  - fix NPTL hanging mozilla
  - initialize malloc in mALLOPt (fixes problems with squid, #79957)
  - make linuxthreads work with dl_dynamic_weak 0
  - clear dl_dynamic_weak everywhere

* Tue Dec 17 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-17
- update from CVS
  - NPTL socket fixes, flockfile/ftrylockfile/funlockfile fix
  - kill -debug sub-package, rename -debug-static to -debug
  - clear dl_dynamic_weak for NPTL

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-16
- fix <bits/mathinline.h> and <bits/nan.h> for C++
- automatically generate NPTL libpthread wrappers

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-15
- update from CVS
  - all functions which need cancellation should now be cancellable
    both in libpthread.so and libc.so
  - removed @@GLIBC_2.3.2 cancellation wrappers

* Fri Dec 13 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-14
- update from CVS
  - replace __libc_lock_needed@GOTOFF(%ebx) with
    %gs:offsetof(tcbhead_t, multiple_threads)
  - start of new NPTL cancellation wrappers

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-13
- update from CVS
- use inline locks in malloc

* Tue Dec 10 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-12
- update from CVS
  - support LD_ASSUME_KERNEL=2.2.5 in statically linked programs

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-11
- update from CVS
- rebuilt with gcc-3.2.1-2

* Fri Dec  6 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-10
- update from CVS
- non-nptl --with-tls --without-__thread FLOATING_STACKS libpthread
  should work now
- faster libc locking when using nptl
- add OUTPUT_FORMAT to linker scripts
- fix x86_64 sendfile (#79111)

* Wed Dec  4 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-9
- update from CVS
  - RUSCII support (#78906)
- for nptl builds add BuildRequires
- fix byteswap.h for non-gcc (#77689)
- add nptl-devel package

* Tue Dec  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-8
- update from CVS
  - make --enable-kernel=2.2.5 --with-tls --without-__thread
    ld.so load nptl and other --with-__thread libs
- disable nptl by default for now

* Wed Nov 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-7
- update from CVS
- restructured redhat/Makefile and spec, so that src.rpm contains
  glibc-<date>.tar.bz2, glibc-redhat-<date>.tar.bz2 and glibc-redhat.patch
- added nptl

* Fri Nov  8 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-6
- update from CVS
  - even more regex fixes
- run sed testsuite to check glibc regex

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-5
- fix LD_DEBUG=statistics and LD_TRACE_PRELINKING in programs
  using libpthread.so.

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-4
- update from CVS
  - fixed %a and %A in *printf (#75821)
  - fix re_comp memory leaking (#76594)

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-3
- update from CVS
  - some more regex fixes
- fix libpthread.a (#76484)
- fix locale-archive enlarging

* Fri Oct 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-2
- update from CVS
  - don't need to use 128K of stacks for DNS lookups
  - regex fixes
  - updated timezone data e.g. for this year's Brasil DST
    changes
  - expand ${LIB} in RPATH/RUNPATH/dlopen filenames

* Fri Oct 11 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-1
- update to 2.3.1 final
  - support really low thread stack sizes (#74073)
- tzdata update

* Wed Oct  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3-2
- update from CVS
  - handle low stack limits
  - move s390x into */lib64

* Thu Oct  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3-1
- update to 2.3 final
  - fix freopen on libstdc++ <= 2.96 stdin/stdout/stderr (#74800)

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-3
- don't prelink -r libc.so on ppc/x86-64/sparc*, it doesn't
  speed things up, because they are neither REL arches, nor
  ELF_MACHINE_REL_RELATIVE
- fix sparc64 build

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-2
- update from CVS

* Sat Sep 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-1
- update from CVS
- prelink on ppc and x86-64 too
- don't remove ppc memset
- instead of listing on which arches to remove glibc-compat
  list where it should stay

* Fri Sep  6 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-5
- fix wcsmbs functions with invalid character sets (or malloc
  failures)
- make sure __ctype_b etc. compat vars are updated even if
  they are copy relocs in the main program

* Thu Sep  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-4
- fix /lib/libnss1_dns.so.1 (missing __set_h_errno definition
  leading to unresolved __set_h_errno symbol)

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-3
- security fix - increase dns-network.c MAXPACKET to at least
  65536 to avoid buffer overrun. Likewise glibc-compat
  dns-{host,network}.c.

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-2
- temporarily add back __ctype_b, __ctype_tolower and __ctype_toupper to
  libc.a and export them as @@GLIBC_2.0 symbols, not @GLIBC_2.0
  from libc.so - we have still lots of .a libraries referencing
  __ctype_{b,tolower,toupper} out there...

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-1
- update from CVS
  - 2.2.93 release
  - use double instead of single indirection in isXXX macros
  - per-locale wcsmbs conversion state

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-2
- update from CVS
  - fix newlocale/duplocale/uselocale
- disable profile on x86_64 for now

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-1
- update from CVS
  - 2.2.92 release
  - fix gettext after uselocale
  - fix locales in statically linked threaded programs
  - fix NSS

* Thu Aug 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.91-1
- update from CVS
  - 2.2.91 release
  - fix fd leaks in locale-archive reader (#72043)
- handle EROFS in build-locale-archive gracefully (#71665)

* Wed Aug 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-27
- update from CVS
  - fix re_match (#72312)
- support more than 1024 threads

* Fri Aug 23 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-26
- update from CVS
  - fix i386 build

* Thu Aug 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-25
- update from CVS
  - fix locale-archive loading hang on some (non-primary) locales
    (#72122, #71878)
  - fix umount problems with locale-archives when /usr is a separate
    partition (#72043)
- add LICENSES file

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-24
- update from CVS
  - only mmap up to 2MB of locale-archive on 32-bit machines
    initially
  - fix fseek past end + fread segfault with mmaped stdio
- include <sys/debugreg.h> which is mistakenly not included
  in glibc-devel on IA-32

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-23
- don't return normalized locale name in setlocale when using
  locale-archive

* Thu Aug 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-22
- update from CVS
  - optimize for primary system locale
- localedef fixes (#71552, #67705)

* Wed Aug 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-21
- fix path to locale-archive in libc reader
- build locale archive at glibc-common %post time
- export __strtold_internal and __wcstold_internal on Alpha again
- workaround some localedata problems

* Tue Aug 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-20
- update from CVS
- patch out set_thread_area for now

* Fri Aug  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-19
- update from CVS
- GB18030 patch from Yu Shao
- applied Debian patch for getaddrinfo IPv4 vs. IPv6
- fix regcomp (#71039)

* Sun Aug  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-18
- update from CVS
- use /usr/sbin/prelink, not prelink (#70376)

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-17
- update from CVS

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-16
- update from CVS
  - ungetc fix (#69586)
  - fseek errno fix (#69589)
  - change *etrlimit prototypes for C++ (#68588)
- use --without-tls instead of --disable-tls

* Thu Jul 11 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-15
- set nscd user's shell to /sbin/nologin (#68369)
- fix glibc-compat buffer overflows (security)
- buildrequire prelink, don't build glibc's own copy of it (#67567)
- update from CVS
  - regex fix (#67734)
  - fix unused warnings (#67706)
  - fix freopen with mmap stdio (#67552)
  - fix realloc (#68499)

* Tue Jun 25 2002 Bill Nottingham <notting@redhat.com> 2.2.90-14
- update from CVS
  - fix argp on long words
  - update atime in libio

* Sat Jun 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-13
- update from CVS
  - a thread race fix
  - fix readdir on invalid dirp

* Wed Jun 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-12
- update from CVS
  - don't use __thread in headers
- fix system(3) in threaded apps
- update prelink, so that it is possible to prelink -u libc.so.6.1
  on Alpha

* Fri Jun  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-11
- update from CVS
  - fix __moddi3 (#65612, #65695)
  - fix ether_line (#64427)
- fix setvbuf with mmap stdio (#65864)
- --disable-tls for now, waiting for kernel
- avoid duplication of __divtf3 etc. on IA-64
- make sure get*ent_r and _IO_wfile_jumps are exported (#62278)

* Tue May 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-10
- update from CVS
  - fix Alpha pthread bug with gcc 3.1

* Fri Apr 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-35
- fix nice

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
