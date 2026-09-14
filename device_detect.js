/* ═══════════════════════════════════════════════════
   DP Control Panel — Device Detection & Auto-Redirect
   Redirects mobile browsers to dedicated mobile HTMLs
   while leaving PC/Desktop browsers 100% unaffected.
   ═══════════════════════════════════════════════════ */

(function () {
  // Respect explicit Desktop View user preference
  if (sessionStorage.getItem('prefer_desktop_view') === 'true') {
    return;
  }

  const ua = (navigator.userAgent || navigator.vendor || window.opera || '').toLowerCase();
  const isMobileUA = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile/i.test(ua);
  const isMobileWidth = window.innerWidth <= 768;
  const isMobileDevice = isMobileUA || isMobileWidth;

  const currentPath = window.location.pathname;
  let pageName = currentPath.substring(currentPath.lastIndexOf('/') + 1);
  if (!pageName || pageName === '') {
    pageName = 'index.html';
  }

  // Redirect maps
  const desktopToMobileMap = {
    'index.html': 'mobile_index.html',
    'admin.html': 'mobile_admin.html',
    'panel_admin.html': 'mobile_panel_admin.html',
    'silent_aim_admin.html': 'mobile_silent_aim_admin.html',
    'offsets_manager.html': 'mobile_offsets_manager.html',
    'feature_builder.html': 'mobile_feature_builder.html',
    'aob_finder.html': 'mobile_aob_finder.html'
  };

  const mobileToDesktopMap = {
    'mobile_index.html': 'index.html',
    'mobile_admin.html': 'admin.html',
    'mobile_panel_admin.html': 'panel_admin.html',
    'mobile_silent_aim_admin.html': 'silent_aim_admin.html',
    'mobile_offsets_manager.html': 'offsets_manager.html',
    'mobile_feature_builder.html': 'feature_builder.html',
    'mobile_aob_finder.html': 'aob_finder.html'
  };

  if (isMobileDevice && desktopToMobileMap[pageName]) {
    window.location.replace(desktopToMobileMap[pageName]);
  } else if (!isMobileDevice && mobileToDesktopMap[pageName]) {
    window.location.replace(mobileToDesktopMap[pageName]);
  }
})();
