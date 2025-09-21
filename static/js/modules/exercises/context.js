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

export class ContextExercise {
    render(container, vocabulary) {
        if (!(container instanceof HTMLElement)) {
            return;
        }
        const exercises = this.buildExercises(vocabulary);
        if (!exercises.length) {
            container.innerHTML = '<div class="exercise-empty-state">В этой фазе нет предложений для контекстного перевода.</div>';
            return;
        }
        container.innerHTML = this.buildMarkup(exercises);
        this.attachHandlers(container);
    }

    buildExercises(vocabulary) {
        const entries = vocabulary?.vocabulary || [];
        const result = [];
        entries.forEach((word, index) => {
            if (!word.german || !word.russian || !word.sentence || !word.sentence_translation) {
                return;
            }
            const germanWord = word.german.replace(/^(der|die|das)\s+/i, '');
            const pattern = new RegExp(`\\b${germanWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\w*\\b`, 'gi');
            if (!word.sentence.match(pattern)) {
                return;
            }
            const germanBlank = word.sentence.replace(pattern, '_____');
            const russianBlank = word.sentence_translation.includes(word.russian)
                ? word.sentence_translation.replace(word.russian, '_____')
                : word.sentence_translation;
            result.push({
                id: `context-${index}`,
                germanWord: word.german,
                germanBlank,
                russianBlank,
                correctAnswer: word.russian,
                options: this.generateOptions(word.russian, vocabulary),
            });
        });
        return shuffleArray(result).slice(0, 5);
    }

    buildMarkup(exercises) {
        return `
            <div class="context-exercises">
                <div class="context-instruction">Выберите правильный перевод пропущенного слова в контексте</div>
                ${exercises.map((exercise, index) => `
                    <div class="context-exercise-card" data-exercise-id="${exercise.id}">
                        <div class="exercise-number">Упражнение ${index + 1}</div>
                        <div class="context-sentences">
                            <div class="sentence-german">${exercise.germanBlank}</div>
                            <div class="sentence-russian">${exercise.russianBlank}</div>
                        </div>
                        <div class="context-question">Пропущенное слово: <strong>${exercise.germanWord}</strong></div>
                        <div class="context-options">
                            ${exercise.options.map((option, optionIndex) => `
                                <button class="context-option" type="button" data-answer="${option}" data-correct="${option === exercise.correctAnswer}">
                                    ${String.fromCharCode(65 + optionIndex)}) ${option}
                                </button>
                            `).join('')}
                        </div>
                        <div class="context-feedback"></div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    generateOptions(correctAnswer, vocabulary) {
        const options = [correctAnswer];
        const translations = [];
        const entries = vocabulary?.vocabulary || [];
        entries.forEach(word => {
            if (word.russian && word.russian !== correctAnswer) {
                translations.push(word.russian);
            }
        });
        if (translations.length < 3) {
            const fallback = [
                'власть', 'трон', 'корона', 'королевство',
                'предательство', 'верность', 'гордость', 'дочь',
                'судьба', 'мудрость', 'безумие', 'правда'
            ].filter(option => option !== correctAnswer);
            translations.push(...fallback);
        }
        const wrongOptions = shuffleArray(translations).slice(0, 3);
        options.push(...wrongOptions);
        return shuffleArray(options);
    }

    attachHandlers(container) {
        const cards = container.querySelectorAll('.context-exercise-card');
        cards.forEach(card => {
            const options = card.querySelectorAll('.context-option');
            const feedback = card.querySelector('.context-feedback');
            options.forEach(option => {
                option.addEventListener('click', event => {
                    event.stopPropagation();
                    if (card.classList.contains('answered')) {
                        return;
                    }
                    card.classList.add('answered');
                    options.forEach(btn => {
                        btn.disabled = true;
                        btn.classList.remove('selected');
                    });
                    option.classList.add('selected');
                    if (option.dataset.correct === 'true') {
                        option.classList.add('correct');
                        if (feedback) {
                            feedback.innerHTML = '<span class="success">[OK] Правильно!</span>';
                            feedback.className = 'context-feedback success';
                        }
                        card.classList.add('success-animation');
                        vibrate(20);
                    } else {
                        option.classList.add('incorrect');
                        options.forEach(btn => {
                            if (btn.dataset.correct === 'true') {
                                btn.classList.add('correct');
                            }
                        });
                        if (feedback) {
                            feedback.innerHTML = '<span class="error">[X] Неверно. Правильный ответ выделен зеленым.</span>';
                            feedback.className = 'context-feedback error';
                        }
                        vibrate([40]);
                    }
                    refreshActiveExerciseContentHeight();
                });
            });
        });
    }
}
