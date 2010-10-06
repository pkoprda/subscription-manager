Name: subscription-manager      
Version: 0.85
Release: 1%{?dist}
Summary: Supported tools and libraries for subscription and repo Management       
Group:   System Environment/Base         
License: GPLv2 
Source0: %{name}-%{version}.tar.gz
URL:     https://engineering.redhat.com/trac/subscription-manager 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: python-dmidecode
Requires:  python-ethtool 
Requires:  python-simplejson
Requires:  python-iniparse
Requires:  PyXML 
Requires:  python-rhsm
Requires:  yum >= 3.2.19-15
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: unique-devel
BuildRequires: libnotify-devel
BuildRequires: gtk2-devel
BuildRequires: desktop-file-utils


%description
Subscription Manager package provides programs and libraries to allow users 
to manager subscriptions/yumrepos from Red Hat entitlement or deployment 
Platform.

%package -n python-rhsm
Summary: A Python library to communicate with a Red Hat Unified Entitlement Platform
Group: Development/Libraries
Requires: m2crypto
Requires: python-simplejson
BuildArch: noarch

%description -n python-rhsm
A small library for communicating with the REST interface of a Red Hat Unified
Entitlement Platform. This interface is used for the management of system
entitlements, certificates, and access to content.

%package -n subscription-manager-gnome
Summary: A GUI interface to manage Red Hat product subscriptions
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: pygtk2 pygtk2-libglade gnome-python2 gnome-python2-canvas
Requires: usermode-gtk
Requires: subscription-manager

%description -n subscription-manager-gnome
This package contains a GTK+ graphical interface for configuring and 
registering a system with a Red Hat Entitlement platform and manage 
subscriptions.


%prep
%setup -q

%build
make -f Makefile

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT MANPATH=%{_mandir}

desktop-file-validate \
        %{buildroot}/etc/xdg/autostart/rhsm-compliance-icon.desktop
desktop-file-validate \
        %{buildroot}/usr/share/applications/subscription-manager.desktop        

%post -n subscription-manager-gnome
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n subscription-manager-gnome
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n subscription-manager-gnome
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

%dir %{_datadir}/rhsm
%dir %{_datadir}/rhsm/gui
%dir %{_datadir}/rhsm/gui/data
%dir %{_datadir}/rhsm/gui/data/icons
%dir /etc/rhsm/facts
%dir %{_datarootdir}/locale

%{_datadir}/rhsm/__init__.py*
%{_datadir}/rhsm/managercli.py*
%{_datadir}/rhsm/managerlib.py*
%{_datadir}/rhsm/repolib.py*
/usr/lib/yum-plugins/rhsmplugin.py*
/usr/lib/yum-plugins/pidplugin.py*
%{_datadir}/rhsm/certmgr.py*
%{_datadir}/rhsm/certlib.py*
%{_datadir}/rhsm/hwprobe.py*
%{_datadir}/rhsm/constants.py*
%{_datadir}/rhsm/lock.py*
%{_datadir}/rhsm/facts.py*
%{_datadir}/rhsm/factlib.py*
%{_datadir}/rhsm/productid.py*
%{_datarootdir}/locale/*
%attr(755,root,root) %{_sbindir}/subscription-manager-cli
%attr(755,root,root) %dir %{_var}/log/rhsm
%attr(755,root,root) %dir %{_var}/lib/rhsm
%attr(755,root,root) %dir %{_var}/lib/rhsm/facts
%attr(755,root,root) %{_bindir}/rhsmcertd
%attr(755,root,root) %{_sysconfdir}/init.d/rhsmcertd
%attr(755,root,root) %{_libexecdir}/rhsm-complianced

# config files
%attr(644,root,root) /etc/yum/pluginconf.d/rhsmplugin.conf
%attr(644,root,root) /etc/yum/pluginconf.d/pidplugin.conf

%{_sysconfdir}/cron.daily/rhsm-complianced
%{_sysconfdir}/dbus-1/system.d/com.redhat.SubscriptionManager.conf
%{_datadir}/dbus-1/system-services/com.redhat.SubscriptionManager.service

%doc
%{_mandir}/man8/subscription-manager-cli.8*

%files -n subscription-manager-gnome
%dir %{_datadir}/firstboot/modules
%defattr(-,root,root,-)
%{_datadir}/rhsm/gui/__init__.py* 
%{_datadir}/rhsm/gui/factsgui.py*
%{_datadir}/rhsm/gui/managergui.py*  
%{_datadir}/rhsm/gui/messageWindow.py*  
%{_datadir}/rhsm/gui/progress.py* 
%{_datadir}/rhsm/gui/data/factsdialog.glade  
%{_datadir}/rhsm/gui/data/rhsm.glade  
%{_datadir}/rhsm/gui/data/registration.glade
%{_datadir}/rhsm/gui/data/regtoken.glade
%{_datadir}/rhsm/gui/data/subsgui.glade  
%{_datadir}/rhsm/gui/data/progress.glade
%{_datadir}/rhsm/gui/data/icons/subsmgr-empty.png
%{_datadir}/rhsm/gui/data/icons/subsmgr-full.png
%{_datadir}/icons/hicolor/16x16/apps/subsmgr.png
%{_datadir}/firstboot/modules/rhsm_entitlement_choose.py*
%{_datadir}/firstboot/modules/rhsm_login.py*
%{_datadir}/firstboot/modules/rhsm_subscriptions.py*
%{_datadir}/applications/subscription-manager.desktop
%attr(755,root,root) %{_sbindir}/subscription-manager-gui
%attr(755,root,root) %{_bindir}/subscription-manager-gui
%{_bindir}/rhsm-compliance-icon
%{_sysconfdir}/xdg/autostart/rhsm-compliance-icon.desktop
%{_sysconfdir}/pam.d/subscription-manager-gui
%{_sysconfdir}/security/console.apps/subscription-manager-gui

%files -n python-rhsm
%{_datadir}/rhsm/connection.py*
%{_datadir}/rhsm/logutil.py*
%{_datadir}/rhsm/config.py*
%{_datadir}/rhsm/certificate.py*
%config(noreplace) %attr(644,root,root) /etc/rhsm/rhsm.conf
%dir %{_sysconfdir}/rhsm/ca
%{_sysconfdir}/rhsm/ca

%post
chkconfig --add rhsmcertd
# /sbin/service rhsmcertd start

%preun
if [ $1 = 0 ] ; then
   /sbin/service rhsmcertd stop >/dev/null 2>&1
   /sbin/chkconfig --del rhsmcertd
fi

%changelog
* Wed Oct 06 2010 Devan Goodwin <dgoodwin@redhat.com> 0.85-1
- Resolves: #638696,#585193
- Fix broken directory path joining. (dgoodwin@redhat.com)
- Display error messages sent from the server on entitlement bind
  (jbowes@redhat.com)
- Update the config name for the ca cert dir to ca_cert_dir (jbowes@redhat.com)
- clean up a gtk warning about the bad button group (alikins@redhat.com)
- 638696: bugfix 'cli fails silently with wrong server SSL cert'
  (anadathu@redhat.com)
- unregister should delete identity certs if candlepin call is successfull.
  (anadathu@redhat.com)
- some glade reference renaming s/treeview_2/treeview_matching, etc
  (alikins@redhat.com)
- refactor the populate*Subscriptions methods. (alikins@redhat.com)
- 585193: refractor error handling code. (anadathu@redhat.com)

* Tue Oct 05 2010 Devan Goodwin <dgoodwin@redhat.com> 0.84-1
- Resolves: #632612,#640128,#639320,#639491,#637160,#638289
- When re-registering, previously subscribed-to subscriptions are checked 
  by default) (alikins@redhat.com)
- update CA trust chain (jbowes@redhat.com)
- Write identity cert with correct permissions initially. (dgoodwin@redhat.com)
- Check and fix identity cert permissions on every run. (dgoodwin@redhat.com)
- Type in the identity command (bkearney@redhat.com)
- fix for bz#639320 (anadathu@redhat.com)
- Fix segfault when adding subs during firstboot. (dgoodwin@redhat.com)
- 639491: Put register by consumer back in (bkearney@redhat.com)
- Moving re-register to be identity. (bkearney@redhat.com)
- Get firstboot displaying the right subscription screen. (dgoodwin@redhat.com)
- Fix separate subscription window in firstboot. (dgoodwin@redhat.com)
- 637160 - require --all to unsubscribe to unsub all (jbowes@redhat.com)
- merge getAllAvailableSubscriptions and getAvailableEntitlements
  (jbowes@redhat.com)
- getAvailableEntitlementsCLI isn't needed, just call the regular version
  (jbowes@redhat.com)
- remove some code duplication for getting available entitlements/subscriptions
  (jbowes@redhat.com)
- remove unneeded wrapper method (jbowes@redhat.com)
- Move registration status on main UI page. (dgoodwin@redhat.com)
- Handle errors during unregistration. (dgoodwin@redhat.com)
- Add "Activate Subscription" button. (dgoodwin@redhat.com)
- Add unregister button to main screen. (dgoodwin@redhat.com)
- Display UUID on main page of the GUI. (dgoodwin@redhat.com)
- 638289: Fix broken re-register if identity cert doesn't exist.
  (dgoodwin@redhat.com)
- Fix broken list all subscriptions. (dgoodwin@redhat.com)
- Update registration screen to match new mockups. (dgoodwin@redhat.com)
- remove some unused imports (jbowes@redhat.com)
- Add missing imports (jbowes@redhat.com)
- Split registration screens into separate glade files. (dgoodwin@redhat.com)
- Remove duplicate log initialization in connection.py (jbowes@redhat.com)
- Ship the CA chain (jbowes@redhat.com)
- Load CA trust chains from a directory of pem formatted files
  (jbowes@redhat.com)

* Tue Sep 28 2010 Devan Goodwin <dgoodwin@redhat.com> 0.83-1
- Resolves: #617685
- Cleanup authentication logic. (dgoodwin@redhat.com)
- Split out REST lib into seprate rpm. (dgoodwin@redhat.com)
- config: define defaults in the config module (jbowes@redhat.com)
- Start of glade name cleanup. Make glade names per top level.
  (alikins@redhat.com)
- Initial work in adding facts dialog. (jharris@redhat.com)
- Line length fixups in the firstboot module (jbowes@redhat.com)
- 617685: Ensure that the baseurl works with and without trailing slashes.
  (bkearney@redhat.com)
- Use config file for directories to use. (dgoodwin@redhat.com)
- Specify default cert location in default config. (dgoodwin@redhat.com)
- Fix insecure setting comparison. (dgoodwin@redhat.com)
- Refactor to use Python ConfigParser. (dgoodwin@redhat.com)
- Fallback to console logging if we cannot write to /var/log.
  (dgoodwin@redhat.com)

* Wed Sep 22 2010 Devan Goodwin <dgoodwin@redhat.com> 0.80-1
- Resolves: #628589
- Updated I18N strings. (dgoodwin@redhat.com)
- added username & password check for reregister with --consumerid option
  command (dmitri@redhat.com)
- Fix bad translation. (dgoodwin@redhat.com)
- fix for #628589 -removed --consumerid option from register command
  (dmitri@redhat.com)
- 623264: Fix multiple issues with registration. (dgoodwin@redhat.com)

* Tue Sep 21 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.79-1
- Resolves: #631472
- update these screens priorities so we show the management screen first to
  simplify the flow (alikins@redhat.com)
- Have the UEP Connection read the values from the local config file
  (bkearney@redhat.com)
- escape the product name in unsubscribe confirm dialog. (alikins@redhat.com)
- return True from delete_event handlers. fix bz#631472 (alikins@redhat.com)
- 635844:If there is a colossal failure, and no json is returned.. then assume
  it is a network erorr and provide a generic response (bkearney@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- Change the name of the entitlement chooser module to a more vibrant and
  impressive name as to better establish our brand and mark in a challenging
  marketplace. (alikins@redhat.com)

* Tue Sep 21 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.78-1
- Resolves: #631537, #633514
- Only escape strings that need it (aka, product name for now) instead of all
  strings sent to the messageWindow. Escaping all of them broke the formating.
  (alikins@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- change packing on register/close buttons so they display correctly in
  firstboot (alikins@redhat.com)
- Catch locale errors (bkearney@redhat.com)
- Move close button in the subscription token/modify subscription dialog
  (alikins@redhat.com)
- change paths for firstboot modules (alikins@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- Escape text passed to gtk's text markup. (alikins@redhat.com)
- 623448: Added the new config options to the example config file
  (bkearney@redhat.com)
- 596136 ensure that the daemon only runs one time (jbowes@redhat.com)
- Fix up some spec file issues with the local being double listed and the first
  boot stuff not being included (bkearney@redhat.com)
- bugfix for bz#631537 (anadathu@redhat.com)
- rename files firstboot modules (alikins@redhat.com)
- Add an option on the entitlement choose screen for "local"
  (alikins@redhat.com)
- bugfix for bz#633514 (anadathu@redhat.com)
- Change rhms screen priority to match those of rhn. (alikins@redhat.com)
- add chooser screen (alikins@redhat.com)
- start of adding a rhn or rhesus screen (alikins@redhat.com)
- Fix missing gettext import. (dgoodwin@redhat.com)
- fixed a problem with prefix config (dmitri@redhat.com)
- made '/candlepin' prefix configurable as 'prefix' configuration file
  parameter (dmitri@redhat.com)
- Merge branch 'i18n' (dgoodwin@redhat.com)
- Remove the translations used for testing. (dgoodwin@redhat.com)
- Deploy translations to /usr/share/locale/. (dgoodwin@redhat.com)
- Add po/build to gitignore (jbowes@redhat.com)
- Make a seperate update-po makefile target (jbowes@redhat.com)
- glob po files for compile_pos (jbowes@redhat.com)
- Add a menu icon for subscription-manager (bkearney@redhat.com)
- Minor strings update. (dgoodwin@redhat.com)
- Safer generation of glade.h string files. (dgoodwin@redhat.com)
- Add missing translation markers in Python code. (dgoodwin@redhat.com)
- Remove bad glade translatable markers. (dgoodwin@redhat.com)
- We need to import certlib after setting path in include rhsm
  (alikins@redhat.com)
- I18N for compliance icon. (dgoodwin@redhat.com)
- Include Glade strings for translation. (dgoodwin@redhat.com)
- Enable I18N in subscription manager itself. (dgoodwin@redhat.com)
- Compile .po files during install. (dgoodwin@redhat.com)
- Remove (most of) HATEOAS. (dgoodwin@redhat.com)
- 608005: checking for bad html characters on the client (bkearney@redhat.com)
- Handle window manager delete_entry signals. fix bz#631472
  (alikins@redhat.com)
- fix for bz#628070 Do not try to unsubscribe from the server for local
  management (alikins@redhat.com)
- 632019: Remove hyphen from re-register (bkearney@redhat.com)
- 613650: Improved the text a bit (bkearney@redhat.com)
- 632019: Clean up typo in the help message (bkearney@redhat.com)
- Add make target to extract strings for i18n. (dgoodwin@redhat.com)
- bugfix for bz#617703 (anadathu@redhat.com)

* Mon Sep 20 2010 Adrian Likins <alikins@redhat.com>
- names on firstboot modules changed

* Thu Sep 09 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.77-1
- Resolves: #627915
- Update for Candlepin HATEOAS changes. (dgoodwin@redhat.com)
- Comment out logging response from server. bz#627915 (anadathu@redhat.com)

* Wed Sep 08 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.76-1
Resolves: #627681, #616137, #618819, #627707
- bugfix for bz#627681 (anadathu@redhat.com)
- compliance-icon: support warning period notification (jbowes@redhat.com)
- bugfix for bz#618819 (anadathu@redhat.com)
- fix for bz#616137 (anadathu@redhat.com)
- Fix broken exception handling. (dgoodwin@redhat.com)
- Use the write method name when saving facts. fix bz#628679
  (alikins@redhat.com)
- fix for bz#585193 (anadathu@redhat.com)
- Fix  bz #627707 - facts cache not being updated for "update facts now" button
  if the facts file is deleted under it (alikins@redhat.com)
- add /etc/rhsm/facts to makefile (alikins@redhat.com)
- add /etc/rhsm/facts to spec file (alikins@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- 624106 - handle the consumerid properly (jesusr@redhat.com)
- 624106 - add consumerid param to reregister. (jesusr@redhat.com)
- fix for bz#609126 (anadathu@redhat.com)
- bugzilla fix#601848 (anadathu@redhat.com)
- 624816 - unlimited flag unavailable, check quantity for -1.
  (jesusr@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- Change the firstboot ordering (alikins@redhat.com)
- Missing config options for insecure options and ca certs.
  (pkilambi@redhat.com)
- bugfix/enhancement for bugzilla#597210 (anadathu@redhat.com)
- BZ624794: Start using basic auth (bkearney@redhat.com)
- date format did not change. reverting it back to original
  (anadathu@redhat.com)
- Fix format string and added logging to detect failures when running cert-
  daemon (anadathu@redhat.com)
- add user certs in all the places it makes sense (alikins@redhat.com)
- add user/cert based auth for unregister as well. fix bz#624025
  (alikins@redhat.com)
- Remove debug "raise" that was breaking some of the error handling
  (alikins@redhat.com)
- Try to only create the UEP once, and add ssl certs to it when we get them
  (alikins@redhat.com)
- move around where we init the connection object (alikins@redhat.com)
- add my favorite "trace_me" helper method that dumps the stack of where it is
  called from to logutil.py. (alikins@redhat.com)

* Wed Aug 11 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.75-1
- Resolves: #622839, #612250 
- get rid of stray print debug (jbowes@redhat.com)
- missed an instance of create_connection_with_userIdentity
  (alikins@redhat.com)
- remove unneeded printing of consumer id bz#622839 (alikins@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- implement entitlement grace periods (jbowes@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- Adding some firstboot niceties for registration. (jharris@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- Somewhat rough fix for BZ #612250 (jharris@redhat.com)
- Add back some missing atk strings (alikins@redhat.com)
- remove the executable bit from productid.py (jbowes@redhat.com)
- Add bin to gitignore (jbowes@redhat.com)
- Remove unused 'test' file (from repo check) (jbowes@redhat.com)
- s/create_connection_with_userIdentity/create_connection_with_userIdentity
  (alikins@redhat.com)
- remove reference to non existent variable (alikins@redhat.com)
- More moving of ImportCertificate screen dialog around (alikins@redhat.com)
- refactor ImportCertificate screen a bit. (alikins@redhat.com)
- more refactoring (alikins@redhat.com)
- refactor AddSubscriptionScreen.init to be slightly less indented
  (alikins@redhat.com)
- remove unused imports cleanup indention (alikins@redhat.com)
- remove unused "os" import (alikins@redhat.com)
- indention cleanup pylint cleanups (alikins@redhat.com)
- unused variable removed pychecker cleanups (alikins@redhat.com)
- import os here pychecker fix (alikins@redhat.com)
- BZ615357: Can now pass in --all if you are doing list --available
  (root@localhost.localdomain)
- BZ615404 changed the name (bkearney@redhat.com)

* Tue Aug 03 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.74-1
- Resolves: #614015, #613635, #612730
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager (alikins@redhat.com)
- compliance-icon: fix up right click handling (jbowes@redhat.com)
- compliance-icon: call notify_init for older distros (jbowes@redhat.com)
- make add subscriptions dialog a singleton (alikins@redhat.com)
- Making register screen and regtoken screen singletons. (jharris@redhat.com)
- Getting the firstboot screens working again with the common glade file.
  (jharris@redhat.com)
-     Refactoring managergui to use signals for consumer updates.
  (jharris@redhat.com)
- Make the progress dialog for subscribing to channels a little better.
  (alikins@redhat.com)
- Change getMatchedSubscriptions to uniq the list of products based on pool id.
  (alikins@redhat.com)
- Moving firstboot regsiter screen to use common network init method.
  (jharris@redhat.com)
- Tweaking the registration screen. (jharris@redhat.com)
- remove unwanted print statement (anadathu@redhat.com)
- unregister functionality implemented (anadathu@redhat.com)
- Make RegisterScreen run as a dialog (alikins@redhat.com)
- remove redundant connection method (jesusr@redhat.com)
- register client if consumer cert doesn't exist (jesusr@redhat.com)
- fix typo (jesusr@redhat.com)
- remove --regen option from facts, use the reregister command
  (jesusr@redhat.com)
- add reregister command (jesusr@redhat.com)
- add rhms_subscriptions module to spec (alikins@redhat.com)
- remove debug spew (alikins@redhat.com)
- Turn subscriptionToken/status/factupdate/kitchen sink screen back on
  (alikins@redhat.com)
- Several small UI tweaks to register screen. (jharris@redhat.com)
- turn on "subscriptionTokenScreen" again (alikins@redhat.com)
- change the add subscription dialog to "run" so we don't block in it's main
  loop. (alikins@redhat.com)
- refactoring to make firstboot gui work (alikins@redhat.com)
- Merge branch 'firstboot' of git+ssh://axiom.rdu.redhat.com/scm/git
  /subscription-manager into firstboot (alikins@redhat.com)
- abstract more rhsm gui stuff so we can redefine them in firstboot
  (alikins@redhat.com)
- Basically adding documentation. (jharris@redhat.com)
- Merge branch 'firstboot' of git+ssh://axiom.rdu.redhat.com/scm/git
  /subscription-manager into firstboot (alikins@redhat.com)
- Merge branch 'master' of git+ssh://axiom.rdu.redhat.com/scm/git/subscription-
  manager into firstboot (alikins@redhat.com)
- bugfix for connection not using usr credentials after registration.
  (anadathu@redhat.com)
- remove unused code (alikins@redhat.com)
- Merging in master and doing further work on register screen.
  (jharris@redhat.com)
- Getting the basics of the register screen in and working.
  (jharris@redhat.com)
- add the main "rhms_subscriptions" screen. (alikins@redhat.com)
- Disarm "reload" since it causes firstboot ui to freak out.
  (alikins@redhat.com)
- s/rhms_module/rhms_login (alikins@redhat.com)
- reenabled installing rhsm.conf. (alikins@redhat.com)
- create firstboot dirs in make install (alikins@redhat.com)
- add rhms firstboot module to repo (alikins@redhat.com)
- add firstboot modules to spec (alikins@redhat.com)
- install the firstboot modules in make install (alikins@redhat.com)
- Changes to make this module also work as a firstboot screen.
  (alikins@redhat.com)
- force the symlink to console helper. Do not install the config file on make
  install. (alikins@redhat.com)
- Merging in master and doing further work on register screen.
  (jharris@redhat.com)
- insecure mode option moved to rhsm.conf file (anadathu@redhat.com)
- Getting the basics of the register screen in and working.
  (jharris@redhat.com)
- add the main "rhms_subscriptions" screen. (alikins@redhat.com)
- Disarm "reload" since it causes firstboot ui to freak out.
  (alikins@redhat.com)
- s/rhms_module/rhms_login (alikins@redhat.com)
- reenabled installing rhsm.conf. (alikins@redhat.com)
- create firstboot dirs in make install (alikins@redhat.com)
- add rhms firstboot module to repo (alikins@redhat.com)
- add firstboot modules to spec (alikins@redhat.com)
- install the firstboot modules in make install (alikins@redhat.com)
- Changes to make this module also work as a firstboot screen.
  (alikins@redhat.com)
- force the symlink to console helper. Do not install the config file on make
  install. (alikins@redhat.com)
- Create /var/lib/rhsm/facts if it doesn't exist. Fix for bz#613003
  (alikins@redhat.com)
- Always push the facts up if users click "update facts" even if we don't think
  there has been a change. (adrian@alikins.usersys.redhat.com)
- Add a "update facts" button the the "modify registration" screen.
  (adrian@alikins.usersys.redhat.com)
- Merge branch 'master' of git://axiom.rdu.redhat.com/scm/git/subscription-
  manager (adrian@alikins.usersys.redhat.com)
- add "facts --list" and "facts --update" to cli
  (adrian@alikins.usersys.redhat.com)
- add factlib.py to repo (adrian@alikins.usersys.redhat.com)
- Swap OrderNumber and SerialNumber fields for formatting in list --consumed
  (adrian@alikins.usersys.redhat.com)

* Fri Jul 30 2010 Adrian Likins <alikins@redhat.com> 0.74-1
- add rhms_subscriptions firstboot module

* Tue Jul 27 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.73-1
- Resolves: #614015, #613635, #612730
- remove prints, use proper method name (jesusr@redhat.com)
- store the cert (jesusr@redhat.com)
- adding regen identity certs to client (jesusr@redhat.com)
- moving importing of logutils after PYTHONPATH is set (pkilambi@redhat.com)
- fix for bugzilla#607162 (anadathu@redhat.com)
- bugfix for 'connection.UEPConnection' instance. (anadathu@redhat.com)
- renaming the main subscription-manager-gui glade as rhsm
  (pkilambi@redhat.com)
- Show and accept consumer names via the gui (bkearney@redhat.com)
- Show the name in the register page (bkearney@redhat.com)
- Removed setters. Multiple connections not spawned for every execution.
  (anadathu@redhat.com)
- BZ616065: Allow a name to passed into the register command
  (bkearney@redhat.com)
- added exception logging and fix for one bug. (anadathu@redhat.com)
- 614015 - fixing name mismatches (pkilambi@redhat.com)
- 613635 - remove printing cp instance (pkilambi@redhat.com)
- 612730 - fixing typo (pkilambi@redhat.com)
- display error when unregister fails (pkilambi@redhat.com)

* Thu Jul 22 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.72-1
- Resolves: #617303
- BZ613650: Clean up the help text (root@localhost.localdomain)
- Make insecure by default for testing purposes. (anadathu@redhat.com)

* Wed Jul 21 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.71-1
- Resolves: #613003
- Make subscription-manager-gui run as root (jbowes@redhat.com)
- Pass the UUID in the subject, and name in the subjectAlternateName
  (bkearney@redhat.com)
- hook up consolehelper for subscription-manager-gui (jbowes@redhat.com)
- Add compliance notification syslogging/desktop icon (jbowes@redhat.com)
- Make candlepin_ca_file an instance variable (root@localhost.localdomain)
- subscription-manager now checks server's certificate before performing
  further commands (anadathu@redhat.com)
- From: Adrian Likins <alikins@redhat.com> Date: Mon, 12 Jul 2010 15:23:59
  -0400 Subject: [PATCH 7/7] Don't try to use any existing consumer certs for
  registration (anadathu@redhat.com)
- Need to add pidplugin.conf to Makefile. (jortel@redhat.com)
- Daemon not started at install; pidplugin disabled. As per fedora packaging
  guidelines, the rhsm daemon is not started during rpm install.
  (jortel@redhat.com)
- Add product ID (yum) plugin conf. (jortel@redhat.com)
- Add support for alternate root directories. Change the root dir to
  /mnt/sysimage when it exists to support running the product id plugin within
  an Anaconda install. (jortel@redhat.com)
- Add productid plugin. (jortel@redhat.com)
- Remove unnecessary import. (jortel@redhat.com)
- Removing bind by product name. Use pool or reg-token to do future binds
  (pkilambi@redhat.com)

*Wed Jul 21 2010 Adrian Likins <alikins@redhat.com> 0.69-1
- add firstboot modules

* Fri Jul 09 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.68-1
- Resolves: #613003
- putting back accessibility strings overridden by facts commit
  (pkilambi@redhat.com)

* Fri Jul 09 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.67-1
- Resolves: #613003
- Create /var/lib/rhsm/facts if it doesn't exist. Fix for bz#613003
  (alikins@redhat.com)
- New button in gui for refreshing facts - alikins (pkilambi@redhat.com)
- Adding the facts lib (pkilambi@redhat.com)
- First pass at support for supporting updating facts for subscription-manager.
  (pkilambi@redhat.com)
- subscribing to a regnumber was failing (bkearney@redhat.com)

* Thu Jun 24 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.66-1
- Resolves: #589626
- Adding in 'unlimited' quantity support. (jharris@redhat.com)
- Candlepin connection library updates. (dgoodwin@redhat.com)
- Allow the user to sepcify a type at registration (bkearney@redhat.com)
- Force username and password to always be required on register
  (bkearney@redhat.com)
- more alignment changes on reg token screen (pkilambi@redhat.com)
- fxing alignment issues on reg token screen and fix for other tab content
  (pkilambi@redhat.com)
- removing raise (pkilambi@redhat.com)
- fixing unregistered case to load cert import (pkilambi@redhat.com)
- load match object intead of other by default (pkilambi@redhat.com)
- compare by productId for other tab as well (pkilambi@redhat.com)
- compare matched and compatible by productId (pkilambi@redhat.com)
- comare matched package list with productids (pkilambi@redhat.com)
- changing the matched bucket to use productId for matching
  (pkilambi@redhat.com)
- Hide the incompatible pools tab by default and make it a config option
  (pkilambi@redhat.com)
- Teach the gui to send up email/lang during token activation, too
  (jbowes@redhat.com)
- Update cli option names for regtoken activation to match api
  (jbowes@redhat.com)
- Teach the cli to send up email/lang on regtoken activation
  (jbowes@redhat.com)
- Swap OrderNumber and SerialNumber fields for formatting in list --consumed
  (adrian@alikins.usersys.redhat.com)
- Adding some changes to disable horizontal scrolling and align the columns
  appropriately (pkilambi@redhat.com)
- fix the display order for contract info (pkilambi@redhat.com)
- 602258 - represent subscription data as productId instead of sku
  (pkilambi@redhat.com)

* Wed Jun 09 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.63-1
- Resolves: #589626
- Adding accessibility string for widgets for automation support
  (pkilambi@redhat.com)
- updating spec to include new files (pkilambi@prad.rdu.redhat.com)
- Add support for a /etc/rhsn/facts/*.facts files that can define additional
  facts (adrian@alikins.usersys.redhat.com)
- test (pkilambi@redhat.com)
- adding some todos for later (pkilambi@redhat.com)
- get the other tab to populate entitlements (pkilambi@redhat.com)
- rename oder with contract (pkilambi@redhat.com)
- fixing progress dialog path (pkilambi@redhat.com)
- minor fixed (pkilambi@redhat.com)
- Adding order info to list call (pkilambi@redhat.com)

* Tue Jun 01 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.61-1
- Resolves: #591247
- clean up (pkilambi@redhat.com)
- Revert "Add uep wrapper where async logic will live" (pkilambi@redhat.com)
- Revert "Hook up register/unregister to be async" (pkilambi@redhat.com)
- if we get an error from IT lets show it instead of generic error for reg
  token activation (pkilambi@redhat.com)
- removing test checks (pkilambi@redhat.com)
- Hook up register/unregister to be async (jbowes@redhat.com)
- Add uep wrapper where async logic will live (jbowes@redhat.com)
- error message is now a popup (pkilambi@redhat.com)
- Load gui resources relative to the python code (to run from src)
  (jbowes@redhat.com)
- Append consistant python path (jbowes@redhat.com)
- Add .gitignore (jbowes@redhat.com)
- Adding Order info to cli and gui (pkilambi@redhat.com)
- Convert to using candlepin's jackson formatted json (jbowes@redhat.com)
- Fix OID ending in 10+.  Add Order.getContract(). (jortel@redhat.com)
- Changing the Add subscriptions screen to bucketize entitlements into
  categories and use a tabbed interface (pkilambi@redhat.com)
- Changing name of referenced variable to regnum (calfonso@redhat.com)
- test (pkilambi@redhat.com)
- test (pkilambi@redhat.com)
- fix autosubscribe to user right consumer (pkilambi@redhat.com)

* Tue May 11 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.60-1
- Resolves: #591247 - format the dat correctly for gui add
- send in product hash as part of autobind  
- Format the cli print to be sequential instead of a table form. This makes the
  output more reliable (pkilambi@redhat.com)
- Fix rhsmcertd not sleeping properly.  Add Bundle class for combining key &
  cert next sprint. (jortel@redhat.com)
- unsubscribe uses serial number directly from subscription info per subscribed
  product (pkilambi@redhat.com)
- Change unsubscribe to use serial number instead of product names
  (pkilambi@redhat.com)

* Mon May 10 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.55-1
- Resolves:  #590094 - encode translated error strings before displaying
  (pkilambi@redhat.com)

* Fri May 07 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.54-1
- Resolves: #584510
- Adding a progress bar to Apply subscriptions process (pkilambi@redhat.com)

* Thu May 06 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.52-1
- Resolves: #589626 - unregister now removes stale entitlement certs from the clients (pkilambi@redhat.com)

* Wed May 05 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.51-1
- Resolves: #585193, #587647, #584440, #586462, #588408
- 585193, 587647 - Handle Non-Network case Gracefully
- 584440 - Validate manually uploaded entitlement certs
- 586462 - strip out http connection stuff and default all connections through
  ssl (pkilambi@redhat.com)
- 588408 - re initialize CP instance with consumer certs post registration
  (pkilambi@redhat.com)
- fixing registration to not load certs while creating a cp instance
  (pkilambi@redhat.com)
- 588389: Ensure list of expired products is unique. (jortel@redhat.com)

* Fri Apr 30 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.48-1
- Resolves: #586388, #586525
- Adding support to unsubscribe user by serial number (pkilambi@redhat.com)
- Disable update/unsubscribe buttons if a product is not selected or if a
  selected product is not yet subscribed to any subscription
  (pkilambi@redhat.com)
- hide the add/update windows after successfully applying the subscription
  (pkilambi@redhat.com)
- Fix certlib exception and linger bug. (jortel@redhat.com)
- Removing testing comment.  Add code doc. (jortel@redhat.com)
- Stop removing expired certificates; Display warning in yum for expired
  certificates. (jortel@redhat.com)
- 586388 - Allow multiple pools/products/regnumbers to be able to subscribe
  from commandline (pkilambi@redhat.com)
- exception handling for unsubscribe functionality (pkilambi@redhat.com)
- 586525: Interpret interval as minutes. (jortel@redhat.com)
- clean up (pkilambi@redhat.com)
- Subscribe to pools in Add/Update button by pool id instead of
  productName.Ignore the productId and use productname in the list to identity
  the product pool in the list (pkilambi@redhat.com)
- Beautify error message display on bad login (jbowes@redhat.com)
- clean up old modules (pkilambi@redhat.com)

* Tue Apr 27 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.47-1
- Resolves:  #584330
- Add PyXML to the requires
- fixing the date format to be human readable for GUI (pkilambi@redhat.com)
- Add tzinfo to datetime objects returned by DateRange.begin() and
  DateRange.end() (jortel@redhat.com)
- Provide a command line and GUI option for user to automacally subscribe upon
  register. By default we only register the system (pkilambi@redhat.com)
- fixing the cli date format to be human readable (pkilambi@redhat.com)
- spec clean up (pkilambi@redhat.com)
- Adding support to show registration status on the main screen and direct
  users appropriately (pkilambi@redhat.com)
- 584330: Fix init.d script start() output. (jortel@redhat.com)
- 584137 - cli subscribe now uses cert serial number as ent Id until told
  otherwise (pkilambi@redhat.com)
- Add Reader to skip double newlines left by iniparse when sections are
  removed. (jortel@redhat.com)
- Migrate to iniparse. (jortel@redhat.com)
- Add certmgr to replace direct calling of certlib & repolib.
  (jortel@redhat.com)

* Tue Apr 20 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.41-1
- Resolves: #580043
- jbowes's fix for locale string replacement (pkilambi@redhat.com)
- unsubscribe products based on ent id from cert serial (pkilambi@redhat.com)
- dont show the content/role sets if the list is empty (pkilambi@redhat.com)
- Add access to product hash. (jortel@redhat.com)
- Preserve custom repo properties. (jortel@redhat.com)

* Fri Apr 16 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.39-1
- Resolves: #581032, #581489
- cleaning up obsolete exceptions (pkilambi@redhat.com)
- Certlib robustness & testing. Remove InvalidCertificate exception; no longer
  raised by ProductCertificate.getProduct() and
  EntitlementCertificate.getOrder() Ensure Directory classes only return 'good'
  certificates (not bogus ones). Detect and log invalid cert bundles from UEP.
  Overall more robust error handling. (jortel@redhat.com)

* Wed Apr 14 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.38-1
- Resolves: #568427
- eol string literal missing (pkilambi@redhat.com)
- modify the sequence in whihc subscription column is shown
  (pkilambi@redhat.com)
- fixing index issue due to mismatched product tuple (pkilambi@redhat.com)
- Exception Handling for custom exceptions sent down from candlepin
  (pkilambi@redhat.com)
- Remove all certificate caching; Change certificate read() to be instance
  based. (jortel@redhat.com)
- change to right header based on product state (pkilambi@redhat.com)
- Adding support to list products that are consuming a subscription but not
  installed (pkilambi@redhat.com)
- including locale info in request headers (pkilambi@redhat.com)
- clean up (pkilambi@redhat.com)
- adding a new column called subscription to gui/cli (pkilambi@redhat.com)
- support to handle multiple products per certs for cli/tui
  (pkilambi@redhat.com)
- Backtrack on some of the snapshot stuff. (jortel@redhat.com)
- unbregister account before re-registereing user from GUI
  (pkilambi@redhat.com)
- unregister existing consumer before re-registering with a force flag
  (pkilambi@redhat.com)
- Adding support to manually unregister a client to cli (pkilambi@redhat.com)

* Mon Apr 12 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.37-1
- Resolves: #580576 - fixing error message on failed registration (pkilambi@redhat.com)
- Resolves: #580955 - set ssl_port to cfg value instead of default (pkilambi@redhat.com)
- Ground work for directory snapshot caching. (jortel@redhat.com)
- Resolves: #580630 -  register window will now not be resizable (pkilambi@redhat.com)
- Updated for OID structure 04-07-10. (jortel@redhat.com)
- reflecting changes to the oid schema structure in the client tooling
  (pkilambi@redhat.com)
- Remove 'layered product versioning' prototype code. (jortel@redhat.com)

* Tue Apr 06 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.36-1
- Support for register system by consumerId
- rpmlint fixes
- Resolves: #578860 - alignment issues on registration details screen
- Resolves: #570489: Updating man page to reflect latest functionality
  (pkilambi@redhat.com)
- updating frame icon (pkilambi@redhat.com)

* Mon Apr 05 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.33-1
- Resolves: #578113 - lscpu is localized, use the right locale to accumulate hwdata
- Resolves: #578520 - if no products are selected, clicking 'Unsubscribe' should be a noop
- Resolves: #578517 registration dialog validates for missing input
- Resolves: #576568 catch the socket exceptions or any other unknow exception and  error gracefully (pkilambi@redhat.com)
- removing test files (pkilambi@redhat.com)
- specfile clean up (pkilambi@redhat.com)
- updated icons (pkilambi@redhat.com)
- some minor UI tweaks based on feedback from the demo (pkilambi@redhat.com)
- multiple bug fixes to gui, cli and proxy (pkilambi@redhat.com)
- Update product __str__ to show valid and valid date range.
  (jortel@redhat.com)
- test (pkilambi@redhat.com)
- updating config to remove cert paths (pkilambi@redhat.com)
- Fix extension parsing with values on following line as '.\n<value>'.
  (jortel@redhat.com)

* Tue Mar 30 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.28-1
- Resolves:  #577238 #577140
- Use SSLv3 for Candlepin communication. (dgoodwin@redhat.com)
- Fix edge case in OID seaching. (jortel@redhat.com)
- dont use ssl certs for register even for re registration
  (pkilambi@redhat.com)
- Update for entitlement OID schema 3-29-10 spec=DOC-33548 which includes yum
  repo (.1) namespace. (jortel@redhat.com)
- make --force default true (pkilambi@redhat.com)
- Ability to unsubscribe in offline mode. Adding a confirm window before
  unsubscribing (pkilambi@redhat.com)
- --force option to override existing registrations (pkilambi@redhat.com)
- adding dist to rpm spec (pkilambi@redhat.com)
- bug#571242 return error code of 0 for help options (pkilambi@redhat.com)

* Fri Mar 26 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.26-1
- Resolves:  #568427
- bug#577238 dont replace config upon reinstall (pkilambi@redhat.com)
- breaking clients. comment our ssl cert stuff until its functional on cp
  (pkilambi@redhat.com)
- some ssl changes (pkilambi@redhat.com)
- Update for getCertificateSerials() returned format change.
  (jortel@redhat.com)
- Initial layered product version work. (jortel@redhat.com)
- notify user politely if there are no available ents (pkilambi@redhat.com)
- adding id to the available list (pkilambi@redhat.com)
- Added icon support for rhsm gui (pkilambi@redhat.com)

* Thu Mar 25 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.22-1
- Resolves: #568427
- Spec file clean up
- moving gnome tools to separate package
- methods to define concrete description for products based on the state, product info and entitlement info.
- constants file to accumulate all static strings in one place 

* Wed Mar 24 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.21-1
- Resolves: #568427
- event notification from add/remove and update subscription actions to main window
- error notification windows
- registration should now auto subscribe products and redirect to already-registered screen

* Mon Mar 22 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.20-1
- Resolves: #568427
- logging support
- changes to support identity cert parsing

* Fri Mar 19 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.19-1
- Resolves: #568427 
- Changes to support dynamic icon changes
- changes to support resteasy api changes
- fixed alignment issues in mainWindow

* Wed Mar 17 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.17-1
- Resolves:  #568427 - New registration/regtoken/add subscriptions screens

* Mon Mar 15 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.17-1
- Resolves:  #568426
- More changes to api proxy
- new gui screens 

* Thu Mar 11 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.16-1
- Resolves:  #568426 
- more updates to connection.py api flush down
- updates to new screens and layout in gui

* Mon Mar 08 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.14-1
- Resolves: #568426 - new build

* Wed Mar 03 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.12-1
- Resolves: #568433 - Flushed out hardware info
- man page for cli

* Mon Feb 22 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.1-1
- packaging subscription-manager

