const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const port = 3000;

// Настройка шаблонизатора EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// БД
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

// ❌ Hardcoded API key
const API_KEY = 'test-api-key-12345';

// ── Маршруты ──────────────────────────────────────────────────────

app.get('/', (req, res) => {
    db.all(`SELECT * FROM comments ORDER BY created_at DESC`, (err, comments) => {
        if (err) return res.status(500).send('Database error');
        res.render('index_vulnerable', { comments, error: null });
    });
});

app.post('/comment', (req, res) => {
    const { username, comment } = req.body;
    // ❌ Нет санитизации — XSS Stored
    db.run(`INSERT INTO comments (username, comment) VALUES (?, ?)`,
        [username || 'Anonymous', comment],
        (err) => {
            if (err) return res.status(500).send('Error saving comment');
            res.redirect('/');
        });
});

app.get('/api/comments', (req, res) => {
    const sort = req.query.sort || 'created_at DESC';
    // ❌ SQL Injection — динамическая сортировка без allow-list
    db.all(`SELECT * FROM comments ORDER BY ${sort}`, (err, comments) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(comments);
    });
});

app.get('/api/search', (req, res) => {
    const search = req.query.q || '';
    // ❌ SQL Injection
    db.all(`SELECT * FROM comments WHERE comment LIKE '%${search}%'`, (err, comments) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(comments);
    });
});

app.get('/api/config', (req, res) => {
    // ❌ Hardcoded secret + debug info
    res.json({ api_key: API_KEY, environment: 'development', debug: true });
});

app.listen(port, () => {
    console.log(`[VULNERABLE] App running at http://localhost:${port}`);
    console.log('Run: npm audit   to see dependency vulnerabilities');
});
