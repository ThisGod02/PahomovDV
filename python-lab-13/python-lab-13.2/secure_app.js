const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');
const path = require('path');

const app = express();
const port = 3001;

// ✅ ИСПРАВЛЕНИЕ 1: секрет из переменной окружения
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
    console.error('ERROR: API_KEY environment variable is not set');
    process.exit(1);
}

// ✅ ИСПРАВЛЕНИЕ 2: Allow-list для сортировки
const ALLOWED_SORT = ['created_at DESC', 'created_at ASC', 'username ASC', 'username DESC'];

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// ✅ ИСПРАВЛЕНИЕ 3: CSP middleware
app.use((req, res, next) => {
    const nonce = crypto.randomBytes(16).toString('base64');
    res.locals.nonce = nonce;
    res.setHeader('Content-Security-Policy',
        `default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline';`
    );
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    next();
});

const db = new sqlite3.Database(path.join(__dirname, 'comments.db'));

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    db.run(`INSERT OR IGNORE INTO comments (id, username, comment) VALUES
        (1, 'admin', 'Добро пожаловать на сайт!'),
        (2, 'user1', 'Отличный ресурс'),
        (3, 'user2', 'Очень полезная информация')`);
});

// ✅ Функция санитизации
const sanitizeHtml = (input) => {
    if (!input) return '';
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');
};

// ── Маршруты ──────────────────────────────────────────────────────

app.get('/', (req, res) => {
    db.all(`SELECT * FROM comments ORDER BY created_at DESC`, (err, comments) => {
        if (err) return res.status(500).send('Database error');
        res.render('index_secure', { comments, error: null, nonce: res.locals.nonce });
    });
});

app.post('/comment', (req, res) => {
    let { username, comment } = req.body;

    // ✅ ИСПРАВЛЕНИЕ 4: санитизация входных данных
    username = sanitizeHtml(username || 'Anonymous').substring(0, 50);
    comment  = sanitizeHtml(comment  || '').substring(0, 500);

    if (!comment.trim()) {
        return res.status(400).json({ error: 'Comment cannot be empty' });
    }

    // ✅ Параметризованный запрос
    db.run(`INSERT INTO comments (username, comment) VALUES (?, ?)`,
        [username, comment],
        (err) => {
            if (err) return res.status(500).send('Error saving comment');
            res.redirect('/');
        });
});

app.get('/api/comments', (req, res) => {
    const sortParam = req.query.sort || 'created_at DESC';

    // ✅ ИСПРАВЛЕНИЕ 5: allow-list для сортировки
    if (!ALLOWED_SORT.includes(sortParam)) {
        return res.status(400).json({ error: `Invalid sort. Allowed: ${ALLOWED_SORT.join(', ')}` });
    }

    db.all(`SELECT * FROM comments ORDER BY ${sortParam}`, (err, comments) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(comments);
    });
});

app.get('/api/search', (req, res) => {
    const search = (req.query.q || '').substring(0, 100);

    // ✅ ИСПРАВЛЕНИЕ 6: параметризованный запрос
    db.all(`SELECT * FROM comments WHERE comment LIKE ?`,
        [`%${search}%`],
        (err, comments) => {
            if (err) return res.status(500).json({ error: 'Database error' });
            res.json(comments);
        });
});

app.get('/api/config', (req, res) => {
    // ✅ ИСПРАВЛЕНИЕ 7: ключ не раскрывается, убран debug
    res.json({ environment: 'production', status: 'ok' });
});

// ✅ Глобальная обработка ошибок без раскрытия деталей
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(port, () => {
    console.log(`[SECURE] App running at http://localhost:${port}`);
});
