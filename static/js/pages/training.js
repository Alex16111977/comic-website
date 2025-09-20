const STORAGE_KEY = 'liraJourney:reviewQueue';
const TRANSLATION_DISTRACTORS = ['власть', 'корона', 'злоба', 'верность', 'предательство', 'судьба', 'честь', 'трон'];
const REVERSE_DISTRACTORS = ['die Macht', 'die Krone', 'die Bosheit', 'die Treue', 'der Verrat', 'das Schicksal', 'die Ehre', 'der Thron'];

const normalize = value => (value === undefined || value === null ? '' : String(value).trim().toLowerCase().replace(/[\s_-]+/g, '_'));
const readStoredWords = key => {
    if (typeof window === 'undefined' || !window.localStorage) return [];
    try {
        const raw = window.localStorage.getItem(key);
        if (!raw) return [];
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
        console.warn('[Training] Не удалось прочитать слова из localStorage', error);
        return [];
    }
};
const buildFallbackWord = wordId => {
    const label = decodeURIComponent(wordId || '').replace(/_/g, ' ');
    return {
        id: wordId,
        word: label || 'unbekannt',
        translation: 'наследство',
        transcription: '[дас ЭР-бе]',
        sentence: 'Das Wort „das Erbe" bleibt lebendig.',
        sentenceTranslation: 'Слово «наследство» остаётся живым.'
    };
};
const candidateKeys = word => {
    if (!word || typeof word !== 'object') return [];
    const values = [word.id, word.word, word.wordId, word.german];
    if (typeof word.word === 'string') values.push(word.word.replace(/\s+/g, '_'));
    return values.filter(Boolean);
};

export class WordTrainer {
    constructor(options = {}) {
        this.storageKey = options.storageKey || STORAGE_KEY;
        this.progressText = document.getElementById('progress-text');
        this.progressFill = document.getElementById('progress-fill');
        this.area = document.getElementById('exercise-area');
        this.currentWord = null;
        this.exercises = [];
        this.currentExerciseIndex = 0;
        this.correctAnswers = 0;
        this.totalAnswers = 0;
    }

    init() {
        if (!this.area) {
            console.warn('[Training] Отсутствует контейнер упражнений');
            return;
        }
        const params = new URLSearchParams(window.location.search);
        const rawWord = params.get('word');
        if (!rawWord) {
            this.showError('Слово не указано');
            return;
        }
        const decodedWordId = decodeURIComponent(rawWord);
        const storedWords = readStoredWords(this.storageKey);
        const match = storedWords.find(entry => candidateKeys(entry).some(key => normalize(key) === normalize(decodedWordId)));
        this.currentWord = match || buildFallbackWord(decodedWordId);
        if (!match) console.warn('[Training] Слово не найдено в очереди повторения, используется шаблон', decodedWordId);
        this.createExercises();
        this.showExercise();
    }

    createExercises() {
        this.exercises = [
            { type: 'introduction', title: 'Запомните слово' },
            { type: 'translation', title: 'Выберите перевод' },
            { type: 'reverse', title: 'Выберите немецкое слово' }
        ];
        if (typeof this.currentWord?.word === 'string' && /^(der|die|das)\s+/i.test(this.currentWord.word)) {
            this.exercises.push({ type: 'article', title: 'Выберите артикль' });
        }
        this.currentExerciseIndex = 0;
        this.correctAnswers = 0;
        this.totalAnswers = 0;
    }

    showExercise() {
        if (this.currentExerciseIndex >= this.exercises.length) {
            this.showResults();
            return;
        }
        this.updateProgress();
        const exercise = this.exercises[this.currentExerciseIndex];
        if (exercise.type === 'introduction') this.showIntroduction();
        else if (exercise.type === 'translation') this.showTranslationQuiz();
        else if (exercise.type === 'reverse') this.showReverseQuiz();
        else if (exercise.type === 'article') this.showArticleQuiz();
        else this.showError('Упражнение пока недоступно');
    }

    showIntroduction() {
        const transcription = this.currentWord.transcription ? `<div class="transcription">${this.currentWord.transcription}</div>` : '';
        const exampleBox = this.currentWord.sentence
            ? `<div class="example-box"><div class="example-label">Пример использования:</div><div class="example-text">"${this.currentWord.sentence}"</div>${this.currentWord.sentenceTranslation ? `<div class="example-translation">${this.currentWord.sentenceTranslation}</div>` : ''}</div>`
            : '';
        this.area.innerHTML = `<div class="introduction"><div class="word-display">${this.currentWord.word}</div>${transcription}<div class="translation">${this.currentWord.translation}</div>${exampleBox}<button class="next-btn" type="button" data-action="next">Далее →</button></div>`;
        const nextButton = this.area.querySelector('[data-action="next"]');
        if (nextButton) nextButton.addEventListener('click', () => this.nextExercise());
    }

    showTranslationQuiz() {
        const options = this.generateOptions('translation');
        this.area.innerHTML = `<div class="quiz"><div class="quiz-question"><div class="quiz-instruction">Выберите перевод слова:</div><div class="quiz-word">${this.currentWord.word}</div></div><div class="options-grid">${options.map((option, index) => `<button class="option-btn" type="button" data-index="${index}">${option}</button>`).join('')}</div></div>`;
        this.area.querySelectorAll('.option-btn').forEach(button => button.addEventListener('click', () => this.checkAnswer(button, 'translation')));
    }

    showReverseQuiz() {
        const options = this.generateOptions('reverse');
        this.area.innerHTML = `<div class="quiz"><div class="quiz-question"><div class="quiz-instruction">Выберите немецкое слово:</div><div class="quiz-word">${this.currentWord.translation}</div></div><div class="options-grid">${options.map((option, index) => `<button class="option-btn" type="button" data-index="${index}">${option}</button>`).join('')}</div></div>`;
        this.area.querySelectorAll('.option-btn').forEach(button => button.addEventListener('click', () => this.checkAnswer(button, 'reverse')));
    }

    showArticleQuiz() {
        const wordWithoutArticle = this.currentWord.word.replace(/^(der|die|das)\s+/i, '');
        this.area.innerHTML = `<div class="quiz"><div class="quiz-question"><div class="quiz-instruction">Выберите правильный артикль:</div><div class="quiz-word">_____ ${wordWithoutArticle}</div></div><div class="options-grid"><button class="option-btn" type="button" data-article="der">der</button><button class="option-btn" type="button" data-article="die">die</button><button class="option-btn" type="button" data-article="das">das</button></div></div>`;
        this.area.querySelectorAll('.option-btn').forEach(button => button.addEventListener('click', () => this.checkArticle(button.dataset.article)));
    }

    generateOptions(type) {
        const options = [];
        const correctAnswer = type === 'translation' ? this.currentWord.translation : this.currentWord.word;
        if (correctAnswer) options.push(correctAnswer);
        const pool = (type === 'translation' ? TRANSLATION_DISTRACTORS : REVERSE_DISTRACTORS).filter(item => item !== correctAnswer);
        while (options.length < 4 && pool.length) {
            const index = Math.floor(Math.random() * pool.length);
            options.push(pool.splice(index, 1)[0]);
        }
        return this.shuffle(options);
    }

    shuffle(items) {
        const list = items.slice();
        for (let i = list.length - 1; i > 0; i -= 1) {
            const j = Math.floor(Math.random() * (i + 1));
            [list[i], list[j]] = [list[j], list[i]];
        }
        return list;
    }

    checkAnswer(button, type) {
        if (!button) return;
        const buttons = Array.from(this.area.querySelectorAll('.option-btn'));
        const selected = button.textContent.trim();
        const correct = type === 'translation' ? this.currentWord.translation : this.currentWord.word;
        this.totalAnswers += 1;
        buttons.forEach(btn => { btn.disabled = true; });
        if (selected === correct) {
            this.correctAnswers += 1;
            button.classList.add('correct');
            setTimeout(() => this.nextExercise(), 1500);
        } else {
            button.classList.add('incorrect');
            if (button.parentElement) button.parentElement.classList.add('shake');
            buttons.forEach(btn => { if (btn.textContent.trim() === correct) btn.classList.add('correct'); });
            setTimeout(() => {
                if (button.parentElement) button.parentElement.classList.remove('shake');
                this.nextExercise();
            }, 2500);
        }
    }

    checkArticle(selectedArticle) {
        if (!selectedArticle) return;
        const buttons = Array.from(this.area.querySelectorAll('.option-btn'));
        const correctArticle = (this.currentWord.word.match(/^(der|die|das)\s+/i) || [''])[0].trim().toLowerCase();
        this.totalAnswers += 1;
        buttons.forEach(btn => {
            const value = (btn.dataset.article || '').toLowerCase();
            btn.disabled = true;
            if (value === correctArticle) btn.classList.add('correct');
            if (value === selectedArticle.toLowerCase() && value !== correctArticle) btn.classList.add('incorrect');
        });
        if (selectedArticle.toLowerCase() === correctArticle) this.correctAnswers += 1;
        setTimeout(() => this.nextExercise(), 2000);
    }

    nextExercise() {
        this.currentExerciseIndex += 1;
        this.showExercise();
    }

    updateProgress() {
        const total = this.exercises.length;
        const current = Math.min(this.currentExerciseIndex + 1, total);
        const percent = total ? Math.round((current / total) * 100) : 0;
        if (this.progressFill) this.progressFill.style.width = `${percent}%`;
        if (this.progressText) this.progressText.textContent = `Упражнение ${current} из ${total}`;
    }

    showResults() {
        const accuracy = this.totalAnswers ? Math.round((this.correctAnswers / this.totalAnswers) * 100) : 0;
        this.area.innerHTML = `<div class="results"><div class="success-icon">🎉</div><div class="results-title">Отличная работа!</div><div class="results-stats"><div class="stat"><div class="stat-value">${this.correctAnswers}/${this.totalAnswers}</div><div class="stat-label">Правильных ответов</div></div><div class="stat"><div class="stat-value">${accuracy}%</div><div class="stat-label">Точность</div></div></div><button class="continue-btn" type="button" data-action="home">Вернуться на главную</button></div>`;
        const homeButton = this.area.querySelector('[data-action="home"]');
        if (homeButton) homeButton.addEventListener('click', () => { window.location.href = 'index.html'; });
        if (this.progressText) this.progressText.textContent = 'Упражнения завершены';
        if (this.progressFill) this.progressFill.style.width = '100%';
    }

    showError(message) {
        this.area.innerHTML = `<div style="text-align: center; color: #6b7280;"><p style="font-size: 1.2em; margin: 20px 0;">${message}</p><button class="continue-btn" type="button" data-action="home">Вернуться на главную</button></div>`;
        const homeButton = this.area.querySelector('[data-action="home"]');
        if (homeButton) homeButton.addEventListener('click', () => { window.location.href = 'index.html'; });
    }
}

export function initTrainingPage(options = {}) {
    if (typeof document === 'undefined') return null;
    const start = () => {
        const trainer = new WordTrainer(options);
        trainer.init();
        if (typeof window !== 'undefined') window.trainingPage = { trainer };
        return trainer;
    };
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start, { once: true });
        return null;
    }
    return start();
}

if (typeof window !== 'undefined') window.initTrainingPage = initTrainingPage;
