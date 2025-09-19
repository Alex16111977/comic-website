"""JavaScript Generator for Lira Journey interactivity"""

import json


class LiraJSGenerator:
    """Generate JavaScript for journey interactivity with mobile support"""

    @staticmethod
    def generate(character_data, constructor_exercises=None):
        """Generate JS with vocabulary data from character JSON"""

        # Build vocabulary object from character data using JSON serialization
        phase_vocabularies = {}
        constructor_exercises = constructor_exercises or {}

        for phase in character_data.get('journey_phases', []):
            phase_id = phase.get('id')
            if not phase_id:
                continue

            words = []
            raw_constructors = constructor_exercises.get(phase_id, [])
            constructors = []

            if isinstance(raw_constructors, list):
                for exercise in raw_constructors:
                    if not isinstance(exercise, dict):
                        continue

                    parts = exercise.get('parts')
                    if not isinstance(parts, list):
                        parts = []

                    constructors.append({
                        'word': exercise.get('word', ''),
                        'translation': exercise.get('translation', ''),
                        'sentence': exercise.get('sentence', ''),
                        'sentenceTranslation': exercise.get('sentence_translation')
                            or exercise.get('sentenceTranslation', ''),
                        'parts': parts,
                    })
            else:
                constructors = []
            for word in phase.get('vocabulary', []):
                themes = word.get('themes') or []
                if isinstance(themes, str):
                    themes = [themes]
                elif not isinstance(themes, list):
                    themes = []

                sentence_parts = []
                raw_parts = word.get('sentence_parts')
                if isinstance(raw_parts, list):
                    for part in raw_parts:
                        if isinstance(part, dict):
                            text = str(part.get('text', '')).strip()
                            if not text:
                                continue
                            entry = {'text': text}
                            translation = part.get('translation')
                            if translation:
                                entry['translation'] = str(translation)
                            hint = part.get('hint')
                            if hint:
                                entry['hint'] = str(hint)
                            sentence_parts.append(entry)
                        elif isinstance(part, str):
                            text = part.strip()
                            if text:
                                sentence_parts.append({'text': text})

                # Добавляем поля для relations функционала
                word_family = word.get('wordFamily') or []
                if isinstance(word_family, str):
                    word_family = [word_family]
                elif not isinstance(word_family, list):
                    word_family = []

                synonyms = word.get('synonyms') or []
                if isinstance(synonyms, str):
                    synonyms = [synonyms]
                elif not isinstance(synonyms, list):
                    synonyms = []

                collocations = word.get('collocations') or []
                if isinstance(collocations, str):
                    collocations = [collocations]
                elif not isinstance(collocations, list):
                    collocations = []

                words.append({
                    'word': word.get('german', ''),
                    'translation': word.get('russian', ''),
                    'transcription': word.get('transcription', ''),
                    'sentence': word.get('sentence', ''),
                    'sentenceTranslation': word.get('sentence_translation', ''),
                    'visual_hint': word.get('visual_hint', ''),
                    'themes': themes,
                    'sentenceParts': sentence_parts,
                    'wordFamily': word_family,  # Для relations
                    'synonyms': synonyms,        # Для relations
                    'collocations': collocations # Для relations
                })

            quizzes = []
            for quiz in phase.get('quizzes', []):
                choices = list(quiz.get('choices', []))
                correct_index = quiz.get('correct_index')
                if correct_index is None:
                    correct_index = quiz.get('correctIndex', 0)

                try:
                    correct_index = int(correct_index)
                except (TypeError, ValueError):
                    correct_index = 0

                quizzes.append({
                    'question': quiz.get('question', ''),
                    'choices': choices,
                    'correctIndex': correct_index,
                })

            phase_vocabularies[phase_id] = {
                'title': phase.get('title', ''),
                'description': phase.get('description', ''),
                'words': words,
                'quizzes': quizzes,
                'constructorExercises': constructors,
            }

        vocab_js = (
            "const phaseVocabularies = "
            f"{json.dumps(phase_vocabularies, ensure_ascii=False, indent=4)};\n\n"
        )
        
        # Add enhanced mobile-friendly interaction code
        vocab_js += '''
let currentPhaseIndex = 0;
const phaseKeys = Object.keys(phaseVocabularies);
let isTransitioning = false; // Prevent double clicks/taps
let progressLineElement = null;
let progressLineLength = 0;
const QUIZ_ADVANCE_DELAY = 1200;

// Device detection
const isTouchDevice = ('ontouchstart' in window) ||
                      (navigator.maxTouchPoints > 0) ||
                      (navigator.msMaxTouchPoints > 0);
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
const isAndroid = /Android/.test(navigator.userAgent);

const constructorState = {
    phaseIndexes: {},
    activePhase: null,
    activeExercise: null
};
let constructorElements = null;
let constructorDraggedChip = null;

function getConstructorElements() {
    const section = document.querySelector('.constructor-section');
    if (!section) return null;

    return {
        section,
        exercise: section.querySelector('.constructor-exercise'),
        emptyState: section.querySelector('.constructor-empty-state'),
        pool: section.querySelector('.constructor-pool'),
        dropzone: section.querySelector('.constructor-dropzone'),
        feedback: section.querySelector('.constructor-feedback'),
        word: section.querySelector('.constructor-word'),
        translation: section.querySelector('.constructor-word-translation'),
        sentenceTranslation: section.querySelector('.constructor-sentence-translation'),
        progress: section.querySelector('.constructor-progress-indicator'),
        checkBtn: section.querySelector('.constructor-check'),
        resetBtn: section.querySelector('.constructor-reset'),
        nextBtn: section.querySelector('.constructor-next')
    };
}

function initializeConstructor() {
    constructorElements = getConstructorElements();
    if (!constructorElements) return;

    const { checkBtn, resetBtn, nextBtn, dropzone, pool } = constructorElements;

    if (checkBtn) {
        registerConstructorButton(checkBtn, handleConstructorCheck);
    }
    if (resetBtn) {
        registerConstructorButton(resetBtn, handleConstructorReset);
    }
    if (nextBtn) {
        registerConstructorButton(nextBtn, handleConstructorNext);
    }

    if (dropzone) {
        dropzone.addEventListener('dragover', handleConstructorDropzoneDragOver);
        dropzone.addEventListener('drop', handleConstructorDropzoneDrop);
        dropzone.addEventListener('dragleave', handleConstructorDropzoneDragLeave);
    }

    if (pool) {
        pool.addEventListener('dragover', handleConstructorPoolDragOver);
        pool.addEventListener('drop', handleConstructorPoolDrop);
        pool.addEventListener('dragleave', handleConstructorPoolDragLeave);
    }
}

function registerConstructorButton(button, handler) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        handler();
    });

    if (isTouchDevice) {
        button.addEventListener('touchstart', function() {
            this.classList.add('touching');
        });

        button.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('touching');
            }, 120);
        });
    }
}

function normalizeConstructorSentence(sentence) {
    return (sentence || '').replace(/\\s+/g, ' ').trim();
}

function shuffleArray(items) {
    const array = Array.isArray(items) ? items.slice() : [];
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function renderConstructor(phaseKey) {
    if (!constructorElements) {
        constructorElements = getConstructorElements();
    }
    if (!constructorElements || !constructorElements.section) return;

    const phase = phaseVocabularies[phaseKey];
    const exercises = Array.isArray(phase && phase.constructorExercises)
        ? phase.constructorExercises
        : [];

    const { exercise, emptyState, feedback, progress, dropzone, pool, word, translation, sentenceTranslation } = constructorElements;

    constructorState.activePhase = phaseKey;

    if (!exercises.length) {
        if (exercise) {
            exercise.setAttribute('hidden', 'hidden');
        }
        if (emptyState) {
            emptyState.removeAttribute('hidden');
        }
        if (feedback) {
            feedback.textContent = '';
            feedback.classList.remove('success', 'error');
        }
        if (progress) {
            progress.textContent = '—';
        }
        if (dropzone) {
            dropzone.innerHTML = '';
            dropzone.classList.remove('constructor-dropzone--success');
        }
        if (pool) {
            pool.innerHTML = '';
            pool.classList.remove('constructor-pool--active');
        }
        if (word) {
            word.textContent = '';
        }
        if (translation) {
            translation.textContent = '';
        }
        if (sentenceTranslation) {
            sentenceTranslation.textContent = '';
        }
        constructorState.activeExercise = null;
        return;
    }

    if (emptyState) {
        emptyState.setAttribute('hidden', 'hidden');
    }
    if (exercise) {
        exercise.removeAttribute('hidden');
    }

    const savedIndex = constructorState.phaseIndexes[phaseKey] || 0;
    const normalizedIndex = Math.max(0, Math.min(savedIndex, exercises.length - 1));
    renderConstructorExercise(phaseKey, normalizedIndex);
}

function renderConstructorExercise(phaseKey, exerciseIndex) {
    if (!constructorElements) {
        constructorElements = getConstructorElements();
    }
    if (!constructorElements || !constructorElements.section) return;

    const phase = phaseVocabularies[phaseKey];
    const exercises = Array.isArray(phase && phase.constructorExercises)
        ? phase.constructorExercises
        : [];
    if (!exercises.length) return;

    const { pool, dropzone, feedback, word, translation, sentenceTranslation, progress, nextBtn } = constructorElements;
    const safeIndex = Math.max(0, Math.min(exerciseIndex, exercises.length - 1));
    const exerciseData = exercises[safeIndex];

    constructorState.phaseIndexes[phaseKey] = safeIndex;
    constructorState.activeExercise = exerciseData;

    if (word) {
        word.textContent = exerciseData.word || '';
    }
    if (translation) {
        translation.textContent = exerciseData.translation || '';
    }
    if (sentenceTranslation) {
        sentenceTranslation.textContent = exerciseData.sentence_translation || exerciseData.sentenceTranslation || '';
    }
    if (progress) {
        progress.textContent = `${safeIndex + 1} / ${exercises.length}`;
    }
    if (feedback) {
        feedback.textContent = '';
        feedback.classList.remove('success', 'error');
    }

    if (dropzone) {
        dropzone.innerHTML = '';
        dropzone.dataset.expected = exerciseData.sentence || '';
        dropzone.dataset.expectedNormalized = normalizeConstructorSentence(exerciseData.sentence || '');
        dropzone.dataset.parts = String((exerciseData.parts || []).length);
        dropzone.classList.remove('constructor-dropzone--success', 'constructor-dropzone--active');

        const placeholder = document.createElement('div');
        placeholder.className = 'constructor-drop-placeholder';
        placeholder.textContent = 'Перетащите фрагменты сюда по порядку';
        dropzone.appendChild(placeholder);
    }

    if (pool) {
        pool.innerHTML = '';
        pool.classList.remove('constructor-pool--active');
        const shuffledParts = shuffleArray(exerciseData.parts || []);
        shuffledParts.forEach((part, index) => {
            const chip = createConstructorChip(part, index);
            pool.appendChild(chip);
        });
    }

    if (nextBtn) {
        const isSingle = exercises.length <= 1;
        nextBtn.disabled = isSingle;
        nextBtn.classList.toggle('disabled', isSingle);
    }
}

function createConstructorChip(part, index) {
    const chip = document.createElement('div');
    chip.className = 'constructor-chip';
    chip.textContent = part.text || '';
    chip.setAttribute('draggable', 'true');
    chip.dataset.partIndex = String(index);
    chip.dataset.partText = part.text || '';
    chip.tabIndex = 0;

    chip.addEventListener('dragstart', handleConstructorDragStart);
    chip.addEventListener('dragend', handleConstructorDragEnd);

    chip.addEventListener('click', function(event) {
        event.preventDefault();
        toggleChipPlacement(this);
    });

    chip.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            toggleChipPlacement(this);
        }
    });

    return chip;
}

function toggleChipPlacement(chip) {
    if (!constructorElements) return;

    const parent = chip.parentElement;
    if (parent === constructorElements.pool) {
        moveChipToDropzone(chip);
    } else {
        moveChipToPool(chip);
    }
}

function moveChipToDropzone(chip) {
    if (!constructorElements) return;

    const { dropzone, pool } = constructorElements;
    if (!dropzone) return;

    const placeholder = dropzone.querySelector('.constructor-drop-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    dropzone.appendChild(chip);
    dropzone.classList.remove('constructor-dropzone--active', 'constructor-dropzone--success');
    chip.classList.add('constructor-chip--placed');
    chip.setAttribute('aria-pressed', 'true');

    if (pool) {
        pool.classList.remove('constructor-pool--active');
    }

    updateConstructorFeedback('');
}

function moveChipToPool(chip) {
    if (!constructorElements) return;

    const { pool, dropzone } = constructorElements;
    if (!pool) return;

    pool.appendChild(chip);
    chip.classList.remove('constructor-chip--placed');
    chip.setAttribute('aria-pressed', 'false');

    if (dropzone) {
        dropzone.classList.remove('constructor-dropzone--active', 'constructor-dropzone--success');
    }

    ensureConstructorPlaceholder();
    updateConstructorFeedback('');
}

function ensureConstructorPlaceholder() {
    if (!constructorElements || !constructorElements.dropzone) return;

    const dropzone = constructorElements.dropzone;
    const hasChips = dropzone.querySelectorAll('.constructor-chip').length > 0;
    let placeholder = dropzone.querySelector('.constructor-drop-placeholder');

    if (hasChips) {
        if (placeholder) {
            placeholder.remove();
        }
    } else if (!placeholder) {
        placeholder = document.createElement('div');
        placeholder.className = 'constructor-drop-placeholder';
        placeholder.textContent = 'Перетащите фрагменты сюда по порядку';
        dropzone.appendChild(placeholder);
    }
}

function handleConstructorDragStart(event) {
    constructorDraggedChip = this;
    this.classList.add('constructor-chip--dragging');
    if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.setData('text/plain', this.dataset.partText || '');
    }
}

function handleConstructorDragEnd() {
    this.classList.remove('constructor-chip--dragging');
    constructorDraggedChip = null;
}

function handleConstructorDropzoneDragOver(event) {
    if (!constructorDraggedChip) return;
    event.preventDefault();
    if (constructorElements && constructorElements.dropzone) {
        constructorElements.dropzone.classList.add('constructor-dropzone--active');
    }
}

function handleConstructorDropzoneDrop(event) {
    if (!constructorDraggedChip) return;
    event.preventDefault();
    if (constructorElements && constructorElements.dropzone) {
        constructorElements.dropzone.classList.remove('constructor-dropzone--active');
    }
    moveChipToDropzone(constructorDraggedChip);
}

function handleConstructorDropzoneDragLeave() {
    if (constructorElements && constructorElements.dropzone) {
        constructorElements.dropzone.classList.remove('constructor-dropzone--active');
    }
}

function handleConstructorPoolDragOver(event) {
    if (!constructorDraggedChip) return;
    event.preventDefault();
    if (constructorElements && constructorElements.pool) {
        constructorElements.pool.classList.add('constructor-pool--active');
    }
}

function handleConstructorPoolDrop(event) {
    if (!constructorDraggedChip) return;
    event.preventDefault();
    if (constructorElements && constructorElements.pool) {
        constructorElements.pool.classList.remove('constructor-pool--active');
    }
    moveChipToPool(constructorDraggedChip);
}

function handleConstructorPoolDragLeave() {
    if (constructorElements && constructorElements.pool) {
        constructorElements.pool.classList.remove('constructor-pool--active');
    }
}

function updateConstructorFeedback(message, status) {
    if (!constructorElements || !constructorElements.feedback) return;

    const feedback = constructorElements.feedback;
    feedback.textContent = message || '';
    feedback.classList.remove('success', 'error');

    if (status === 'success') {
        feedback.classList.add('success');
    } else if (status === 'error') {
        feedback.classList.add('error');
    }
}

function handleConstructorCheck() {
    if (!constructorElements || !constructorElements.dropzone) return;

    const dropzone = constructorElements.dropzone;
    const chips = Array.from(dropzone.querySelectorAll('.constructor-chip'));
    const expectedNormalized = dropzone.dataset.expectedNormalized || '';
    const totalParts = parseInt(dropzone.dataset.parts || '0', 10);
    const assembled = chips.map(chip => chip.dataset.partText || '').join(' ');
    const assembledNormalized = normalizeConstructorSentence(assembled);

    if (!chips.length) {
        updateConstructorFeedback('Сначала перенесите фрагменты предложения.', 'error');
        return;
    }

    if (chips.length !== totalParts) {
        updateConstructorFeedback('Кажется, один из фрагментов ещё в списке. Проверьте себя!', 'error');
        return;
    }

    if (assembledNormalized && assembledNormalized === expectedNormalized) {
        dropzone.classList.add('constructor-dropzone--success');
        updateConstructorFeedback('Отлично! Предложение собрано верно.', 'success');
        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(20);
        }
    } else {
        dropzone.classList.remove('constructor-dropzone--success');
        updateConstructorFeedback('Попробуйте ещё раз: порядок фрагментов отличается.', 'error');
        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(40);
        }
    }
}

function handleConstructorReset() {
    if (!constructorState.activePhase) return;
    const phaseKey = constructorState.activePhase;
    const index = constructorState.phaseIndexes[phaseKey] || 0;
    renderConstructorExercise(phaseKey, index);
}

function handleConstructorNext() {
    if (!constructorState.activePhase) return;

    const phaseKey = constructorState.activePhase;
    const phase = phaseVocabularies[phaseKey];
    const exercises = Array.isArray(phase && phase.constructorExercises)
        ? phase.constructorExercises
        : [];
    if (!exercises.length) return;

    const currentIndex = constructorState.phaseIndexes[phaseKey] || 0;
    const nextIndex = (currentIndex + 1) % exercises.length;
    renderConstructorExercise(phaseKey, nextIndex);

    if (navigator.vibrate && isTouchDevice) {
        navigator.vibrate(15);
    }
}

// Prevent iOS zoom on double tap
if (isIOS) {
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function(event) {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
}

function clampProgress(value) {
    if (isNaN(value)) return 0;
    return Math.min(100, Math.max(0, value));
}

function ensureProgressLineLength() {
    if (!progressLineElement) return 0;
    if (progressLineLength) return progressLineLength;

    if (typeof progressLineElement.getTotalLength === 'function') {
        progressLineLength = progressLineElement.getTotalLength();
    }

    if (!progressLineLength && typeof progressLineElement.getBBox === 'function') {
        try {
            const bbox = progressLineElement.getBBox();
            if (bbox && bbox.width) {
                progressLineLength = bbox.width;
            }
        } catch (error) {
            console.warn('[ProgressLine] Unable to get bounding box length', error);
        }
    }

    if (!progressLineLength) {
        const parent = progressLineElement.parentElement;
        if (parent) {
            const parentWidth = parent.getBoundingClientRect().width;
            if (parentWidth) {
                progressLineLength = parentWidth;
            }
        }
    }

    if (!progressLineLength) {
        progressLineLength = 1;
    }

    return progressLineLength;
}

function updateProgressLineByPercent(progressPercent) {
    if (!progressLineElement) return;

    const length = ensureProgressLineLength();
    progressLineElement.style.strokeDasharray = `${length} ${length}`;

    const clamped = clampProgress(progressPercent);
    const offset = length - (length * clamped / 100);
    progressLineElement.style.strokeDashoffset = offset;
}

function initializeProgressLine() {
    progressLineElement = document.querySelector('.progress-line');
    if (!progressLineElement) return;

    const startValue = clampProgress(parseFloat(progressLineElement.dataset.startProgress || '0'));
    ensureProgressLineLength();
    updateProgressLineByPercent(startValue);
}

function displayVocabulary(phaseKey) {
    // Prevent multiple rapid transitions
    if (isTransitioning) return;
    isTransitioning = true;

    const phase = phaseVocabularies[phaseKey];
    const grid = document.querySelector('.vocabulary-grid');
    const phaseTitle = document.getElementById('current-phase');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    
    if (!phase || !grid || !phaseTitle) {
        console.error('Missing required elements');
        isTransitioning = false;
        return;
    }
    
    phaseTitle.textContent = phase.title;
    
    // Update theatrical scene with smooth transition
    const scenes = document.querySelectorAll('.theatrical-scene');
    scenes.forEach(scene => {
        if (scene.dataset.phase === phaseKey) {
            scene.classList.add('active');
            // Scroll to scene on mobile
            if (isTouchDevice && window.innerWidth < 768) {
                setTimeout(() => {
                    scene.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }, 100);
            }
        } else {
            scene.classList.remove('active');
        }
    });
    
    // Update exercises
    const exercises = document.querySelectorAll('.exercise-container');
    exercises.forEach(exercise => {
        if (exercise.dataset.phase === phaseKey) {
            exercise.classList.add('active');
        } else {
            exercise.classList.remove('active');
        }
    });

    // Update quizzes
    const quizContainers = document.querySelectorAll('.quiz-phase-container');
    quizContainers.forEach(container => {
        const isCurrent = container.dataset.phase === phaseKey;
        container.classList.toggle('active', isCurrent);
        resetQuizContainer(container, isCurrent);
    });

    const quizCountElement = document.querySelector('.quiz-count');
    if (quizCountElement) {
        const quizData = Array.isArray(phase.quizzes) ? phase.quizzes : [];
        quizCountElement.textContent = quizData.length;
    }

    // Setup relations for current phase
    setupRelationsForPhase(phaseKey);

    grid.innerHTML = '';

    phase.words.forEach((item, index) => {
        setTimeout(() => {
            const card = document.createElement('div');
            card.className = 'word-card';
            card.style.animationDelay = `${index * 0.1}s`;

            const visualHintMarkup = item.visual_hint
                ? `<div class="word-visual-hint" aria-hidden="true">${item.visual_hint}</div>`
                : '';

            const themesMarkup = Array.isArray(item.themes) && item.themes.length
                ? `<div class="word-themes">${item.themes.map(theme => `<span class=\"word-theme\">${theme}</span>`).join('')}</div>`
                : '';

            card.innerHTML = `
                <div class="word-card-header">
                    ${visualHintMarkup}
                    <div class="word-meta">
                        <div class="word-german">${item.word}</div>
                        <div class="word-translation">${item.translation}</div>
                        <div class="word-transcription">${item.transcription}</div>
                    </div>
                </div>
                ${themesMarkup}
                <div class="word-sentence">
                    <div class="sentence-german">"${item.sentence}"</div>
                    <div class="sentence-translation">${item.sentenceTranslation}</div>
                </div>
            `;
            grid.appendChild(card);
        }, index * 50);
    });

    renderConstructor(phaseKey);

    // Update progress bar
    const progress = ((currentPhaseIndex + 1) / phaseKeys.length) * 100;
    if (progressFill) progressFill.style.width = progress + '%';
    if (progressText) progressText.textContent = phase.description;
    updateProgressLineByPercent(progress);

    // Update navigation buttons state
    updateNavigationButtons();
    
    // Reset transition flag
    setTimeout(() => {
        isTransitioning = false;
    }, 500);
}

// ============= QUIZ FUNCTIONS (lines 240-400) =============

function resetQuizContainer(container, activateFirstCard = false) {
    if (!container) return;

    const cards = Array.from(container.querySelectorAll('.quiz-card'));
    let firstVisibleSet = false;

    cards.forEach(card => {
        const isPlaceholder = card.classList.contains('empty');
        if (activateFirstCard && !firstVisibleSet && !isPlaceholder) {
            card.classList.add('active');
            firstVisibleSet = true;
        } else {
            card.classList.remove('active');
        }

        card.dataset.answered = 'false';

        const choices = card.querySelectorAll('.quiz-choice');
        choices.forEach(choice => {
            choice.disabled = false;
            choice.classList.remove('correct', 'incorrect', 'locked', 'touching');
            choice.removeAttribute('aria-disabled');
        });

        const feedback = card.querySelector('.quiz-feedback');
        if (feedback) {
            feedback.textContent = '';
        }
    });

    const completion = container.querySelector('.quiz-completion');
    if (completion) {
        completion.classList.remove('visible');
        completion.setAttribute('aria-hidden', 'true');
    }

    if (activateFirstCard && !firstVisibleSet) {
        const placeholder = container.querySelector('.quiz-card');
        if (placeholder) {
            placeholder.classList.add('active');
        }
    }
}

function advanceQuiz(currentCard) {
    const container = currentCard ? currentCard.closest('.quiz-phase-container') : null;
    if (!container) return;

    const cards = Array.from(container.querySelectorAll('.quiz-card')).filter(card => !card.classList.contains('empty'));
    const currentIndex = cards.indexOf(currentCard);

    if (currentIndex === -1) return;

    if (currentIndex < cards.length - 1) {
        currentCard.classList.remove('active');
        const nextCard = cards[currentIndex + 1];
        nextCard.classList.add('active');
        nextCard.dataset.answered = 'false';

        const choices = nextCard.querySelectorAll('.quiz-choice');
        choices.forEach(choice => {
            choice.disabled = false;
            choice.classList.remove('correct', 'incorrect', 'locked', 'touching');
            choice.removeAttribute('aria-disabled');
        });

        const feedback = nextCard.querySelector('.quiz-feedback');
        if (feedback) {
            feedback.textContent = '';
        }

        if (isTouchDevice && window.innerWidth < 768) {
            setTimeout(() => {
                nextCard.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 150);
        }
    } else {
        const completion = container.querySelector('.quiz-completion');
        if (completion) {
            completion.classList.add('visible');
            completion.setAttribute('aria-hidden', 'false');

            if (isTouchDevice && window.innerWidth < 768) {
                setTimeout(() => {
                    completion.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 150);
            }
        }
    }
}

function handleQuizChoiceSelection(button) {
    if (!button) return;

    const quizCard = button.closest('.quiz-card');
    if (!quizCard || quizCard.dataset.answered === 'true') {
        return;
    }

    const selectedIndex = parseInt(button.dataset.choiceIndex || '0', 10);
    const correctIndex = parseInt(quizCard.dataset.correctIndex || '0', 10);
    const choices = Array.from(quizCard.querySelectorAll('.quiz-choice'));
    const feedback = quizCard.querySelector('.quiz-feedback');

    quizCard.dataset.answered = 'true';

    choices.forEach(choice => {
        choice.disabled = true;
        choice.classList.add('locked');
        choice.setAttribute('aria-disabled', 'true');
    });

    const correctChoice = choices.find(choice => parseInt(choice.dataset.choiceIndex || '0', 10) === correctIndex);

    if (selectedIndex === correctIndex) {
        button.classList.add('correct');
        if (feedback) {
            feedback.textContent = 'Верно! Отличная работа.';
        }
    } else {
        button.classList.add('incorrect');
        if (correctChoice) {
            correctChoice.classList.add('correct');
        }
        if (feedback) {
            feedback.textContent = 'Неверно. Правильный ответ подсвечен.';
        }
    }

    if (navigator.vibrate && isTouchDevice) {
        navigator.vibrate(selectedIndex === correctIndex ? 20 : 40);
    }

    setTimeout(() => {
        advanceQuiz(quizCard);
    }, QUIZ_ADVANCE_DELAY);
}

function attachQuizHandlers() {
    const choiceButtons = document.querySelectorAll('.quiz-choice');
    choiceButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            handleQuizChoiceSelection(this);
        });

        if (isTouchDevice) {
            button.addEventListener('touchstart', function() {
                this.classList.add('touching');
            });

            button.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touching');
                }, 120);
            });
        }
    });
}

// ============= RELATIONS FUNCTIONS (lines 400-600) =============

function setupRelationsForPhase(phaseKey) {
    const relationsContainers = document.querySelectorAll('.relations-container');
    relationsContainers.forEach(container => {
        if (container.dataset.phase === phaseKey) {
            container.classList.add('active');
            renderRelations(container, phaseKey);
        } else {
            container.classList.remove('active');
        }
    });
}

function renderRelations(container, phaseKey) {
    if (!container || !phaseKey) return;

    const phase = phaseVocabularies[phaseKey];
    if (!phase || !phase.words) return;

    // Collect all relations data
    const wordFamilies = [];
    const synonymGroups = [];
    const collocations = [];

    phase.words.forEach(word => {
        if (word.wordFamily && word.wordFamily.length > 0) {
            wordFamilies.push({
                base: word.word,
                family: word.wordFamily
            });
        }
        if (word.synonyms && word.synonyms.length > 0) {
            synonymGroups.push({
                word: word.word,
                synonyms: word.synonyms
            });
        }
        if (word.collocations && word.collocations.length > 0) {
            collocations.push({
                word: word.word,
                collocations: word.collocations
            });
        }
    });

    // Render Word Families section
    const familiesSection = container.querySelector('.word-families-section');
    if (familiesSection && wordFamilies.length > 0) {
        const content = familiesSection.querySelector('.relations-content');
        if (content) {
            content.innerHTML = wordFamilies.map((item, idx) => `
                <div class="relation-group" data-group-index="${idx}">
                    <div class="relation-header">${item.base}</div>
                    <div class="drag-targets">
                        ${item.family.map((word, wordIdx) => `
                            <div class="drag-target" 
                                 data-target="${word}"
                                 data-group="${idx}"
                                 data-word-index="${wordIdx}">
                                <span class="target-placeholder">?</span>
                                <span class="target-answer" style="display: none;">${word}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="drag-sources">
                        ${item.family.map((word, wordIdx) => `
                            <div class="drag-source" 
                                 data-source="${word}"
                                 data-group="${idx}"
                                 data-word-index="${wordIdx}"
                                 draggable="true">
                                ${word}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('');
            attachDragDropHandlers(content);
        }
    }

    // Render Synonyms section
    const synonymsSection = container.querySelector('.synonyms-section');
    if (synonymsSection && synonymGroups.length > 0) {
        const content = synonymsSection.querySelector('.relations-content');
        if (content) {
            content.innerHTML = synonymGroups.map((item, idx) => `
                <div class="synonym-group">
                    <div class="synonym-word">${item.word}</div>
                    <div class="synonym-list">
                        ${item.synonyms.map(syn => `<span class="synonym-item">${syn}</span>`).join('')}
                    </div>
                </div>
            `).join('');
        }
    }

    // Render Collocations section
    const collocationsSection = container.querySelector('.collocations-section');
    if (collocationsSection && collocations.length > 0) {
        const content = collocationsSection.querySelector('.relations-content');
        if (content) {
            content.innerHTML = collocations.map((item, idx) => `
                <div class="collocation-group">
                    <div class="collocation-word">${item.word}</div>
                    <div class="collocation-list">
                        ${item.collocations.map(coll => `<span class="collocation-item">${coll}</span>`).join('')}
                    </div>
                </div>
            `).join('');
        }
    }
}

function attachDragDropHandlers(container) {
    const sources = container.querySelectorAll('.drag-source');
    const targets = container.querySelectorAll('.drag-target');

    sources.forEach(source => {
        source.addEventListener('dragstart', handleDragStart);
        source.addEventListener('dragend', handleDragEnd);

        // Touch events for mobile
        source.addEventListener('touchstart', handleTouchStart);
        source.addEventListener('touchmove', handleTouchMove);
        source.addEventListener('touchend', handleTouchEnd);
    });

    targets.forEach(target => {
        target.addEventListener('dragover', handleDragOver);
        target.addEventListener('drop', handleDrop);
        target.addEventListener('dragleave', handleDragLeave);

        // Click to select on mobile
        target.addEventListener('click', handleTargetClick);
    });
}

let draggedElement = null;
let selectedSource = null;

function handleDragStart(e) {
    draggedElement = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
    draggedElement = null;
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
    return false;
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    this.classList.remove('drag-over');

    if (draggedElement && draggedElement !== this) {
        const sourceData = draggedElement.dataset.source;
        const targetData = this.dataset.target;

        if (sourceData === targetData) {
            this.classList.add('correct');
            const placeholder = this.querySelector('.target-placeholder');
            const answer = this.querySelector('.target-answer');
            if (placeholder) placeholder.style.display = 'none';
            if (answer) answer.style.display = 'block';
            draggedElement.style.visibility = 'hidden';
        } else {
            this.classList.add('incorrect');
            setTimeout(() => {
                this.classList.remove('incorrect');
            }, 500);
        }
    }
    return false;
}

// Touch handlers for mobile
let touchItem = null;

function handleTouchStart(e) {
    touchItem = this;
    selectedSource = this;
    this.classList.add('selected');
}

function handleTouchMove(e) {
    e.preventDefault();
}

function handleTouchEnd(e) {
    if (!touchItem) return;
    
    const touch = e.changedTouches[0];
    const target = document.elementFromPoint(touch.clientX, touch.clientY);
    
    if (target && target.classList.contains('drag-target')) {
        handleTargetSelection(target, touchItem);
    }
    
    touchItem.classList.remove('selected');
    touchItem = null;
}

function handleTargetClick(e) {
    if (selectedSource) {
        handleTargetSelection(this, selectedSource);
        selectedSource.classList.remove('selected');
        selectedSource = null;
    }
}

function handleTargetSelection(target, source) {
    const sourceData = source.dataset.source;
    const targetData = target.dataset.target;

    if (sourceData === targetData) {
        target.classList.add('correct');
        const placeholder = target.querySelector('.target-placeholder');
        const answer = target.querySelector('.target-answer');
        if (placeholder) placeholder.style.display = 'none';
        if (answer) answer.style.display = 'block';
        source.style.visibility = 'hidden';
        
        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(20);
        }
    } else {
        target.classList.add('incorrect');
        setTimeout(() => {
            target.classList.remove('incorrect');
        }, 500);
        
        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(40);
        }
    }
}

// ============= END OF RELATIONS FUNCTIONS =============

// Update navigation buttons based on current position
function updateNavigationButtons() {
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (prevBtn) {
        prevBtn.disabled = currentPhaseIndex === 0;
        prevBtn.style.opacity = currentPhaseIndex === 0 ? '0.5' : '1';
        prevBtn.style.cursor = currentPhaseIndex === 0 ? 'not-allowed' : 'pointer';
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentPhaseIndex >= phaseKeys.length - 1;
        nextBtn.style.opacity = currentPhaseIndex >= phaseKeys.length - 1 ? '0.5' : '1';
        nextBtn.style.cursor = currentPhaseIndex >= phaseKeys.length - 1 ? 'not-allowed' : 'pointer';
    }
}

// Safe click handler for journey points
function handleJourneyPointClick(point, index) {
    if (isTransitioning) return;
    
    const journeyPoints = document.querySelectorAll('.journey-point');
    journeyPoints.forEach(p => p.classList.remove('active'));
    point.classList.add('active');
    currentPhaseIndex = index;
    displayVocabulary(point.dataset.phase);

    // Provide haptic feedback on supported devices
    if (navigator.vibrate && isTouchDevice) {
        navigator.vibrate(10); // Short vibration feedback
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('[Init] Starting initialization...');

    const journeyPoints = document.querySelectorAll('.journey-point');
    initializeProgressLine();
    attachQuizHandlers();
    initializeConstructor();

    // Initialize relation toggles
    const relationToggles = document.querySelectorAll('.relation-toggle');
    relationToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const section = this.closest('.relation-section');
            if (section) {
                section.classList.toggle('expanded');
                const content = section.querySelector('.relations-content');
                if (content) {
                    if (section.classList.contains('expanded')) {
                        content.style.maxHeight = content.scrollHeight + 'px';
                    } else {
                        content.style.maxHeight = '0';
                    }
                }
            }
        });
    });

    console.log('[Init] Found', journeyPoints.length, 'journey points');
    
    // ИСПРАВЛЕНИЕ: Упрощенная логика обработчиков для всех устройств
    journeyPoints.forEach((point, index) => {
        // Универсальный обработчик клика для всех устройств
        point.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            handleJourneyPointClick(this, index);
        });
        
        // Дополнительная поддержка touch для мобильных
        if (isTouchDevice) {
            // Визуальная обратная связь при касании
            point.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            point.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 100);
            });
        }
        
        // Курсор pointer для всех устройств
        point.style.cursor = 'pointer';
    });
    
    // Previous button handler - ИСПРАВЛЕНО
    const prevBtn = document.querySelector('.prev-btn');
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (!isTransitioning && currentPhaseIndex > 0) {
                currentPhaseIndex--;
                const targetPoint = journeyPoints[currentPhaseIndex];
                if (targetPoint) {
                    handleJourneyPointClick(targetPoint, currentPhaseIndex);
                }
                
                // Haptic feedback для мобильных
                if (navigator.vibrate && isTouchDevice) {
                    navigator.vibrate(10);
                }
            }
        });
    }
    
    // Next button handler - ИСПРАВЛЕНО
    const nextBtn = document.querySelector('.next-btn');
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (!isTransitioning && currentPhaseIndex < phaseKeys.length - 1) {
                currentPhaseIndex++;
                const targetPoint = journeyPoints[currentPhaseIndex];
                if (targetPoint) {
                    handleJourneyPointClick(targetPoint, currentPhaseIndex);
                }
                
                // Haptic feedback для мобильных
                if (navigator.vibrate && isTouchDevice) {
                    navigator.vibrate(10);
                }
            }
        });
    }
    
    // Initialize first phase
    if (journeyPoints.length > 0 && phaseKeys.length > 0) {
        console.log('[Init] Initializing first phase:', phaseKeys[0]);
        journeyPoints[0].classList.add('active');
        displayVocabulary(phaseKeys[0]);
    } else {
        console.error('[Init] No journey points or phases found!');
    }
    
    // Add swipe support for mobile navigation
    if (isTouchDevice) {
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, false);
        
        document.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, false);
        
        function handleSwipe() {
            const swipeThreshold = 50; // Minimum distance for swipe
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swiped left - go to next phase
                    if (nextBtn && !nextBtn.disabled) {
                        nextBtn.click();
                    }
                } else {
                    // Swiped right - go to previous phase
                    if (prevBtn && !prevBtn.disabled) {
                        prevBtn.click();
                    }
                }
            }
        }
    }
    
    console.log('[Init] Initialization complete');
});

// Function to toggle answers in exercise - РАБОТАЕТ ДЛЯ ВСЕХ
function toggleAnswers(button) {
    // Prevent double tap/click
    if (button.dataset.processing === 'true') return;
    button.dataset.processing = 'true';
    
    const exerciseSection = button.closest('.exercise-section');
    if (!exerciseSection) {
        console.error('Exercise section not found');
        button.dataset.processing = 'false';
        return;
    }
    
    const exerciseText = exerciseSection.querySelector('.exercise-text');
    const blanks = exerciseText.querySelectorAll('.blank');
    
    if (button.textContent === 'Показать ответы') {
        // Show answers
        blanks.forEach(blank => {
            const answer = blank.getAttribute('data-answer');
            const hint = blank.getAttribute('data-hint');
            if (answer && hint) {
                blank.innerHTML = answer + ' (' + hint + ')';
                blank.style.color = '#d97706';
                blank.style.fontWeight = '600';
                blank.style.fontStyle = 'normal';
                blank.style.borderBottomColor = '#22c55e';
            }
        });
        button.textContent = 'Скрыть ответы';
        button.style.background = 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)';
    } else {
        // Hide answers
        blanks.forEach(blank => {
            const hint = blank.getAttribute('data-hint');
            if (hint) {
                blank.innerHTML = '_______ (' + hint + ')';
                blank.style.color = '#a0aec0';
                blank.style.fontWeight = 'normal';
                blank.style.fontStyle = 'italic';
                blank.style.borderBottomColor = '#f6ad55';
            }
        });
        button.textContent = 'Показать ответы';
        button.style.background = 'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)';
    }
    
    // Haptic feedback for mobile
    if (navigator.vibrate && isTouchDevice) {
        navigator.vibrate(15);
    }
    
    // Reset processing flag
    setTimeout(() => {
        button.dataset.processing = 'false';
    }, 300);
}

// Initialize answer button handlers - УПРОЩЕНО
document.addEventListener('DOMContentLoaded', function() {
    const answerButtons = document.querySelectorAll('.show-answer-btn');
    
    answerButtons.forEach(button => {
        // Универсальный обработчик для всех устройств
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleAnswers(this);
        });
        
        // Визуальная обратная связь для мобильных
        if (isTouchDevice) {
            button.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.98)';
                this.style.opacity = '0.9';
            });
            
            button.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                    this.style.opacity = '1';
                }, 100);
            });
        }
    });
});

// Log device info for debugging
console.log('[Device Info]', {
    isTouchDevice: isTouchDevice,
    isIOS: isIOS,
    isAndroid: isAndroid,
    userAgent: navigator.userAgent,
    phaseCount: phaseKeys.length
});
'''
        return vocab_js
