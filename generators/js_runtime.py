"""Runtime JavaScript generator - inline JavaScript without modules."""

def generate_runtime_js():
    """Generate complete runtime JavaScript code."""
    return '''
let currentPhaseIndex = 0;
const phaseKeys = Object.keys(phaseVocabularies);
let isTransitioning = false;
let progressLineElement = null;
let progressLineLength = 0;
const QUIZ_ADVANCE_DELAY = 1200;
const constructorState = {};

function shuffleWords(words) {
    const shuffled = Array.isArray(words) ? [...words] : [];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function displayVocabulary(phaseKey) {
    // Prevent multiple rapid transitions
    if (isTransitioning) return;
    isTransitioning = true;

    const phase = phaseVocabularies[phaseKey];
    const grid = document.querySelector('.vocabulary-grid');
    const phaseTitle = document.getElementById('current-phase');
    const progressFill = document.querySelector('.journey-progress .progress-fill');
    const progressText = document.querySelector('.journey-progress .progress-text');
    
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

    // Clear and populate vocabulary grid
    grid.innerHTML = '';

    phase.words.forEach((item, index) => {
        setTimeout(() => {
            const card = document.createElement('div');
            card.className = 'word-card';
            card.style.animationDelay = `${index * 0.1}s`;

            const hintMarkup = item.russian_hint
                ? `<div class="word-hint">(${item.russian_hint})</div>`
                : '';

            card.innerHTML = `
                <div class="word-meta">
                    <div class="word-german">${item.word}</div>
                    <div class="word-translation">${item.translation}</div>
                    ${hintMarkup}
                    <div class="word-transcription">${item.transcription}</div>
                </div>
                <button class="btn-study" type="button">Изучить</button>
            `;

            grid.appendChild(card);
        }, index * 50);
    });

    // Update progress bar
    const progress = ((currentPhaseIndex + 1) / phaseKeys.length) * 100;
    if (progressFill) progressFill.style.width = progress + '%';
    if (progressText) progressText.textContent = phase.description;

    // Update navigation buttons state
    updateNavigationButtons();

    // Reset transition flag
    setTimeout(() => {
        isTransitioning = false;
    }, 500);
}

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

function handleJourneyPointClick(point, index) {
    if (isTransitioning) return;
    
    const journeyPoints = document.querySelectorAll('.journey-point');
    journeyPoints.forEach(p => p.classList.remove('active'));
    point.classList.add('active');
    currentPhaseIndex = index;
    displayVocabulary(point.dataset.phase);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Init] Starting initialization...');

    const journeyPoints = document.querySelectorAll('.journey-point');
    console.log('[Init] Found', journeyPoints.length, 'journey points');
    
    // Setup journey point clicks
    journeyPoints.forEach((point, index) => {
        point.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            handleJourneyPointClick(this, index);
        });
        
        point.style.cursor = 'pointer';
    });
    
    // Previous button handler
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
            }
        });
    }
    
    // Next button handler
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
    
    console.log('[Init] Initialization complete');
});

// Exercise toggle handlers
function toggleAnswers(button) {
    const exerciseSection = button.closest('.exercise-section');
    if (!exerciseSection) return;
    
    const exerciseText = exerciseSection.querySelector('.exercise-text');
    const blanks = exerciseText.querySelectorAll('.blank');
    
    if (button.textContent === 'Показать ответы') {
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
}

// Initialize answer button handlers
document.addEventListener('DOMContentLoaded', function() {
    const answerButtons = document.querySelectorAll('.show-answer-btn');
    answerButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleAnswers(this);
        });
    });
});

console.log('[Runtime] JavaScript loaded successfully');
'''
