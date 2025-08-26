const express = require('express');
const multer = require('multer');
const jobController = require('../controllers/jobController');

const router = express.Router();

// Configure multer for temporary file storage
const upload = multer({ dest: 'uploads/' });

// Define API routes
router.post('/upload', upload.single('resume'), jobController.uploadResume);
router.get('/matches/:resumeId', jobController.getMatches);

module.exports = router;