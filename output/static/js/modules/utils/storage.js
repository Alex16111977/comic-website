function hasLocalStorage() {
    try {
        return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
    } catch (error) {
        return false;
    }
}

export function readJSON(key, fallback = null) {
    if (!hasLocalStorage()) {
        return fallback;
    }

    try {
        const stored = window.localStorage.getItem(key);
        if (!stored) {
            return fallback;
        }
        return JSON.parse(stored);
    } catch (error) {
        console.warn('[Storage] Failed to read key', key, error);
        return fallback;
    }
}

export function writeJSON(key, value) {
    if (!hasLocalStorage()) {
        return false;
    }

    try {
        window.localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.warn('[Storage] Failed to write key', key, error);
        return false;
    }
}

export function onStorageChange(key, callback) {
    if (typeof window === 'undefined' || typeof window.addEventListener !== 'function') {
        return () => {};
    }

    const handler = event => {
        if (!event || event.key !== key) {
            return;
        }
        callback(event);
    };

    window.addEventListener('storage', handler);
    return () => window.removeEventListener('storage', handler);
}
