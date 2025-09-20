import { VocabularyManager } from '../modules/vocabulary/loader.js';
import { StudyManager } from '../modules/vocabulary/study.js';
import { VocabularyDisplay } from '../modules/vocabulary/display.js';
import { WordExercises } from '../modules/exercises/word-match.js';
import { ConstructorExercise } from '../modules/exercises/constructor.js';
import { QuizManager } from '../modules/exercises/quiz.js';
import { ProgressTracker } from '../modules/navigation/progress.js';
import { PhaseNavigator } from '../modules/navigation/phases.js';
import { calculateExpandedExerciseContentHeight, refreshActiveExerciseContentHeight, updateWordColumnScrollIndicators } from '../modules/utils/dom.js';
import { vibrate } from '../modules/utils/animations.js';

export class JourneyApp {
    constructor() {
        this.isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0);
        this.isInitialized = false;
    }

    init() {
        if (this.isInitialized) {
            return;
        }
        this.vocabulary = new VocabularyManager();
        this.studyManager = new StudyManager({ characterId: this.vocabulary.getCharacterId() });
        this.wordExercises = new WordExercises();
        this.constructorExercise = new ConstructorExercise();
        this.quizManager = new QuizManager();
        this.progressTracker = new ProgressTracker();
        this.display = new VocabularyDisplay({
            vocabulary: this.vocabulary,
            studyManager: this.studyManager,
            quizManager: this.quizManager,
            wordExercises: this.wordExercises,
            constructorExercise: this.constructorExercise,
            progressTracker: this.progressTracker,
            isTouchDevice: this.isTouchDevice,
            onRendered: () => refreshActiveExerciseContentHeight(),
        });
        this.navigator = new PhaseNavigator({
            vocabulary: this.vocabulary,
            display: this.display,
            progress: this.progressTracker,
            isTouchDevice: this.isTouchDevice,
        });
        this.studyManager.init();
        this.constructorExercise.init();
        this.setupAccordion();
        this.setupAnswerButtons();
        this.navigator.init();
        this.isInitialized = true;
    }

    setupAccordion() {
        const toggles = Array.from(document.querySelectorAll('.exercise-toggle'));
        const contents = Array.from(document.querySelectorAll('.exercise-content'));
        const collapseAll = () => {
            contents.forEach(content => {
                content.classList.add('collapsed');
                content.classList.remove('expanded');
                if (content instanceof HTMLElement) {
                    content.style.maxHeight = '0px';
                }
            });
            toggles.forEach(toggle => toggle.classList.remove('active'));
        };
        toggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                const content = toggle.nextElementSibling;
                if (!(content instanceof HTMLElement)) {
                    return;
                }
                const collapsed = content.classList.contains('collapsed');
                collapseAll();
                if (collapsed) {
                    content.classList.remove('collapsed');
                    content.classList.add('expanded');
                    toggle.classList.add('active');
                    requestAnimationFrame(() => {
                        const height = calculateExpandedExerciseContentHeight(content);
                        content.style.maxHeight = `${height}px`;
                        updateWordColumnScrollIndicators(content);
                    });
                }
            });
        });
        if (toggles.length > 0) {
            const firstToggle = toggles[0];
            const firstContent = firstToggle.nextElementSibling;
            if (firstContent instanceof HTMLElement) {
                firstToggle.classList.add('active');
                firstContent.classList.remove('collapsed');
                firstContent.classList.add('expanded');
                requestAnimationFrame(() => {
                    const height = calculateExpandedExerciseContentHeight(firstContent);
                    firstContent.style.maxHeight = `${height}px`;
                    updateWordColumnScrollIndicators(firstContent);
                });
            }
        }
        window.addEventListener('resize', () => {
            refreshActiveExerciseContentHeight();
            updateWordColumnScrollIndicators();
        });
    }

    setupAnswerButtons() {
        const toggle = button => this.toggleAnswers(button);
        const buttons = Array.from(document.querySelectorAll('.show-answer-btn'));
        buttons.forEach(button => {
            button.addEventListener('click', event => {
                event.preventDefault();
                event.stopPropagation();
                toggle(button);
            });
            if (this.isTouchDevice) {
                button.addEventListener('touchstart', () => {
                    button.style.transform = 'scale(0.98)';
                    button.style.opacity = '0.9';
                });
                button.addEventListener('touchend', () => {
                    setTimeout(() => {
                        button.style.transform = 'scale(1)';
                        button.style.opacity = '1';
                    }, 100);
                });
            }
        });
        window.toggleAnswers = toggle;
    }

    toggleAnswers(button) {
        if (!button || button.dataset.processing === 'true') {
            return;
        }
        button.dataset.processing = 'true';
        const section = button.closest('.exercise-section');
        const exerciseText = section ? section.querySelector('.exercise-text') : null;
        const blanks = exerciseText ? exerciseText.querySelectorAll('.blank') : [];
        const showAnswers = button.textContent === 'Показать ответы';
        blanks.forEach(blank => {
            if (!(blank instanceof HTMLElement)) return;
            const answer = blank.getAttribute('data-answer');
            const hint = blank.getAttribute('data-hint');
            if (!hint) return;
            if (showAnswers && answer) {
                blank.innerHTML = `${answer} (${hint})`;
                blank.style.color = '#d97706';
                blank.style.fontWeight = '600';
                blank.style.fontStyle = 'normal';
                blank.style.borderBottomColor = '#22c55e';
            } else {
                blank.innerHTML = `_______ (${hint})`;
                blank.style.color = '#a0aec0';
                blank.style.fontWeight = 'normal';
                blank.style.fontStyle = 'italic';
                blank.style.borderBottomColor = '#f6ad55';
            }
        });
        if (showAnswers) {
            button.textContent = 'Скрыть ответы';
            button.style.background = 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)';
        } else {
            button.textContent = 'Показать ответы';
            button.style.background = 'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)';
        }
        if (navigator.vibrate && this.isTouchDevice) {
            vibrate(showAnswers ? 15 : 10);
        }
        setTimeout(() => {
            button.dataset.processing = 'false';
        }, 300);
    }
}

if (typeof window !== 'undefined') {
    window.JourneyApp = JourneyApp;
}
