
const express = require('express');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

// Homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Success page
app.get('/success', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'success.html'));
});

// Forward form submission to Flask
app.post('/submit', async (req, res) => {
    try {
        const response = await axios.post(
            `${process.env.BACKEND_URL}/submit`,
            req.body
        );

        res.status(response.status).json(response.data);

    } catch (error) {
        console.error('Backend error:', error.message);

        res.status(error.response?.status || 502).json(
            error.response?.data || {
                error: 'Unable to connect to Flask backend'
            }
        );
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Express frontend running on port ${PORT}`);
});
