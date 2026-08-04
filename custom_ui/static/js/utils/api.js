/**
 * API Utility
 * Centralized API call wrapper with error handling
 */

class ApiClient {
    constructor() {
        this.baseUrl = '';
        this.defaultTimeout = 30000;
    }

    /**
     * Make a fetch request with error handling
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = this.baseUrl + endpoint;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        const fetchOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, fetchOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * GET request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Additional options
     * @returns {Promise<Object>} Response data
     */
    async get(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'GET',
            ...options
        });
    }

    /**
     * POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body data
     * @param {Object} options - Additional options
     * @returns {Promise<Object>} Response data
     */
    async post(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            ...options
        });
    }

    /**
     * PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body data
     * @param {Object} options - Additional options
     * @returns {Promise<Object>} Response data
     */
    async put(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
            ...options
        });
    }

    /**
     * DELETE request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Additional options
     * @returns {Promise<Object>} Response data
     */
    async delete(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'DELETE',
            ...options
        });
    }
}

// Create global instance
const apiClient = new ApiClient();

// Convenience functions for common API calls
const API = {
    /**
     * Get list of Excel files
     */
    getExcelFiles: () => apiClient.get('/get-excel-files'),

    /**
     * Run Swagger scraper
     */
    runSwaggerScraper: (url) => apiClient.post('/run-test', { url }),

    /**
     * Run OpenAPI JSON parser
     */
    runOpenApiParser: (url) => apiClient.post('/run-json-parser', { url }),

    /**
     * Run executor
     */
    runExecutor: (data) => apiClient.post('/run-executor', data),

    /**
     * Run generator
     */
    runGenerator: (data) => apiClient.post('/run-generator', data),

    /**
     * Execute test
     */
    executeTest: (data) => apiClient.post('/execute-test', data),

    /**
     * Generate Allure report
     */
    generateAllureReport: (data) => apiClient.post('/generate-allure-report', data)
};
