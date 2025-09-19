"""JavaScript Generator for Lira Journey interactivity"""

import json


class LiraJSGenerator:
    """Generate JavaScript for journey interactivity with mobile support"""
    
    @staticmethod
    def generate(character_data):
        """Generate JS with vocabulary data from character JSON"""
        
        # Build vocabulary object from character data using JSON serialization
        phase_vocabularies = {}
        phase_constructor_data = {}

        for phase in character_data.get('journey_phases', []):
            phase_id = phase.get('id')
            if not phase_id:
                continue

            words = []
            constructor_items = []
            for index, word in enumerate(phase.get('vocabulary', [])):
                themes = word.get('themes') or []
                if isinstance(themes, str):
                    themes = [themes]
                elif not isinstance(themes, list):
                    themes = []

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

                sentence_parts_raw = word.get('sentence_parts') or []
                if isinstance(sentence_parts_raw, list):
                    sentence_parts = [
                        part for part in sentence_parts_raw if isinstance(part, str)
                    ]
                else:
                    sentence_parts = []

                words.append({
                    'word': word.get('german', ''),
                    'translation': word.get('russian', ''),
                    'transcription': word.get('transcription', ''),
                    'sentence': word.get('sentence', ''),
                    'sentenceTranslation': word.get('sentence_translation', ''),
                    'sentenceParts': sentence_parts,
                    'visual_hint': word.get('visual_hint', ''),
                    'themes': themes,
                    'wordFamily': word_family,  # Для relations
                    'synonyms': synonyms,        # Для relations
                    'collocations': collocations # Для relations
                })

                if sentence_parts and len(sentence_parts) >= 2:
                    constructor_items.append({
                        'uid': f"{phase_id}-{index}",
                        'word': word.get('german', ''),
                        'sentence': word.get('sentence', ''),
                        'sentenceTranslation': word.get('sentence_translation', ''),
                        'sentenceParts': sentence_parts,
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
                'quizAttempts': {},
                'constructorItems': constructor_items,
            }

            if constructor_items:
                phase_constructor_data[phase_id] = constructor_items

        character_id = character_data.get('id') or character_data.get('slug') or 'journey'

        vocab_js = (
            "const phaseVocabularies = "
            f"{json.dumps(phase_vocabularies, ensure_ascii=False, indent=4)};\n\n"
        )

        vocab_js += (
            "const phaseConstructorData = "
            f"{json.dumps(phase_constructor_data, ensure_ascii=False, indent=4)};\n\n"
        )

        vocab_js += f"const characterId = {json.dumps(character_id)};\n"
        vocab_js += "const STORAGE_PREFIX = 'liraJourney';\n"
        vocab_js += "const REVIEW_QUEUE_KEY = `${STORAGE_PREFIX}:reviewQueue`;\n"
        vocab_js += "const quizStateCache = {};\n\n"

        # Add enhanced mobile-friendly interaction code
        vocab_js += '''
let currentPhaseIndex = 0;
const phaseKeys = Object.keys(phaseVocabularies);
let isTransitioning = false; // Prevent double clicks/taps
let progressLineElement = null;
let progressLineLength = 0;
const QUIZ_ADVANCE_DELAY = 1200;

function getPhaseStorageKey(phaseKey) {
    const safePhase = phaseKey || 'unknown';
    return `${STORAGE_PREFIX}:${characterId}:${safePhase}:quizAttempts`;
}

function loadPhaseQuizState(phaseKey) {
    if (quizStateCache[phaseKey]) {
        return quizStateCache[phaseKey];
    }

    if (typeof localStorage === 'undefined') {
        quizStateCache[phaseKey] = {};
        return quizStateCache[phaseKey];
    }

    let storedValue = null;
    try {
        storedValue = localStorage.getItem(getPhaseStorageKey(phaseKey));
    } catch (error) {
        console.warn(`[QuizState] Unable to access storage for ${phaseKey}`, error);
    }

    if (!storedValue) {
        quizStateCache[phaseKey] = {};
        return quizStateCache[phaseKey];
    }

    try {
        const parsed = JSON.parse(storedValue);
        if (parsed && typeof parsed === 'object') {
            quizStateCache[phaseKey] = parsed;
            return parsed;
        }
    } catch (error) {
        console.warn(`[QuizState] Failed to parse stored state for ${phaseKey}`, error);
    }

    quizStateCache[phaseKey] = {};
    return quizStateCache[phaseKey];
}

function savePhaseQuizState(phaseKey, state) {
    quizStateCache[phaseKey] = state;
    if (phaseVocabularies[phaseKey]) {
        phaseVocabularies[phaseKey].quizAttempts = state;
    }

    if (typeof localStorage === 'undefined') {
        return;
    }

    try {
        localStorage.setItem(getPhaseStorageKey(phaseKey), JSON.stringify(state));
    } catch (error) {
        console.warn(`[QuizState] Unable to save state for ${phaseKey}`, error);
    }
}

function getPhaseQuizState(phaseKey) {
    const phase = phaseVocabularies[phaseKey];
    if (!phase) {
        return {};
    }

    const storedState = loadPhaseQuizState(phaseKey);
    if (!phase.quizAttempts || phase.quizAttempts !== storedState) {
        phase.quizAttempts = storedState;
    }

    return phase.quizAttempts;
}

function extractQuizWord(questionText) {
    if (!questionText || typeof questionText !== 'string') {
        return '';
    }

    const angleMatch = questionText.match(/«([^»]+)»/);
    if (angleMatch && angleMatch[1]) {
        return angleMatch[1].trim();
    }

    const quoteMatch = questionText.match(/"([^"]+)"/);
    if (quoteMatch && quoteMatch[1]) {
        return quoteMatch[1].trim();
    }

    return '';
}

function findPhaseWord(phaseKey, targetWord) {
    if (!targetWord) {
        return null;
    }

    const phase = phaseVocabularies[phaseKey];
    if (!phase || !Array.isArray(phase.words)) {
        return null;
    }

    const normalizedTarget = targetWord.toLowerCase();
    return phase.words.find(entry => {
        const wordValue = (entry.word || '').toLowerCase();
        return wordValue === normalizedTarget;
    }) || null;
}

function recordQuizAttempt(phaseKey, questionIndex, selectedIndex, correctIndex, choiceLabels) {
    if (!phaseKey) {
        return;
    }

    const phase = phaseVocabularies[phaseKey];
    if (!phase) {
        return;
    }

    const quizState = getPhaseQuizState(phaseKey);
    const quizList = Array.isArray(phase.quizzes) ? phase.quizzes : [];
    const questionMeta = quizList[questionIndex] || {};
    const questionText = questionMeta.question || '';
    const detectedWord = questionMeta.targetWord || extractQuizWord(questionText);
    if (detectedWord && !questionMeta.targetWord) {
        questionMeta.targetWord = detectedWord;
    }

    const timestamp = new Date().toISOString();
    const attemptRecord = {
        selectedIndex: selectedIndex,
        correctIndex: correctIndex,
        isCorrect: selectedIndex === correctIndex,
        timestamp: timestamp,
        selectedChoice: Array.isArray(choiceLabels) && choiceLabels[selectedIndex] !== undefined
            ? choiceLabels[selectedIndex]
            : null,
        correctChoice: Array.isArray(choiceLabels) && choiceLabels[correctIndex] !== undefined
            ? choiceLabels[correctIndex]
            : null,
    };

    if (!quizState[questionIndex] || typeof quizState[questionIndex] !== 'object') {
        quizState[questionIndex] = {
            attempts: [],
            targetWord: detectedWord || '',
            question: questionText,
        };
    }

    const questionState = quizState[questionIndex];
    if (detectedWord && !questionState.targetWord) {
        questionState.targetWord = detectedWord;
    }
    if (questionText && !questionState.question) {
        questionState.question = questionText;
    }

    questionState.attempts.push(attemptRecord);
    questionState.lastCorrect = attemptRecord.isCorrect;
    questionState.lastUpdated = timestamp;
    questionState.lastSelectedChoice = attemptRecord.selectedChoice;
    questionState.correctChoice = attemptRecord.correctChoice;

    savePhaseQuizState(phaseKey, quizState);
    updateQuizStatsUI(phaseKey);
}

function computePhaseQuizStats(phaseKey) {
    const phase = phaseVocabularies[phaseKey];
    const quizList = phase && Array.isArray(phase.quizzes) ? phase.quizzes : [];
    const quizState = getPhaseQuizState(phaseKey);

    const total = quizList.length;
    let answered = 0;
    let correct = 0;
    const incorrectDetails = [];

    quizList.forEach((quizItem, index) => {
        const stateEntry = quizState[index];
        if (!stateEntry || !Array.isArray(stateEntry.attempts) || stateEntry.attempts.length === 0) {
            return;
        }

        answered += 1;
        const lastAttempt = stateEntry.attempts[stateEntry.attempts.length - 1];
        const questionText = stateEntry.question || (quizItem ? quizItem.question : '');
        const targetWord = stateEntry.targetWord || (quizItem ? quizItem.targetWord : '');
        const wordData = findPhaseWord(phaseKey, targetWord);

        if (lastAttempt.isCorrect) {
            correct += 1;
        } else {
            incorrectDetails.push({
                word: targetWord || (wordData ? wordData.word : ''),
                translation: wordData ? wordData.translation : '',
                question: questionText,
                selected: lastAttempt.selectedChoice,
                correctAnswer: lastAttempt.correctChoice,
                questionIndex: index,
            });
        }
    });

    return {
        total: total,
        answered: answered,
        correct: correct,
        incorrectDetails: incorrectDetails,
    };
}

function updateQuizStatsUI(phaseKey) {
    const statsPanel = document.querySelector('.quiz-stats-panel');
    if (!statsPanel) {
        return;
    }

    const phase = phaseVocabularies[phaseKey];
    const stats = computePhaseQuizStats(phaseKey);
    const phaseNameElement = statsPanel.querySelector('[data-quiz-phase-name]');
    const summaryElement = statsPanel.querySelector('[data-quiz-summary]');
    const progressElement = statsPanel.querySelector('[data-quiz-progress]');
    const errorsContainer = statsPanel.querySelector('[data-quiz-errors]');

    statsPanel.dataset.phase = phaseKey || '';

    if (phaseNameElement) {
        phaseNameElement.textContent = phase ? phase.title : '—';
    }

    if (summaryElement) {
        if (!stats.total) {
            summaryElement.textContent = 'Для этой фазы пока нет викторины.';
        } else {
            summaryElement.textContent = `Пройдено ${stats.answered} из ${stats.total} вопросов.`;
        }
    }

    if (progressElement) {
        if (!stats.total) {
            progressElement.textContent = '—';
        } else {
            const percent = Math.round((stats.correct / stats.total) * 100);
            progressElement.textContent = `${stats.correct} из ${stats.total} верно (${percent}%)`;
        }
    }

    if (errorsContainer) {
        if (!stats.total) {
            errorsContainer.innerHTML = '<p class="quiz-errors-empty">Ошибок пока нет — вопросы появятся позже.</p>';
        } else if (!stats.incorrectDetails.length) {
            errorsContainer.innerHTML = '<p class="quiz-errors-empty">Ошибок пока нет — отличная работа!</p>';
        } else {
            const items = stats.incorrectDetails.map(detail => {
                const translation = detail.translation ? ` — ${detail.translation}` : '';
                const question = detail.question
                    ? `<div class="quiz-error-question">${detail.question}</div>`
                    : '';
                const userAnswer = detail.selected
                    ? `<span class="quiz-error-answer">Ваш ответ: ${detail.selected}</span>`
                    : '';
                const correctAnswer = detail.correctAnswer
                    ? `<span class="quiz-error-correct">Верно: ${detail.correctAnswer}</span>`
                    : '';
                return `
                    <li class="quiz-error-item" data-question-index="${detail.questionIndex}">
                        <strong>${detail.word || 'Слово'}</strong>${translation}
                        ${question}
                        <div class="quiz-error-meta">
                            ${userAnswer}
                            ${correctAnswer}
                        </div>
                    </li>
                `;
            }).join('');
            errorsContainer.innerHTML = `<ul class="quiz-error-list">${items}</ul>`;
        }
    }

    statsPanel.classList.toggle('quiz-stats-empty', !stats.total);
    statsPanel.classList.toggle('quiz-stats-has-errors', stats.incorrectDetails.length > 0);
}

function queuePhaseReview(detail) {
    if (typeof localStorage === 'undefined') {
        return;
    }

    let queue = [];
    try {
        const stored = localStorage.getItem(REVIEW_QUEUE_KEY);
        if (stored) {
            const parsed = JSON.parse(stored);
            if (Array.isArray(parsed)) {
                queue = parsed;
            }
        }
    } catch (error) {
        console.warn('[ReviewQueue] Unable to read review queue', error);
    }

    queue = queue.filter(entry => {
        if (!entry) return false;
        return !(entry.characterId === detail.characterId && entry.phaseId === detail.phaseId);
    });

    if (detail.incorrectWords && detail.incorrectWords.length > 0) {
        queue.push(detail);
    }

    try {
        localStorage.setItem(REVIEW_QUEUE_KEY, JSON.stringify(queue));
    } catch (error) {
        console.warn('[ReviewQueue] Unable to update review queue', error);
    }
}

function handlePhaseCompletion(phaseKey) {
    if (!phaseKey) {
        return;
    }

    const stats = computePhaseQuizStats(phaseKey);
    if (!stats.total || stats.answered < stats.total) {
        return;
    }

    const timestamp = new Date().toISOString();
    const phase = phaseVocabularies[phaseKey] || {};
    const eventDetail = {
        characterId: characterId,
        phaseId: phaseKey,
        phaseTitle: phase.title || '',
        completedAt: timestamp,
        incorrectWords: stats.incorrectDetails.map(item => ({
            word: item.word,
            translation: item.translation,
            question: item.question,
            selected: item.selected,
            correctAnswer: item.correctAnswer,
        })),
    };

    queuePhaseReview(eventDetail);

    try {
        document.dispatchEvent(new CustomEvent('journeyPhaseCompleted', { detail: eventDetail }));
    } catch (error) {
        console.warn('[JourneyPhase] Unable to dispatch completion event', error);
    }

    const quizState = getPhaseQuizState(phaseKey);
    quizState.__lastCompletion = timestamp;
    savePhaseQuizState(phaseKey, quizState);
}

// Device detection
const isTouchDevice = ('ontouchstart' in window) ||
                      (navigator.maxTouchPoints > 0) ||
                      (navigator.msMaxTouchPoints > 0);
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
const isAndroid = /Android/.test(navigator.userAgent);

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

    getPhaseQuizState(phaseKey);
    updateQuizStatsUI(phaseKey);

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

    const phaseKey = container.dataset.phase || null;
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

        if (phaseKey) {
            handlePhaseCompletion(phaseKey);
        }
    }

    if (phaseKey) {
        updateQuizStatsUI(phaseKey);
    }
}

function handleQuizChoiceSelection(button) {
    if (!button) return;

    const quizCard = button.closest('.quiz-card');
    if (!quizCard || quizCard.dataset.answered === 'true') {
        return;
    }

    const container = quizCard.closest('.quiz-phase-container');
    const phaseKey = container ? container.dataset.phase : null;
    const questionIndex = parseInt(quizCard.dataset.questionIndex || '0', 10);
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

    const choiceLabels = choices.map(choice => choice.textContent.trim());
    recordQuizAttempt(phaseKey, questionIndex, selectedIndex, correctIndex, choiceLabels);

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
    if (familiesSection) {
        const content = familiesSection.querySelector('.relations-content');
        familiesSection.dataset.hasContent = wordFamilies.length > 0 ? 'true' : 'false';

        if (content) {
            if (wordFamilies.length > 0) {
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
            } else {
                content.innerHTML = '';
            }
        }
    }

    // Render Synonyms section
    const synonymsSection = container.querySelector('.synonyms-section');
    if (synonymsSection) {
        const content = synonymsSection.querySelector('.relations-content');
        const synonymPairs = [];

        synonymGroups.forEach((item, groupIdx) => {
            if (!item || !item.synonyms) return;
            item.synonyms.forEach((synonym, synonymIdx) => {
                synonymPairs.push({
                    id: `syn-${groupIdx}-${synonymIdx}`,
                    prompt: item.word,
                    match: synonym
                });
            });
        });

        synonymsSection.dataset.hasContent = synonymPairs.length > 0 ? 'true' : 'false';

        if (content) {
            if (synonymPairs.length > 0) {
                content.innerHTML = '';
                buildPairMatchingActivity(content, synonymPairs, {
                    promptLabel: 'Слова',
                    matchLabel: 'Синонимы',
                    matchMessage: 'Отлично! Пара найдена.',
                    mismatchMessage: 'Не совпало. Попробуйте ещё раз.',
                    successMessage: 'Вы подобрали все синонимичные пары!'
                });
            } else {
                content.innerHTML = '<div class="relations-empty-state">Синонимы для этой фазы отсутствуют.</div>';
            }
        }
    }

    // Render Collocations section
    const collocationsSection = container.querySelector('.collocations-section');
    if (collocationsSection) {
        const content = collocationsSection.querySelector('.relations-content');
        const collocationPairs = [];

        collocations.forEach((item, groupIdx) => {
            if (!item || !item.collocations) return;
            item.collocations.forEach((phrase, phraseIdx) => {
                collocationPairs.push({
                    id: `col-${groupIdx}-${phraseIdx}`,
                    prompt: item.word,
                    match: phrase
                });
            });
        });

        collocationsSection.dataset.hasContent = collocationPairs.length > 0 ? 'true' : 'false';

        if (content) {
            if (collocationPairs.length > 0) {
                content.innerHTML = '';
                buildMemoryGame(content, collocationPairs, {
                    matchMessage: 'Ура! Коллокация открыта.',
                    mismatchMessage: 'Эти карточки не образуют пару.',
                    successMessage: 'Все коллокации найдены!'
                });
            } else {
                content.innerHTML = '<div class="relations-empty-state">Коллокации для этой фазы отсутствуют.</div>';
            }
        }
    }
}

function addInteractiveListener(element, handler) {
    if (!element || typeof handler !== 'function') return;

    let touchTriggered = false;
    const invokeHandler = function(event) {
        handler.call(this, event);
    };

    if (isTouchDevice) {
        element.addEventListener('touchstart', function(event) {
            touchTriggered = true;
            if (event.cancelable) {
                event.preventDefault();
            }
            invokeHandler.call(this, event);
        }, { passive: false });

        element.addEventListener('click', function(event) {
            if (touchTriggered) {
                touchTriggered = false;
                return;
            }
            if (event.cancelable) {
                event.preventDefault();
            }
            invokeHandler.call(this, event);
        });
    } else {
        element.addEventListener('click', function(event) {
            if (event.cancelable) {
                event.preventDefault();
            }
            invokeHandler.call(this, event);
        });
    }
}

function shuffleArray(array) {
    const copy = Array.isArray(array) ? array.slice() : [];
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
}

function buildPairMatchingActivity(container, pairs, options = {}) {
    if (!container || !pairs || pairs.length === 0) return;

    const settings = Object.assign({
        promptLabel: 'Колонка 1',
        matchLabel: 'Колонка 2',
        matchMessage: 'Верно! Пара найдена.',
        mismatchMessage: 'Пока не то. Попробуйте снова.',
        successMessage: 'Все пары подобраны!'
    }, options);

    container.classList.add('pair-matching-container');
    container.innerHTML = '';

    const layout = document.createElement('div');
    layout.className = 'pair-matching-layout';

    const promptsWrapper = document.createElement('div');
    promptsWrapper.className = 'pair-column-wrapper';
    const promptsLabel = document.createElement('div');
    promptsLabel.className = 'pair-column-label';
    promptsLabel.textContent = settings.promptLabel;
    const promptsColumn = document.createElement('div');
    promptsColumn.className = 'pair-column pair-prompts';

    const matchesWrapper = document.createElement('div');
    matchesWrapper.className = 'pair-column-wrapper';
    const matchesLabel = document.createElement('div');
    matchesLabel.className = 'pair-column-label';
    matchesLabel.textContent = settings.matchLabel;
    const matchesColumn = document.createElement('div');
    matchesColumn.className = 'pair-column pair-matches';

    promptsWrapper.appendChild(promptsLabel);
    promptsWrapper.appendChild(promptsColumn);
    matchesWrapper.appendChild(matchesLabel);
    matchesWrapper.appendChild(matchesColumn);

    layout.appendChild(promptsWrapper);
    layout.appendChild(matchesWrapper);

    const status = document.createElement('div');
    status.className = 'pair-status';
    status.textContent = 'Выберите слово и подходящий синоним.';

    container.appendChild(layout);
    container.appendChild(status);

    const promptCards = shuffleArray(pairs.map(pair => ({
        label: pair.prompt,
        pairId: pair.id
    })));

    const matchCards = shuffleArray(pairs.map(pair => ({
        label: pair.match,
        pairId: pair.id
    })));

    let activePrompt = null;
    let activeMatch = null;
    let remainingPairs = pairs.length;

    function updateStatus(message, type) {
        status.textContent = message || '';
        status.classList.remove('success', 'error');
        if (type) {
            status.classList.add(type);
        }
    }

    function handleMatchSuccess(promptCard, matchCard) {
        [promptCard, matchCard].forEach(card => {
            card.classList.remove('selected', 'incorrect');
            card.classList.add('matched', 'correct');
            card.setAttribute('disabled', 'true');
            card.setAttribute('aria-disabled', 'true');
        });

        remainingPairs -= 1;

        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(20);
        }

        if (remainingPairs === 0) {
            updateStatus(settings.successMessage, 'success');
        } else {
            updateStatus(settings.matchMessage, 'success');
        }
    }

    function handleMatchFailure(promptCard, matchCard) {
        [promptCard, matchCard].forEach(card => {
            card.classList.add('incorrect');
        });

        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(40);
        }

        updateStatus(settings.mismatchMessage, 'error');

        setTimeout(() => {
            [promptCard, matchCard].forEach(card => {
                card.classList.remove('incorrect', 'selected');
            });
        }, 650);
    }

    function evaluateSelection() {
        if (!activePrompt || !activeMatch) return;

        const promptCard = activePrompt;
        const matchCard = activeMatch;

        activePrompt = null;
        activeMatch = null;

        if (promptCard.dataset.pairId === matchCard.dataset.pairId) {
            handleMatchSuccess(promptCard, matchCard);
        } else {
            handleMatchFailure(promptCard, matchCard);
        }
    }

    function toggleSelection(card, type) {
        if (card.classList.contains('matched')) {
            return;
        }

        if (card.classList.contains('selected')) {
            card.classList.remove('selected');
            if (type === 'prompt') {
                activePrompt = null;
            } else {
                activeMatch = null;
            }
            return;
        }

        if (type === 'prompt') {
            if (activePrompt) {
                activePrompt.classList.remove('selected');
            }
            activePrompt = card;
        } else {
            if (activeMatch) {
                activeMatch.classList.remove('selected');
            }
            activeMatch = card;
        }

        card.classList.add('selected');
        evaluateSelection();
    }

    promptCards.forEach(data => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'pair-card pair-card-prompt';
        card.dataset.pairId = data.pairId;
        card.textContent = data.label;

        addInteractiveListener(card, function() {
            toggleSelection(card, 'prompt');
        });

        promptsColumn.appendChild(card);
    });

    matchCards.forEach(data => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'pair-card pair-card-match';
        card.dataset.pairId = data.pairId;
        card.textContent = data.label;

        addInteractiveListener(card, function() {
            toggleSelection(card, 'match');
        });

        matchesColumn.appendChild(card);
    });
}

function buildMemoryGame(container, pairs, options = {}) {
    if (!container || !pairs || pairs.length === 0) return;

    const settings = Object.assign({
        matchMessage: 'Пара найдена!',
        mismatchMessage: 'Это не пара.',
        successMessage: 'Все пары найдены!'
    }, options);

    container.classList.add('memory-game-container');
    container.innerHTML = '';

    const grid = document.createElement('div');
    grid.className = 'memory-card-grid';

    const status = document.createElement('div');
    status.className = 'memory-status';
    status.textContent = 'Откройте карточки и найдите совпадающие пары.';

    container.appendChild(grid);
    container.appendChild(status);

    const cardsData = [];
    pairs.forEach(pair => {
        cardsData.push({
            pairId: pair.id,
            label: pair.prompt,
            role: 'prompt'
        });
        cardsData.push({
            pairId: pair.id,
            label: pair.match,
            role: 'match'
        });
    });

    const shuffledCards = shuffleArray(cardsData);

    let flippedCards = [];
    let matchedPairs = 0;
    let boardLocked = false;

    function updateStatus(message, type) {
        status.textContent = message || '';
        status.classList.remove('success', 'error');
        if (type) {
            status.classList.add(type);
        }
    }

    function resetFlippedCards() {
        flippedCards.forEach(card => {
            card.classList.remove('flipped', 'incorrect');
        });
        flippedCards = [];
        boardLocked = false;
    }

    function handleCorrectMatch(firstCard, secondCard) {
        [firstCard, secondCard].forEach(card => {
            card.classList.add('matched', 'correct');
            card.setAttribute('disabled', 'true');
            card.setAttribute('aria-disabled', 'true');
        });

        matchedPairs += 1;
        flippedCards = [];

        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(25);
        }

        if (matchedPairs === pairs.length) {
            updateStatus(settings.successMessage, 'success');
        } else {
            updateStatus(settings.matchMessage, 'success');
        }
    }

    function handleIncorrectMatch(firstCard, secondCard) {
        boardLocked = true;
        [firstCard, secondCard].forEach(card => {
            card.classList.add('incorrect');
        });

        if (navigator.vibrate && isTouchDevice) {
            navigator.vibrate(40);
        }

        updateStatus(settings.mismatchMessage, 'error');

        setTimeout(() => {
            resetFlippedCards();
        }, 850);
    }

    function evaluateFlippedCards() {
        if (flippedCards.length < 2) return;

        const [firstCard, secondCard] = flippedCards;

        if (firstCard.dataset.pairId === secondCard.dataset.pairId && firstCard.dataset.cardRole !== secondCard.dataset.cardRole) {
            handleCorrectMatch(firstCard, secondCard);
        } else {
            handleIncorrectMatch(firstCard, secondCard);
        }
    }

    function handleCardInteraction(card) {
        if (boardLocked || card.classList.contains('matched') || card.classList.contains('flipped')) {
            return;
        }

        card.classList.add('flipped');
        flippedCards.push(card);
        evaluateFlippedCards();
    }

    shuffledCards.forEach(data => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'memory-card';
        card.dataset.pairId = data.pairId;
        card.dataset.cardRole = data.role;
        card.innerHTML = `
            <span class="memory-card-placeholder">?</span>
            <span class="memory-card-content">${data.label}</span>
        `;

        addInteractiveListener(card, function() {
            handleCardInteraction(card);
        });

        grid.appendChild(card);
    });
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
