import { refreshActiveExerciseContentHeight } from '../utils/dom.js';
import { vibrate } from '../utils/animations.js';

function shuffleArray(array) {
    const copy = Array.isArray(array) ? array.slice() : [];
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
}

function buildFragment(text, index) {
    const fragment = document.createElement('button');
    fragment.type = 'button';
    fragment.className = 'constructor-fragment';
    fragment.dataset.index = String(index);
    fragment.textContent = text;
    return fragment;
}

export class ConstructorExercise {
    constructor() {
        this.state = {};
        this.isTouchDevice = ('ontouchstart' in window)
            || (navigator.maxTouchPoints > 0)
            || (navigator.msMaxTouchPoints > 0);
    }

    init() {
        const panels = document.querySelectorAll('.constructor-panel');
        panels.forEach(panel => {
            panel.addEventListener('click', event => {
                const target = event.target;
                if (target instanceof HTMLElement && target.classList.contains('constructor-fragment')) {
                    this.toggleFragment(panel, target);
                }
            });
            const checkBtn = panel.querySelector('.constructor-check');
            if (checkBtn) {
                checkBtn.addEventListener('click', () => this.check(panel));
            }
            const resetBtn = panel.querySelector('.constructor-reset');
            if (resetBtn) {
                resetBtn.addEventListener('click', () => this.reset(panel));
            }
            const nextBtn = panel.querySelector('.constructor-next');
            if (nextBtn) {
                nextBtn.addEventListener('click', () => this.next(panel));
            }
        });
    }

    activate(phaseKey, phase) {
        const panels = document.querySelectorAll('.constructor-panel');
        let rendered = false;
        panels.forEach(panel => {
            const isCurrent = panel.dataset.phase === phaseKey;
            panel.classList.toggle('active', isCurrent);
            if (isCurrent && !rendered) {
                this.render(panel, phaseKey, phase);
                rendered = true;
            }
        });
    }

    getSets(phaseKey, phase) {
        if (phase && Array.isArray(phase.sentenceParts)) {
            return phase.sentenceParts;
        }
        const data = window.phaseVocabularies && window.phaseVocabularies[phaseKey];
        return data && Array.isArray(data.sentenceParts) ? data.sentenceParts : [];
    }

    ensureState(phaseKey) {
        if (!this.state[phaseKey]) {
            this.state[phaseKey] = { index: 0 };
        }
        return this.state[phaseKey];
    }

    render(panel, phaseKey, phase) {
        const sets = this.getSets(phaseKey, phase);
        const state = this.ensureState(phaseKey);
        const wordElement = panel.querySelector('[data-constructor-word]');
        const translationElement = panel.querySelector('[data-constructor-translation]');
        const progressElement = panel.querySelector('[data-constructor-progress]');
        const hintElement = panel.querySelector('[data-constructor-hint]');
        const source = panel.querySelector('[data-constructor-source]');
        const target = panel.querySelector('[data-constructor-target]');
        const checkBtn = panel.querySelector('.constructor-check');
        const resetBtn = panel.querySelector('.constructor-reset');
        const nextBtn = panel.querySelector('.constructor-next');
        const feedback = panel.querySelector('.constructor-feedback');
        const original = panel.querySelector('[data-constructor-original]');

        const disableButtons = () => {
            [checkBtn, resetBtn, nextBtn].forEach(btn => {
                if (btn) {
                    btn.disabled = true;
                }
            });
        };

        if (!sets.length) {
            if (wordElement) wordElement.textContent = '—';
            if (translationElement) translationElement.textContent = '';
            if (progressElement) progressElement.textContent = '';
            if (hintElement) {
                hintElement.textContent = 'Для этой фазы пока нет предложений для конструктора.';
            }
            if (source) source.innerHTML = '';
            if (target) {
                target.innerHTML = '<div class="constructor-placeholder">Предложения появятся позже.</div>';
                target.classList.remove('has-fragments');
            }
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('success', 'error');
            }
            if (original) {
                original.textContent = '';
            }
            disableButtons();
            refreshActiveExerciseContentHeight();
            return;
        }

        if (state.index >= sets.length) {
            state.index = 0;
        }
        if (state.index < 0) {
            state.index = sets.length - 1;
        }
        const current = sets[state.index];
        if (wordElement) {
            wordElement.textContent = current.word || '—';
        }
        if (translationElement) {
            translationElement.textContent = 'Перевод появится после проверки.';
        }
        if (progressElement) {
            progressElement.textContent = `${state.index + 1} / ${sets.length}`;
        }
        if (hintElement) {
            hintElement.textContent = current.translation
                ? `Соберите предложение со словом «${current.word}». Подсказка: ${current.translation}.`
                : `Соберите предложение со словом «${current.word}».`;
        }
        if (source) {
            source.innerHTML = '';
            const order = shuffleArray(current.parts.map((_, idx) => idx));
            order.forEach(idx => {
                const fragment = buildFragment(current.parts[idx], idx);
                source.appendChild(fragment);
            });
        }
        if (target) {
            target.innerHTML = '<div class="constructor-placeholder">Перетащите или нажмите на фрагменты, чтобы собрать предложение.</div>';
            target.classList.remove('has-fragments');
        }
        [checkBtn, resetBtn, nextBtn].forEach(btn => {
            if (btn) {
                btn.disabled = false;
            }
        });
        if (feedback) {
            feedback.textContent = '';
            feedback.classList.remove('success', 'error');
        }
        if (original) {
            original.textContent = '';
        }
        panel.dataset.constructorIndex = String(state.index);
        refreshActiveExerciseContentHeight();
    }

    toggleFragment(panel, fragment) {
        const source = panel.querySelector('[data-constructor-source]');
        const target = panel.querySelector('[data-constructor-target]');
        if (!source || !target) {
            return;
        }
        if (fragment.parentElement === source) {
            target.appendChild(fragment);
            fragment.classList.add('in-target');
        } else {
            source.appendChild(fragment);
            fragment.classList.remove('in-target');
        }
        vibrate(10);
        const translationElement = panel.querySelector('[data-constructor-translation]');
        if (translationElement) {
            translationElement.textContent = 'Перевод появится после проверки.';
        }
        this.updatePlaceholder(panel);
        this.clearFeedback(panel);
        refreshActiveExerciseContentHeight();
    }

    updatePlaceholder(panel) {
        const target = panel.querySelector('[data-constructor-target]');
        if (!target) {
            return;
        }
        const fragments = target.querySelectorAll('.constructor-fragment');
        target.classList.toggle('has-fragments', fragments.length > 0);
    }

    clearFeedback(panel) {
        const feedback = panel.querySelector('.constructor-feedback');
        if (feedback) {
            feedback.textContent = '';
            feedback.classList.remove('success', 'error');
        }
        const original = panel.querySelector('[data-constructor-original]');
        if (original) {
            original.textContent = '';
        }
    }

    check(panel) {
        const phaseKey = panel.dataset.phase;
        const sets = this.getSets(phaseKey);
        if (!sets.length) {
            return;
        }
        const state = this.ensureState(phaseKey);
        const current = sets[state.index] || sets[0];
        const target = panel.querySelector('[data-constructor-target]');
        const feedback = panel.querySelector('.constructor-feedback');
        const translationElement = panel.querySelector('[data-constructor-translation]');
        const originalElement = panel.querySelector('[data-constructor-original]');
        if (!target || !feedback) {
            return;
        }
        const fragments = Array.from(target.querySelectorAll('.constructor-fragment'));
        if (fragments.length !== current.parts.length) {
            feedback.textContent = 'Используйте все фрагменты, прежде чем проверять.';
            feedback.classList.add('error');
            feedback.classList.remove('success');
            vibrate(30);
            return;
        }
        const indices = fragments.map(fragment => parseInt(fragment.dataset.index || '0', 10));
        const isCorrect = indices.every((value, idx) => value === idx);
        if (isCorrect) {
            feedback.textContent = 'Отлично! Предложение собрано верно.';
            feedback.classList.add('success');
            feedback.classList.remove('error');
            if (translationElement) {
                translationElement.textContent = current.sentenceTranslation
                    ? `Перевод: ${current.sentenceTranslation}`
                    : 'Перевод: —';
            }
            if (originalElement) {
                originalElement.textContent = current.sentence
                    ? `Оригинал: "${current.sentence}"`
                    : '';
            }
            vibrate(20);
        } else {
            feedback.textContent = 'Порядок фрагментов пока неверный. Попробуйте ещё раз.';
            feedback.classList.add('error');
            feedback.classList.remove('success');
            vibrate([40]);
        }
        refreshActiveExerciseContentHeight();
    }

    reset(panel) {
        const phaseKey = panel.dataset.phase;
        this.render(panel, phaseKey);
        this.updatePlaceholder(panel);
        refreshActiveExerciseContentHeight();
    }

    next(panel) {
        const phaseKey = panel.dataset.phase;
        const sets = this.getSets(phaseKey);
        if (!sets.length) {
            return;
        }
        const state = this.ensureState(phaseKey);
        state.index = (state.index + 1) % sets.length;
        this.render(panel, phaseKey);
        this.updatePlaceholder(panel);
        vibrate(15);
    }
}
