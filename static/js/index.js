(function () {
    const REVIEW_QUEUE_KEY = 'reviewQueue';

    function safeJSONParse(raw) {
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch (error) {
            console.warn('[ReviewQueue] Failed to parse stored data', error);
            return null;
        }
    }

    function loadQueue() {
        if (typeof window === 'undefined' || !('localStorage' in window)) {
            return [];
        }
        const parsed = safeJSONParse(localStorage.getItem(REVIEW_QUEUE_KEY));
        return Array.isArray(parsed) ? parsed : [];
    }

    function saveQueue(queue) {
        if (typeof window === 'undefined' || !('localStorage' in window)) {
            return;
        }
        try {
            localStorage.setItem(REVIEW_QUEUE_KEY, JSON.stringify(queue));
        } catch (error) {
            console.warn('[ReviewQueue] Unable to persist queue', error);
        }
    }

    function slugify(text) {
        if (!text) return null;
        return text
            .toString()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '') || null;
    }

    function buildEntryFromCard(card) {
        if (!card) return null;
        const wordId = card.dataset.wordId || card.dataset.vocabularyId || null;
        const wordText = card.querySelector('.review-word');
        const translationText = card.querySelector('.review-translation');

        return {
            wordId,
            vocabularyId: card.dataset.vocabularyId || wordId,
            slug: card.dataset.wordSlug || slugify(wordText ? wordText.textContent : null),
            word: wordText ? wordText.textContent.trim() : null,
            translation: translationText ? translationText.textContent.trim() : null,
            characterId: card.dataset.characterId || null,
            characterName: card.dataset.characterName || null,
            phaseId: card.dataset.phaseId || null,
            phaseTitle: card.dataset.phaseTitle || null,
            addedAt: card.dataset.addedAt || new Date().toISOString(),
        };
    }

    function syncQueueFromDom() {
        const cards = Array.from(document.querySelectorAll('.review-card'));
        if (!cards.length) {
            saveQueue([]);
            return [];
        }

        const entries = cards
            .map(buildEntryFromCard)
            .filter(Boolean);

        saveQueue(entries);
        return entries;
    }

    function updateEmptyState() {
        const grid = document.querySelector('.review-grid');
        if (!grid) {
            return;
        }

        if (grid.querySelector('.review-card')) {
            const empty = grid.querySelector('.review-empty');
            if (empty) {
                empty.remove();
            }
            return;
        }

        if (!grid.querySelector('.review-empty')) {
            const empty = document.createElement('p');
            empty.className = 'review-empty';
            empty.textContent = 'Очередь повторения пока пуста.';
            grid.appendChild(empty);
        }
    }

    function removeFromQueue(wordId, characterId, phaseId) {
        const queue = loadQueue();
        const filtered = queue.filter(entry => {
            if (!entry || entry.wordId !== wordId) {
                return true;
            }

            if (characterId && entry.characterId && entry.characterId !== characterId) {
                return true;
            }

            if (phaseId && entry.phaseId && entry.phaseId !== phaseId) {
                return true;
            }

            return false;
        });

        saveQueue(filtered);
    }

    function handleRemove(button) {
        const card = button.closest('.review-card');
        if (!card) {
            return;
        }

        const wordId = card.dataset.wordId || card.dataset.vocabularyId || null;
        const characterId = card.dataset.characterId || null;
        const phaseId = card.dataset.phaseId || null;

        removeFromQueue(wordId, characterId, phaseId);
        card.remove();
        updateEmptyState();

        window.dispatchEvent(
            new CustomEvent('review-queue:remove', {
                detail: { wordId, characterId, phaseId },
            })
        );
    }

    document.addEventListener('DOMContentLoaded', () => {
        const grid = document.querySelector('.review-grid');
        if (!grid) {
            return;
        }

        syncQueueFromDom();
        updateEmptyState();

        grid.addEventListener('click', event => {
            const target = event.target;
            if (target && target.closest('.review-remove-btn')) {
                event.preventDefault();
                handleRemove(target.closest('.review-remove-btn'));
            }
        });
    });
})();
