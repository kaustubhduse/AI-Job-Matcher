require('dotenv').config();
const express = require('express');
const cors = require('cors');
const apiRoutes = require('./src/routes/api');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// API Routes
app.use('/api', apiRoutes);

// Health check route
app.get('/', (req, res) => {
    res.send('Backend server is running!');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});