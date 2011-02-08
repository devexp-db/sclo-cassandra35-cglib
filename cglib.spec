Name:           cglib
Version:        2.2
Release:        8%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0
Group:          Development/Tools
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.jar
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
# Remove the repackaging step that includes other jars into the final thing
Patch0:         %{name}-build_xml.patch

Requires: java >= 0:1.6.0
Requires: objectweb-asm

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  objectweb-asm
BuildRequires:  unzip
BuildArch:      noarch
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
cglib is a powerful, high performance and quality code generation library 
for Java. It is used to extend Java classes and implements interfaces 
at runtime.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -c %{name}-%{version}
rm lib/*.jar
%patch0 -p1

%build
export CLASSPATH=`build-classpath objectweb-asm`
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_javadocdir}/
cp -r docs ${RPM_BUILD_ROOT}%{_javadocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{version}.jar  $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap net.sf.cglib %{name} %{version} JPP %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_javadir}/*.jar
%{_mavenpomdir}/*
%config(noreplace) %{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-7
- Add missing pom file (Resolves rhbz#655793)

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2-6
- BR unzip to fix openSUSE build

* Tue Dec  9 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-5
- Add dist to version
- Fix BuildRoot to follow the latest guidelines

* Mon Nov 24 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-4
- Add a comment explaining the patch

* Thu Nov  6 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-3
- Flag Maven depmap as "config"

* Wed Nov  5 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-2
- Explicitly require Java > 1.6 because it won't compile with gcj
- Fix cosmetic issues in spec file

* Tue Nov  4 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-1
- Initial package (based on previous JPP version)
