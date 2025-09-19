"""JavaScript Generator for Lira Journey interactivity"""

import json
from pathlib import Path


class LiraJSGenerator:
    """Generate JavaScript for journey interactivity with mobile support"""

    _vocabulary_index = None

    @classmethod
    def _load_vocabulary_index(cls):
        """Load vocabulary enrichment data from the shared vocabulary file."""

        if cls._vocabulary_index is not None:
            return cls._vocabulary_index

        vocab_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "vocabulary"
            / "vocabulary.json"
        )

        index = {}

        if vocab_path.exists():
            with open(vocab_path, 'r', encoding='utf-8') as vocab_file:
                data = json.load(vocab_file)
                for entry in data.get('vocabulary', []):
                    german = (entry.get('german') or '').strip().lower()
                    if german:
                        index[german] = entry

        cls._vocabulary_index = index
        return cls._vocabulary_index

    @classmethod
    def _collect_relations(cls, german_word, phase_reference):
        """Return word family, synonyms and collocations for the given word/phase."""

        vocabulary = cls._load_vocabulary_index()
        entry = vocabulary.get((german_word or '').strip().lower())

        if not entry:
            return [], [], []

        def _filter_items(items, base_word_key):
            filtered = []
            for item in items:
                if not isinstance(item, dict):
                    continue

                phases = item.get('phases') or []
                if phases and phase_reference and phase_reference not in phases:
                    continue

                formatted = {
                    base_word_key: entry.get('german', ''),
                }

                for key, value in item.items():
                    if key == 'phases':
                        continue
                    formatted_key = {
                        'part_of_speech': 'partOfSpeech',
                    }.get(key, key)
                    formatted[formatted_key] = value

                filtered.append(formatted)

            return filtered

        families = _filter_items(entry.get('word_family', []), 'baseWord')
        synonyms = _filter_items(entry.get('synonyms', []), 'baseWord')
        collocations = _filter_items(entry.get('collocations', []), 'baseWord')

        return families, synonyms, collocations

    @staticmethod
    def generate(character_data):
        """Generate JS with vocabulary data from character JSON"""

        character_id = character_data.get('id', '')

        # Build vocabulary object from character data using JSON serialization
        phase_vocabularies = {}

        for phase in character_data.get('journey_phases', []):
            phase_id = phase.get('id')
            if not phase_id:
                continue

            phase_reference = f"{character_id}:{phase_id}" if character_id else None

            words = []
            for word in phase.get('vocabulary', []):
                word_families, synonyms, collocations = LiraJSGenerator._collect_relations(
                    word.get('german'),
                    phase_reference,
                )

                words.append({
                    'word': word.get('german', ''),
                    'translation': word.get('russian', ''),
                    'transcription': word.get('transcription', ''),
                    'sentence': word.get('sentence', ''),
                    'sentenceTranslation': word.get('sentence_translation', ''),
                    'wordFamily': word_families,
                    'synonyms': synonyms,
                    'collocations': collocations,
                })

            phase_vocabularies[phase_id] = {
                'title': phase.get('title', ''),
                'description': phase.get('description', ''),
                'words': words,
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
let relationsContainer = null;
let relationsEmptyState = null;
let relationsFeedbackElement = null;
let relationsBaseList = null;
let relationsTargetList = null;
let relationsTargetTitle = null;
let relationToggles = [];
const relationState = {
    activeType: 'families',
    selectedBase: null,
    matchedBases: new Set(),
    matchedTargets: new Set(),
    data: {
        families: [],
        collocations: [],
        baseWords: {
            families: [],
            collocations: []
        }
    }
};

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

function resetRelationState() {
    relationState.selectedBase = null;
    relationState.matchedBases.clear();
    relationState.matchedTargets.clear();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function handleTargetSelection(item, itemId) {
    if (!relationState.selectedBase) {
        if (relationsFeedbackElement) {
            relationsFeedbackElement.textContent = 'Сначала выберите слово слева.';
        }
        return;
    }

    if (relationState.matchedTargets.has(itemId)) {
        return;
    }

    if (item.baseWord === relationState.selectedBase) {
        relationState.matchedTargets.add(itemId);
        relationState.matchedBases.add(item.baseWord);
        relationState.selectedBase = null;

        if (relationsFeedbackElement) {
            const mainPart = relationState.activeType === 'families'
                ? `${item.word} — ${item.translation || ''}`
                : `${item.phrase} — ${item.translation || ''}`;
            let detail = `Отлично! ${mainPart.trim()}`;
            if (relationState.activeType === 'collocations' && item.example) {
                detail += ` (${item.example})`;
            }
            relationsFeedbackElement.textContent = detail;

            const totalMatches = relationState.data.baseWords[relationState.activeType].length;
            if (totalMatches > 0 && relationState.matchedBases.size === totalMatches) {
                relationsFeedbackElement.textContent += ' Все пары для этой категории подобраны!';
            }
        }

        renderRelations();
    } else {
        if (relationsFeedbackElement) {
            relationsFeedbackElement.textContent = 'Это не подходит, попробуйте другую пару.';
        }
        if (relationsBaseList) {
            const selectedButton = relationsBaseList.querySelector(`button[data-word="${relationState.selectedBase}"]`);
            if (selectedButton) {
                selectedButton.classList.add('shake');
                setTimeout(() => selectedButton.classList.remove('shake'), 400);
            }
        }
    }
}

function renderRelations() {
    if (!relationsBaseList || !relationsTargetList) return;

    const type = relationState.activeType;
    const baseWords = relationState.data.baseWords[type] || [];
    const items = relationState.data[type] || [];

    relationsBaseList.innerHTML = '';
    relationsTargetList.innerHTML = '';

    if (relationsTargetTitle) {
        relationsTargetTitle.textContent = type === 'families' ? 'Родственные формы' : 'Устойчивые выражения';
    }

    baseWords.forEach(baseWord => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'relation-card base-card';
        button.textContent = baseWord;
        button.dataset.word = baseWord;
        button.disabled = relationState.matchedBases.has(baseWord);

        if (relationState.selectedBase === baseWord) {
            button.classList.add('selected');
        }
        if (relationState.matchedBases.has(baseWord)) {
            button.classList.add('matched');
        }

        button.addEventListener('click', () => {
            if (relationState.matchedBases.has(baseWord)) return;
            relationState.selectedBase = relationState.selectedBase === baseWord ? null : baseWord;
            renderRelations();
        });

        relationsBaseList.appendChild(button);
    });

    const shuffledItems = shuffleArray(items.slice());
    shuffledItems.forEach(item => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'relation-card target-card';

        const identifier = `${type}:${item.baseWord}:${type === 'families' ? item.word : item.phrase}`;
        button.dataset.id = identifier;
        button.dataset.baseWord = item.baseWord;

        if (relationState.matchedTargets.has(identifier)) {
            button.classList.add('matched');
            button.disabled = true;
        }

        const mainLine = type === 'families' ? item.word : item.phrase;
        const details = [];

        if (item.translation) {
            details.push(item.translation);
        }

        if (type === 'families') {
            if (item.partOfSpeech) {
                details.push(item.partOfSpeech);
            }
            if (item.note) {
                details.push(item.note);
            }
        } else if (item.example) {
            details.push(item.example);
        }

        button.innerHTML = `<span class="relation-main">${mainLine}</span>` +
            (details.length ? `<span class="relation-sub">${details.join(' • ')}</span>` : '');

        button.addEventListener('click', () => handleTargetSelection(item, identifier));
        relationsTargetList.appendChild(button);
    });
}

function setupRelationsForPhase(phaseKey) {
    if (!relationsContainer || !relationsEmptyState) return;

    const phase = phaseVocabularies[phaseKey];
    if (!phase) return;

    const families = [];
    const collocations = [];
    const familyBaseWords = new Set();
    const collocationBaseWords = new Set();

    (phase.words || []).forEach(word => {
        if (Array.isArray(word.wordFamily) && word.wordFamily.length) {
            word.wordFamily.forEach(item => {
                families.push({
                    baseWord: word.word,
                    word: item.word,
                    translation: item.translation || '',
                    partOfSpeech: item.partOfSpeech || '',
                    note: item.note || ''
                });
            });
            familyBaseWords.add(word.word);
        }

        if (Array.isArray(word.collocations) && word.collocations.length) {
            word.collocations.forEach(item => {
                collocations.push({
                    baseWord: word.word,
                    phrase: item.phrase,
                    translation: item.translation || '',
                    example: item.example || ''
                });
            });
            collocationBaseWords.add(word.word);
        }
    });

    relationState.data = {
        families,
        collocations,
        baseWords: {
            families: Array.from(familyBaseWords),
            collocations: Array.from(collocationBaseWords)
        }
    };

    resetRelationState();

    const hasFamilies = families.length > 0;
    const hasCollocations = collocations.length > 0;

    relationState.activeType = hasFamilies ? 'families' : 'collocations';

    relationToggles.forEach(toggle => {
        const type = toggle.dataset.type;
        const hasData = type === 'families' ? hasFamilies : hasCollocations;
        toggle.disabled = !hasData;
        toggle.classList.toggle('disabled', !hasData);
        toggle.setAttribute('aria-disabled', String(!hasData));
        toggle.classList.toggle('active', relationState.activeType === type && hasData);
    });

    if (!hasFamilies && !hasCollocations) {
        relationsContainer.classList.add('hidden');
        relationsEmptyState.classList.remove('hidden');
        if (relationsFeedbackElement) {
            relationsFeedbackElement.textContent = 'Для этой фазы пока нет данных о родственных словах или коллокациях.';
        }
        if (relationsBaseList) relationsBaseList.innerHTML = '';
        if (relationsTargetList) relationsTargetList.innerHTML = '';
        return;
    }

    relationsEmptyState.classList.add('hidden');
    relationsContainer.classList.remove('hidden');

    if (relationsFeedbackElement) {
        relationsFeedbackElement.textContent = relationState.activeType === 'families'
            ? 'Сопоставьте слово с родственной формой справа.'
            : 'Сопоставьте слово с подходящим выражением справа.';
    }

    renderRelations();
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
    
    grid.innerHTML = '';
    
    phase.words.forEach((item, index) => {
        setTimeout(() => {
            const card = document.createElement('div');
            card.className = 'word-card';
            card.style.animationDelay = `${index * 0.1}s`;
            card.innerHTML = `
                <div class="word-german">${item.word}</div>
                <div class="word-translation">${item.translation}</div>
                <div class="word-transcription">${item.transcription}</div>
                <div class="word-sentence">
                    <div class="sentence-german">"${item.sentence}"</div>
                    <div class="sentence-translation">${item.sentenceTranslation}</div>
                </div>
            `;
            grid.appendChild(card);
        }, index * 50);
    });

    setupRelationsForPhase(phaseKey);

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
    relationsContainer = document.getElementById('word-relations-game');
    relationsEmptyState = document.querySelector('.relations-empty-state');
    relationsFeedbackElement = document.querySelector('.relations-feedback');
    relationsBaseList = document.querySelector('.relations-list.base-list');
    relationsTargetList = document.querySelector('.relations-list.target-list');
    relationsTargetTitle = document.querySelector('.target-title');
    relationToggles = Array.from(document.querySelectorAll('.relations-toggle'));

    relationToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            if (this.disabled || this.classList.contains('disabled')) {
                return;
            }

            relationState.activeType = this.dataset.type;
            resetRelationState();
            relationToggles.forEach(btn => btn.classList.toggle('active', btn === this));

            if (relationsFeedbackElement) {
                relationsFeedbackElement.textContent = this.dataset.type === 'families'
                    ? 'Сопоставьте слово с родственной формой справа.'
                    : 'Сопоставьте слово с подходящим выражением справа.';
            }

            renderRelations();
        });
    });

    initializeProgressLine();

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
