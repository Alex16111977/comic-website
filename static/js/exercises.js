/**
 * Модуль упражнений для изучения немецкого
 * Упражнение 1: Артикли и род
 * Упражнение 2: Контекстный перевод
 */

// ==========================================
// 1. УПРАЖНЕНИЕ "АРТИКЛИ И РОД"
// ==========================================

function initializeArticlesExercise(container, phaseVocabulary) {
    const section = container.querySelector('.word-families-section');
    if (!section) return;
    
    const content = section.querySelector('.relations-content');
    if (!content) return;
    
    // Собираем слова с артиклями из текущей фазы
    const wordsWithArticles = [];
    if (phaseVocabulary && phaseVocabulary.vocabulary) {
        phaseVocabulary.vocabulary.forEach(word => {
            if (word.german && word.russian) {
                const parts = word.german.split(' ');
                if (parts[0] === 'der' || parts[0] === 'die' || parts[0] === 'das') {
                    wordsWithArticles.push({
                        article: parts[0],
                        german: parts.slice(1).join(' '),
                        russian: word.russian,
                        fullWord: word.german
                    });
                }
            }
        });
    }
    
    // Обновляем атрибут наличия контента
    section.dataset.hasContent = wordsWithArticles.length > 0 ? 'true' : 'false';
    
    if (wordsWithArticles.length === 0) {
        content.innerHTML = '<div class="relations-empty-state">В этой фазе нет слов с артиклями.</div>';
        return;
    }
    
    // Ограничиваем до 9 слов за раз
    const exerciseWords = wordsWithArticles.slice(0, 9);
    
    // Генерируем HTML упражнения
    content.innerHTML = `
        <div class="articles-exercise">
            <div class="articles-instruction">Распределите слова по родам, перетаскивая их в нужные колонки</div>
            
            <div class="article-columns">
                <div class="article-column" data-article="der">
                    <h5 class="article-header">DER<br><span>мужской род</span></h5>
                    <div class="article-drop-zone" data-zone="der"></div>
                </div>
                <div class="article-column" data-article="die">
                    <h5 class="article-header">DIE<br><span>женский род</span></h5>
                    <div class="article-drop-zone" data-zone="die"></div>
                </div>
                <div class="article-column" data-article="das">
                    <h5 class="article-header">DAS<br><span>средний род</span></h5>
                    <div class="article-drop-zone" data-zone="das"></div>
                </div>
            </div>
            
            <div class="words-to-sort">
                ${exerciseWords.map((word, idx) => `
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
                <button class="reset-articles-btn" type="button">Сброс</button>
            </div>
            <div class="articles-feedback"></div>
        </div>
    `;
    
    // Добавляем обработчики
    attachArticlesDragDrop(content);
}

function attachArticlesDragDrop(container) {
    const cards = container.querySelectorAll('.article-word-card');
    const zones = container.querySelectorAll('.article-drop-zone');
    const checkBtn = container.querySelector('.check-articles-btn');
    const resetBtn = container.querySelector('.reset-articles-btn');
    const feedback = container.querySelector('.articles-feedback');
    const wordsContainer = container.querySelector('.words-to-sort');
    
    // Drag and Drop для десктопа
    cards.forEach(card => {
        card.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('article', card.dataset.article);
            e.dataTransfer.setData('word', card.dataset.word);
            e.dataTransfer.setData('index', card.dataset.index);
            card.classList.add('dragging');
        });
        
        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
        });
        
        // Клик для мобильных устройств
        card.addEventListener('click', function() {
            const selected = container.querySelector('.article-word-card.selected');
            if (selected && selected !== this) {
                selected.classList.remove('selected');
            }
            this.classList.toggle('selected');
        });
    });
    
    zones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });
        
        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });
        
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            
            const word = e.dataTransfer.getData('word');
            const card = container.querySelector(`[data-word="${word}"]`);
            if (card) {
                zone.appendChild(card);
                card.classList.remove('selected');
            }
        });
        
        // Клик на зону для мобильных
        zone.addEventListener('click', function() {
            const selected = container.querySelector('.article-word-card.selected');
            if (selected) {
                this.appendChild(selected);
                selected.classList.remove('selected');
            }
        });
    });
    
    // Проверка ответов
    if (checkBtn) {
        checkBtn.addEventListener('click', () => {
            let correct = 0;
            let total = 0;
            
            zones.forEach(zone => {
                const targetArticle = zone.dataset.zone;
                const cardsInZone = zone.querySelectorAll('.article-word-card');
                
                cardsInZone.forEach(card => {
                    total++;
                    if (card.dataset.article === targetArticle) {
                        card.classList.add('correct');
                        card.classList.remove('incorrect');
                        correct++;
                    } else {
                        card.classList.add('incorrect');
                        card.classList.remove('correct');
                    }
                });
            });
            
            // Проверяем карточки, оставшиеся в исходной зоне
            const unplacedCards = wordsContainer.querySelectorAll('.article-word-card');
            unplacedCards.forEach(card => {
                card.classList.add('unplaced');
                total++;
            });
            
            if (feedback) {
                if (total === 0) {
                    feedback.innerHTML = '<span class="warning">Разместите карточки по колонкам!</span>';
                } else if (correct === total && unplacedCards.length === 0) {
                    feedback.innerHTML = '<span class="success">🎉 Отлично! Все артикли правильные!</span>';
                } else if (unplacedCards.length > 0) {
                    feedback.innerHTML = `<span class="warning">Разместите все карточки!</span>`;
                } else {
                    feedback.innerHTML = `<span class="partial">Правильно: ${correct} из ${total}. Попробуйте ещё раз!</span>`;
                }
            }
        });
    }
    
    // Сброс упражнения
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            cards.forEach(card => {
                wordsContainer.appendChild(card);
                card.classList.remove('correct', 'incorrect', 'selected', 'unplaced');
            });
            if (feedback) {
                feedback.innerHTML = '';
            }
        });
    }
}

// ==========================================
// 2. УПРАЖНЕНИЕ "КОНТЕКСТНЫЙ ПЕРЕВОД"
// ==========================================

function initializeContextExercise(container, phaseVocabulary) {
    const section = container.querySelector('.collocations-section');
    if (!section) return;
    
    const content = section.querySelector('.relations-content');
    if (!content) return;
    
    // Собираем слова с предложениями
    const contextExercises = [];
    if (phaseVocabulary && phaseVocabulary.vocabulary) {
        phaseVocabulary.vocabulary.forEach((word, idx) => {
            if (word.german && word.russian && word.sentence && word.sentence_translation) {
                // Удаляем артикль для поиска в предложении
                const germanWord = word.german.replace(/^(der|die|das)\s+/, '');
                
                // Создаем регулярное выражение для поиска слова (с учетом склонений)
                const wordRoot = germanWord.substring(0, Math.max(4, germanWord.length - 2));
                const germanRegex = new RegExp(wordRoot + '\\w*', 'gi');
                
                // Проверяем наличие слова в предложении
                const matches = word.sentence.match(germanRegex);
                if (matches && matches.length > 0) {
                    // Заменяем первое вхождение на пропуск
                    const germanBlank = word.sentence.replace(matches[0], '_____');
                    
                    contextExercises.push({
                        id: idx,
                        germanWord: word.german,
                        russianWord: word.russian,
                        germanSentence: germanBlank,
                        russianSentence: word.sentence_translation,
                        correctAnswer: word.russian,
                        originalWord: matches[0]
                    });
                }
            }
        });
    }
    
    // Ограничиваем до 5 упражнений
    const exercises = contextExercises.slice(0, 5);
    
    // Обновляем атрибут наличия контента
    section.dataset.hasContent = exercises.length > 0 ? 'true' : 'false';
    
    if (exercises.length === 0) {
        content.innerHTML = '<div class="relations-empty-state">В этой фазе нет предложений для контекстного перевода.</div>';
        return;
    }
    
    // Генерируем HTML упражнений
    content.innerHTML = `
        <div class="context-exercises">
            ${exercises.map((ex, idx) => {
                // Генерируем варианты ответов
                const options = [ex.correctAnswer];
                
                // Добавляем неправильные варианты из других слов фазы
                const otherWords = phaseVocabulary.vocabulary
                    .filter(w => w.russian && w.russian !== ex.correctAnswer)
                    .map(w => w.russian)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3);
                
                // Если недостаточно слов из фазы, добавляем общие отвлекающие варианты
                while (options.length + otherWords.length < 4) {
                    const distractors = ['власть', 'корона', 'королевство', 'трон', 'дочь', 'любовь', 'гнев'];
                    const randomDistractor = distractors[Math.floor(Math.random() * distractors.length)];
                    if (!options.includes(randomDistractor) && !otherWords.includes(randomDistractor)) {
                        otherWords.push(randomDistractor);
                    }
                }
                
                options.push(...otherWords.slice(0, 3));
                const shuffledOptions = options.sort(() => Math.random() - 0.5);
                
                return `
                    <div class="context-exercise-card" data-exercise-id="${ex.id}">
                        <div class="exercise-number">Упражнение ${idx + 1}</div>
                        <div class="sentence-german">${ex.germanSentence}</div>
                        <div class="sentence-russian">${ex.russianSentence}</div>
                        <div class="context-question">Выберите правильный перевод пропущенного слова:</div>
                        <div class="context-options">
                            ${shuffledOptions.map((opt, optIdx) => `
                                <button class="context-option" 
                                        type="button"
                                        data-answer="${opt}"
                                        data-correct="${opt === ex.correctAnswer}">
                                    ${opt}
                                </button>
                            `).join('')}
                        </div>
                        <div class="context-feedback"></div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    
    // Добавляем обработчики
    attachContextHandlers(content);
}

function attachContextHandlers(container) {
    const cards = container.querySelectorAll('.context-exercise-card');
    
    cards.forEach(card => {
        const options = card.querySelectorAll('.context-option');
        const feedback = card.querySelector('.context-feedback');
        
        options.forEach(option => {
            option.addEventListener('click', function() {
                // Блокируем все кнопки в этой карточке
                options.forEach(opt => opt.disabled = true);
                
                if (this.dataset.correct === 'true') {
                    this.classList.add('correct');
                    if (feedback) {
                        feedback.innerHTML = '<span class="success">✓ Правильно!</span>';
                    }
                } else {
                    this.classList.add('incorrect');
                    // Показываем правильный ответ
                    options.forEach(opt => {
                        if (opt.dataset.correct === 'true') {
                            opt.classList.add('correct');
                        }
                    });
                    if (feedback) {
                        feedback.innerHTML = '<span class="error">✗ Неверно. См. правильный ответ.</span>';
                    }
                }
            });
        });
    });
}

// ==========================================
// 3. ИНИЦИАЛИЗАЦИЯ УПРАЖНЕНИЙ
// ==========================================

function initializeExercises(phaseKey) {
    // Находим контейнер для текущей фазы
    const containers = document.querySelectorAll('.relations-container');
    
    containers.forEach(container => {
        if (container.dataset.phase === phaseKey) {
            // Получаем данные словаря для текущей фазы
            const phaseVocabulary = window.phaseVocabularies ? window.phaseVocabularies[phaseKey] : null;
            
            // Инициализируем упражнение с артиклями
            initializeArticlesExercise(container, phaseVocabulary);
            
            // Инициализируем контекстный перевод
            initializeContextExercise(container, phaseVocabulary);
        }
    });
}

// Экспортируем функцию для использования в основном runtime
window.initializeExercises = initializeExercises;
