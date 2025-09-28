/**
 * Модуль интерактивных упражнений для изучения немецкого
 * Версия: 2.0
 */

(function() {
    'use strict';

    // ==========================================
    // ГЛОБАЛЬНАЯ ИНИЦИАЛИЗАЦИЯ
    // ==========================================
    
    window.initializeExercises = function(phaseId) {
        console.log('[Exercises] Initializing for phase:', phaseId);

        if (!phaseId) {
            return;
        }

        const phaseVocabulary = window.phaseData && window.phaseData[phaseId];
        if (!phaseVocabulary) {
            console.warn('[Exercises] No data for phase:', phaseId);
            return;
        }

        initializeArticlesExercise(phaseId, phaseVocabulary);

        const synonymsContainer = document.querySelector(
            `[data-synonyms-container][data-phase="${phaseId}"]`
        );
        if (synonymsContainer) {
            initializeSynonymAntonymExercise(synonymsContainer, phaseVocabulary);
        }

        const contextContainer = document.querySelector(`[data-context-container][data-phase="${phaseId}"]`);
        if (contextContainer) {
            initializeContextTranslation(contextContainer, phaseVocabulary);
        }
    };

    // ==========================================
    // 1. УПРАЖНЕНИЕ "АРТИКЛИ И РОД"
    // ==========================================
    
    function initializeArticlesExercise(activePhaseId, phaseVocabulary) {
        const containers = document.querySelectorAll('[data-articles-container]');

        if (!containers.length) {
            return;
        }

        containers.forEach(container => {
            if (container.dataset.phase === activePhaseId) {
                renderArticlesQuiz(container, phaseVocabulary);
            } else {
                container.innerHTML = '';
            }
        });
    }

    function renderArticlesQuiz(container, phaseVocabulary) {
        if (!(container instanceof HTMLElement)) {
            return;
        }

        const quizWords = collectArticleWords(phaseVocabulary);

        if (quizWords.length === 0) {
            container.innerHTML = '<div class="exercise-empty-state">В этой фазе нет слов с артиклями.</div>';
            return;
        }

        container.innerHTML = createArticlesQuizMarkup(quizWords);

        const quizElement = container.querySelector('.articles-quiz');
        if (quizElement) {
            attachArticlesQuizHandlers(quizElement);
        }
    }

    function collectArticleWords(phaseVocabulary) {
        if (!phaseVocabulary || !Array.isArray(phaseVocabulary.vocabulary)) {
            return [];
        }

        return phaseVocabulary.vocabulary
            .map(entry => {
                if (!entry || !entry.german) {
                    return null;
                }

                const parts = entry.german.trim().split(/\s+/);
                if (parts.length < 2) {
                    return null;
                }

                const article = parts[0].toLowerCase();
                if (!['der', 'die', 'das'].includes(article)) {
                    return null;
                }

                return {
                    article,
                    noun: parts.slice(1).join(' '),
                    translation: entry.russian || '—'
                };
            })
            .filter(Boolean);
    }

    function createArticlesQuizMarkup(words) {
        const itemsMarkup = words.map(item => `
        <div class="quiz-item" data-correct="${item.article}">
            <div class="quiz-word">${escapeHtml(item.noun)}</div>
            <div class="quiz-translation">${escapeHtml(item.translation)}</div>
            <div class="article-buttons">
                <button class="article-btn der" data-article="der">
                    <span class="article-icon">♂</span> der
                </button>
                <button class="article-btn die" data-article="die">
                    <span class="article-icon">♀</span> die
                </button>
                <button class="article-btn das" data-article="das">
                    <span class="article-icon">⚪</span> das
                </button>
            </div>
        </div>`).join('');

        return `
        <section class="articles-quiz" data-quiz="articles">
            <div class="quiz-header">
                <h3 class="quiz-title">🎯 Артикли и род</h3>
                <p class="quiz-description">Выберите правильный артикль для существительных из урока</p>
            </div>

            <div class="articles-legend">
                <div class="legend-item legend-der">
                    <span class="legend-icon">♂</span>
                    <span>der — мужской</span>
                </div>
                <div class="legend-item legend-die">
                    <span class="legend-icon">♀</span>
                    <span>die — женский</span>
                </div>
                <div class="legend-item legend-das">
                    <span class="legend-icon">⚪</span>
                    <span>das — средний</span>
                </div>
            </div>

            <div class="quiz-progress">
                <div class="progress-count">
                    <strong>0</strong>/<span class="total">0</span> правильных
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
            </div>

            <div class="quiz-grid">
                ${itemsMarkup}
            </div>
        </section>`;
    }

    function attachArticlesQuizHandlers(quizElement) {
        const items = quizElement.querySelectorAll('.quiz-item');
        const total = items.length;
        const progressCount = quizElement.querySelector('.progress-count strong');
        const totalElement = quizElement.querySelector('.total');
        const progressFill = quizElement.querySelector('.progress-fill');

        if (totalElement) {
            totalElement.textContent = total;
        }

        let solved = 0;

        items.forEach(item => {
            const buttons = item.querySelectorAll('.article-btn');
            const correctArticle = item.dataset.correct;
            let answered = false;

            buttons.forEach(button => {
                button.addEventListener('click', () => {
                    if (answered) {
                        return;
                    }

                    const selected = button.dataset.article;

                    if (selected === correctArticle) {
                        answered = true;
                        solved += 1;
                        item.classList.add('item-solved');
                        button.classList.add('is-correct');
                        buttons.forEach(btn => {
                            btn.disabled = true;
                        });

                        updateArticlesProgress(progressCount, progressFill, solved, total);

                        if (solved === total) {
                            showQuizCompletion(quizElement, solved, total);
                        }
                    } else {
                        button.classList.add('is-wrong');
                        setTimeout(() => {
                            button.classList.remove('is-wrong');
                        }, 500);
                    }
                });
            });
        });

        updateArticlesProgress(progressCount, progressFill, solved, total);
    }

    function updateArticlesProgress(counterElement, barElement, solved, total) {
        if (counterElement) {
            counterElement.textContent = solved;
        }

        if (barElement) {
            const percentage = total > 0 ? (solved / total) * 100 : 0;
            barElement.style.width = `${percentage}%`;
        }
    }

    function showQuizCompletion(quizElement, solved, total) {
        if (!quizElement) {
            return;
        }

        const existing = quizElement.querySelector('.quiz-completion');
        if (existing) {
            existing.remove();
        }

        const message = document.createElement('div');
        message.className = 'quiz-completion';
        message.setAttribute('role', 'status');
        message.innerHTML = `
            <h4>🎉 Отлично!</h4>
            <p>Вы правильно определили все артикли!</p>
            <p class="completion-stats">Правильно: ${solved} из ${total}</p>
        `;

        quizElement.appendChild(message);
    }

    function escapeHtml(value) {
        if (value == null) {
            return '';
        }

        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }


    // ==========================================
    // 2. УПРАЖНЕНИЕ "КОНТЕКСТНЫЙ ПЕРЕВОД"  
    // ==========================================
    
    function initializeContextTranslation(container, phaseVocabulary) {
        if (!(container instanceof HTMLElement)) {
            return;
        }

        // Собираем слова с полными предложениями
        const contextExercises = [];

        if (phaseVocabulary && phaseVocabulary.vocabulary) {
            phaseVocabulary.vocabulary.forEach((word, idx) => {
                // Проверяем наличие всех необходимых полей
                if (!word.german || !word.russian || !word.sentence || !word.sentence_translation) {
                    return;
                }
                
                // Убираем артикль для поиска в предложении
                const germanWord = word.german.replace(/^(der|die|das)\s+/i, '');
                
                // Создаем регулярное выражение для поиска слова с учетом окончаний
                const wordPattern = new RegExp(
                    `\\b${germanWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\w*\\b`,
                    'gi'
                );
                
                // Проверяем, есть ли слово в предложении
                if (word.sentence.match(wordPattern)) {
                    contextExercises.push({
                        id: `context-${idx}`,
                        germanWord: word.german,
                        russianWord: word.russian,
                        germanSentence: word.sentence,
                        russianSentence: word.sentence_translation,
                        // Создаем предложение с пропуском
                        germanBlank: word.sentence.replace(wordPattern, '_____'),
                        russianBlank: word.sentence_translation.includes(word.russian) 
                            ? word.sentence_translation.replace(word.russian, '_____')
                            : word.sentence_translation,
                        correctAnswer: word.russian
                    });
                }
            });
        }
        
        // Ограничиваем до 5 упражнений и перемешиваем
        const exercises = contextExercises
            .sort(() => Math.random() - 0.5)
            .slice(0, 5);
        
        if (exercises.length === 0) {
            container.innerHTML = '<div class="exercise-empty-state">В этой фазе нет предложений для контекстного перевода.</div>';
            return;
        }

        container.innerHTML = `
            <div class="context-exercises">
                <div class="context-instruction">
                    Выберите правильный перевод пропущенного слова в контексте
                </div>
                ${exercises.map((ex, idx) => {
                    const options = generateOptions(ex.correctAnswer, phaseVocabulary);

                    return `
                        <div class="context-exercise-card" data-exercise-id="${ex.id}">
                            <div class="exercise-number">Упражнение ${idx + 1}</div>

                            <div class="context-sentences">
                                <div class="sentence-german">${ex.germanBlank}</div>
                                <div class="sentence-russian">${ex.russianBlank}</div>
                            </div>

                            <div class="context-question">
                                Пропущенное слово: <strong>${ex.germanWord}</strong>
                            </div>

                            <div class="context-options">
                                ${options.map((opt, optIdx) => `
                                    <button class="context-option"
                                            type="button"
                                            data-answer="${opt}"
                                            data-correct="${opt === ex.correctAnswer}">
                                        ${String.fromCharCode(65 + optIdx)}) ${opt}
                                    </button>
                                `).join('')}
                            </div>

                            <div class="context-feedback"></div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        attachContextHandlers(container);
    }
    
    function generateOptions(correctAnswer, phaseVocabulary) {
        const options = [correctAnswer];
        const allTranslations = [];
        
        // Собираем все переводы из текущей фазы
        if (phaseVocabulary && phaseVocabulary.vocabulary) {
            phaseVocabulary.vocabulary.forEach(word => {
                if (word.russian && word.russian !== correctAnswer) {
                    allTranslations.push(word.russian);
                }
            });
        }
        
        // Если недостаточно вариантов из текущей фазы, добавляем общие
        if (allTranslations.length < 3) {
            const fallbackOptions = [
                'власть', 'трон', 'корона', 'королевство', 
                'предательство', 'верность', 'гордость', 'дочь',
                'судьба', 'мудрость', 'безумие', 'правда'
            ].filter(opt => opt !== correctAnswer);
            
            allTranslations.push(...fallbackOptions);
        }
        
        // Выбираем 3 случайных неправильных варианта
        const wrongOptions = allTranslations
            .sort(() => Math.random() - 0.5)
            .slice(0, 3);
        
        options.push(...wrongOptions);
        
        // Перемешиваем варианты
        return options.sort(() => Math.random() - 0.5);
    }
    
    function attachContextHandlers(container) {
        const cards = container.querySelectorAll('.context-exercise-card');

        cards.forEach(card => {
            const options = card.querySelectorAll('.context-option');
            const feedback = card.querySelector('.context-feedback');
            
            options.forEach(option => {
                option.addEventListener('click', function(e) {
                    e.stopPropagation();
                    
                    // Проверяем, не был ли уже дан ответ
                    if (card.classList.contains('answered')) {
                        return;
                    }
                    
                    // Блокируем все кнопки
                    options.forEach(opt => {
                        opt.disabled = true;
                        opt.classList.remove('selected');
                    });
                    
                    // Отмечаем карточку как отвеченную
                    card.classList.add('answered');
                    this.classList.add('selected');
                    
                    // Проверяем ответ
                    if (this.dataset.correct === 'true') {
                        this.classList.add('correct');
                        feedback.innerHTML = '<span class="success">[OK] Правильно!</span>';
                        feedback.className = 'context-feedback success';
                        
                        // Анимация успеха
                        card.classList.add('success-animation');
                    } else {
                        this.classList.add('incorrect');
                        
                        // Показываем правильный ответ
                        options.forEach(opt => {
                            if (opt.dataset.correct === 'true') {
                                opt.classList.add('correct');
                            }
                        });
                        
                        feedback.innerHTML = '<span class="error">[X] Неверно. Правильный ответ выделен зеленым.</span>';
                        feedback.className = 'context-feedback error';
                    }
                });
            });
        });
    }

    function initializeSynonymAntonymExercise(container, phaseVocabulary) {
        if (!(container instanceof HTMLElement)) return;

        const sets = Array.isArray(phaseVocabulary.synonymAntonymSets)
            ? phaseVocabulary.synonymAntonymSets.filter(
                set => set && set.target && set.synonyms && set.antonyms
              )
            : [];

        if (!sets.length) {
            container.innerHTML = `
                <div class="exercise-empty-state">
                    <p>📚 В этой главе пока нет упражнений на синонимы и антонимы.</p>
                    <p class="empty-state-hint">Они появятся в следующих обновлениях!</p>
                </div>
            `;
            return;
        }

        const cardsHtml = sets.map(set => renderSynonymSet(set)).join('');
        container.innerHTML = `<div class="synonym-exercise">${cardsHtml}</div>`;

        // Инициализация каждого набора
        container.querySelectorAll('.synonym-set').forEach(setElement => {
            new SynonymAntonymSet(setElement);
        });

        refreshActiveExerciseContentHeight();
    }

    function renderSynonymSet(set) {
        const synonyms = shuffleArray(set.synonyms || []);
        const antonyms = shuffleArray(set.antonyms || []);
        const cards = shuffleArray([
            ...synonyms.map(item => ({ ...item, role: 'synonym' })),
            ...antonyms.map(item => ({ ...item, role: 'antonym' }))
        ]);

        return `
            <article class="synonym-set" data-set-id="${set.id}">
                <header class="synonym-header">
                    <h4>📖 ${set.title || 'Найдите синонимы и антонимы'}</h4>
                    <div class="synonym-target">
                        <span class="target-label">Целевое слово:</span>
                        <span class="target-word">${set.target.word}</span>
                        <span class="target-translation">(${set.target.translation})</span>
                        ${set.target.hint ? `
                            <span class="target-hint" title="${set.target.hint}">
                                💡 ${set.target.hint}
                            </span>
                        ` : ''}
                    </div>
                    ${set.narration ? `
                        <p class="synonym-narration">
                            <em>${set.narration}</em>
                        </p>
                    ` : ''}
                </header>

                <div class="synonym-board">
                    <section class="synonym-column" data-role="synonym">
                        <h5>✅ Синонимы</h5>
                        <p class="column-hint">Близкие по значению</p>
                        <div class="synonym-dropzone" 
                             data-dropzone="synonym"
                             ondrop="event.preventDefault()"
                             ondragover="event.preventDefault()">
                        </div>
                    </section>

                    <section class="synonym-column" data-role="antonym">
                        <h5>❌ Антонимы</h5>
                        <p class="column-hint">Противоположные</p>
                        <div class="synonym-dropzone" 
                             data-dropzone="antonym"
                             ondrop="event.preventDefault()"
                             ondragover="event.preventDefault()">
                        </div>
                    </section>
                </div>

                <div class="synonym-cards-pool">
                    <p class="pool-label">Перетащите карточки в нужные колонки:</p>
                    <div class="synonym-cards">
                        ${cards.map((item, index) => `
                            <button class="synonym-card"
                                    type="button"
                                    draggable="true"
                                    data-role="${item.role}"
                                    data-word="${item.word}"
                                    data-index="${index}">
                                <span class="card-word">${item.word}</span>
                                <span class="card-translation">${item.translation}</span>
                            </button>
                        `).join('')}
                    </div>
                </div>

                <footer class="synonym-controls">
                    <button type="button" class="btn-check synonym-check">
                        ✔️ Проверить
                    </button>
                    <button type="button" class="btn-reset synonym-reset">
                        🔄 Сбросить
                    </button>
                    <button type="button" class="btn-hint synonym-hint">
                        💡 Подсказка
                    </button>
                    <div class="synonym-feedback" aria-live="polite"></div>
                    <div class="synonym-progress">
                        <span class="progress-text">Прогресс: </span>
                        <span class="progress-value">0 / ${cards.length}</span>
                    </div>
                </footer>
            </article>
        `;
    }

    class SynonymAntonymSet {
        constructor(root) {
            this.root = root;
            this.cards = Array.from(root.querySelectorAll('.synonym-card'));
            this.dropzones = Array.from(root.querySelectorAll('.synonym-dropzone'));
            this.feedback = root.querySelector('.synonym-feedback');
            this.checkButton = root.querySelector('.synonym-check');
            this.resetButton = root.querySelector('.synonym-reset');
            this.hintButton = root.querySelector('.synonym-hint');
            this.progressValue = root.querySelector('.progress-value');
            this.cardsPool = root.querySelector('.synonym-cards');

            this.selectedCard = null;
            this.hintsUsed = 0;
            this.attempts = 0;

            this.bindEvents();
            this.updateProgress();
        }

        bindEvents() {
            // Drag and Drop
            this.cards.forEach(card => {
                card.addEventListener('dragstart', e => this.handleDragStart(e, card));
                card.addEventListener('dragend', e => this.handleDragEnd(e, card));
                card.addEventListener('click', () => this.handleCardClick(card));

                // Touch events для мобильных
                card.addEventListener('touchstart', e => this.handleTouchStart(e, card), {passive: false});
                card.addEventListener('touchmove', e => this.handleTouchMove(e, card), {passive: false});
                card.addEventListener('touchend', e => this.handleTouchEnd(e, card));
            });

            this.dropzones.forEach(zone => {
                zone.addEventListener('dragover', e => this.handleDragOver(e, zone));
                zone.addEventListener('dragleave', e => this.handleDragLeave(e, zone));
                zone.addEventListener('drop', e => this.handleDrop(e, zone));
                zone.addEventListener('click', () => this.handleZoneClick(zone));
            });

            // Кнопки
            this.checkButton?.addEventListener('click', () => this.checkAnswers());
            this.resetButton?.addEventListener('click', () => this.reset());
            this.hintButton?.addEventListener('click', () => this.showHint());

            // Возврат карточки в пул по клику
            this.root.addEventListener('click', e => {
                if (e.target.closest('.synonym-dropzone .synonym-card')) {
                    const card = e.target.closest('.synonym-card');
                    this.returnToPool(card);
                }
            });
        }

        handleDragStart(event, card) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', card.dataset.index || '');
            card.classList.add('dragging');
            this.selectedCard = card;
        }

        handleDragEnd(event, card) {
            card.classList.remove('dragging');
            this.dropzones.forEach(zone => zone.classList.remove('drag-over'));
        }

        handleDragOver(event, zone) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'move';
            zone.classList.add('drag-over');
        }

        handleDragLeave(event, zone) {
            if (!zone.contains(event.relatedTarget)) {
                zone.classList.remove('drag-over');
            }
        }

        handleDrop(event, zone) {
            event.preventDefault();
            zone.classList.remove('drag-over');

            const draggingCard = this.root.querySelector('.synonym-card.dragging') || this.selectedCard;
            if (!draggingCard) return;

            // Анимация
            draggingCard.style.transition = 'transform 0.3s ease';

            // Проверка правильности сразу (опционально)
            const isCorrect = this.isCorrectDrop(draggingCard, zone);

            zone.appendChild(draggingCard);
            draggingCard.classList.add('placed');
            draggingCard.classList.remove('dragging');

            if (isCorrect) {
                this.animateSuccess(draggingCard);
                this.setFeedback('Отлично! ✨', true);
            } else {
                this.animateError(draggingCard);
                this.setFeedback('Попробуйте ещё раз 🤔', false);
            }

            this.updateProgress();
            refreshActiveExerciseContentHeight();
        }

        handleCardClick(card) {
            // Toggle selection
            if (card.classList.contains('selected')) {
                card.classList.remove('selected');
                this.selectedCard = null;
            } else {
                this.cards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                this.selectedCard = card;
            }
        }

        handleZoneClick(zone) {
            if (this.selectedCard && !this.selectedCard.classList.contains('placed')) {
                zone.appendChild(this.selectedCard);
                this.selectedCard.classList.add('placed');
                this.selectedCard.classList.remove('selected');

                const isCorrect = this.isCorrectDrop(this.selectedCard, zone);
                if (isCorrect) {
                    this.animateSuccess(this.selectedCard);
                }

                this.selectedCard = null;
                this.updateProgress();
                refreshActiveExerciseContentHeight();
            }
        }

        handleTouchStart(event, card) {
            event.preventDefault();
            this.touchCard = card;
            card.classList.add('dragging');
        }

        handleTouchMove(event, card) {
            event.preventDefault();
            const touch = event.touches[0];
            const elem = document.elementFromPoint(touch.clientX, touch.clientY);
            const zone = elem?.closest('.synonym-dropzone');

            this.dropzones.forEach(z => z.classList.remove('drag-over'));
            if (zone) zone.classList.add('drag-over');
        }

        handleTouchEnd(event, card) {
            event.preventDefault();
            const touch = event.changedTouches[0];
            const elem = document.elementFromPoint(touch.clientX, touch.clientY);
            const zone = elem?.closest('.synonym-dropzone');

            if (zone) {
                this.handleDrop(event, zone);
            }

            card.classList.remove('dragging');
            this.dropzones.forEach(z => z.classList.remove('drag-over'));
        }

        returnToPool(card) {
            card.classList.remove('placed', 'correct', 'incorrect');
            this.cardsPool?.appendChild(card);
            this.updateProgress();
            this.setFeedback('Карточка возвращена в пул', true);
            refreshActiveExerciseContentHeight();
        }

        isCorrectDrop(card, zone) {
            const expectedRole = zone.dataset.dropzone;
            return card.dataset.role === expectedRole;
        }

        checkAnswers() {
            this.attempts++;
            let correctCount = 0;
            let total = this.cards.length;
            let placedCount = 0;

            this.dropzones.forEach(zone => {
                Array.from(zone.children).forEach(card => {
                    placedCount++;
                    if (this.isCorrectDrop(card, zone)) {
                        correctCount++;
                        card.classList.add('correct');
                        card.classList.remove('incorrect');
                        this.animateSuccess(card);
                    } else {
                        card.classList.add('incorrect');
                        card.classList.remove('correct');
                        this.animateError(card);
                    }
                });
            });

            if (placedCount === 0) {
                this.setFeedback('Сначала распределите карточки! 📝', false);
            } else if (placedCount < total) {
                this.setFeedback(
                    `Распределите все карточки! Осталось: ${total - placedCount}`,
                    false
                );
            } else if (correctCount === total) {
                this.setFeedback(
                    `🎉 Превосходно! Все ${total} слов распределены правильно! ` +
                    `${this.attempts === 1 ? 'С первой попытки!' : `Попыток: ${this.attempts}`}`,
                    true
                );
                this.celebrateSuccess();
            } else {
                this.setFeedback(
                    `Правильно: ${correctCount} из ${total}. ` +
                    `Проверьте красные карточки и попробуйте снова! 💪`,
                    false
                );
            }
        }

        showHint() {
            this.hintsUsed++;
            const unplacedCards = this.cards.filter(card => !card.classList.contains('placed'));

            if (unplacedCards.length === 0) {
                this.setFeedback('Все карточки уже размещены! Нажмите "Проверить"', true);
                return;
            }

            // Показываем подсказку для первой неразмещённой карточки
            const card = unplacedCards[0];
            const correctZone = this.dropzones.find(
                zone => zone.dataset.dropzone === card.dataset.role
            );

            if (correctZone) {
                // Подсвечиваем нужную зону
                correctZone.classList.add('hint-highlight');
                card.classList.add('hint-card');

                this.setFeedback(
                    `Подсказка: "${card.dataset.word}" должно быть в колонке ` +
                    `"${card.dataset.role === 'synonym' ? 'Синонимы' : 'Антонимы'}"`,
                    true
                );

                setTimeout(() => {
                    correctZone.classList.remove('hint-highlight');
                    card.classList.remove('hint-card');
                }, 3000);
            }
        }

        reset() {
            const pool = this.cardsPool;
            if (!pool) return;

            this.cards.forEach(card => {
                card.classList.remove(
                    'placed', 'correct', 'incorrect',
                    'selected', 'hint-card'
                );
                card.style.transition = 'all 0.3s ease';
                pool.appendChild(card);
            });

            this.selectedCard = null;
            this.attempts = 0;
            this.hintsUsed = 0;

            this.setFeedback('Упражнение сброшено. Попробуйте снова! 🔄', true);
            this.updateProgress();
            refreshActiveExerciseContentHeight();
        }

        updateProgress() {
            if (!this.progressValue) return;

            const placed = this.cards.filter(
                card => card.classList.contains('placed')
            ).length;
            const total = this.cards.length;

            this.progressValue.textContent = `${placed} / ${total}`;

            // Добавляем визуальный индикатор прогресса
            const percent = (placed / total) * 100;
            this.progressValue.style.background = `linear-gradient(
                to right, 
                #7c3aed ${percent}%, 
                #f3f4f6 ${percent}%
            )`;
        }

        animateSuccess(card) {
            card.style.animation = 'pulseSuccess 0.5s ease';
            setTimeout(() => {
                card.style.animation = '';
            }, 500);
        }

        animateError(card) {
            card.style.animation = 'shakeError 0.5s ease';
            setTimeout(() => {
                card.style.animation = '';
            }, 500);
        }

        celebrateSuccess() {
            // Конфетти или другая праздничная анимация
            this.root.classList.add('success-celebration');
            setTimeout(() => {
                this.root.classList.remove('success-celebration');
            }, 2000);
        }

        setFeedback(message, isSuccess) {
            if (!this.feedback) return;

            this.feedback.textContent = message;
            this.feedback.className = 'synonym-feedback ' + 
                (isSuccess ? 'feedback-success' : 'feedback-error');

            // Анимация появления
            this.feedback.style.animation = 'fadeInUp 0.3s ease';
            setTimeout(() => {
                this.feedback.style.animation = '';
            }, 300);
        }
    }

    // Вспомогательная функция перемешивания
    function shuffleArray(items) {
        const array = Array.isArray(items) ? [...items] : [];
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // ==========================================
    // ОБНОВЛЕНИЕ НАЗВАНИЙ В UI
    // ==========================================

    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(() => {
            if (window.phaseKeys && window.phaseKeys.length > 0) {
                window.initializeExercises(window.phaseKeys[0]);
            }
        }, 120);
    });

})();
