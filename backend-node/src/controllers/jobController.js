const fs = require('fs');
const parserService = require('../services/parserService');

/**
 * Handles the resume upload process.
 */
const uploadResume = async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No resume file uploaded.' });
    }

    const filePath = req.file.path;

    try {
        const result = await parserService.sendResumeToParser(filePath, req.file.originalname);
        res.status(200).json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    } finally {
        // Clean up the temporarily uploaded file
        fs.unlink(filePath, (err) => {
            if (err) console.error("Error deleting temp file:", err);
        });
    }
};

/**
 * Fetches job matches for a given resume.
 */
const getMatches = async (req, res) => {
    const { resumeId } = req.params;
    if (!resumeId) {
        return res.status(400).json({ error: 'Resume ID is required.' });
    }

    try {
        const matches = await parserService.fetchJobMatches(parseInt(resumeId, 10));
        res.status(200).json(matches);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};


module.exports = {
    uploadResume,
    getMatches,
};