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
%__mkdir_p -p %{buildroot}/usr/lib/systemd/system
%__install -m 0644 src/systemd/rb-exporter.service %{buildroot}/usr/lib/systemd/system/rb-exporter.service

%__mkdir_p -p %{buildroot}%{_initrddir}
%__install -m 0755 src/systemd/rb-exporter-start %{buildroot}%{_initrddir}/rb-exporter-start
%__install -m 0755 src/systemd/rb-exporter-stop %{buildroot}%{_initrddir}/rb-exporter-stop
%__install -m 0755 src/systemd/rb-exporter-has-config %{buildroot}%{_initrddir}/rb-exporter-has-config

%pre
getent group rb-exporter >/dev/null || groupadd -r rb-exporter
getent passwd rb-exporter >/dev/null || useradd -r -g rb-exporter -d /var/lib/rb-exporter -s /sbin/nologin -c "rb-exporter user" rb-exporter
pkill -TERM pmacctd >/dev/null 2>&1 || true

%post
if [ -f /etc/rc.d/init.d/rb-exporter ]; then
  rm -f /etc/rc.d/init.d/rb-exporter
fi

systemctl daemon-reload >/dev/null 2>&1 || true
systemctl reset-failed rb-exporter >/dev/null 2>&1 || true

%postun
if [ $1 -eq 0 ]; then
  systemctl daemon-reload >/dev/null 2>&1 || true
fi

%preun
if [ $1 -eq 0 ]; then
  systemctl stop rb-exporter >/dev/null 2>&1 || true
fi

%files
%defattr(755,root,root)
%{_initrddir}/rb-exporter-start
%{_initrddir}/rb-exporter-stop
%{_initrddir}/rb-exporter-has-config
%defattr(644,root,root)
/usr/lib/systemd/system/rb-exporter.service

%doc README.md LICENSE

%changelog
* Thu Jan 29 2026 Akira García <agarcia@redborder.com>
- Replace legacy SysV init script with systemd-native service
- Align service state with real exporter status
- Fix dead-but-locked and false running states

* Wed Apr 24 2024 David Vanhoucke <dvanhoucke@redborder.com>
- First version of rb-exporter