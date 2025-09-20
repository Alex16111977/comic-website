const STORAGE_PREFIX = 'liraJourney';
const REVIEW_QUEUE_KEY = `${STORAGE_PREFIX}:reviewQueue`;
const ID_KEYS = new Set(['wordId', 'characterId', 'phaseId']);
let lastQueue = [];

const hasStorage = () => typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
const clone = value => Array.isArray(value)
    ? value.map(clone)
    : (value && typeof value === 'object' ? Object.fromEntries(Object.entries(value).map(([k, v]) => [k, clone(v)])) : value);

function sanitizeItem(item) {
    if (!item || typeof item !== 'object') return null;
    const sanitized = {};
    for (const [key, raw] of Object.entries(item)) {
        if (raw === undefined || raw === null) continue;
        if (ID_KEYS.has(key)) {
            const normalized = typeof raw === 'string' ? raw.trim() : String(raw);
            if (!normalized) continue;
            sanitized[key] = normalized;
            continue;
        }
        if (typeof raw === 'string') {
            const trimmed = raw.trim();
            if (trimmed) sanitized[key] = trimmed;
            continue;
        }
        if (Array.isArray(raw)) {
            sanitized[key] = raw.slice();
            continue;
        }
        if (raw && typeof raw === 'object') {
            const nested = sanitizeItem(raw);
            sanitized[key] = nested || { ...raw };
            continue;
        }
        sanitized[key] = raw;
    }
    return Object.keys(sanitized).length ? sanitized : null;
}

function readQueue() {
    if (!hasStorage()) return [];
    try {
        const stored = window.localStorage.getItem(REVIEW_QUEUE_KEY);
        if (!stored) return [];
        const parsed = JSON.parse(stored);
        if (!Array.isArray(parsed)) return [];
        return parsed.map(item => sanitizeItem(item) || (item && typeof item === 'object' ? { ...item } : null)).filter(Boolean);
    } catch (error) {
        console.warn('[ReviewQueue] Unable to read queue', error);
        return [];
    }
}

function writeQueue(queue) {
    if (!hasStorage() || !Array.isArray(queue)) return false;
    try {
        window.localStorage.setItem(REVIEW_QUEUE_KEY, JSON.stringify(queue));
        lastQueue = queue.map(clone);
        return true;
    } catch (error) {
        console.warn('[ReviewQueue] Unable to write queue', error);
        return false;
    }
}

const isObject = value => value && typeof value === 'object' && !Array.isArray(value);
const deepEqual = (a, b) => {
    if (a === b) return true;
    if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((item, idx) => deepEqual(item, b[idx]));
    if (isObject(a) && isObject(b)) {
        const keys = Object.keys(a);
        return keys.length === Object.keys(b).length && keys.every(key => deepEqual(a[key], b[key]));
    }
    return false;
};

function mergeEntries(base, incoming) {
    if (!base) return incoming ? clone(incoming) : base;
    if (!incoming) return clone(base);
    const merged = { ...base };
    for (const [key, value] of Object.entries(incoming)) {
        if (value === undefined) continue;
        if (merged[key] === undefined || merged[key] === null) {
            merged[key] = clone(value);
            continue;
        }
        if (Array.isArray(merged[key]) && Array.isArray(value)) {
            const existing = merged[key].slice();
            value.forEach(item => { if (!existing.some(entry => deepEqual(entry, item))) existing.push(item); });
            merged[key] = existing;
            continue;
        }
        if (isObject(merged[key]) && isObject(value)) {
            merged[key] = mergeEntries(merged[key], value);
            continue;
        }
    }
    return merged;
}

function keyForItem(item) {
    if (!item || typeof item !== 'object') return null;
    if (item.wordId) return `word:${item.wordId}`;
    if (item.characterId && item.phaseId) return `phase:${item.characterId}::${item.phaseId}`;
    if (item.characterId) return `character:${item.characterId}`;
    if (item.phaseId) return `phase:${item.phaseId}`;
    return null;
}

function mergeQueues(existing, incoming) {
    const map = new Map();
    const order = [];
    let fallback = 0;
    const add = (raw, origin) => {
        const sanitized = sanitizeItem(raw) || (raw && typeof raw === 'object' ? { ...raw } : null);
        if (!sanitized) return;
        const key = keyForItem(sanitized) || `${origin}:${fallback++}`;
        const next = map.has(key) ? mergeEntries(map.get(key), sanitized) : clone(sanitized);
        if (!map.has(key)) order.push(key);
        map.set(key, next);
    };
    (existing || []).forEach(item => add(item, 'existing'));
    (incoming || []).forEach(item => add(item, 'dom'));
    return order.map(key => map.get(key));
}

const normalizeId = value => {
    if (value === undefined || value === null) return '';
    return typeof value === 'string' ? value.trim() : String(value);
};

function extractDomItems() {
    if (typeof document === 'undefined') return [];
    return Array.from(document.querySelectorAll('.review-card')).map(card => {
        const dataset = card.dataset || {};
        const item = sanitizeItem({
            wordId: dataset.wordId,
            characterId: dataset.characterId,
            phaseId: dataset.phaseId,
            word: card.querySelector('.review-word')?.textContent?.trim(),
            translation: card.querySelector('.review-translation')?.textContent?.trim(),
            example: card.querySelector('.review-example')?.textContent?.replace(/[«»]/g, '').trim(),
            practiceUrl: card.querySelector('.review-link')?.getAttribute('href'),
            tags: Array.from(card.querySelectorAll('.review-tag')).map(tag => tag.textContent?.trim()).filter(Boolean),
        });
        return item;
    }).filter(Boolean);
}

const tupleFromCard = card => ({
    wordId: normalizeId(card?.dataset?.wordId),
    characterId: normalizeId(card?.dataset?.characterId),
    phaseId: normalizeId(card?.dataset?.phaseId),
});

function matchesEntry(entry, tuple) {
    return entry
        && normalizeId(entry.wordId) === tuple.wordId
        && normalizeId(entry.characterId) === tuple.characterId
        && normalizeId(entry.phaseId) === tuple.phaseId;
}

async function persistRemoval(tuple) {
    if (typeof fetch !== 'function') throw new Error('Fetch API unavailable');
    const response = await fetch('/api/review-queue/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            wordId: tuple.wordId || '',
            characterId: tuple.characterId || '',
            phaseId: tuple.phaseId || '',
        }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json().catch(() => null);
    if (payload && payload.success === false) {
        throw new Error(payload.error || payload.message || 'Removal rejected');
    }
    return payload;
}

async function removeCard(card) {
    if (!card) return false;
    const tuple = tupleFromCard(card);
    const previous = readQueue();
    const nextQueue = previous.filter(item => !matchesEntry(item, tuple));
    writeQueue(nextQueue);
    try {
        await persistRemoval(tuple);
        if (card.parentElement && typeof card.parentElement.removeChild === 'function') {
            card.parentElement.removeChild(card);
        } else if (typeof card.remove === 'function') {
            card.remove();
        }
        return true;
    } catch (error) {
        console.error('[ReviewQueue] Removal failed', error);
        writeQueue(previous);
        card.classList?.add('remove-error');
        setTimeout(() => card.classList?.remove('remove-error'), 2500);
        throw error;
    }
}

function setupRemovalHandlers() {
    const grid = document.querySelector('.review-grid');
    if (!grid) return;
    grid.addEventListener('click', event => {
        const button = event.target && event.target.closest('.review-remove');
        if (!button || button.disabled) return;
        const card = button.closest('.review-card');
        if (!card) return;
        event.preventDefault();
        button.disabled = true;
        removeCard(card).catch(() => { button.disabled = false; });
    });
}

function syncQueue() {
    lastQueue = readQueue();
    const domItems = extractDomItems();
    const merged = mergeQueues(lastQueue, domItems);
    if (Array.isArray(merged)) {
        if (!merged.length && lastQueue.length) {
            writeQueue(lastQueue);
        } else {
            writeQueue(merged);
        }
    }
    setupRemovalHandlers();
}

export function initReviewQueue() {
    if (typeof document === 'undefined') return;
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', syncQueue, { once: true });
    } else {
        syncQueue();
    }
}

if (typeof window !== 'undefined') {
    window.reviewQueueIndex = {
        initReviewQueue,
        readQueue,
        writeQueue,
        extractDomItems,
        mergeQueues,
        removeCard,
        setupRemovalHandlers,
    };
}
