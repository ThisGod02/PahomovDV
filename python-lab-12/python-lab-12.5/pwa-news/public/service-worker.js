const STATIC_CACHE = 'static-v1';
const API_CACHE = 'api-cache-v1';

const STATIC_ASSETS = ['/', '/index.html', '/css/styles.css', '/js/app.js', '/js/pwa.js'];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(STATIC_CACHE).then(c => c.addAll(STATIC_ASSETS)).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys()
            .then(names => Promise.all(names.filter(n => n !== STATIC_CACHE && n !== API_CACHE).map(n => caches.delete(n))))
            .then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', e => {
    const url = new URL(e.request.url);
    if (url.pathname.startsWith('/api/')) {
        e.respondWith(networkFirst(e.request));
    } else if (isStatic(e.request)) {
        e.respondWith(cacheFirst(e.request));
    } else if (e.request.mode === 'navigate') {
        e.respondWith(networkFirst(e.request));
    } else {
        e.respondWith(networkFirst(e.request));
    }
});

// Network-First с таймаутом 3 с
async function networkFirst(request, timeout = 3000) {
    const timeoutRes = new Promise(resolve =>
        setTimeout(async () => resolve(await caches.match(request) || new Response('Timeout', { status: 408 })), timeout)
    );
    const fetchRes = fetch(request.clone()).then(async res => {
        if (res.ok) {
            const cache = await caches.open(API_CACHE);
            cache.put(request, res.clone());
        }
        return res;
    }).catch(async () => await caches.match(request) || new Response('Offline', { status: 503 }));

    return Promise.race([fetchRes, timeoutRes]);
}

// Cache-First для статики
async function cacheFirst(request) {
    const cached = await caches.match(request);
    if (cached) return cached;
    try {
        const res = await fetch(request);
        if (res.ok) { const c = await caches.open(STATIC_CACHE); c.put(request, res.clone()); }
        return res;
    } catch {
        return new Response('Not available offline', { status: 404 });
    }
}

function isStatic(req) {
    return ['.css', '.js', '.png', '.jpg', '.svg', '.ico', '.woff2'].some(e => req.url.endsWith(e));
}

// Push-уведомления
self.addEventListener('push', e => {
    let data = {};
    try { data = e.data?.json() || {}; } catch { data = { title: 'Новости PWA', body: e.data?.text() }; }
    e.waitUntil(self.registration.showNotification(data.title || 'Новости PWA', {
        body: data.body || 'Новые статьи',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png',
        vibrate: [200, 100, 200],
        data: { url: data.url || '/' },
        actions: [{ action: 'open', title: 'Открыть' }, { action: 'close', title: 'Закрыть' }],
        tag: 'news-notification',
        renotify: true,
    }));
});

self.addEventListener('notificationclick', e => {
    e.notification.close();
    if (e.action === 'close') return;
    e.waitUntil(clients.matchAll({ type: 'window' }).then(list => {
        const url = e.notification.data?.url || '/';
        const win = list.find(c => c.url === url);
        return win ? win.focus() : clients.openWindow(url);
    }));
});

// Фоновая синхронизация
self.addEventListener('sync', e => {
    if (e.tag === 'sync-articles') e.waitUntil(syncArticles());
});

async function syncArticles() {
    const actions = await getPendingActions();
    for (const action of actions) {
        try {
            await fetch(action.url, { method: action.method, headers: action.headers, body: action.body });
            await removePendingAction(action.id);
        } catch (err) { console.error('Sync failed:', err); }
    }
    if (actions.length > 0) {
        self.registration.showNotification('Синхронизация', {
            body: `Синхронизировано ${actions.length} действий`,
            icon: '/icons/icon-192x192.png',
        });
    }
}

function getPendingActions() {
    return new Promise((resolve, reject) => {
        const req = indexedDB.open('SyncDB', 1);
        req.onsuccess = e => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('pendingActions')) { resolve([]); db.close(); return; }
            const tx = db.transaction(['pendingActions'], 'readonly');
            const all = tx.objectStore('pendingActions').getAll();
            all.onsuccess = () => { resolve(all.result); db.close(); };
        };
        req.onerror = () => resolve([]);
    });
}

function removePendingAction(id) {
    return new Promise(resolve => {
        const req = indexedDB.open('SyncDB', 1);
        req.onsuccess = e => {
            const db = e.target.result;
            db.transaction(['pendingActions'], 'readwrite').objectStore('pendingActions').delete(id);
            db.close(); resolve();
        };
        req.onerror = () => resolve();
    });
}
