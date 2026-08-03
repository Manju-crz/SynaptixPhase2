/**
 * Form Validation Utilities
 * Reusable validation functions for form inputs
 */

const Validators = {
    /**
     * Check if value is not empty
     */
    isNotEmpty(value) {
        return value !== null && value !== undefined && value.trim() !== '';
    },

    /**
     * Validate URL format
     */
    isUrl(value) {
        try {
            new URL(value);
            return true;
        } catch {
            return false;
        }
    },

    /**
     * Validate if value is a valid HTTP/HTTPS URL
     */
    isHttpUrl(value) {
        if (!this.isUrl(value)) return false;
        const url = new URL(value);
        return url.protocol === 'http:' || url.protocol === 'https:';
    },

    /**
     * Validate Excel file extension
     */
    isExcelFile(filename) {
        if (!filename) return false;
        const ext = filename.toLowerCase().split('.').pop();
        return ext === 'xlsx' || ext === 'xls';
    },

    /**
     * Validate if value matches a pattern
     */
    matchesPattern(value, pattern) {
        if (!value) return false;
        const regex = new RegExp(pattern);
        return regex.test(value);
    },

    /**
     * Validate if value is a number
     */
    isNumber(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    },

    /**
     * Validate if value is within a range
     */
    isInRange(value, min, max) {
        if (!this.isNumber(value)) return false;
        const num = parseFloat(value);
        return num >= min && num <= max;
    },

    /**
     * Validate email format
     */
    isEmail(value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(value);
    },

    /**
     * Validate minimum length
     */
    minLength(value, length) {
        return value && value.length >= length;
    },

    /**
     * Validate maximum length
     */
    maxLength(value, length) {
        return value && value.length <= length;
    },

    /**
     * Validate if value is a valid JSON
     */
    isJson(value) {
        try {
            JSON.parse(value);
            return true;
        } catch {
            return false;
        }
    },

    /**
     * Validate file size (in bytes)
     */
    isValidFileSize(file, maxSizeInMB) {
        if (!file) return false;
        const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
        return file.size <= maxSizeInBytes;
    },

    /**
     * Custom validation with error message
     */
    validate(value, rules) {
        const errors = [];

        for (const rule of rules) {
            const { validator, message, ...params } = rule;

            let isValid = false;
            if (typeof validator === 'function') {
                isValid = validator(value, params);
            } else if (typeof this[validator] === 'function') {
                isValid = this[validator](value, ...Object.values(params));
            }

            if (!isValid) {
                errors.push(message);
            }
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }
};

/**
 * Form Validator Class
 * Validates entire forms with multiple fields
 */
class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.fields = new Map();
    }

    addField(fieldId, rules) {
        this.fields.set(fieldId, rules);
        return this;
    }

    validateField(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return { isValid: false, errors: ['Field not found'] };

        const rules = this.fields.get(fieldId);
        if (!rules) return { isValid: true, errors: [] };

        return Validators.validate(field.value, rules);
    }

    validateAll() {
        const results = {};
        let isFormValid = true;

        for (const [fieldId, rules] of this.fields) {
            const result = this.validateField(fieldId);
            results[fieldId] = result;
            if (!result.isValid) {
                isFormValid = false;
            }
        }

        return {
            isValid: isFormValid,
            fields: results
        };
    }

    showErrors(fieldId, errors) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        // Remove existing error messages
        this.clearErrors(fieldId);

        // Add error class to field
        field.classList.add('error');

        // Create error message container
        const errorContainer = document.createElement('div');
        errorContainer.className = 'field-error';
        errorContainer.id = `${fieldId}-error`;
        errorContainer.innerHTML = errors.map(err => `<div>${err}</div>`).join('');

        // Insert after field
        field.parentNode.insertBefore(errorContainer, field.nextSibling);
    }

    clearErrors(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.remove('error');
        }

        const errorContainer = document.getElementById(`${fieldId}-error`);
        if (errorContainer) {
            errorContainer.remove();
        }
    }

    clearAllErrors() {
        for (const fieldId of this.fields.keys()) {
            this.clearErrors(fieldId);
        }
    }
}
