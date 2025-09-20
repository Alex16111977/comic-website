import { refreshActiveExerciseContentHeight } from '../utils/dom.js';
import { vibrate } from '../utils/animations.js';

function shuffle(items) {
    const list = Array.isArray(items) ? items.slice() : [];
    for (let i = list.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [list[i], list[j]] = [list[j], list[i]];
    }
    return list;
}
function collectValues(type) {
    const values = [];
    const seen = new Set();
    Object.values(window.phaseVocabularies || {}).forEach(phase => {
        (phase.words || []).forEach(entry => {
            const value = type === 'russian' ? entry.translation : entry.word;
            if (value && !seen.has(value)) {
                seen.add(value);
                values.push(value);
            }
        });
    });
    return values;
}

const globalOptions = {
    german: collectValues('german'),
    russian: collectValues('russian'),
};

class VocabularyQuiz {
    constructor(phaseKey, words, title) {
        this.phaseKey = phaseKey;
        this.phaseTitle = title || '';
        this.originalWords = Array.isArray(words) ? words.map(word => ({ ...word })) : [];
        this.elements = {
            content: document.querySelector('.quiz-content'),
            current: document.getElementById('current-question'),
            total: document.getElementById('total-questions'),
            progress: document.querySelector('.quiz-progress .progress-fill'),
            forward: document.querySelector('.mode-badge[data-mode="forward"]'),
            reverse: document.querySelector('.mode-badge[data-mode="reverse"]'),
        };
        this.advanceDelay = 1200;
        this.reset();
    }

    reset() {
        this.words = shuffle(this.originalWords);
        this.currentIndex = 0;
        this.currentMode = 'forward';
        this.completedForward = false;
        this.totalQuestions = this.originalWords.length * 2;
        this.answered = 0;
        this.correct = 0;
        this.incorrect = [];
        this.quizCompleted = false;
        this.optionLocked = false;
        this.feedbackElement = null;
        this.optionButtons = [];
        this.activeQuestion = null;
        this.clearTimeout();
    }

    start() {
        this.reset();
        this.updateUI();
        if (!this.originalWords.length) return this.renderEmptyState();
        this.renderQuestion(this.nextQuestion());
    }

    renderEmptyState() {
        if (!this.elements.content) return;
        this.elements.content.innerHTML = '<div class="quiz-placeholder">Слова для этой викторины появятся позже.</div>';
        refreshActiveExerciseContentHeight();
    }

    nextQuestion() {
        if (this.currentIndex >= this.words.length) {
            if (!this.completedForward) {
                this.completedForward = true;
                this.currentMode = 'reverse';
                this.words = shuffle(this.originalWords);
                this.currentIndex = 0;
            } else return this.showResults() || null;
        }
        const word = this.words[this.currentIndex++];
        return this.buildQuestion(word, this.currentMode);
    }

    buildQuestion(word, mode) {
        if (!word) return null;
        const isForward = mode === 'forward';
        const target = isForward ? word.russian : word.german;
        const options = this.generateOptions(target, isForward ? 'russian' : 'german');
        return {
            type: mode,
            prompt: isForward ? word.german : word.russian,
            transcription: word.transcription,
            correct: target,
            germanWord: word.german,
            options,
        };
    }

    generateOptions(correct, type) {
        const set = new Set(correct ? [correct] : []);
        const local = this.originalWords.map(word => (type === 'russian' ? word.russian : word.german)).filter(Boolean);
        const pool = shuffle([...new Set([...local, ...(globalOptions[type] || [])])]);
        pool.forEach(option => {
            if (!option || set.has(option)) return;
            set.add(option);
            if (set.size === 4) return;
        });
        if (set.size < 4) {
            shuffle(globalOptions[type] || []).forEach(option => {
                if (!option || set.has(option)) return;
                set.add(option);
            });
        }
        return shuffle(Array.from(set).slice(0, 4));
    }

    renderQuestion(question) {
        if (!question || !this.elements.content) return;
        this.clearTimeout();
        this.optionLocked = false;
        this.activeQuestion = question;
        const card = document.createElement('div');
        card.className = 'quiz-question-card';
        card.dataset.mode = question.type;
        card.innerHTML = `
            <div class="quiz-question-text">${question.type === 'forward'
                ? `Что означает немецкое слово «${question.prompt}»?`
                : `Как переводится на немецкий слово «${question.prompt}»?`}</div>
            <div class="quiz-word-meta">
                <span class="quiz-word">${question.prompt}</span>
                ${question.type === 'forward' && question.transcription
                    ? `<span class="quiz-transcription">${question.transcription}</span>`
                    : ''}
            </div>
            <div class="quiz-options"></div>
            <div class="quiz-feedback"></div>
        `;
        const optionsList = card.querySelector('.quiz-options');
        question.options.forEach(option => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'quiz-option';
            button.textContent = option;
            button.addEventListener('click', () => this.handleOption(button, option));
            optionsList.appendChild(button);
        });
        this.elements.content.innerHTML = '';
        this.elements.content.appendChild(card);
        this.feedbackElement = card.querySelector('.quiz-feedback');
        this.optionButtons = Array.from(card.querySelectorAll('.quiz-option'));
        this.updateUI();
        refreshActiveExerciseContentHeight();
    }

    handleOption(button, value) {
        if (this.optionLocked || !this.activeQuestion) return;
        this.optionLocked = true;
        this.answered += 1;
        const isCorrect = value === this.activeQuestion.correct;
        if (isCorrect) {
            this.correct += 1;
            button.classList.add('correct');
            this.showFeedback('Верно! Отличная работа.', 'success');
            vibrate(15);
        } else {
            button.classList.add('incorrect');
            this.showFeedback(`Нужно слово: ${this.activeQuestion.correct}`, 'error');
            this.optionButtons.forEach(opt => {
                if (opt.textContent === this.activeQuestion.correct) opt.classList.add('correct');
            });
            this.incorrect.push({
                word: this.activeQuestion.germanWord,
                translation: this.activeQuestion.correct,
                selected: value,
                mode: this.activeQuestion.type,
            });
            vibrate([40]);
        }
        this.updateUI();
        this.timeout = setTimeout(() => this.renderQuestion(this.nextQuestion()), this.advanceDelay);
    }

    showFeedback(message, type) {
        if (!this.feedbackElement) return;
        this.feedbackElement.textContent = message;
        this.feedbackElement.classList.toggle('success', type === 'success');
        this.feedbackElement.classList.toggle('error', type === 'error');
    }

    updateUI() {
        if (this.elements.total) this.elements.total.textContent = String(this.totalQuestions || 0);
        if (this.elements.current) {
            const current = !this.totalQuestions ? 0 : Math.min(this.totalQuestions, this.answered + 1);
            this.elements.current.textContent = String(current);
        }
        if (this.elements.progress) {
            const percent = this.totalQuestions ? Math.min(100, Math.round((this.answered / this.totalQuestions) * 100)) : 0;
            this.elements.progress.style.width = `${percent}%`;
        }
        if (this.elements.forward) this.elements.forward.classList.toggle('active', this.currentMode === 'forward' && !this.quizCompleted);
        if (this.elements.reverse) this.elements.reverse.classList.toggle('active', this.currentMode === 'reverse' && !this.quizCompleted);
    }

    showResults() {
        if (!this.elements.content) return;
        this.clearTimeout();
        this.quizCompleted = true;
        this.answered = this.totalQuestions;
        this.updateUI();
        const percent = this.totalQuestions ? Math.round((this.correct / this.totalQuestions) * 100) : 0;
        this.elements.content.innerHTML = `
            <div class="quiz-results">
                <h3>🏆 Викторина завершена!</h3>
                <p>Результат: ${this.correct} из ${this.totalQuestions} (${percent}%)</p>
                <button type="button" class="quiz-restart">Начать заново</button>
            </div>
        `;
        const restart = this.elements.content.querySelector('.quiz-restart');
        if (restart) restart.addEventListener('click', () => this.restart());
        refreshActiveExerciseContentHeight();
        this.dispatchCompletionEvent();
        return null;
    }

    dispatchCompletionEvent() {
        if (!this.phaseKey) return;
        const detail = {
            characterId: typeof window.characterId === 'string' ? window.characterId : '',
            phaseId: this.phaseKey,
            phaseTitle: this.phaseTitle,
            completedAt: new Date().toISOString(),
            totalQuestions: this.totalQuestions,
            correctAnswers: this.correct,
            incorrectWords: this.incorrect.slice(),
        };
        try {
            document.dispatchEvent(new CustomEvent('journeyPhaseCompleted', { detail }));
        } catch (error) {
            console.warn('[VocabularyQuiz] Unable to dispatch completion event', error);
        }
    }

    continueReverse() {
        if (!this.completedForward || this.quizCompleted) return;
        this.optionLocked = false;
        this.renderQuestion(this.nextQuestion());
    }

    restart() {
        this.start();
    }

    clearTimeout() {
        if (this.timeout) {
            clearTimeout(this.timeout);
            this.timeout = null;
        }
    }
}

export class QuizManager {
    constructor() {
        this.activeQuiz = null;
        if (typeof window !== 'undefined') {
            window.continueQuiz = () => this.continue();
            window.restartQuiz = () => this.restart();
        }
    }

    initialize(phaseKey, phase) {
        const words = Array.isArray(phase?.words)
            ? phase.words.map(word => ({
                german: word.word || '',
                russian: word.translation || '',
                transcription: word.transcription || '',
            })).filter(word => word.german && word.russian)
            : [];
        const title = phase ? phase.title : '';
        if (this.activeQuiz) this.activeQuiz.clearTimeout();
        this.activeQuiz = new VocabularyQuiz(phaseKey, words, title);
        this.activeQuiz.start();
    }

    continue() { if (this.activeQuiz) this.activeQuiz.continueReverse(); }

    restart() { if (this.activeQuiz) this.activeQuiz.restart(); }
}
