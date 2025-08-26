const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const parserApi = axios.create({
    baseURL: process.env.PARSER_SERVICE_URL,
});

/**
 * Sends a resume file to the Python parser service.
 * @param {string} filePath - The path to the temporary file.
 * @param {string} originalName - The original name of the file.
 * @returns {Promise<object>} The response data from the parser service.
 */
const sendResumeToParser = async (filePath, originalName) => {
    const formData = new FormData();
    formData.append('file', fs.createReadStream(filePath), originalName);

    try {
        const response = await parserApi.post('/api/v1/parse-resume/', formData, {
            headers: formData.getHeaders(),
        });
        return response.data;
    } catch (error) {
        console.error("Error sending file to parser:", error.response ? error.response.data : error.message);
        throw new Error("Failed to communicate with the parser service.");
    }
};

/**
 * Fetches job matches for a given resume ID from the parser service.
 * @param {number} resumeId - The ID of the resume.
 * @returns {Promise<object>} The job matches from the parser service.
 */
const fetchJobMatches = async (resumeId) => {
    try {
        const response = await parserApi.get(`/api/v1/match-jobs/${resumeId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching matches from parser:", error.response ? error.response.data : error.message);
        throw new Error("Failed to get job matches from the parser service.");
    }
};


module.exports = {
    sendResumeToParser,
    fetchJobMatches,
};