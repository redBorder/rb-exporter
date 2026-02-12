Name:      rb-exporter
Version:   %{__version}
Release:   %{__release}%{?dist}
BuildArch: x86_64
Summary:   rb-exporter service to convert traffic to netslow/sflow based on pmacct

License:   AGPL-3.0
URL:       https://github.com/redBorder/rb-exporter
Source0:   %{name}-%{version}.tar.gz

Requires: pmacct arpwatch rsyslog

%global debug_package %{nil}

%description
%{summary}

%prep
%autosetup

%build

%install
%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_initrddir}
%__mkdir_p -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
%__install -p -m 0755 src/systemd/rb-exporter $RPM_BUILD_ROOT%{_initrddir}
%__install -p -m 0644 src/systemd/rb-exporter.service $RPM_BUILD_ROOT/usr/lib/systemd/system

%pre
getent group rb-exporter >/dev/null || groupadd -r rb-exporter
getent passwd rb-exporter >/dev/null || useradd -r -g rb-exporter -d /var/lib/rb-exporter -s /sbin/nologin -c "rb-exporter user" rb-exporter

%post
systemctl daemon-reload

%files
%defattr(755,root,root)
%{_initrddir}/rb-exporter
%defattr(644,root,root)
/usr/lib/systemd/system/rb-exporter.service

%doc

%changelog
* Wed Apr 24 2024 David Vanhoucke <dvanhoucke@redborder.com>
- First version of rb-exporter

