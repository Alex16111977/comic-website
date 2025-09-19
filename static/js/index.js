(function () {
    "use strict";

    const STORAGE_PREFIX = "liraJourney";
    const REVIEW_QUEUE_KEY = `${STORAGE_PREFIX}:reviewQueue`;
    const ID_KEYS = new Set(["wordId", "characterId", "phaseId"]);

    let lastReadQueue = [];

    function readQueueFromStorage() {
        if (typeof window === "undefined" || typeof localStorage === "undefined") {
            return [];
        }

        try {
            const storedValue = localStorage.getItem(REVIEW_QUEUE_KEY);
            if (!storedValue) {
                return [];
            }

            const parsed = JSON.parse(storedValue);
            if (!Array.isArray(parsed)) {
                return [];
            }

            return parsed
                .map(item => sanitizeQueueItem(item) || (item && typeof item === "object" ? { ...item } : null))
                .filter(Boolean);
        } catch (error) {
            console.warn("[ReviewQueue] Unable to read existing queue", error);
            return [];
        }
    }

    function writeQueueToStorage(queue) {
        if (typeof window === "undefined" || typeof localStorage === "undefined") {
            return false;
        }

        if (!Array.isArray(queue)) {
            return false;
        }

        try {
            localStorage.setItem(REVIEW_QUEUE_KEY, JSON.stringify(queue));
            lastReadQueue = queue.map(item => cloneValue(item));
            return true;
        } catch (error) {
            console.warn("[ReviewQueue] Unable to persist merged queue", error);
            return false;
        }
    }

    function sanitizeQueueItem(item) {
        if (!item || typeof item !== "object") {
            return null;
        }

        const sanitized = {};

        for (const [key, rawValue] of Object.entries(item)) {
            if (rawValue === undefined || rawValue === null) {
                continue;
            }

            if (ID_KEYS.has(key)) {
                if (typeof rawValue === "string") {
                    const trimmed = rawValue.trim();
                    if (!trimmed) {
                        continue;
                    }
                    sanitized[key] = trimmed;
                    continue;
                }

                if (typeof rawValue === "number" || typeof rawValue === "boolean") {
                    sanitized[key] = String(rawValue);
                    continue;
                }
            }

            if (typeof rawValue === "string") {
                const trimmed = rawValue.trim();
                if (!trimmed) {
                    continue;
                }
                sanitized[key] = trimmed;
                continue;
            }

            if (Array.isArray(rawValue)) {
                sanitized[key] = rawValue.slice();
                continue;
            }

            if (typeof rawValue === "object") {
                const nested = sanitizeQueueItem(rawValue);
                sanitized[key] = nested || { ...rawValue };
                continue;
            }

            sanitized[key] = rawValue;
        }

        if (!Object.keys(sanitized).length) {
            return null;
        }

        return sanitized;
    }

    function getDedupeKey(item) {
        if (!item || typeof item !== "object") {
            return null;
        }

        if (item.wordId) {
            return `word:${item.wordId}`;
        }

        if (item.characterId && item.phaseId) {
            return `phase:${item.characterId}::${item.phaseId}`;
        }

        if (item.characterId) {
            return `character:${item.characterId}`;
        }

        if (item.phaseId) {
            return `phase:${item.phaseId}`;
        }

        return null;
    }

    function mergeEntries(baseEntry, incomingEntry) {
        if (!baseEntry) {
            return incomingEntry ? { ...incomingEntry } : baseEntry;
        }

        if (!incomingEntry) {
            return { ...baseEntry };
        }

        const merged = { ...baseEntry };

        for (const [key, value] of Object.entries(incomingEntry)) {
            if (value === undefined) {
                continue;
            }

            if (merged[key] === undefined || merged[key] === null) {
                merged[key] = cloneValue(value);
                continue;
            }

            if (Array.isArray(merged[key]) && Array.isArray(value)) {
                const existingValues = merged[key].slice();
                value.forEach(item => {
                    if (!existingValues.some(existing => deepEqual(existing, item))) {
                        existingValues.push(item);
                    }
                });
                merged[key] = existingValues;
                continue;
            }

            if (isPlainObject(merged[key]) && isPlainObject(value)) {
                merged[key] = mergeEntries(merged[key], value);
            }
        }

        return merged;
    }

    function isPlainObject(value) {
        return value && typeof value === "object" && !Array.isArray(value);
    }

    function cloneValue(value) {
        if (Array.isArray(value)) {
            return value.map(cloneValue);
        }

        if (isPlainObject(value)) {
            const cloned = {};
            for (const [key, nested] of Object.entries(value)) {
                cloned[key] = cloneValue(nested);
            }
            return cloned;
        }

        return value;
    }

    function deepEqual(a, b) {
        if (a === b) {
            return true;
        }

        if (Array.isArray(a) && Array.isArray(b)) {
            if (a.length !== b.length) {
                return false;
            }
            return a.every((item, index) => deepEqual(item, b[index]));
        }

        if (isPlainObject(a) && isPlainObject(b)) {
            const aKeys = Object.keys(a);
            const bKeys = Object.keys(b);
            if (aKeys.length !== bKeys.length) {
                return false;
            }
            return aKeys.every(key => deepEqual(a[key], b[key]));
        }

        return false;
    }

    function extractDomQueueItems() {
        if (typeof document === "undefined") {
            return [];
        }

        const cards = Array.from(document.querySelectorAll(".review-card"));
        if (!cards.length) {
            return [];
        }

        return cards
            .map(card => {
                const dataset = card.dataset || {};
                const item = {};

                if (dataset.wordId) {
                    item.wordId = dataset.wordId;
                }
                if (dataset.characterId) {
                    item.characterId = dataset.characterId;
                }
                if (dataset.phaseId) {
                    item.phaseId = dataset.phaseId;
                }

                const wordElement = card.querySelector(".review-word");
                if (wordElement && wordElement.textContent) {
                    item.word = wordElement.textContent.trim();
                }

                const translationElement = card.querySelector(".review-translation");
                if (translationElement && translationElement.textContent) {
                    item.translation = translationElement.textContent.trim();
                }

                const exampleElement = card.querySelector(".review-example");
                if (exampleElement && exampleElement.textContent) {
                    const example = exampleElement.textContent.replace(/[«»]/g, "").trim();
                    if (example) {
                        item.example = example;
                    }
                }

                const practiceLink = card.querySelector(".review-link");
                if (practiceLink) {
                    const href = practiceLink.getAttribute("href");
                    if (href) {
                        item.practiceUrl = href;
                    }
                }

                const tags = Array.from(card.querySelectorAll(".review-tag"))
                    .map(tag => (tag.textContent || "").trim())
                    .filter(Boolean);
                if (tags.length) {
                    item.tags = tags;
                }

                return sanitizeQueueItem(item);
            })
            .filter(Boolean);
    }

    function mergeQueues(existingQueue, domItems) {
        const mergedMap = new Map();
        const order = [];
        let fallbackIndex = 0;

        const addItem = (rawItem, origin) => {
            const sanitized = sanitizeQueueItem(rawItem) || (rawItem && typeof rawItem === "object" ? { ...rawItem } : null);
            if (!sanitized) {
                return;
            }

            const key = getDedupeKey(sanitized);
            const prepared = cloneValue(sanitized);
            if (key && mergedMap.has(key)) {
                const mergedEntry = mergeEntries(mergedMap.get(key), prepared);
                mergedMap.set(key, mergedEntry);
                return;
            }

            const targetKey = key || `${origin}:${fallbackIndex++}`;
            if (mergedMap.has(targetKey)) {
                const mergedEntry = mergeEntries(mergedMap.get(targetKey), prepared);
                mergedMap.set(targetKey, mergedEntry);
            } else {
                mergedMap.set(targetKey, prepared);
                order.push(targetKey);
            }
        };

        if (Array.isArray(existingQueue)) {
            existingQueue.forEach(item => addItem(item, "existing"));
        }

        if (Array.isArray(domItems)) {
            domItems.forEach(item => addItem(item, "dom"));
        }

        return order.map(key => mergedMap.get(key));
    }

    function syncQueueFromDom() {
        lastReadQueue = readQueueFromStorage();
        const domQueueItems = extractDomQueueItems();
        return mergeQueues(lastReadQueue, domQueueItems);
    }

    if (typeof document !== "undefined" && document.addEventListener) {
        document.addEventListener("DOMContentLoaded", () => {
            const mergedQueue = syncQueueFromDom();
            if (!Array.isArray(mergedQueue)) {
                return;
            }

            if (!mergedQueue.length) {
                if (lastReadQueue.length) {
                    writeQueueToStorage(lastReadQueue);
                }
                return;
            }

            writeQueueToStorage(mergedQueue);
        });
    }

    if (typeof window !== "undefined") {
        window.reviewQueueIndex = {
            syncQueueFromDom,
            readQueueFromStorage,
            writeQueueToStorage,
            extractDomQueueItems,
            mergeQueues,
        };
    }
})();
