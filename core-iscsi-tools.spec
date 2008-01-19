%define		core_ver	3.5
%define		isns_ver	1.8
Summary:	iSCSI initiator tools
Summary(pl.UTF-8):	Narzędzia do inicjatora iSCSI
Name:		core-iscsi-tools
Version:	%{core_ver}
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/storage/iscsi/%{name}-v%{version}.tar.bz2
# Source0-md5:	73bdf5b504fc594ceb02bf879d72988d
Patch0:		%{name}-make.patch
URL:		http://linux-iscsi.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iSCSI initiator tools.

%description -l pl.UTF-8
Narzędzia do inicjatora iSCSI.

%package -n isnsclient-common
Summary:	iSNS Client Toolkit - common tools
Summary(pl.UTF-8):	Wspólne narzędzia klienckie iSNS
Version:	%{isns_ver}
Group:		Applications/System

%description -n isnsclient-common
iSNS Client Toolkit - common tools.

%description -n isnsclient-common -l pl.UTF-8
Wspólne narzędzia klienckie iSNS.

%package -n isnsclient-initiator
Summary:	iSNS Client Toolkit for iSCSI Initiator
Summary(pl.UTF-8):	Narzędzia klienckie iSNS dla inicjatora iSCSI
Version:	%{isns_ver}
Group:		Applications/System
Requires:	isnsclient-common = %{isns_ver}-%{release}

%description -n isnsclient-initiator
iSNS Client Toolkit for iSCSI Initiator.

%description -n isnsclient-initiator -l pl.UTF-8
Narzędzia klienckie iSNS dla inicjatora iSCSI.

%package -n isnsclient-target
Summary:	iSNS Client Toolkit for iSCSI Target
Summary(pl.UTF-8):	Narzędzia klienckie iSNS dla obiektu iSCSI
Version:	%{isns_ver}
Group:		Applications/System
Requires:	isnsclient-common = %{isns_ver}-%{release}

%description -n isnsclient-target
iSNS Client Toolkit for iSCSI Target.

%description -n isnsclient-target -l pl.UTF-8
Narzędzia klienckie iSNS dla obiektu iSCSI.

%prep
%setup -q -n %{name}-v%{core_ver}
%patch0 -p1

mv isnsclient-v%{isns_ver}/{"iSNS License.txt",iSNS_License.txt}

%build
%{__make} -C core-iscsi \
	CC="%{__cc}" \
	AUTHFLAGS="%{rpmcflags} -Wall -Iinclude" \
	DEBUGFLAGS="%{rpmcflags}"

%{__make} -C isnsclient-v%{isns_ver} \
	CC="%{__cc} %{rpmcflags}"
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{1,5}}

%{__make} -C core-iscsi initiator_install \
	DESTDIR=$RPM_BUILD_ROOT

cd isnsclient-v%{isns_ver}
install -d $RPM_BUILD_ROOT/var/spool/isns
install isnsc scripts/* $RPM_BUILD_ROOT/sbin
# TODO: PLDize, add sysconfig files
install sysvinit/redhat.initiator_isns $RPM_BUILD_ROOT/etc/rc.d/init.d/initiator_isns
install sysvinit/redhat.target_isns $RPM_BUILD_ROOT/etc/rc.d/init.d/target_isns

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG HOWTO README RELEASE_NOTES ROADMAP
%attr(755,root,root) /sbin/initiator-authd
%attr(755,root,root) /sbin/initiator-ctl
%attr(755,root,root) /sbin/initiator-iname
%attr(755,root,root) /sbin/iscsi-map-channel
%attr(755,root,root) /sbin/iscsi-remap-channel
%attr(755,root,root) /sbin/iscsi-unmap-channel
%attr(755,root,root) /sbin/iscsi-mount
%attr(755,root,root) /sbin/iscsi-umount
%attr(755,root,root) /sbin/proc.iscsi-map-channel
%attr(755,root,root) /sbin/proc.iscsi-unmap-channel
%attr(755,root,root) /sbin/sysfs.iscsi-map-channel
%attr(755,root,root) /sbin/sysfs.iscsi-unmap-channel
%dir %{_sysconfdir}/iscsi
%attr(755,root,root) %{_sysconfdir}/iscsi/install.channel
%attr(754,root,root) /etc/rc.d/init.d/initiator
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/initiator
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/iscsi_device_maps
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/initiator_auth
%{_mandir}/man1/initiator-ctl.1*
%{_mandir}/man5/initiator.5*
%{_mandir}/man5/initiator_auth.5*
%{_mandir}/man5/iscsi_device_maps.5*

%files -n isnsclient-common
%defattr(644,root,root,755)
%doc isnsclient-v%{isns_ver}/{iSNS_License.txt,scripts_README.txt}
%attr(755,root,root) /sbin/isnsc
%attr(755,root,root) /sbin/isns_register
%attr(755,root,root) /sbin/isns_deregister
%attr(755,root,root) /sbin/isns_reregister
%attr(755,root,root) /sbin/isns_iscsi_index
%attr(755,root,root) /sbin/isns_nodes
%attr(755,root,root) /sbin/isns_network_portals
#%attr(755,root,root) /sbin/isns_update_portals
%dir /var/spool/isns

%files -n isnsclient-initiator
%defattr(644,root,root,755)
#%attr(755,root,root) /sbin/isns_initiators
%attr(755,root,root) /sbin/isns_register_initiator
%attr(755,root,root) /sbin/isns_deregister_initiator
%attr(755,root,root) /sbin/isns_initiator_node_status
%attr(754,root,root) /etc/rc.d/init.d/initiator_isns

%files -n isnsclient-target
%defattr(644,root,root,755)
#%attr(755,root,root) /sbin/isns_register_target
#%attr(755,root,root) /sbin/isns_deregister_target
#%attr(755,root,root) /sbin/isns_target_node_status
#%attr(755,root,root) /sbin/isns_create_dd
#%attr(755,root,root) /sbin/isns_delete_dd
#%attr(755,root,root) /sbin/isns_add_node_to_dd
#%attr(755,root,root) /sbin/isns_remove_node_from_dd
#%attr(755,root,root) /sbin/isns_list_dd_all
#%attr(755,root,root) /sbin/isns_list_dd_members
#%attr(755,root,root) /sbin/isns_create_dds
#%attr(755,root,root) /sbin/isns_delete_dds
#%attr(755,root,root) /sbin/isns_enable_dds
#%attr(755,root,root) /sbin/isns_disable_dds
#%attr(755,root,root) /sbin/isns_add_dd_to_dds
#%attr(755,root,root) /sbin/isns_remove_dd_from_dds
#%attr(755,root,root) /sbin/isns_list_dds_all
#%attr(755,root,root) /sbin/isns_list_dds_members
#%attr(755,root,root) /sbin/isns_is_control_node
%attr(755,root,root) /sbin/isns_is_node_registered
#%attr(755,root,root) /sbin/isns_list_node_detail
#%attr(755,root,root) /sbin/isns_list_nodes_all
#%attr(755,root,root) /sbin/isns_save_config
%attr(754,root,root) /etc/rc.d/init.d/target_isns
