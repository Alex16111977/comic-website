import { qs, qsa } from '../utils/dom.js';
import { onStorageChange, readJSON, writeJSON } from '../utils/storage.js';
import { vibrate } from '../utils/animations.js';

const STORAGE_KEY = typeof window !== 'undefined' && window.REVIEW_QUEUE_KEY
    ? window.REVIEW_QUEUE_KEY
    : 'liraJourney:reviewQueue';

function sanitizeExample(example) {
    if (!example || typeof example !== 'object') {
        return null;
    }
    const german = typeof example.german === 'string' ? example.german : '';
    const russian = typeof example.russian === 'string' ? example.russian : '';
    if (!german && !russian) {
        return null;
    }
    return { german, russian };
}

function sanitizeEntry(entry) {
    if (!entry || typeof entry !== 'object') {
        return null;
    }
    const sanitized = { ...entry };
    sanitized.word = typeof sanitized.word === 'string' ? sanitized.word : '';
    sanitized.translation = typeof sanitized.translation === 'string' ? sanitized.translation : '';
    sanitized.russian_hint = typeof sanitized.russian_hint === 'string' ? sanitized.russian_hint : '';
    sanitized.transcription = typeof sanitized.transcription === 'string' ? sanitized.transcription : '';
    sanitized.characterId = typeof sanitized.characterId === 'string' ? sanitized.characterId : '';
    sanitized.phaseKey = typeof sanitized.phaseKey === 'string' ? sanitized.phaseKey : '';
    sanitized.sentence = typeof sanitized.sentence === 'string' ? sanitized.sentence : '';
    sanitized.sentenceTranslation = typeof sanitized.sentenceTranslation === 'string'
        ? sanitized.sentenceTranslation
        : '';
    sanitized.emoji = typeof sanitized.emoji === 'string' && sanitized.emoji ? sanitized.emoji : '📝';

    if (Array.isArray(sanitized.examples)) {
        sanitized.examples = sanitized.examples.map(sanitizeExample).filter(Boolean);
    } else {
        sanitized.examples = [];
    }

    if (!sanitized.examples.length && (sanitized.sentence || sanitized.sentenceTranslation)) {
        sanitized.examples.push({
            german: sanitized.sentence || '',
            russian: sanitized.sentenceTranslation || '',
        });
    }

    if (typeof sanitized.example !== 'string' || !sanitized.example) {
        sanitized.example = sanitized.sentence || '';
    }

    return sanitized;
}

function buildKey(source) {
    if (!source) {
        return null;
    }
    const wordValue = typeof source.word === 'string' ? source.word.trim().toLowerCase() : '';
    const characterValue = typeof source.characterId === 'string' ? source.characterId.trim() : '';
    if (!wordValue) {
        return null;
    }
    return `${characterValue || 'unknown'}::${wordValue}`;
}

export class StudyManager {
    constructor(options = {}) {
        this.characterId = typeof options.characterId === 'string'
            ? options.characterId
            : (typeof window.characterId === 'string' ? window.characterId : '');
        this.queue = [];
        this.lookup = new Map();
        this.initialized = false;
        this.unsubscribe = null;
    }

    init() {
        this.load();
        this.unsubscribe = onStorageChange(STORAGE_KEY, () => {
            this.load(true);
            this.refreshUI();
        });
        this.refreshUI();
    }

    destroy() {
        if (typeof this.unsubscribe === 'function') {
            this.unsubscribe();
        }
    }

    load(force = false) {
        if (this.initialized && !force) {
            return;
        }
        const stored = readJSON(STORAGE_KEY, []);
        this.queue = Array.isArray(stored) ? stored.map(sanitizeEntry).filter(Boolean) : [];
        this.rebuildLookup();
        this.initialized = true;
    }

    rebuildLookup() {
        this.lookup = new Map();
        this.queue.forEach(entry => {
            const key = buildKey(entry);
            if (key) {
                this.lookup.set(key, entry);
            }
        });
    }

    isInQueue(entry) {
        const key = buildKey(entry);
        return key ? this.lookup.has(key) : false;
    }

    add(entry) {
        const sanitized = sanitizeEntry({ characterId: this.characterId, ...entry });
        if (!sanitized) {
            return false;
        }
        const key = buildKey(sanitized);
        if (!key || this.lookup.has(key)) {
            return true;
        }
        const newQueue = this.queue.concat([sanitized]);
        if (!writeJSON(STORAGE_KEY, newQueue)) {
            return false;
        }
        this.queue = newQueue;
        this.lookup.set(key, sanitized);
        this.refreshUI();
        return true;
    }

    remove(entry) {
        const key = buildKey(entry);
        if (!key || !this.lookup.has(key)) {
            return false;
        }
        const newQueue = this.queue.filter(item => buildKey(item) !== key);
        if (!writeJSON(STORAGE_KEY, newQueue)) {
            return false;
        }
        this.queue = newQueue;
        this.lookup.delete(key);
        this.refreshUI();
        return true;
    }

    toggle(entry) {
        const key = buildKey(entry);
        if (!key) {
            return null;
        }
        if (this.lookup.has(key)) {
            return this.remove(entry) ? false : null;
        }
        return this.add(entry) ? true : null;
    }

    bindButton(button, item) {
        if (!(button instanceof HTMLElement)) {
            return;
        }
        const payload = this.buildPayloadFromButton(button, item);
        this.applyButtonState(button, this.isInQueue(payload));
        button.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            const toggled = this.toggle(payload);
            if (toggled === null) {
                alert('Не удалось обновить список изучения');
                this.applyButtonState(button, this.isInQueue(payload));
                return;
            }
            vibrate(toggled ? 20 : 10);
        });
    }

    buildPayloadFromButton(button, item = {}) {
        const dataset = button ? button.dataset || {} : {};
        const payload = {
            word: dataset.word || item.word || '',
            translation: dataset.translation || item.translation || '',
            russian_hint: dataset.russianHint || item.russian_hint || '',
            transcription: dataset.transcription || item.transcription || '',
            characterId: dataset.characterId || this.characterId || '',
            phaseKey: dataset.phaseKey || '',
            sentence: dataset.sentence || item.sentence || '',
            sentenceTranslation: dataset.sentenceTranslation || item.sentenceTranslation || '',
            emoji: dataset.emoji || item.visual_hint || '📝',
        };

        const examples = [];
        if (payload.sentence || payload.sentenceTranslation) {
            examples.push({
                german: payload.sentence,
                russian: payload.sentenceTranslation,
            });
        }
        payload.examples = examples;
        payload.example = payload.example || payload.sentence || '';

        if (item && Array.isArray(item.themes)) {
            payload.themes = item.themes.slice();
        }
        if (item && Array.isArray(item.wordFamily)) {
            payload.wordFamily = item.wordFamily.slice();
        }
        if (item && Array.isArray(item.sentenceParts)) {
            payload.sentenceParts = item.sentenceParts.slice();
        }
        return payload;
    }

    refreshUI() {
        this.updateBadge();
        this.updateButtons();
    }

    updateBadge() {
        const counter = qs('[data-study-count]');
        if (!counter) {
            return;
        }
        const count = this.queue.length;
        counter.textContent = String(count);
        const container = counter.closest('[data-study-counter]');
        if (!container) {
            return;
        }
        container.classList.toggle('study-counter-badge--active', count > 0);
        let wordForm = 'слов';
        if (count > 0) {
            const mod10 = count % 10;
            const mod100 = count % 100;
            if (mod10 === 1 && mod100 !== 11) {
                wordForm = 'слово';
            } else if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) {
                wordForm = 'слова';
            }
        }
        const label = count > 0
            ? `В списке изучения ${count} ${wordForm}`
            : 'Список изучения пуст';
        container.setAttribute('aria-label', label);
    }

    updateButtons(scope = document) {
        const buttons = qsa('.btn-study', scope);
        buttons.forEach(button => {
            const payload = this.buildPayloadFromButton(button);
            this.applyButtonState(button, this.isInQueue(payload));
        });
    }

    applyButtonState(button, isActive) {
        if (!(button instanceof HTMLElement)) {
            return;
        }
        const defaultLabel = button.dataset.defaultLabel || 'Изучить';
        const activeLabel = button.dataset.activeLabel || 'В списке';
        const inactiveTitle = button.dataset.inactiveTitle || 'Добавить слово в список изучения';
        const activeTitle = button.dataset.activeTitle || 'Удалить слово из списка изучения';
        button.disabled = false;
        button.style.background = '';
        button.classList.toggle('added', Boolean(isActive));
        button.dataset.inStudy = isActive ? 'true' : 'false';
        button.textContent = isActive ? activeLabel : defaultLabel;
        button.title = isActive ? activeTitle : inactiveTitle;
        button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    }
}
