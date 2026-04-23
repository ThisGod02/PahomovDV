const express = require('express');
const path = require('path');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

// web-push опционально (если не установлен — push отключается)
let webPush;
try { webPush = require('web-push'); } catch (e) { webPush = null; }

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Настройка VAPID
if (webPush && process.env.VAPID_PUBLIC_KEY && process.env.VAPID_PRIVATE_KEY) {
  webPush.setVapidDetails(
    `mailto:${process.env.CONTACT_EMAIL || 'admin@example.com'}`,
    process.env.VAPID_PUBLIC_KEY,
    process.env.VAPID_PRIVATE_KEY
  );
}

let subscriptions = [];

// ── API: новости по категории ──────────────────────────────
app.get('/api/news', async (req, res) => {
  try {
    const category = req.query.category || 'general';
    if (!process.env.NEWS_API_KEY || process.env.NEWS_API_KEY === 'your_api_key_here') {
      // Возвращаем демо-данные если ключ не задан
      return res.json({ articles: getDemoArticles(category), status: 'demo' });
    }
    const response = await axios.get(`${process.env.NEWS_API_URL}/top-headlines`, {
      params: { country: 'ru', category, apiKey: process.env.NEWS_API_KEY, pageSize: 20 }
    });
    res.json(response.data);
  } catch (error) {
    console.error('News API error:', error.message);
    res.json({ articles: getDemoArticles(req.query.category || 'general'), status: 'fallback' });
  }
});

// ── API: поиск ────────────────────────────────────────────
app.get('/api/news/search', async (req, res) => {
  try {
    const query = req.query.q;
    if (!query) return res.status(400).json({ error: 'Query parameter required' });
    if (!process.env.NEWS_API_KEY || process.env.NEWS_API_KEY === 'your_api_key_here') {
      return res.json({ articles: getDemoArticles('general').filter(a =>
        a.title.toLowerCase().includes(query.toLowerCase())), status: 'demo' });
    }
    const response = await axios.get(`${process.env.NEWS_API_URL}/everything`, {
      params: { q: query, apiKey: process.env.NEWS_API_KEY, pageSize: 20, sortBy: 'relevancy' }
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to search news' });
  }
});

// ── API: категории (реализован TODO) ─────────────────────
app.get('/api/categories', (req, res) => {
  const categories = [
    { id: 'general', name: 'Главное', icon: '📰' },
    { id: 'technology', name: 'Технологии', icon: '💻' },
    { id: 'science', name: 'Наука', icon: '🔬' },
    { id: 'sports', name: 'Спорт', icon: '⚽' },
    { id: 'entertainment', name: 'Культура', icon: '🎭' },
    { id: 'business', name: 'Бизнес', icon: '💼' },
    { id: 'health', name: 'Здоровье', icon: '🏥' },
  ];
  res.json(categories);
});

// ── API: архив новостей по дате (реализован TODO) ────────
app.get('/api/news/archive', async (req, res) => {
  try {
    const { date, category = 'general' } = req.query;
    if (!date) return res.status(400).json({ error: 'Date parameter required' });
    if (!process.env.NEWS_API_KEY || process.env.NEWS_API_KEY === 'your_api_key_here') {
      return res.json({ articles: getDemoArticles(category), status: 'demo' });
    }
    const response = await axios.get(`${process.env.NEWS_API_URL}/everything`, {
      params: {
        q: category === 'general' ? 'news' : category,
        from: date, to: date,
        sortBy: 'publishedAt',
        apiKey: process.env.NEWS_API_KEY,
        pageSize: 50,
        language: 'ru',
      }
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch archive news' });
  }
});

// ── Push-уведомления ──────────────────────────────────────
app.get('/api/vapid-public-key', (req, res) => {
  res.json({ publicKey: process.env.VAPID_PUBLIC_KEY || null });
});

app.post('/api/subscribe', (req, res) => {
  const subscription = req.body;
  if (!subscriptions.some(s => s.endpoint === subscription.endpoint)) {
    subscriptions.push(subscription);
  }
  res.status(201).json({ message: 'Subscribed successfully' });
});

app.post('/api/unsubscribe', (req, res) => {
  subscriptions = subscriptions.filter(s => s.endpoint !== req.body.endpoint);
  res.json({ message: 'Unsubscribed successfully' });
});

app.post('/api/send-notification', async (req, res) => {
  if (!webPush) return res.status(503).json({ error: 'web-push not configured' });
  const { title, body, url } = req.body;
  const payload = JSON.stringify({
    title: title || 'Новости PWA',
    body: body || 'Есть новые статьи для вас',
    url: url || '/',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
  });
  await Promise.all(subscriptions.map(sub =>
    webPush.sendNotification(sub, payload).catch(err => {
      if (err.statusCode === 410) subscriptions = subscriptions.filter(s => s.endpoint !== sub.endpoint);
    })
  ));
  res.json({ message: `Sent to ${subscriptions.length} subscribers` });
});

// SPA fallback
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));

// ── Демо-данные ───────────────────────────────────────────
function getDemoArticles(category) {
  const now = new Date().toISOString();
  return [
    { title: `[${category}] Демо-статья 1: Технологии будущего`, description: 'Описание первой демо-статьи о технологиях.', url: '#', urlToImage: null, publishedAt: now, source: { name: 'Демо-источник' } },
    { title: `[${category}] Демо-статья 2: Наука и открытия`, description: 'Описание второй демо-статьи о науке.', url: '#', urlToImage: null, publishedAt: now, source: { name: 'Демо-источник' } },
    { title: `[${category}] Демо-статья 3: Мировые события`, description: 'Описание третьей демо-статьи.', url: '#', urlToImage: null, publishedAt: now, source: { name: 'Демо-источник' } },
  ];
}
