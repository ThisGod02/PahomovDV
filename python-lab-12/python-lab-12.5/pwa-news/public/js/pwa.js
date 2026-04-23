// ── Service Worker регистрация ─────────────────────────
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            const reg = await navigator.serviceWorker.register('/service-worker.js');
            console.log('SW registered:', reg.scope);
            reg.addEventListener('updatefound', () => {
                reg.installing?.addEventListener('statechange', () => {
                    if (reg.installing?.state === 'installed' && navigator.serviceWorker.controller) {
                        showUpdateBanner();
                    }
                });
            });
        } catch (e) { console.error('SW registration failed:', e); }
    });
}

// ── A2HS (Add to Home Screen) ─────────────────────────
let deferredPrompt;
const installBtn = document.getElementById('installBtn');

window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.classList.remove('hidden');
});

installBtn?.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log('Install outcome:', outcome);
    deferredPrompt = null;
    installBtn.classList.add('hidden');
});

window.addEventListener('appinstalled', () => installBtn?.classList.add('hidden'));

// ── Push-уведомления ──────────────────────────────────
const notifBanner = document.getElementById('notificationPermission');
const allowBtn = document.getElementById('allowNotifications');
const closeBtn = document.getElementById('closeNotificationBanner');

async function setupPushNotifications() {
    if (!('Notification' in window) || !('serviceWorker' in navigator)) return;
    if (localStorage.getItem('notificationPermissionAsked')) return;
    setTimeout(() => {
        if (Notification.permission === 'default') notifBanner?.classList.remove('hidden');
    }, 5000);
    allowBtn?.addEventListener('click', requestPermission);
    closeBtn?.addEventListener('click', () => {
        notifBanner?.classList.add('hidden');
        localStorage.setItem('notificationPermissionAsked', 'true');
    });
}

async function requestPermission() {
    const perm = await Notification.requestPermission();
    if (perm === 'granted') {
        notifBanner?.classList.add('hidden');
        localStorage.setItem('notificationPermissionAsked', 'true');
        await subscribeToPush();
    }
}

async function subscribeToPush() {
    try {
        const res = await fetch('/api/vapid-public-key');
        const { publicKey } = await res.json();
        if (!publicKey) return;
        const reg = await navigator.serviceWorker.ready;
        const sub = await reg.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(publicKey),
        });
        await fetch('/api/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sub),
        });
    } catch (e) { console.error('Push subscribe error:', e); }
}

async function unsubscribeFromPush() {
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    if (sub) {
        await fetch('/api/unsubscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ endpoint: sub.endpoint }),
        });
        await sub.unsubscribe();
    }
}

function urlBase64ToUint8Array(base64) {
    const pad = '='.repeat((4 - base64.length % 4) % 4);
    const b64 = (base64 + pad).replace(/-/g, '+').replace(/_/g, '/');
    const raw = atob(b64);
    return Uint8Array.from([...raw].map(c => c.charCodeAt(0)));
}

function showUpdateBanner() {
    const div = document.createElement('div');
    div.className = 'notification-banner';
    div.innerHTML = `<p>🔄 Доступна новая версия</p>
        <button onclick="location.reload()">Обновить</button>
        <button onclick="this.parentElement.remove()">✕</button>`;
    document.body.appendChild(div);
}

async function checkCacheSize() {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
        const { usage, quota } = await navigator.storage.estimate();
        console.log(`Cache: ${(usage / 1024 / 1024).toFixed(2)} MB / ${(quota / 1024 / 1024).toFixed(0)} MB`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupPushNotifications();
    checkCacheSize();
});
