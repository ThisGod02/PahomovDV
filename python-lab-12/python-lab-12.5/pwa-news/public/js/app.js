// Состояние приложения
const state = {
    currentCategory: 'general',
    articles: [],
    isLoading: false,
    error: null,
    isOffline: !navigator.onLine,
    searchMode: false,
};

const newsGrid = document.getElementById('newsGrid');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const offlineIndicator = document.getElementById('offlineIndicator');
const navButtons = document.querySelectorAll('.nav-btn');
const searchBar = document.getElementById('searchBar');
const searchInput = document.getElementById('searchInput');

document.addEventListener('DOMContentLoaded', () => {
    loadNews(state.currentCategory);
    setupEventListeners();
    checkOnlineStatus();
    cleanOldCache();
});

function setupEventListeners() {
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            setActiveCategory(btn.dataset.category);
            state.searchMode = false;
            searchBar.classList.add('hidden');
            loadNews(btn.dataset.category);
        });
    });
    document.getElementById('searchToggle').addEventListener('click', toggleSearch);
    document.getElementById('searchBtn').addEventListener('click', performSearch);
    document.getElementById('searchClose').addEventListener('click', closeSearch);
    searchInput.addEventListener('keypress', e => { if (e.key === 'Enter') performSearch(); });
    document.getElementById('retryBtn').addEventListener('click', () => loadNews(state.currentCategory));
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
}

function setActiveCategory(category) {
    state.currentCategory = category;
    navButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.category === category));
}

function toggleSearch() {
    searchBar.classList.toggle('hidden');
    if (!searchBar.classList.contains('hidden')) { searchInput.focus(); state.searchMode = true; }
}

function closeSearch() {
    searchBar.classList.add('hidden');
    state.searchMode = false;
    searchInput.value = '';
    loadNews(state.currentCategory);
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;
    state.isLoading = true; updateUI();
    try {
        const res = await fetch(`/api/news/search?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        displayNews(data.articles);
    } catch {
        loadCachedNews();
    } finally {
        state.isLoading = false; updateUI();
    }
}

async function loadNews(category) {
    state.isLoading = true; state.error = null; updateUI();
    try {
        const res = await fetch(`/api/news?category=${category}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        displayNews(data.articles);
        cacheNews(category, data.articles);
    } catch {
        state.error = 'Ошибка загрузки';
        loadCachedNews(category);
    } finally {
        state.isLoading = false; updateUI();
    }
}

function displayNews(articles) {
    if (!articles || articles.length === 0) {
        newsGrid.innerHTML = '<p style="padding:2rem;text-align:center">Новости не найдены</p>';
        return;
    }
    state.articles = articles;
    newsGrid.innerHTML = articles.map((a, i) => createCard(a, i)).join('');
    document.querySelectorAll('.news-card').forEach((card, i) => {
        card.addEventListener('click', () => {
            if (articles[i].url && articles[i].url !== '#') window.open(articles[i].url, '_blank');
        });
        // Кнопка сохранения
        card.querySelector('.save-btn')?.addEventListener('click', e => {
            e.stopPropagation();
            saveArticleForOffline(articles[i]);
        });
    });
}

function createCard(article, index) {
    const date = article.publishedAt ? new Date(article.publishedAt).toLocaleDateString('ru-RU') : '';
    const img = article.urlToImage
        ? `<img src="${article.urlToImage}" alt="${article.title}" loading="lazy" onerror="this.style.display='none'">`
        : '';
    return `
    <div class="news-card ${article._cached ? 'offline' : ''}">
        ${article._cached ? '<span class="offline-badge">Сохранено</span>' : ''}
        ${img}
        <div class="news-content">
            <h3 class="news-title">${article.title || 'Без заголовка'}</h3>
            <p class="news-description">${article.description || ''}</p>
            <div class="news-meta">
                <span class="news-source">${article.source?.name || ''}</span>
                <span>${date}</span>
            </div>
            <button class="save-btn" title="Сохранить для офлайн">💾 Сохранить</button>
        </div>
    </div>`;
}

function updateUI() {
    loadingSpinner.classList.toggle('hidden', !state.isLoading);
    newsGrid.classList.toggle('hidden', state.isLoading || !!state.error);
    errorMessage.classList.toggle('hidden', !state.error || state.isLoading);
}

function checkOnlineStatus() { state.isOffline = !navigator.onLine; updateOfflineIndicator(); }
function handleOnline() { state.isOffline = false; updateOfflineIndicator(); if (!state.searchMode) loadNews(state.currentCategory); }
function handleOffline() { state.isOffline = true; updateOfflineIndicator(); loadCachedNews(state.currentCategory); }
function updateOfflineIndicator() { offlineIndicator.classList.toggle('hidden', !state.isOffline); }

// ── Кэширование через Cache API ──────────────────────────
async function cacheNews(category, articles) {
    if (!('caches' in window)) return;
    try {
        const cache = await caches.open('news-cache');
        const tagged = articles.map(a => ({ ...a, _cached: true, _cachedAt: Date.now() }));
        await cache.put(`/api/news?category=${category}`,
            new Response(JSON.stringify(tagged), { headers: { 'Content-Type': 'application/json' } }));
    } catch (e) { console.error('Cache error', e); }
}

async function loadCachedNews(category = state.currentCategory) {
    if (!('caches' in window)) return;
    try {
        const cache = await caches.open('news-cache');
        const res = await cache.match(`/api/news?category=${category}`);
        if (res) displayNews(await res.json());
    } catch (e) { console.error('Load cache error', e); }
}

// ── IndexedDB: сохранение статьи для офлайн-чтения ──────
function saveArticleForOffline(article) {
    if (!('indexedDB' in window)) { alert('IndexedDB не поддерживается'); return; }
    const req = indexedDB.open('NewsDB', 1);
    req.onupgradeneeded = e => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains('savedArticles')) {
            const store = db.createObjectStore('savedArticles', { keyPath: 'url' });
            store.createIndex('savedAt', 'savedAt', { unique: false });
        }
    };
    req.onsuccess = e => {
        const db = e.target.result;
        const tx = db.transaction(['savedArticles'], 'readwrite');
        tx.objectStore('savedArticles').put({ ...article, savedAt: Date.now(), _cached: true });
        tx.oncomplete = () => { showToast('Статья сохранена 💾'); db.close(); };
        tx.onerror = () => { showToast('Ошибка сохранения', true); db.close(); };
    };
}

async function loadSavedArticles() {
    return new Promise((resolve, reject) => {
        const req = indexedDB.open('NewsDB', 1);
        req.onerror = () => reject(req.error);
        req.onsuccess = e => {
            const db = e.target.result;
            const tx = db.transaction(['savedArticles'], 'readonly');
            const getAll = tx.objectStore('savedArticles').getAll();
            getAll.onsuccess = () => { resolve(getAll.result); db.close(); };
            getAll.onerror = () => { reject(getAll.error); db.close(); };
        };
    });
}

function cleanOldCache(maxAge = 30 * 24 * 60 * 60 * 1000) {
    if (!('indexedDB' in window)) return;
    const req = indexedDB.open('NewsDB', 1);
    req.onsuccess = e => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains('savedArticles')) { db.close(); return; }
        const tx = db.transaction(['savedArticles'], 'readwrite');
        const store = tx.objectStore('savedArticles');
        const index = store.index('savedAt');
        const range = IDBKeyRange.upperBound(Date.now() - maxAge);
        index.openCursor(range).onsuccess = ev => {
            const cursor = ev.target.result;
            if (cursor) { store.delete(cursor.primaryKey); cursor.continue(); }
        };
        tx.oncomplete = () => db.close();
    };
}

function showToast(msg, isError = false) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = `position:fixed;bottom:80px;left:50%;transform:translateX(-50%);
        background:${isError ? '#ef4444' : '#22c55e'};color:white;padding:.6rem 1.2rem;
        border-radius:20px;font-size:.9rem;z-index:9999;`;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}
