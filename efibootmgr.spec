Summary: EFI Boot Manager
Name: efibootmgr
Version: 0.8.0
Release: 5%{?dist}
Group: System Environment/Base
License: GPLv2+
URL: http://github.com/vathpela/%{name}/
BuildRequires: pciutils-devel, zlib-devel, git
BuildRequires: efivar-libs, efivar-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXXX)
# EFI/UEFI don't exist on PPC
ExclusiveArch: x86_64 aarch64

# for RHEL / Fedora when efibootmgr was part of the elilo package
Conflicts: elilo <= 3.6-6
Obsoletes: elilo <= 3.6-6

Source0: https://github.com/vathpela/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0000: 0001-Make-EFI-redhat-shim.efi-the-default-bootloader-1036.patch
Patch0001: 0001-Fix-a-bad-allocation-size.patch
Patch0002: 0002-Make-the-return-path-something-coverity-can-actually.patch
Patch0003: 0003-Don-t-leak-our-socket-s-fd-when-determining-network-.patch
Patch0004: 0004-Fix-another-leaked-fd.patch
Patch0005: 0005-Fix-some-minor-memory-leaks.patch
Patch0006: 0006-Make-sure-data-created-for-load-options-is-freed.patch
Patch0007: 0007-Fix-an-error-path-not-checking-the-return-right-in-m.patch
Patch0008: 0008-Try-to-avoid-covscan-freaking-out-about-sscanf-with-.patch
Patch0009: 0009-Get-rid-of-an-invalid-comparison.patch
Patch0010: 0010-Covscan-can-t-tell-that-we-re-not-filling-a-buffer.patch
Patch0011: 0011-Don-t-free-something-that-shouldn-t-ever-be-non-NULL.patch
Patch0012: 0012-Don-t-reuse-a-pointer-to-static-data-and-free-condit.patch
Patch0013: 0013-Handle-the-case-where-there-are-no-EFI-variables.patch
Patch0014: 0014-Make-a-free-non-conditional-since-the-condition-can-.patch
Patch0015: 0015-Check-malloc-return.patch
Patch0016: 0016-Check-open-s-return-correctly.patch
Patch0017: 0017-Check-lseek-for-errors.patch
Patch0018: 0018-Don-t-leak-our-partition-table-structures.patch
Patch0019: 0001-Don-t-error-on-unset-BootOrder-when-we-re-trying-to-.patch
Patch0020: 0001-Fix-buffer-overflow-when-remove_from_boot_order-remo.patch
Patch0021: 0001-Make-sure-BootOrder-gets-shortened-while-deleting.patch

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
make %{?_smp_mflags} EXTRA_CFLAGS='%{optflags}'

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_mandir}/man8
install -p --mode 755 src/%{name}/%{name} %{buildroot}%{_sbindir}
gzip -9 -c src/man/man8/%{name}.8 > src/man/man8/%{name}.8.gz
touch -r src/man/man8/%{name}.8 src/man/man8/%{name}.8.gz
install -p --mode 644 src/man/man8/%{name}.8.gz %{buildroot}%{_mandir}/man8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%doc README INSTALL COPYING

%changelog
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
