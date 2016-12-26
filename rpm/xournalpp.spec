Name:      xournalpp
Version:   1.0.1pre
Release:   1%{?dist}
License:   GPLv2
Summary:   Notetaking software designed around a tablet.
Url:       https://github.com/xournalpp/xournalpp
Group:     Applications/Productivity
Source:    %{name}-%{version}.zip
BuildRequires: cmake libglade2-devel texlive-scheme-basic texlive-dvipng glibmm24-devel gtk2-devel gtk+-devel
BuildRequires: boost-devel poppler-glib-devel desktop-file-utils ImageMagick
Requires:  libglade2 texlive-scheme-basic texlive-dvipng glibmm24 gtk2 gtk+ boost poppler-glib poppler-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: xournal

%description
Notetaking software designed around a tablet. A C++ rewrite of Xournal.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

# xournal icons and mime icons
# create 16x16, 32x32, 64x64, 128x128 icons and copy the 48x48 icon
for s in 16 32 48 64 128 ; do
	%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/
	convert -scale ${s}x${s} \
		ui/pixmaps/%{name}.png \
		$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
	%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/mimetypes
	pushd ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${s}x${s}/mimetypes
	%{__ln_s} ../apps/xournalpp.png application-x-xoj.png
	%{__ln_s} application-x-xoj.png gnome-mime-application-x-xoj.png
	popd
done

%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes
%{__mkdir_p} %{buildroot}%{_datadir}/mime/packages
%{__mkdir_p} %{buildroot}%{_datadir}/mimelnk/application

%{__install} -p -m 0644 -D ui/pixmaps/xournalpp.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
%{__install} -p -m 0644 -D ui/pixmaps/xoj.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes
%{__install} -p -m 0644 -D desktop/xournal.xml %{buildroot}%{_datadir}/mime/packages
%{__install} -p -m 0644 -D desktop/x-xoj.desktop %{buildroot}%{_datadir}/mimelnk/application

# Desktop entry
%{__install} -p -m 0644 -D ui/pixmaps/xournalpp.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/xournalpp.png
desktop-file-install \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
	desktop/xournalpp.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files
%defattr(-,root,root)
%doc README.md LICENSE AUTHORS
%{_datadir}/%{name}
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_bindir}/%{name}
%{_bindir}/xournal-thumbnailer
%{_bindir}/mathtex-%{name}.cgi
%{_datadir}/applications/xournalpp.desktop
%{_datadir}/icons/hicolor/scalable/apps/xournalpp.svg
%{_datadir}/icons/hicolor/scalable/mimetypes/xoj.svg
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png
%{_datadir}/icons/hicolor/*x*/mimetypes/application-x-xoj.png
%{_datadir}/icons/hicolor/*x*/mimetypes/gnome-mime-application-x-xoj.png
%{_datadir}/mime/packages/xournal.xml
%{_datadir}/mimelnk/application/x-xoj.desktop
%{_datadir}/pixmaps/xournalpp.png


%changelog
* Mon Dec 26 2016 Andrew Rembrandt <andrew at rembrandt.me.uk> - 1.0.1pre
- Update to 1.0.1pre from github trunk (as of today).
