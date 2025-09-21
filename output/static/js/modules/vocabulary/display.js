import { clearChildren, qs, qsa, setText } from '../utils/dom.js';
import { staggeredAnimation } from '../utils/animations.js';

function createCardElement(item, phaseKey, characterId) {
    const card = document.createElement('div');
    card.className = 'word-card';
    const hintMarkup = item.russian_hint
        ? `<div class="word-hint">(${item.russian_hint})</div>`
        : '';
    card.innerHTML = `
        <div class="word-meta">
            <div class="word-german">${item.word}</div>
            <div class="word-translation">${item.translation}</div>
            ${hintMarkup}
            <div class="word-transcription">${item.transcription || ''}</div>
        </div>
        <button class="btn-study" type="button"
            data-word="${item.word || ''}"
            data-translation="${item.translation || ''}"
            data-transcription="${item.transcription || ''}"
            data-russian-hint="${item.russian_hint || ''}"
            data-sentence="${item.sentence || ''}"
            data-sentence-translation="${item.sentenceTranslation || ''}"
            data-character-id="${characterId || ''}"
            data-phase-key="${phaseKey || ''}"
            data-emoji="${item.visual_hint || '📝'}"
        >Изучить</button>
    `;
    return card;
}

export class VocabularyDisplay {
    constructor(options) {
        this.vocabulary = options.vocabulary;
        this.studyManager = options.studyManager;
        this.quizManager = options.quizManager;
        this.wordExercises = options.wordExercises;
        this.constructorExercise = options.constructorExercise;
        this.progressTracker = options.progressTracker;
        this.isTouchDevice = Boolean(options.isTouchDevice);
        this.onRendered = typeof options.onRendered === 'function' ? options.onRendered : null;
    }

    renderPhase(phaseKey) {
        const phase = this.vocabulary.getPhase(phaseKey);
        const grid = qs('.vocabulary-grid');
        const phaseTitle = qs('#current-phase');
        if (!phase || !grid || !phaseTitle) {
            console.error('[VocabularyDisplay] Missing phase or DOM elements', phaseKey);
            return;
        }

        setText(phaseTitle, phase.title || '—');
        this.studyManager.load();

        this.updateScenes(phaseKey);
        this.updateExerciseContainers(phaseKey);
        this.wordExercises.render(phaseKey, phase);
        this.constructorExercise.activate(phaseKey, phase);
        this.quizManager.initialize(phaseKey, phase);

        clearChildren(grid);
        const cards = phase.words ? phase.words.slice() : [];
        const elements = cards.map(item => createCardElement(item, phaseKey, this.vocabulary.getCharacterId()));

        staggeredAnimation(elements, (element, index) => {
            element.style.animationDelay = `${index * 0.1}s`;
            grid.appendChild(element);
            const button = element.querySelector('.btn-study');
            if (button) {
                this.studyManager.bindButton(button, cards[index]);
            }
        }, 50);

        setTimeout(() => {
            this.studyManager.updateButtons(grid);
        }, cards.length * 60 + 20);

        const index = this.vocabulary.getPhaseIndex(phaseKey);
        this.progressTracker.update({
            index,
            total: this.vocabulary.getPhaseCount(),
            description: phase.description || '',
        });

        if (this.onRendered) {
            this.onRendered();
        }
    }

    updateScenes(phaseKey) {
        const scenes = qsa('.theatrical-scene');
        scenes.forEach(scene => {
            const isActive = scene.dataset.phase === phaseKey;
            scene.classList.toggle('active', isActive);
            if (isActive && this.isTouchDevice && window.innerWidth < 768) {
                setTimeout(() => {
                    scene.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        });
    }

    updateExerciseContainers(phaseKey) {
        qsa('.exercise-container').forEach(container => {
            container.classList.toggle('active', container.dataset.phase === phaseKey);
        });
        qsa('.exercise-phase-wrapper .exercise-phase').forEach(section => {
            const isCurrent = section.dataset.phase === phaseKey;
            section.classList.toggle('active', isCurrent);
            section.setAttribute('aria-hidden', isCurrent ? 'false' : 'true');
        });
    }
}
