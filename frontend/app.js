/**
 * API Client and Utility Functions
 * Privacy-Preserving Virtual Identity System
 */

const API_BASE_URL = 'https://htp-comi.onrender.com';
/**
 * Make an API request
 */
async function apiRequest(endpoint, method = 'GET', body = null, requiresAuth = false) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (requiresAuth) {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        method,
        headers
    };
    
    if (body) {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

/**
 * Get current user from localStorage
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

/**
 * Format date/time
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

/**
 * Format time remaining
 */
function formatTimeRemaining(expiryString) {
    const expiry = new Date(expiryString);
    const now = new Date();
    const diff = expiry - now;
    
    if (diff <= 0) {
        return 'Expired';
    }
    
    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    
    if (minutes > 0) {
        return `${minutes}m ${seconds}s`;
    }
    return `${seconds}s`;
}

/**
 * Generate QR code using qrcode.js library
 */
function generateQRCode(data, elementId) {
    const qrData = typeof data === 'string' ? data : JSON.stringify(data);
    
    // Clear existing QR code
    const element = document.getElementById(elementId);
    element.innerHTML = '';
    
    // Generate new QR code
    new QRCode(element, {
        text: qrData,
        width: 256,
        height: 256,
        colorDark: '#000000',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.H
    });
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        return true;
    }
}
