Name:           cglib
Version:        3.1
Release:        9%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0 and BSD
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.jar
Source1:        https://repo1.maven.org/maven2/cglib/cglib/%{version}/cglib-%{version}.pom
Source2:        bnd.properties

BuildRequires:  ant
BuildRequires:  javapackages-local
BuildRequires:  objectweb-asm
BuildRequires:  unzip
BuildRequires:  aqute-bnd
BuildArch:      noarch

%description
cglib is a powerful, high performance and quality code generation library
for Java. It is used to extend Java classes and implements interfaces
at run-time.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -c %{name}-%{version}
cp -p %{SOURCE1} pom.xml

rm lib/*.jar
build-jar-repository -s lib objectweb-asm

# Remove the repackaging step that includes other jars into the final thing
sed -i "/<taskdef name=.jarjar/,/<.jarjar>/d" build.xml
sed -i '/doctitle/a additionalparam="-Xdoclint:none"' build.xml

%pom_xpath_remove "pom:dependency[pom:artifactId = 'asm-util']/pom:optional"
%pom_xpath_set "pom:dependency[pom:groupId = 'ant']/pom:groupId" "org.apache.ant"

%mvn_file :cglib cglib
%mvn_alias :cglib "net.sf.cglib:cglib" "cglib:cglib-full" "cglib:cglib-nodep" "org.sonatype.sisu.inject:cglib"

%build
ant jar javadoc
# Convert to OSGi bundle
bnd wrap --output dist/cglib-%{version}.bar --properties %{SOURCE2} \
         --version %{version} dist/cglib-%{version}.jar

mv dist/cglib-%{version}.bar dist/cglib-%{version}.jar
%mvn_artifact pom.xml dist/cglib-%{version}.jar

%install
%mvn_install -J docs

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Feb 18 2016 Mat Booth <mat.booth@redhat.com> - 3.1-9
- Modernise spec file

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 09 2015 Michael Simacek <msimacek@redhat.com> - 3.1-7
- Update bnd invocation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-5
- Add alias for cglib:cglib-nodep

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Update to upstream version 3.1
- Remove patch for upstream bug 44 (fixed upstream)

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-1
- Update to upstream version 3.0
- Add alias for org.sonatype.sisu.inject:cglib

* Mon Aug 05 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.2-17
- Remove old call to %%add_to_maven_depmap macro.
- Fixes RHBZ#992051.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-14
- Add additional maven depmap

* Mon Sep 17 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2-13
- Use aqute bnd in order to generate OSGi metadata.

* Fri Aug 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-12
- Add additional depmap

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-11
- Fix license tag
- Install LICENSE and NOTICE with javadoc package
- Convert versioned JARs to unversioned
- Preserve timestamp of POM file
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
