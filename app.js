/* ===================================================
   DP PANEL - Unified Admin Website JS Engine
   Firebase REST API client for:
     1. UID Bypass Accounts (firebase node: /users/)
     2. TITAN BYPASS Panel Accounts (firebase node: /dp_panel_users/)
     3. Feature Definitions (firebase node: /feature_definitions/)
   =================================================== */

const FIREBASE_URL = 'https://dipesh-database-default-rtdb.firebaseio.com';

// Default feature definitions — seeded to Firebase on first load
const DEFAULT_FEATURES = [
  { key: 'aimbot',     label: 'Aimbot',       category: 'Aim Hacks',
    isAimbot: true,
    scanHex: 'FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 ?? ?? ?? ?? 00 00 00 00 ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A5 43',
    aimOffsets: [
      { name: 'Chest(B4) → Head(E8)', offset1: 'E8', offset2: 'B4' }
    ]
  },
  { key: 'chams',      label: 'Chams',        category: 'Visuals' },
  { key: 'fake_lag',   label: 'Fake Lag',     category: 'Extra' },
  
  // Aim Patches
  { key: 'aob_2x',     label: 'Aim Scope 2X', category: 'Aim Hacks', 
    scanHex: '8F C2 F5 3C CD CC CC 3D 02 00 00 00 EC 51 B8 3D CD CC 4C 3F 00 00 00 00 00 00 A0 42 00 00 C0 3F 33 33 13 40 00 00 F0 3F 00 00 80 3F 01 00 00 00 00 00 00 00 00 47 47 92 00 00 00 00 FF FF FF FF 66 CC 03 00 F4 A5 03 00 F4 A5 03 00 FF FF FF FF 00 00 00 00 00 00 80 3F F2 A5 03 00 01 00 00 00 CD CC 8C 3F 33 33 93 3F 8F C2 F5 3C CD CC CC 3D 00 00 00 00 EC 51 B8 3D 00 00 80 3F 00 00 00 00 00 00 C8 42 00 00 A0 40 33 33 13 40 00 00 08 40 00 00 80 3F 01',
    replaceHex: '8F C2 F5 3C CD CC CC 3D 02 00 00 00 EC 51 B8 3D CD CC 4C 3F 00 00 00 00 00 00 A0 42 00 00 C0 3F 33 33 13 40 00 00 F0 3F 00 00 80 4F 01' 
  },
  { key: 'aob_4x',     label: 'Aim Scope 4X', category: 'Aim Hacks',
    scanHex: 'CC CC 3D 04 00 00 00 29 5C 8F 3D 00 00 00 3F 00 00 F0 41 00 00 48 42 00 00 00 3F 33 33 13 40 00 00 D0 3F 00 00 80 3F 01 00 00 00 00 00 C3 94 00 39 8B BD 00 00 00 00 2A 00 00 00 4D 00 54 00 48 00 41 00 53 00 48 00 2E 00 52 00 65 00 73 00 46 00 69 00 6C 00 65 00 4C 00 6F 00 61 00 64 00 65 00 72 00 2E 00 41 00 64 00 64 00 4C 00 6F 00 61 00 64 00 65 00 72 00 54 00 6F 00 4D 00 54 00 51 00 75 00 65 00 75 00 65 00 2E 00 20',
    replaceHex: 'CC CC 3D 04 00 00 00 29 5C 8F 3D 00 00 00 3F 00 00 F0 41 00 00 48 42 00 00 00 3F 33 33 13 40 00 00 D0 3F 00 00 80 4F 01'
  },
  
  // Camera Patches
  { key: 'camera_left',  label: 'Camera Left',  category: 'Camera',
    scanHex: '00 00 00 00 00 00 80 40 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 80 BF',
    replaceHex: '00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00'
  },
  { key: 'camera_right', label: 'Camera Right', category: 'Camera',
    scanHex: '00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 80 7F 00 00 80 7F 00 00 80 7F 00 00 80 FF',
    replaceHex: '00 00 00 00 00 80 40 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 80 7F 00 00 80 7F 00 00 80 7F 00 00 80 FF'
  },
  
  // Movement Patches
  { key: 'fast_landing', label: 'Fast Landing', category: 'Movement Hacks',
    scanHex: '00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 80 7F 00 00 80 7F 00 00 80 7F 00 00 80 FF',
    replaceHex: '00 00 00 00 00 00 FF 41 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 80 BF 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 80 BF 00 00 80 7F 00 00 80 7F 00 00 80 7F 00 00 80 FF'
  },
  { key: 'speed_hack',   label: 'Speed Hack',   category: 'Movement Hacks',
    scanHex: '01 00 00 00 02 2B 07 3D',
    replaceHex: '01 00 00 00 92 E4 70 3D'
  },
  { key: 'fly_hack',     label: 'Fly Hack',     category: 'Movement Hacks',
    scanHex: '9A 99 99 3E A4 70 3D 3F 01',
    replaceHex: '9A 99 BF 3F A4 70 3D 3F 01'
  },
  
  // Combat Patches
  { key: 'fast_fire',    label: 'Fast Fire',    category: 'Combat Hacks',
    scanHex: '00 00 80 40 33 33 93 40 3D 0A F7 3F',
    replaceHex: '00 00 80 40 00 00 80 40 CB D2 4D 3E'
  },
  { key: 'fast_fire_b',  label: 'Fast Fire B',  category: 'Combat Hacks',
    scanHex: '02 2B 07 3D ?? ?? ?? ?? 02 2B 07 3D 00 00 00 00',
    replaceHex: '08 39 75 3B'
  },
  { key: 'glitch_fire',  label: 'Glitch Fire',  category: 'Combat Hacks',
    scanHex: 'C0 41 00 00 10 C1 00 00 90 C1 00 00 70 41 01 00 00 00 00 00 C0 3F 00 00 00 3F 00 00 80 3F 00 00 80 3F',
    replaceHex: 'C0 41 00 00 10 C1 00 00 90 C1 00 00 70 41 01 00 00 00 00 00 C0 00 00 00 00 3C 00 00 80 3F 00 00 80 3F'
  }
];

// In-memory cache of feature list (loaded from Firebase)
let _featureListCache = null;

const App = (() => {

  // --- Firebase REST helpers ---
  const fbGet = async (path) => {
    try {
      const res = await fetch(`${FIREBASE_URL}/${path}.json`);
      if (res.ok) return await res.json();
    } catch (e) { console.warn('[Firebase GET]', e.message); }
    return null;
  };

  const fbPut = async (path, data) => {
    try {
      const res = await fetch(`${FIREBASE_URL}/${path}.json`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) return await res.json();
    } catch (e) { console.warn('[Firebase PUT]', e.message); }
    return null;
  };

  const fbPatch = async (path, data) => {
    try {
      const res = await fetch(`${FIREBASE_URL}/${path}.json`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) return await res.json();
    } catch (e) { console.warn('[Firebase PATCH]', e.message); }
    return null;
  };

  const fbDelete = async (path) => {
    try { await fetch(`${FIREBASE_URL}/${path}.json`, { method: 'DELETE' }); }
    catch (e) { console.warn('[Firebase DELETE]', e.message); }
  };

  // --- Init Firebase structure ---
  const initFirebase = async () => {
    const admin = await fbGet('admin');
    if (!admin) {
      await fbPut('admin', { username: 'admin', password: 'admin123' });
    }
    // Seed default feature definitions if not present
    await seedFeatureDefinitions();
  };

  // ==========================================
  // FEATURE DEFINITIONS (/feature_definitions/)
  // ==========================================

  /** Seed default features into Firebase if node doesn't exist, and migrate existing ones */
  const seedFeatureDefinitions = async () => {
    const existing = await fbGet('feature_definitions');
    if (!existing) {
      // First time — seed everything
      const featureObj = {};
      DEFAULT_FEATURES.forEach(f => {
        featureObj[f.key] = { 
          key: f.key, 
          label: f.label, 
          category: f.category,
          scanHex: f.scanHex || '',
          replaceHex: f.replaceHex || '',
          isAimbot: f.isAimbot || false,
          aimOffsets: f.aimOffsets || []
        };
      });
      await fbPut('feature_definitions', featureObj);
      _featureListCache = DEFAULT_FEATURES.slice();
    } else {
      // Data exists — migrate/patch any missing fields from defaults
      for (const def of DEFAULT_FEATURES) {
        const fb = existing[def.key];
        if (!fb) {
          // Feature doesn't exist in Firebase yet, add it
          await fbPut(`feature_definitions/${def.key}`, {
            key: def.key,
            label: def.label,
            category: def.category,
            scanHex: def.scanHex || '',
            replaceHex: def.replaceHex || '',
            isAimbot: def.isAimbot || false,
            aimOffsets: def.aimOffsets || []
          });
        } else {
          // Feature exists — patch in any missing fields
          const updates = {};
          if (!fb.scanHex && def.scanHex) updates.scanHex = def.scanHex;
          if (!fb.replaceHex && def.replaceHex) updates.replaceHex = def.replaceHex;
          if (fb.isAimbot === undefined && def.isAimbot) updates.isAimbot = def.isAimbot;
          if (!fb.aimOffsets && def.aimOffsets && def.aimOffsets.length > 0) updates.aimOffsets = def.aimOffsets;
          
          if (Object.keys(updates).length > 0) {
            await fbPatch(`feature_definitions/${def.key}`, updates);
          }
        }
      }
      _featureListCache = null; // Force refresh on next get
    }
  };

  /** Get all feature definitions from Firebase (cached) */
  const getFeatureList = async (forceRefresh = false) => {
    if (_featureListCache && !forceRefresh) return _featureListCache;

    const data = await fbGet('feature_definitions');
    if (!data) {
      // Fallback to defaults
      _featureListCache = DEFAULT_FEATURES.slice();
      return _featureListCache;
    }
    _featureListCache = Object.values(data).map(f => ({
      key: f.key,
      label: f.label,
      category: f.category || 'General',
      scanHex: f.scanHex || '',
      replaceHex: f.replaceHex || '',
      isAimbot: f.isAimbot || false,
      aimOffsets: f.aimOffsets || []
    }));
    return _featureListCache;
  };

  /** Add a new feature definition */
  const addFeatureDefinition = async (key, label, category, scanHex = '', replaceHex = '', isAimbot = false, aimOffsets = []) => {
    key = key.toLowerCase().replace(/[^a-z0-9_]/g, '_');
    const existing = await fbGet(`feature_definitions/${key}`);
    if (existing) return { success: false, msg: 'Feature key already exists.' };

    const def = { key, label, category: category || 'General', scanHex, replaceHex, isAimbot, aimOffsets };
    await fbPut(`feature_definitions/${key}`, def);
    _featureListCache = null; // Invalidate cache
    return { success: true };
  };

  /** Update an existing feature definition */
  const updateFeatureDefinition = async (key, label, category, scanHex = '', replaceHex = '', isAimbot = false, aimOffsets = []) => {
    const existing = await fbGet(`feature_definitions/${key}`);
    if (!existing) return { success: false, msg: 'Feature not found.' };

    await fbPatch(`feature_definitions/${key}`, { label, category: category || 'General', scanHex, replaceHex, isAimbot, aimOffsets });
    _featureListCache = null;
    return { success: true };
  };

  /** Delete a feature definition */
  const deleteFeatureDefinition = async (key) => {
    await fbDelete(`feature_definitions/${key}`);
    _featureListCache = null;

    // Also remove this feature key from all panel users
    const users = await fbGet('dp_panel_users');
    if (users) {
      for (const username of Object.keys(users)) {
        if (users[username].features && users[username].features.hasOwnProperty(key)) {
          await fbDelete(`dp_panel_users/${username}/features/${key}`);
        }
      }
    }
    return { success: true };
  };

  /** Get all unique categories from feature definitions */
  const getFeatureCategories = async () => {
    const features = await getFeatureList(true);
    const cats = [...new Set(features.map(f => f.category || 'General'))];
    return cats.sort();
  };

  // --- Admin Auth ---
  const loginAdmin = async (username, password) => {
    const admin = await fbGet('admin');
    if (admin && admin.username === username && admin.password === password) {
      return { success: true, role: 'admin' };
    }
    return { success: false };
  };

  // ==========================================
  // 1. UID BYPASS USER MANAGEMENT (/users/)
  // ==========================================
  const getAllUsers = async () => {
    const users = await fbGet('users');
    if (!users) return [];
    return Object.keys(users).map(key => ({ ...users[key], _key: key }));
  };

  const getUser = async (username) => {
    return await fbGet(`users/${username}`);
  };

  const createUser = async (username, password, maxUids = 10, isTrial = false, trialLimit = 2, trialDays = 1, trialExpiry = '') => {
    const existing = await fbGet(`users/${username}`);
    if (existing) return { success: false, msg: 'Username already exists.' };
    if (username === 'admin') return { success: false, msg: 'Cannot use "admin" as username.' };

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let secret = '';
    for (let i = 0; i < 16; i++) secret += chars.charAt(Math.floor(Math.random() * chars.length));

    const userData = {
      username,
      password,
      displayName: username,
      secret,
      active: true,
      is_trial: isTrial,
      trial_limit: isTrial ? trialLimit : maxUids,
      trial_days: trialDays,
      trial_expiry: trialExpiry,
      maxUids: isTrial ? trialLimit : maxUids,
      createdAt: new Date().toISOString(),
      uids: []
    };

    await fbPut(`users/${username}`, userData);
    return { success: true };
  };

  const deleteUser = async (username) => {
    await fbDelete(`users/${username}`);
  };

  const toggleUserActive = async (username) => {
    const user = await fbGet(`users/${username}`);
    if (user) {
      await fbPatch(`users/${username}`, { active: !user.active });
      return !user.active;
    }
    return null;
  };

  const updateUserMaxUids = async (username, maxUids) => {
    await fbPatch(`users/${username}`, { maxUids: parseInt(maxUids) });
  };

  const removeUid = async (username, uidValue) => {
    const user = await fbGet(`users/${username}`);
    if (!user) return;
    let uids = user.uids || [];
    if (!Array.isArray(uids)) uids = Object.values(uids);
    uids = uids.filter(u => u.uid !== uidValue);
    await fbPatch(`users/${username}`, { uids });
  };

  const addUid = async (username, uidValue, displayName, days = 30) => {
    const user = await fbGet(`users/${username}`);
    if (!user) return { success: false, msg: `User "${username}" not found.` };

    let uids = user.uids || [];
    if (!Array.isArray(uids)) uids = Object.values(uids);

    if (uids.some(u => String(u.uid) === String(uidValue))) {
      return { success: false, msg: `UID ${uidValue} is already added for user "${username}".` };
    }

    const expiryDate = parseInt(days) > 0 ? new Date(Date.now() + parseInt(days) * 86400000).toISOString() : '';
    const newUidObj = {
      uid: String(uidValue),
      displayName: displayName || uidValue,
      status: 'Active',
      addedAt: new Date().toISOString(),
      expiry: expiryDate
    };

    uids.push(newUidObj);
    await fbPatch(`users/${username}`, { uids });
    return { success: true };
  };

  // ==========================================
  // UID ALLOWLIST (GLOBAL / INDEPENDENT BASE)
  // ==========================================
  const getAllowlist = async () => {
    const data = await fbGet('allowlist');
    if (!data) return [];
    return Object.keys(data).map(key => {
      const item = data[key];
      if (typeof item === 'object' && item !== null) {
        return { uid: key, ...item };
      }
      return { uid: key, name: String(item), status: 'Active' };
    });
  };

  const addAllowlistUid = async (uidValue, name, days = 0) => {
    uidValue = String(uidValue).trim();
    if (!uidValue || !/^\d+$/.test(uidValue)) return { success: false, msg: 'Please enter a valid numeric UID.' };
    const existing = await fbGet(`allowlist/${uidValue}`);
    if (existing) return { success: false, msg: `UID ${uidValue} is already on the Allowlist.` };

    const parsedDays = parseInt(days) || 0;
    const expiryDate = parsedDays > 0 ? new Date(Date.now() + parsedDays * 86400000).toISOString() : '';
    const entry = {
      uid: uidValue,
      name: name ? name.trim() : uidValue,
      status: 'Active',
      addedAt: new Date().toISOString(),
      expiry: expiryDate
    };

    await fbPut(`allowlist/${uidValue}`, entry);
    return { success: true };
  };

  const removeAllowlistUid = async (uidValue) => {
    await fbDelete(`allowlist/${String(uidValue).trim()}`);
    return { success: true };
  };

  const toggleAllowlistUid = async (uidValue) => {
    const current = await fbGet(`allowlist/${String(uidValue).trim()}`);
    if (!current) return false;
    const newStatus = current.status === 'Active' ? 'Disabled' : 'Active';
    await fbPatch(`allowlist/${String(uidValue).trim()}`, { status: newStatus });
    return newStatus;
  };

  // ==========================================
  // 2. DP PANEL USER MANAGEMENT (/dp_panel_users/)
  // ==========================================
  const getAllPanelUsers = async () => {
    const users = await fbGet('dp_panel_users');
    if (!users) return [];
    return Object.keys(users).map(key => ({ ...users[key], _key: key }));
  };

  const getPanelUser = async (username) => {
    return await fbGet(`dp_panel_users/${username}`);
  };

  const createPanelUser = async (username, password, _unused, features) => {
    const existing = await fbGet(`dp_panel_users/${username}`);
    if (existing) return { success: false, msg: 'Username already exists.' };
    if (username === 'admin') return { success: false, msg: 'Cannot use "admin" as username.' };

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let secret = '';
    for (let i = 0; i < 16; i++) secret += chars.charAt(Math.floor(Math.random() * chars.length));

    // Build features object from dynamic feature list
    const featureList = await getFeatureList();
    const featureObj = {};
    featureList.forEach(f => { featureObj[f.key] = !!(features && features[f.key]); });

    const userData = {
      username,
      password,
      displayName: username,
      secret,
      active: true,
      createdAt: new Date().toISOString(),
      features: featureObj,
    };

    await fbPut(`dp_panel_users/${username}`, userData);
    return { success: true };
  };

  const deletePanelUser = async (username) => {
    await fbDelete(`dp_panel_users/${username}`);
  };

  const togglePanelUserActive = async (username) => {
    const user = await fbGet(`dp_panel_users/${username}`);
    if (user) {
      await fbPatch(`dp_panel_users/${username}`, { active: !user.active });
      return !user.active;
    }
    return null;
  };

  const updatePanelUserFeatures = async (username, features) => {
    await fbPatch(`dp_panel_users/${username}`, { features });
  };

  // --- Stats ---
  const getGlobalStats = async () => {
    const users = await fbGet('users');
    if (!users) return { totalUsers: 0, activeUsers: 0, disabledUsers: 0, totalUids: 0, activeUids: 0 };

    let totalUsers = 0, activeUsers = 0, disabledUsers = 0, totalUids = 0, activeUids = 0;

    Object.values(users).forEach(user => {
      totalUsers++;
      if (user.active) activeUsers++; else disabledUsers++;
      let uids = user.uids || [];
      if (!Array.isArray(uids)) uids = Object.values(uids);
      uids.forEach(uid => {
        totalUids++;
        const isExpired = new Date(uid.expiry) < new Date();
        if (uid.status !== 'Inactive' && !isExpired) activeUids++;
      });
    });

    return { totalUsers, activeUsers, disabledUsers, totalUids, activeUids };
  };

  const getGlobalPanelStats = async () => {
    const users = await fbGet('dp_panel_users');
    if (!users) return { totalUsers: 0, activeUsers: 0, disabledUsers: 0 };

    let totalUsers = 0, activeUsers = 0, disabledUsers = 0;

    Object.values(users).forEach(user => {
      totalUsers++;
      if (user.active) activeUsers++; else disabledUsers++;
    });

    return { totalUsers, activeUsers, disabledUsers };
  };

  // --- Toast ---
  const toast = (msg, type = 'info') => {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const el = document.createElement('div');
    el.className = `toast toast-${type}`;
    el.textContent = msg;
    container.appendChild(el);
    setTimeout(() => el.remove(), 3000);
  };

  // --- Helpers ---
  const getTimeLeft = (isoString) => {
    const diff = new Date(isoString) - new Date();
    if (diff <= 0) return 'Expired';
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    let parts = [];
    if (d > 0) parts.push(`${d}d`);
    if (h > 0 || d > 0) parts.push(`${h}h`);
    if (m > 0 || h > 0 || d > 0) parts.push(`${m}m`);
    parts.push(`${s}s`);
    return parts.join(' ');
  };

  const updatePanelUserExpiry = async (username, expiresAt) => {
    await fbPatch(`dp_panel_users/${username}`, { expiresAt });
  };

  const updatePanelUserPassword = async (username, password) => {
    await fbPatch(`dp_panel_users/${username}`, { password });
  };

  const createSilentAimUser = async (username, password, durationHours, customExpiryStr, features) => {
    const existing = await fbGet(`dp_panel_users/${username}`);
    if (existing) return { success: false, msg: 'Username already exists.' };
    if (username === 'admin') return { success: false, msg: 'Cannot use "admin" as username.' };

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let secret = '';
    for (let i = 0; i < 16; i++) secret += chars.charAt(Math.floor(Math.random() * chars.length));

    let expiresAt = null;
    if (durationHours === 'custom' && customExpiryStr) {
      expiresAt = new Date(customExpiryStr).toISOString();
    } else if (typeof durationHours === 'number' && durationHours > 0) {
      expiresAt = new Date(Date.now() + durationHours * 3600 * 1000).toISOString();
    }

    const featureList = await getFeatureList();
    const featureObj = {};
    featureList.forEach(f => { featureObj[f.key] = !!(features && features[f.key]); });

    const userData = {
      username,
      password,
      displayName: username,
      secret,
      active: true,
      createdAt: new Date().toISOString(),
      expiresAt: expiresAt || null,
      features: featureObj,
    };

    await fbPut(`dp_panel_users/${username}`, userData);
    return { success: true };
  };

  const getSilentAimStats = async () => {
    const users = await fbGet('dp_panel_users');
    if (!users) return { totalUsers: 0, activeUsers: 0, expiredUsers: 0, disabledUsers: 0 };

    let totalUsers = 0, activeUsers = 0, expiredUsers = 0, disabledUsers = 0;
    const now = new Date();

    Object.values(users).forEach(user => {
      totalUsers++;
      if (!user.active) {
        disabledUsers++;
      } else if (user.expiresAt && new Date(user.expiresAt) < now) {
        expiredUsers++;
      } else {
        activeUsers++;
      }
    });

    return { totalUsers, activeUsers, expiredUsers, disabledUsers };
  };

  return {
    DEFAULT_FEATURES,
    initFirebase,
    loginAdmin,
    // Feature definitions
    getFeatureList,
    addFeatureDefinition,
    updateFeatureDefinition,
    deleteFeatureDefinition,
    getFeatureCategories,
    // UID users
    getAllUsers,
    getUser,
    createUser,
    deleteUser,
    toggleUserActive,
    updateUserMaxUids,
    removeUid,
    addUid,
    // Allowlist (Independent / Main Base)
    getAllowlist,
    addAllowlistUid,
    removeAllowlistUid,
    toggleAllowlistUid,
    // Panel users
    getAllPanelUsers,
    getPanelUser,
    createPanelUser,
    deletePanelUser,
    togglePanelUserActive,
    updatePanelUserFeatures,
    updatePanelUserExpiry,
    updatePanelUserPassword,
    createSilentAimUser,
    getSilentAimStats,
    // Stats
    getGlobalStats,
    getGlobalPanelStats,
    // Game Config (Offsets/Bones)
    getGameConfig: () => fbGet('game_config'),
    updateGameBones: (bones) => fbPatch('game_config', { bones, lastUpdate: new Date().toISOString() }),
    updateGameOffsets: (offsets) => fbPatch('game_config', { offsets, lastUpdate: new Date().toISOString() }),
    updateFullGameConfig: (configData) => fbPut('game_config', { ...configData, lastUpdate: new Date().toISOString() }),
    // Proto Pool
    getProtoPool,
    addProto,
    deleteProto,
    // Utils
    toast,
    getTimeLeft
  };
})();

// ── Proto Pool Firebase helpers ──
async function getProtoPool() {
  const res = await fetch(`${FIREBASE_URL}/protos.json`);
  if (!res.ok) return {};
  const data = await res.json();
  return data || {};
}

async function addProto(hexStr) {
  const key = Date.now().toString();
  const res = await fetch(`${FIREBASE_URL}/protos/${key}.json`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(hexStr)
  });
  return res.ok;
}

async function deleteProto(key) {
  const res = await fetch(`${FIREBASE_URL}/protos/${key}.json`, { method: 'DELETE' });
  return res.ok;
}

