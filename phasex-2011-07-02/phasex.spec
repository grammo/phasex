%define		desktop_vendor	sysex
%define		phasex_version	dev-m2

%ifarch ix86 i386 i486 i586 i686 athlon geode ia32e
%define		build_32bit	1
%endif
%if 0%{!?build_32bit:1} && 0%{?__isa_bits} == 32
%define		build_32bit	1
%endif


Name:		phasex
Version:	%{phasex_version}
Release:	1
Summary:	PHASEX -- Phase Harmonic Advanced Synthesis EXperiment
Group:		Applications/Multimedia
License:	GPL
URL:		http://disabled.github.com/phasex-dev/

Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	glibc-devel >= 2.3.0
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.99.0
BuildRequires:	libsamplerate-devel >= 0.1.0
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:  lash-devel >= 0.5.4
BuildRequires:	perl
BuildRequires:	desktop-file-utils
Requires:	glibc >= 2.3.0
Requires:	alsa-lib >= 0.9.0
Requires:	jack-audio-connection-kit >= 0.99.0
Requires:	libsamplerate >= 0.1.0
Requires:	gtk2 >= 2.4.0
Requires:	lash >= 0.5.4


%description
PHASEX is an experimental JACK audio / ALSA MIDI softsynth for Linux
with a synth engine built around flexible phase modulation and
flexible oscillator/LFO sourcing.  Modulations include AM, FM, offset
PM, and wave select.  PHASEX comes equipped with a 12db/octave filter
with two distortion curves, a stereo crossover delay and chorus with
phaser, ADSR envelopes for amplifier and filter, realtime audio input
processing capabilities, velocity/aftertouch sensitivity, and more.


%prep
%setup -q


%build
echo _arch=%{_arch} _target_cpu=%{_target_cpu} _build_arch=%{_build_arch}
aclocal && autoconf && automake && autoheader
%configure %{?build_32bit:--enable-32bit} --enable-arch=%{_target_cpu} CFLAGS=''
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

for s in 16 22 32 48 ; do
	%{__mkdir} -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
	%{__cp} %{buildroot}%{_datadir}/phasex/pixmaps/phasex-icon-${s}x${s}.png \
		%{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/phasex-icon.png
done

BASE="Application AudioVideo Audio"
XTRA="X-Jack X-MIDI X-Synthesis X-Digital_Processing"

%{__mkdir} -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor %{desktop_vendor} \
	--dir %{buildroot}%{_datadir}/applications \
	`for c in ${BASE} ${XTRA} ; do echo "--add-category $c " ; done` \
	$RPM_BUILD_ROOT%{_datadir}/phasex/%{name}.desktop
rm $RPM_BUILD_ROOT%{_datadir}/phasex/%{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README INSTALL LICENSE AUTHORS GPL-v2.txt ChangeLog TODO doc/ROADMAP
%{_bindir}/phasex
%dir %{_datadir}/phasex
%dir %{_datadir}/phasex/help
%dir %{_datadir}/phasex/pixmaps
%dir %{_datadir}/phasex/sys-midimaps
%dir %{_datadir}/phasex/sys-patches
%dir %{_datadir}/phasex/sys-samples
%dir %{_datadir}/themes/Phasex-Dark
%dir %{_datadir}/themes/Phasex-Light
%{_datadir}/phasex/patchbank
%{_datadir}/phasex/gtkenginerc
%{_datadir}/phasex/help/*
%{_datadir}/phasex/pixmaps/*
%{_datadir}/phasex/sys-midimaps/*
%{_datadir}/phasex/sys-patches/*
%{_datadir}/phasex/sys-samples/*
%{_datadir}/themes/Phasex-Dark/*
%{_datadir}/themes/Phasex-Light/*
%{_datadir}/applications/%{desktop_vendor}-phasex.desktop
%{_datadir}/icons/hicolor/*/apps/phasex-icon.png



%changelog
* Fri Aug 27 2010 Anton Kormakov <assault64@gmail.com> - Milestone 1
- Bugfixes
- LASH support
- Panic button

* Mon Sep 21 2009 William Weston <weston@sysex.net> - 0.12.0-0pre1
- Added 32-bit detection for cross-arch builds.
- Fixed beta versioning handling.
- Updated categories for desktop file install.
- Removed use of RPM_OPT_FLAGS (phasex handles its own optimizations).

* Mon Sep 14 2009 William Weston <weston@sysex.net> - 0.12.0-0beta4
- Update files section to include new Dark and Light themes.

* Mon May 18 2009 William Weston <weston@sysex.net> - 0.12.0-0beta2
- Updated beta version macro system for 0.12.0-0beta2.
- Fixed case typo in ChangeLog filename.

* Thu Jan 29 2009 William Weston <weston@sysex.net> - 0.12.0-0beta
- Updated for 0.12.0.
- Added libsamplerate dependency.
- Added beta versioning macro.

* Wed Sep  3 2008 William Weston <weston@sysex.net> - 0.11.2-0
- Updated for 0.11.2.

* Tue Aug  7 2007 William Weston <weston@sysex.net> - 0.11.0-0
- Updated for 0.11.0.

* Thu May 24 2007 William Weston <weston@sysex.net> - 0.10.3-0
- Updated for 0.10.3.

* Tue May 15 2007 William Weston <weston@sysex.net> - 0.10.2-0
- Updated for 0.10.2.

* Thu May  3 2007 William Weston <weston@sysex.net> - 0.10.1-0
- Added README and COPYING to doc install.
- Updated for 0.10.1.

* Tue May  1 2007 William Weston <weston@sysex.net> - 0.10.0-0
- Initial RPM spec file.
