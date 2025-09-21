import { refreshActiveExerciseContentHeight, updateWordColumnScrollIndicators } from '../utils/dom.js';

export class ArticlesExercise {
    constructor() {
        this.isTouchDevice = ('ontouchstart' in window)
            || (navigator.maxTouchPoints > 0)
            || (navigator.msMaxTouchPoints > 0);
    }

    render(container, vocabulary) {
        if (!(container instanceof HTMLElement)) {
            return;
        }
        const entries = this.extractWords(vocabulary);
        if (!entries.length) {
            container.innerHTML = '<div class="exercise-empty-state">В этой фазе нет слов с артиклями.</div>';
            return;
        }
        container.innerHTML = this.buildMarkup(entries);
        this.attachHandlers(container);
    }

    extractWords(vocabulary) {
        const words = [];
        const list = vocabulary?.vocabulary || [];
        list.forEach(word => {
            if (!word.german || !word.russian) {
                return;
            }
            const parts = word.german.split(' ');
            if (['der', 'die', 'das'].includes(parts[0])) {
                words.push({
                    article: parts[0],
                    german: parts.slice(1).join(' '),
                    russian: word.russian,
                });
            }
        });
        return words.sort(() => Math.random() - 0.5).slice(0, 9);
    }

    buildMarkup(words) {
        const wordMarkup = words.map((word, index) => `
            <div class="article-word-card" data-article="${word.article}" data-index="${index}" draggable="true">
                <span class="word-german">${word.german}</span>
                <span class="word-russian">${word.russian}</span>
            </div>
        `).join('');
        return `
            <div class="articles-exercise">
                <div class="articles-instruction">
                    Распределите слова по родам (drag & drop или клик для мобильных)
                </div>
                <div class="article-columns">
                    ${this.columnMarkup('der', 'мужской род')}
                    ${this.columnMarkup('die', 'женский род')}
                    ${this.columnMarkup('das', 'средний род')}
                </div>
                <div class="words-to-sort">${wordMarkup}</div>
                <div class="articles-controls">
                    <button class="check-articles-btn" type="button">Проверить</button>
                    <button class="reset-articles-btn" type="button">Сбросить</button>
                </div>
                <div class="articles-feedback"></div>
            </div>
        `;
    }

    columnMarkup(article, label) {
        return `
            <div class="article-column" data-article="${article}">
                <h5 class="article-header">
                    <span class="article-label">${article.toUpperCase()}</span>
                    <span class="article-desc">${label}</span>
                </h5>
                <div class="article-drop-zone" data-zone="${article}"></div>
            </div>
        `;
    }

    attachHandlers(container) {
        const exercise = container.querySelector('.articles-exercise');
        if (!exercise) {
            return;
        }
        const cards = exercise.querySelectorAll('.article-word-card');
        const zones = exercise.querySelectorAll('.article-drop-zone');
        const checkBtn = exercise.querySelector('.check-articles-btn');
        const resetBtn = exercise.querySelector('.reset-articles-btn');
        const feedback = exercise.querySelector('.articles-feedback');
        const wordsContainer = exercise.querySelector('.words-to-sort');
        const accordionContent = exercise.closest('.exercise-content');

        const updateLayout = () => {
            requestAnimationFrame(() => {
                refreshActiveExerciseContentHeight();
                updateWordColumnScrollIndicators(exercise);
                if (accordionContent instanceof HTMLElement) {
                    accordionContent.style.maxHeight = `${accordionContent.scrollHeight}px`;
                }
            });
        };

        cards.forEach(card => {
            card.addEventListener('dragstart', event => {
                event.dataTransfer.effectAllowed = 'move';
                event.dataTransfer.setData('text/plain', '');
                card.classList.add('dragging');
            });
            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                updateLayout();
            });
            card.addEventListener('click', () => {
                const wasSelected = card.classList.contains('selected');
                cards.forEach(c => c.classList.remove('selected'));
                if (!wasSelected) {
                    card.classList.add('selected');
                }
            });
        });

        zones.forEach(zone => {
            zone.addEventListener('dragover', event => {
                event.preventDefault();
                event.dataTransfer.dropEffect = 'move';
                zone.classList.add('drag-over');
            });
            zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
            zone.addEventListener('drop', () => {
                const dragging = exercise.querySelector('.dragging');
                if (dragging) {
                    zone.appendChild(dragging);
                    dragging.classList.remove('correct', 'incorrect');
                }
                zone.classList.remove('drag-over');
                updateLayout();
            });
            zone.addEventListener('click', () => {
                const selected = exercise.querySelector('.article-word-card.selected');
                if (selected) {
                    zone.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateLayout();
                }
            });
        });

        if (wordsContainer) {
            wordsContainer.addEventListener('dragover', event => {
                event.preventDefault();
                event.dataTransfer.dropEffect = 'move';
            });
            wordsContainer.addEventListener('drop', () => {
                const dragging = exercise.querySelector('.dragging');
                if (dragging) {
                    wordsContainer.appendChild(dragging);
                    dragging.classList.remove('correct', 'incorrect');
                    updateLayout();
                }
            });
            wordsContainer.addEventListener('click', () => {
                const selected = exercise.querySelector('.article-word-card.selected');
                if (selected && selected.parentElement !== wordsContainer) {
                    wordsContainer.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateLayout();
                }
            });
        }

        checkBtn?.addEventListener('click', () => {
            let correct = 0;
            let total = 0;
            zones.forEach(zone => {
                const target = zone.dataset.zone;
                const assigned = zone.querySelectorAll('.article-word-card');
                assigned.forEach(card => {
                    total++;
                    card.classList.remove('correct', 'incorrect');
                    if (card.dataset.article === target) {
                        card.classList.add('correct');
                        correct++;
                    } else {
                        card.classList.add('incorrect');
                    }
                });
            });
            const unsorted = wordsContainer ? wordsContainer.querySelectorAll('.article-word-card') : [];
            unsorted.forEach(card => {
                total++;
                card.classList.add('incorrect');
            });
            if (feedback) {
                if (correct === total && total > 0) {
                    feedback.innerHTML = '<span class="success">[OK] Отлично! Все артикли правильные!</span>';
                    feedback.className = 'articles-feedback success';
                } else {
                    feedback.innerHTML = `<span class="partial">Правильно: ${correct} из ${total}. Попробуйте ещё раз!</span>`;
                    feedback.className = 'articles-feedback partial';
                }
            }
            updateLayout();
        });

        resetBtn?.addEventListener('click', () => {
            cards.forEach(card => {
                card.classList.remove('correct', 'incorrect', 'selected');
                if (wordsContainer) {
                    wordsContainer.appendChild(card);
                }
            });
            if (feedback) {
                feedback.innerHTML = '';
                feedback.className = 'articles-feedback';
            }
            updateLayout();
        });

        updateLayout();
    }
}
