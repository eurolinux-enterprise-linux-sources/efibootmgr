%define efivar_version 31-1

Summary: EFI Boot Manager
Name: efibootmgr
Version: 15
Release: 2%{?dist}
Group: System Environment/Base
License: GPLv2+
URL: http://github.com/rhinstaller/%{name}/
BuildRequires: git, popt-devel
BuildRequires: efivar-libs >= %{efivar_version}
BuildRequires: efivar-devel >= %{efivar_version}
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXXX)
# EFI/UEFI don't exist on PPC
ExclusiveArch: x86_64 aarch64

# for RHEL / Fedora when efibootmgr was part of the elilo package
Conflicts: elilo <= 3.6-6
Obsoletes: elilo <= 3.6-6

Source0: https://github.com/rhinstaller/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0001: 0001-RHEL-7.x-popt-doesn-t-have-popt.pc-work-around-its-a.patch
Patch0002: 0002-Don-t-build-efibootdump-on-RHEL-7.4.patch
Patch0003: 0003-make_linux_load_option-check-data_size-correctly.patch

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))

%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q
git init
git config user.email "example@example.com"
git config user.name "RHEL Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make %{?_smp_mflags} EXTRA_CFLAGS='%{optflags}' EFIDIR=%{efidir}

%install
rm -rf %{buildroot}
%make_install EFIDIR=%{efidir} libdir=%{_libdir} \
	bindir=%{_bindir} mandir=%{_mandir} localedir=%{_datadir}/locale/ \
	includedir=%{_includedir} libexecdir=%{_libexecdir} \
	datadir=%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/*
%{_mandir}/*/*.?.gz
%doc README

%changelog
* Tue May 09 2017 Peter Jones <pjones@redhat.com> - 15-2
- Fix some coverity issues
  Related: rhbz#1380825

* Mon Mar 13 2017 Peter Jones <pjones@redhat.com> - 15-1
- Update to efivar 15 for fwupdate
  Related: rhbz#1380825

* Tue Jul 19 2016 Peter Jones <pjones@redhat.com> - 0.8.0-10
- Another man page update for Memory Address Range Mirroring
  Related: rhbz#1271412

* Wed Jul 13 2016 Peter Jones <pjones@redhat.com> - 0.8.0-9
- Update man page for Memory Address Range Mirroring
  Related: rhbz#1271412

* Mon Jun 06 2016 Peter Jones <pjones@redhat.com> - - 0.8.0-8
- Add options for Memory Address Range Mirroring
  Resolves: rhbz#1271412

* Thu Jul 09 2015 Peter Jones <pjones@redhat.com> - 0.8.0-7
- Fix a couple of problems parsing command line options QA is seeing.
  Resolves: rhbz#1241411

* Tue Jun 30 2015 Peter Jones <pjones@redhat.com> - 0.8.0-6
- Handle -b and -o parsing in a way that matches the documentation.
  Resolves: rhbz#1174964
- Use the right GUID when setting boot entries active/inactive
  Resolves: rhbz#1221771

* Mon Feb 02 2015 Peter Jones <pjones@redhat.com> - 0.8.0-5
- Fix patch merge error from -4
  Resolves: rhbz#1188313

* Thu Jan 08 2015 Peter Jones <pjones@redhat.com> - 0.8.0-4
- Fix buffer overflow when remove_from_boot_order removes nothing (lennysz)
  Resolves: rhbz#1168019

* Wed Oct 15 2014 Peter Jones <pjones@redhat.com> - 0.8.0-3
- Don't error when BootOrder is unset and we're trying to add to it.
  Related:rhbz#967969

* Wed Sep 10 2014 Peter Jones <pjones@redhat.com> - 0.8.0-2
- Fix some covscan related errors.
  Related: rhbz#1129435

* Fri Sep 05 2014 Peter Jones <pjones@redhat.com> - 0.8.0-1
- Rebase to 0.8.0
  Resolves: rhbz#1129435
