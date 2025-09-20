export class VocabularyManager {
    constructor(data = window.phaseVocabularies || {}) {
        this.data = data || {};
        this.keys = Array.isArray(window.phaseKeys)
            ? window.phaseKeys.slice()
            : Object.keys(this.data);
        this.characterId = typeof window.characterId === 'string' ? window.characterId : '';
    }

    getPhaseKeys() {
        return this.keys.slice();
    }

    getPhase(key) {
        return this.data[key] || null;
    }

    getFirstPhaseKey() {
        return this.keys.length ? this.keys[0] : null;
    }

    getCharacterId() {
        return this.characterId;
    }

    getPhaseCount() {
        return this.keys.length;
    }

    getPhaseIndex(key) {
        return this.keys.indexOf(key);
    }
}
