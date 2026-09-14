/* ═══════════════════════════════════════════════════
   DP Control Panel — Device Detection & Auto-Redirect
   Redirects mobile browsers to dedicated mobile HTMLs
   while leaving PC/Desktop browsers 100% unaffected.
   ═══════════════════════════════════════════════════ */

(function () {
  // Check user explicitly dismissed the prompt for this session
  if (sessionStorage.getItem('dismiss_device_prompt') === 'true') {
    return;
  }

  const ua = (navigator.userAgent || navigator.vendor || window.opera || '').toLowerCase();
  const isMobileUA = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile|tablet|mobi|arm/i.test(ua);
  const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
  const isMobileWidth = window.innerWidth <= 900;
  const isMobileDevice = isMobileUA || (isTouchDevice && isMobileWidth) || isMobileWidth;

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

  const targetMobilePage = desktopToMobileMap[pageName];
  const targetDesktopPage = mobileToDesktopMap[pageName];

  // Helper to show popup modal prompt
  function showSwitchModal(title, msg, targetUrl, isMobileSwitch) {
    if (document.getElementById('deviceDetectModal')) return;

    const modalHtml = `
      <div id="deviceDetectModal" style="position:fixed; inset:0; background:rgba(5,8,14,0.85); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); z-index:999999; display:flex; align-items:center; justify-content:center; padding:1rem; animation:fadeIn 0.3s ease;">
        <div style="background:#090e17; border:1px solid rgba(0,242,254,0.4); border-radius:18px; padding:1.25rem; max-width:380px; width:100%; box-shadow:0 20px 50px rgba(0,0,0,0.8); text-align:center; box-sizing:border-box;">
          <div style="font-size:2.2rem; margin-bottom:0.4rem;">${isMobileSwitch ? '📱' : '💻'}</div>
          <h3 style="font-size:1.1rem; color:#fff; font-weight:700; margin:0 0 0.35rem 0;">${title}</h3>
          <p style="font-size:0.8rem; color:rgba(255,255,255,0.7); margin-bottom:1.1rem; line-height:1.4;">${msg}</p>
          <div style="display:flex; gap:0.5rem;">
            <button type="button" id="deviceModalDismissBtn" style="flex:1; padding:0.6rem; border-radius:10px; border:1px solid rgba(255,255,255,0.15); background:rgba(255,255,255,0.05); color:#fff; font-size:0.8rem; font-weight:600; cursor:pointer;">Stay Here</button>
            <button type="button" id="deviceModalSwitchBtn" style="flex:1; padding:0.6rem; border-radius:10px; border:none; background:linear-gradient(135deg, #00f2fe, #4f8cff); color:#fff; font-size:0.8rem; font-weight:700; cursor:pointer; box-shadow:0 0 15px rgba(0,242,254,0.4);">Switch View</button>
          </div>
        </div>
      </div>
    `;

    function bindModalEvents() {
      const modal = document.getElementById('deviceDetectModal');
      if (!modal) return;

      modal.addEventListener('click', function (e) {
        const dismissBtn = e.target.closest('#deviceModalDismissBtn');
        const switchBtn = e.target.closest('#deviceModalSwitchBtn');

        if (dismissBtn) {
          e.preventDefault();
          sessionStorage.setItem('dismiss_device_prompt', 'true');
          modal.remove();
        } else if (switchBtn) {
          e.preventDefault();
          if (isMobileSwitch) {
            sessionStorage.removeItem('prefer_desktop_view');
          } else {
            sessionStorage.setItem('prefer_desktop_view', 'true');
          }
          window.location.href = targetUrl;
        }
      });
    }

    if (document.body) {
      document.body.insertAdjacentHTML('beforeend', modalHtml);
      bindModalEvents();
    } else {
      document.addEventListener('DOMContentLoaded', () => {
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        bindModalEvents();
      });
    }
  }

  // 1. Mobile/Tablet user on Desktop Page -> Prompt to switch to Mobile view
  if (isMobileDevice && targetMobilePage && sessionStorage.getItem('prefer_desktop_view') !== 'true') {
    showSwitchModal(
      'Mobile/Tablet Detected',
      'We noticed you are visiting on a mobile or tablet device. Would you like to switch to the mobile interface?',
      targetMobilePage,
      true
    );
  }

  // 2. Desktop PC user on Mobile Page -> Prompt to switch to PC view
  if (!isMobileDevice && targetDesktopPage) {
    showSwitchModal(
      'Desktop Computer Detected',
      'You are currently viewing the mobile view on a PC. Would you like to switch to the desktop interface?',
      targetDesktopPage,
      false
    );
  }
})();
