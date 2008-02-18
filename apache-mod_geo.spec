#Module-Specific definitions
%define mod_name mod_geo
%define mod_conf A10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.0.1
Release:	%mkrel 6
Group:		System/Servers
License:	Apache License
URL:		http://www.lexa.ru/programs/mod-geo.html
Source0: 	ftp://ftp.lexa.ru/pub/apache-rus/contrib/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Source2:	README_en.html.bz2
Patch0:		mod_geo-1.3.0-register.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The module is intended for definition of geography of the user of
the WWW-server and transfer of geography to caused script/dynamic
pages as additional argument of search. It can be useful, if
depending on region different contents of reciprocal page are
formed, we shall tell different advertising or different links to
Internets - shops (for example, American for US/CA, European for
the others).

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0 -b .register

bzcat %{SOURCE2} > README_en.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

# fix naming...
perl -p -i -e "s|geo2|geo|g" %{mod_name}2.c
mv %{mod_name}2.c %{mod_name}.c

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_sysconfdir}/httpd/2.0/conf

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

install -m644 country-codes.txt %{buildroot}%{_sysconfdir}/httpd/2.0/conf/mod_geo-country-codes.txt
install -m644 ipranges.2002-01-10 %{buildroot}%{_sysconfdir}/httpd/2.0/conf/mod_geo-ipranges.2002-01-10

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README* libpatricia.copyright
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/2.0/conf/mod_geo-country-codes.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/2.0/conf/mod_geo-ipranges.2002-01-10
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


