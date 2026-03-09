Name:      rb-exporter
Version:   %{__version}
Release:   %{__release}%{?dist}
BuildArch: x86_64
Summary:   rb-exporter service to convert traffic to netslow/sflow based on pmacct

License:   AGPL-3.0
URL:       https://github.com/redBorder/rb-exporter
Source0:   %{name}-%{version}.tar.gz

Requires: pmacct arpwatch rsyslog
%{?systemd_requires}

%global debug_package %{nil}

%description
%{summary}

%prep
%autosetup

%build

%install
%__mkdir_p -p %{buildroot}%{_unitdir}
%__install -m 0644 src/systemd/rb-exporter@.service %{buildroot}%{_unitdir}/rb-exporter@.service

%pre
systemctl stop rb-exporter.service >/dev/null 2>&1 || :

systemctl kill rb-exporter.service >/dev/null 2>&1 || :

systemctl disable rb-exporter.service >/dev/null 2>&1 || :

getent group rb-exporter >/dev/null || groupadd -r rb-exporter
getent passwd rb-exporter >/dev/null || useradd -r -g rb-exporter -d /var/lib/rb-exporter -s /sbin/nologin -c "rb-exporter user" rb-exporter

%post
if [ -f %{_unitdir}/rb-exporter.service ]; then
  rm -f %{_unitdir}/rb-exporter.service
fi
%systemd_post rb-exporter@.service

systemctl daemon-reload >/dev/null 2>&1 || :

if [ -d /etc/rb-exporter ]; then
  for d in /etc/rb-exporter/*; do
    [ -d "$d" ] || continue
    iface=$(basename "$d")
    
    if /usr/sbin/ip link show "$iface" >/dev/null 2>&1; then
      systemctl enable --now rb-exporter@"$iface".service >/dev/null 2>&1 || :
    else
      rm -rf "$d"
    fi    
  done
fi

%preun
if [ $1 -eq 0 ]; then
  systemctl stop 'rb-exporter@*' 2>/dev/null || :
  systemctl disable 'rb-exporter@*' 2>/dev/null || :
fi
%systemd_preun rb-exporter@.service

%postun
%systemd_postun_with_restart rb-exporter@.service

%files
%defattr(644,root,root)
/usr/lib/systemd/system/rb-exporter@.service

%doc

%changelog
* Thu Feb 26 2026 Akira García <agarcia@redborder.com>
- Replace legacy SysV init script with systemd-native service
- Align service state with real exporter status
- Fix dead-but-locked and false running states

* Wed Apr 24 2024 David Vanhoucke <dvanhoucke@redborder.com>
- First version of rb-exporter
