/**
 * Storage Utility
 * Wrapper for localStorage with error handling and JSON support
 */

const Storage = {
    /**
     * Save data to localStorage
     */
    save(key, value) {
        try {
            const serialized = typeof value === 'object' 
                ? JSON.stringify(value) 
                : String(value);
            localStorage.setItem(key, serialized);
            return true;
        } catch (error) {
            console.error('Storage.save error:', error);
            return false;
        }
    },

    /**
     * Load data from localStorage
     */
    load(key, defaultValue = null) {
        try {
            const value = localStorage.getItem(key);
            if (value === null) return defaultValue;

            // Try to parse as JSON, fallback to string
            try {
                return JSON.parse(value);
            } catch {
                return value;
            }
        } catch (error) {
            console.error('Storage.load error:', error);
            return defaultValue;
        }
    },

    /**
     * Remove item from localStorage
     */
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Storage.remove error:', error);
            return false;
        }
    },

    /**
     * Clear all localStorage
     */
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Storage.clear error:', error);
            return false;
        }
    },

    /**
     * Check if key exists
     */
    has(key) {
        return localStorage.getItem(key) !== null;
    },

    /**
     * Get all keys
     */
    keys() {
        return Object.keys(localStorage);
    },

    /**
     * Get storage size in bytes
     */
    getSize() {
        let size = 0;
        for (const key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                size += localStorage[key].length + key.length;
            }
        }
        return size;
    },

    /**
     * Save with expiration
     */
    saveWithExpiry(key, value, expiryInMinutes) {
        const now = new Date();
        const item = {
            value: value,
            expiry: now.getTime() + (expiryInMinutes * 60 * 1000)
        };
        return this.save(key, item);
    },

    /**
     * Load with expiration check
     */
    loadWithExpiry(key, defaultValue = null) {
        const item = this.load(key);
        if (!item) return defaultValue;

        const now = new Date();
        if (now.getTime() > item.expiry) {
            this.remove(key);
            return defaultValue;
        }

        return item.value;
    }
};

/**
 * Session Storage Utility
 * Same interface as Storage but uses sessionStorage
 */
const SessionStorage = {
    save(key, value) {
        try {
            const serialized = typeof value === 'object' 
                ? JSON.stringify(value) 
                : String(value);
            sessionStorage.setItem(key, serialized);
            return true;
        } catch (error) {
            console.error('SessionStorage.save error:', error);
            return false;
        }
    },

    load(key, defaultValue = null) {
        try {
            const value = sessionStorage.getItem(key);
            if (value === null) return defaultValue;

            try {
                return JSON.parse(value);
            } catch {
                return value;
            }
        } catch (error) {
            console.error('SessionStorage.load error:', error);
            return defaultValue;
        }
    },

    remove(key) {
        try {
            sessionStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('SessionStorage.remove error:', error);
            return false;
        }
    },

    clear() {
        try {
            sessionStorage.clear();
            return true;
        } catch (error) {
            console.error('SessionStorage.clear error:', error);
            return false;
        }
    },

    has(key) {
        return sessionStorage.getItem(key) !== null;
    },

    keys() {
        return Object.keys(sessionStorage);
    }
};
