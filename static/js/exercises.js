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

        const articlesContainer = document.querySelector(`[data-articles-container][data-phase="${phaseId}"]`);
        if (articlesContainer) {
            initializeArticlesExercise(articlesContainer, phaseVocabulary);
        }

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
    
    function initializeArticlesExercise(container, phaseVocabulary) {
        if (!(container instanceof HTMLElement)) {
            return;
        }

        // Извлекаем слова с артиклями
        const wordsWithArticles = [];
        if (phaseVocabulary && phaseVocabulary.vocabulary) {
            phaseVocabulary.vocabulary.forEach(word => {
                if (!word.german || !word.russian) return;
                
                const parts = word.german.split(' ');
                if (['der', 'die', 'das'].includes(parts[0])) {
                    wordsWithArticles.push({
                        article: parts[0],
                        german: parts.slice(1).join(' '),
                        russian: word.russian,
                        fullWord: word.german
                    });
                }
            });
        }
        
        // Перемешиваем и ограничиваем до 9 слов
        const shuffled = wordsWithArticles.sort(() => Math.random() - 0.5).slice(0, 9);

        if (shuffled.length === 0) {
            container.innerHTML = '<div class="exercise-empty-state">В этой фазе нет слов с артиклями.</div>';
            return;
        }

        container.innerHTML = `
            <div class="articles-exercise">
                <div class="articles-instruction">
                    Распределите слова по родам (drag & drop или клик для мобильных)
                </div>

                <div class="article-columns">
                    <div class="article-column" data-article="der">
                        <h5 class="article-header">
                            <span class="article-label">DER</span>
                            <span class="article-desc">мужской род</span>
                        </h5>
                        <div class="article-drop-zone" data-zone="der"></div>
                    </div>
                    <div class="article-column" data-article="die">
                        <h5 class="article-header">
                            <span class="article-label">DIE</span>
                            <span class="article-desc">женский род</span>
                        </h5>
                        <div class="article-drop-zone" data-zone="die"></div>
                    </div>
                    <div class="article-column" data-article="das">
                        <h5 class="article-header">
                            <span class="article-label">DAS</span>
                            <span class="article-desc">средний род</span>
                        </h5>
                        <div class="article-drop-zone" data-zone="das"></div>
                    </div>
                </div>

                <div class="words-to-sort">
                    ${shuffled.map((word, idx) => `
                        <div class="article-word-card"
                             data-article="${word.article}"
                             data-word="${word.german}"
                             data-index="${idx}"
                             draggable="true">
                            <span class="word-german">${word.german}</span>
                            <span class="word-russian">${word.russian}</span>
                        </div>
                    `).join('')}
                </div>

                <div class="articles-controls">
                    <button class="check-articles-btn" type="button">Проверить</button>
                    <button class="reset-articles-btn" type="button">Сбросить</button>
                </div>
                <div class="articles-feedback"></div>
            </div>
        `;

        const exerciseElement = container.querySelector('.articles-exercise');
        if (exerciseElement) {
            attachArticlesDragDrop(exerciseElement);
        }
    }
    
    function attachArticlesDragDrop(container) {
        const cards = container.querySelectorAll('.article-word-card');
        const zones = container.querySelectorAll('.article-drop-zone');
        const checkBtn = container.querySelector('.check-articles-btn');
        const resetBtn = container.querySelector('.reset-articles-btn');
        const feedback = container.querySelector('.articles-feedback');
        const wordsContainer = container.querySelector('.words-to-sort');
        const accordionContent = container.closest('.exercise-content');

        function updateArticlesLayout() {
            window.requestAnimationFrame(() => {
                refreshActiveExerciseContentHeight();
                updateWordColumnScrollIndicators(container);
                if (accordionContent instanceof HTMLElement) {
                    accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
                }
            });
        }
        
        // Сохраняем начальные позиции для сброса
        const initialParent = cards[0]?.parentElement;
        
        // DRAG & DROP для десктопа
        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', '');
                card.classList.add('dragging');
                card.dataset.dragArticle = card.dataset.article;
                card.dataset.dragWord = card.dataset.word;
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                updateArticlesLayout();
            });
            
            // КЛИК для мобильных
            card.addEventListener('click', function(e) {
                e.stopPropagation();
                const wasSelected = this.classList.contains('selected');
                
                // Убираем выделение со всех карточек
                cards.forEach(c => c.classList.remove('selected'));
                
                if (!wasSelected) {
                    this.classList.add('selected');
                }
            });
        });
        
        // Обработчики для зон
        zones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                zone.classList.add('drag-over');
            });
            
            zone.addEventListener('dragleave', () => {
                zone.classList.remove('drag-over');
            });
            
            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                zone.classList.remove('drag-over');

                const draggingCard = container.querySelector('.dragging');
                if (draggingCard) {
                    zone.appendChild(draggingCard);
                    draggingCard.classList.remove('correct', 'incorrect');
                    updateArticlesLayout();
                }
            });

            // Клик по зоне для мобильных
            zone.addEventListener('click', function(e) {
                e.stopPropagation();
                const selected = container.querySelector('.article-word-card.selected');
                if (selected) {
                    this.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateArticlesLayout();
                }
            });
        });

        if (wordsContainer) {
            wordsContainer.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            });

            wordsContainer.addEventListener('drop', (e) => {
                e.preventDefault();
                const draggingCard = container.querySelector('.dragging');
                if (draggingCard) {
                    wordsContainer.appendChild(draggingCard);
                    draggingCard.classList.remove('correct', 'incorrect');
                    updateArticlesLayout();
                }
            });

            wordsContainer.addEventListener('click', function(e) {
                e.stopPropagation();
                const selected = container.querySelector('.article-word-card.selected');
                if (selected && selected.parentElement !== wordsContainer) {
                    wordsContainer.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateArticlesLayout();
                }
            });
        }
        
        // Проверка ответов
        checkBtn?.addEventListener('click', () => {
            let correct = 0;
            let total = 0;
            
            zones.forEach(zone => {
                const targetArticle = zone.dataset.zone;
                const cardsInZone = zone.querySelectorAll('.article-word-card');
                
                cardsInZone.forEach(card => {
                    total++;
                    card.classList.remove('correct', 'incorrect');
                    
                    if (card.dataset.article === targetArticle) {
                        card.classList.add('correct');
                        correct++;
                    } else {
                        card.classList.add('incorrect');
                    }
                });
            });
            
            // Проверяем карточки, оставшиеся в исходной зоне
            const unsortedCards = wordsContainer.querySelectorAll('.article-word-card');
            unsortedCards.forEach(card => {
                total++;
                card.classList.add('incorrect');
            });
            
            // Показываем результат
            if (feedback) {
                if (correct === total && total > 0) {
                    feedback.innerHTML = '<span class="success">[OK] Отлично! Все артикли правильные!</span>';
                    feedback.className = 'articles-feedback success';
                } else {
                    feedback.innerHTML = `<span class="partial">Правильно: ${correct} из ${total}. Попробуйте ещё раз!</span>`;
                    feedback.className = 'articles-feedback partial';
                }
            }

            updateArticlesLayout();
        });

        // Сброс
        resetBtn?.addEventListener('click', () => {
            cards.forEach(card => {
                card.classList.remove('correct', 'incorrect', 'selected');
                if (initialParent) {
                    initialParent.appendChild(card);
                }
            });

            if (feedback) {
                feedback.innerHTML = '';
                feedback.className = 'articles-feedback';
            }

            updateArticlesLayout();
        });

        updateArticlesLayout();
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
