%define modname xdiff
%define soname %{modname}.so
%define inifile A64_%{modname}.ini

Summary:	File differences/patches
Name:		php-%{modname}
Version:	1.5.2
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/xdiff
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires:	php-bz2
Requires:	php-hash
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRequires:	libxdiff-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension creates and applies patches to both text and binary files.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS README.API package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-1mdv2012.0
+ Revision: 806419
- 1.5.2

* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-14
+ Revision: 796974
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-13
+ Revision: 761344
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-12
+ Revision: 696489
- rebuilt for php-5.3.8

* Sat Aug 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-11
+ Revision: 695874
- rebuild

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-10
+ Revision: 695490
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-9
+ Revision: 646704
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-8mdv2011.0
+ Revision: 629900
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-7mdv2011.0
+ Revision: 628209
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-6mdv2011.0
+ Revision: 600549
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-5mdv2011.0
+ Revision: 588886
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-4mdv2010.1
+ Revision: 514718
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-3mdv2010.1
+ Revision: 485501
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-2mdv2010.1
+ Revision: 468272
- rebuilt against php-5.3.1

* Mon Oct 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1mdv2010.0
+ Revision: 458154
- 1.5.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-9mdv2010.0
+ Revision: 451375
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.5.0-8mdv2010.0
+ Revision: 397296
- Rebuild

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-7mdv2010.0
+ Revision: 377766
- fix build
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-6mdv2009.1
+ Revision: 346707
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-5mdv2009.1
+ Revision: 341848
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-4mdv2009.1
+ Revision: 323143
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-3mdv2009.1
+ Revision: 310320
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-2mdv2009.0
+ Revision: 238473
- rebuild

* Mon Jul 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-1mdv2009.0
+ Revision: 232377
- 1.5.0

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-4mdv2009.0
+ Revision: 200310
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-3mdv2008.1
+ Revision: 162153
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdv2008.1
+ Revision: 107742
- restart apache if needed

* Tue Sep 04 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdv2008.0
+ Revision: 79410
- Import php-xdiff



* Tue Sep 04 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdv2008.0
- initial Mandriva package
