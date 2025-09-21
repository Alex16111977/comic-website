/**
 * BUNDLE упражнений для King Lear Comic
 * Собрано из модулей в единый файл для работы через file:///
 * Без import/export - всё в глобальной области window
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

        // Используем глобальные данные phaseVocabularies
        const phaseVocabulary = window.phaseVocabularies && window.phaseVocabularies[phaseId];
        if (!phaseVocabulary) {
            console.warn('[Exercises] No data for phase:', phaseId);
            return;
        }

        // Инициализируем упражнение с артиклями
        const articlesContainer = document.querySelector(`[data-articles-container][data-phase="${phaseId}"]`);
        if (articlesContainer) {
            initializeArticlesExercise(articlesContainer, phaseVocabulary);
        }

        // Инициализируем контекстный перевод
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
        if (phaseVocabulary && phaseVocabulary.words) {
            phaseVocabulary.words.forEach(word => {
                if (!word.word || !word.translation) return;
                
                const parts = word.word.split(' ');
                if (['der', 'die', 'das'].includes(parts[0].toLowerCase())) {
                    wordsWithArticles.push({
                        article: parts[0].toLowerCase(),
                        german: parts.slice(1).join(' '),
                        russian: word.translation,
                        fullWord: word.word
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

        // Функция обновления высоты контента
        function updateLayout() {
            window.requestAnimationFrame(() => {
                if (typeof window.refreshActiveExerciseContentHeight === 'function') {
                    window.refreshActiveExerciseContentHeight();
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
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                updateLayout();
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
                    updateLayout();
                }
            });

            // Клик по зоне для мобильных
            zone.addEventListener('click', function(e) {
                e.stopPropagation();
                const selected = container.querySelector('.article-word-card.selected');
                if (selected) {
                    this.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateLayout();
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
                    updateLayout();
                }
            });

            wordsContainer.addEventListener('click', function(e) {
                e.stopPropagation();
                const selected = container.querySelector('.article-word-card.selected');
                if (selected && selected.parentElement !== wordsContainer) {
                    wordsContainer.appendChild(selected);
                    selected.classList.remove('selected', 'correct', 'incorrect');
                    updateLayout();
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

            updateLayout();
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

            updateLayout();
        });

        updateLayout();
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

        if (phaseVocabulary && phaseVocabulary.words) {
            phaseVocabulary.words.forEach((word, idx) => {
                // Проверяем наличие всех необходимых полей
                if (!word.word || !word.translation || !word.sentence || !word.sentenceTranslation) {
                    return;
                }
                
                // Убираем артикль для поиска в предложении
                const germanWord = word.word.replace(/^(der|die|das)\s+/i, '');
                
                // Создаём регулярное выражение для поиска слова с учетом окончаний
                const wordPattern = new RegExp(
                    `\\b${germanWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\w*\\b`,
                    'gi'
                );
                
                // Проверяем, есть ли слово в предложении
                if (word.sentence.match(wordPattern)) {
                    contextExercises.push({
                        id: `context-${idx}`,
                        germanWord: word.word,
                        russianWord: word.translation,
                        germanSentence: word.sentence,
                        russianSentence: word.sentenceTranslation,
                        // Создаём предложение с пропуском
                        germanBlank: word.sentence.replace(wordPattern, '_____'),
                        russianBlank: word.sentenceTranslation.includes(word.translation) 
                            ? word.sentenceTranslation.replace(word.translation, '_____')
                            : word.sentenceTranslation,
                        correctAnswer: word.translation
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
        if (phaseVocabulary && phaseVocabulary.words) {
            phaseVocabulary.words.forEach(word => {
                if (word.translation && word.translation !== correctAnswer) {
                    allTranslations.push(word.translation);
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
    
    // ==========================================
    // ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    // ==========================================
    
    // Обновление высоты контента упражнений
    window.refreshActiveExerciseContentHeight = function() {
        const activeToggle = document.querySelector('.exercise-toggle.active');
        if (!activeToggle) {
            return;
        }

        const content = activeToggle.nextElementSibling;
        if (!(content instanceof HTMLElement) || content.classList.contains('collapsed')) {
            return;
        }

        const previousTransition = content.style.transition;
        content.style.transition = 'none';
        content.style.maxHeight = 'none';
        
        const newHeight = content.scrollHeight;
        requestAnimationFrame(() => {
            content.style.transition = previousTransition || '';
            content.style.maxHeight = `${newHeight}px`;
        });
    };

    window.updateWordColumnScrollIndicators = function(context) {
        // Эта функция может быть пустой, если не используется
        return;
    };
    
    // ==========================================
    // АВТОЗАПУСК ПРИ ЗАГРУЗКЕ
    // ==========================================
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Exercises Bundle] DOM loaded, waiting for data...');
        
        // Ждём загрузки данных и инициализируем упражнения
        setTimeout(() => {
            if (window.phaseKeys && window.phaseKeys.length > 0) {
                console.log('[Exercises Bundle] Initializing first phase:', window.phaseKeys[0]);
                window.initializeExercises(window.phaseKeys[0]);
            }
        }, 120);
    });

    console.log('[Exercises Bundle] ✅ Loaded successfully');
})();
