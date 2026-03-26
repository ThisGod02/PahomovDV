const express = require('express');
const path = require('path');
const cors = require('cors');
const axios = require('axios');
const webPush = require('web-push');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

let subscriptions = [];

app.get('/api/news', async (req, res) => {
    try {
        const category = req.query.category || 'general';
        const response = await axios.get(`${process.env.NEWS_API_URL}/top-headlines`, {
            params: { country: 'ru', category, apiKey: process.env.NEWS_API_KEY, pageSize: 20 }
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed' });
    }
});

app.get('/api/categories', (req, res) => {
    res.json(['general', 'technology', 'science', 'sports', 'entertainment']);
});

app.post('/api/subscribe', (req, res) => {
    const subscription = req.body;
    if (!subscriptions.some(sub => sub.endpoint === subscription.endpoint)) {
        subscriptions.push(subscription);
    }
    res.status(201).json({ message: 'Subscribed' });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
