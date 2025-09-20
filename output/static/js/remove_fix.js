/**
 * РАБОЧЕЕ ИСПРАВЛЕНИЕ УДАЛЕНИЯ КАРТОЧЕК
 * ======================================
 * Простое и прямое решение без лишней сложности
 */

console.log('[WORKING FIX] Инициализация исправления удаления');

// Переопределяем глобальную функцию removeWord если она существует
if (typeof window.removeWord !== 'undefined' || window.removeWord === null) {
    console.log('[WORKING FIX] Переопределяем существующую removeWord');
}

// Новая рабочая функция удаления
window.removeWord = function(wordId) {
    console.log('[WORKING FIX] removeWord вызвана для:', wordId);
    
    // Список всех возможных ключей в localStorage
    const storageKeys = [
        'test_words',      // Для тестовой страницы
        'reviewWords',     // Основной ключ ReviewManager
        'review_words',    // Альтернативный ключ
        'vocabulary',      // Ключ словаря
        'studyWords',      // Слова для изучения
        'study_words'      // Альтернативный ключ
    ];
    
    let totalRemoved = 0;
    
    // Проходим по всем ключам
    storageKeys.forEach(key => {
        try {
            const data = localStorage.getItem(key);
            if (!data) return;
            
            let words = JSON.parse(data);
            if (!Array.isArray(words)) return;
            
            const originalLength = words.length;
            
            // Фильтруем массив - удаляем слово с любым совпадением
            words = words.filter(w => {
                // Получаем все возможные идентификаторы слова
                const wordIds = [
                    w.id,
                    w.wordId, 
                    w.word,
                    w.german,
                    w.name
                ].filter(Boolean); // Убираем undefined/null
                
                // Проверяем каждый идентификатор
                for (let wId of wordIds) {
                    // Приводим к строке и нормализуем
                    const normalizedWId = String(wId).toLowerCase().replace(/[\s_-]+/g, '');
                    const normalizedSearchId = String(wordId).toLowerCase().replace(/[\s_-]+/g, '');
                    
                    if (normalizedWId === normalizedSearchId) {
                        console.log(`[WORKING FIX] Найдено совпадение в ${key}: ${wId}`);
                        return false; // Удаляем это слово
                    }
                }
                
                return true; // Оставляем слово
            });
            
            // Если что-то удалили, сохраняем обратно
            if (words.length < originalLength) {
                localStorage.setItem(key, JSON.stringify(words));
                const removed = originalLength - words.length;
                totalRemoved += removed;
                console.log(`[WORKING FIX] Удалено из ${key}: ${removed} слов`);
            }
        } catch (err) {
            console.error(`[WORKING FIX] Ошибка при обработке ${key}:`, err);
        }
    });
    
    // Удаляем карточку из DOM с анимацией
    const removeButtons = document.querySelectorAll('.btn-remove, .remove-btn, [onclick*="removeWord"]');
    removeButtons.forEach(btn => {
        // Ищем кнопку которая относится к этому wordId
        const btnWordId = btn.getAttribute('data-word-id') || 
                         btn.getAttribute('data-word') ||
                         btn.dataset?.wordId ||
                         btn.dataset?.word ||
                         (btn.onclick ? btn.onclick.toString().match(/removeWord\(['"]([^'"]+)['"]\)/)?.[1] : null);
        
        if (btnWordId && btnWordId.toLowerCase().replace(/[\s_-]+/g, '') === 
            wordId.toLowerCase().replace(/[\s_-]+/g, '')) {
            
            const card = btn.closest('.word-card, .review-card, .vocabulary-card, .card');
            if (card) {
                // Анимация исчезновения
                card.style.transition = 'all 0.3s ease-out';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.95) translateX(50px)';
                
                setTimeout(() => {
                    card.remove();
                    console.log('[WORKING FIX] Карточка удалена из DOM');
                    
                    // Обновляем счетчики
                    updateCounters();
                    
                    // Проверяем остались ли карточки
                    checkEmpty();
                    
                    // Если есть функция обновления отображения - вызываем
                    if (typeof displayWords === 'function') {
                        displayWords();
                    }
                }, 300);
            }
        }
    });
    
    if (totalRemoved > 0) {
        console.log(`[WORKING FIX] Всего удалено: ${totalRemoved} слов`);
    } else {
        console.warn('[WORKING FIX] Слово не найдено ни в одном хранилище');
    }
    
    return totalRemoved > 0;
};

// Функция обновления счетчиков
function updateCounters() {
    const counters = document.querySelectorAll('.review-count, .word-count, .counter, #count');
    counters.forEach(counter => {
        const currentCount = parseInt(counter.textContent) || 0;
        if (currentCount > 0) {
            counter.textContent = currentCount - 1;
        }
    });
}

// Функция проверки пустоты
function checkEmpty() {
    const cards = document.querySelectorAll('.word-card, .review-card, .vocabulary-card, .card');
    if (cards.length === 0) {
        const emptyMessages = document.querySelectorAll('.empty-message, .no-words, .empty');
        emptyMessages.forEach(msg => {
            msg.style.display = 'block';
        });
    }
}

// Также перехватываем клики для дополнительной надежности
document.addEventListener('click', function(e) {
    // Проверяем, это кнопка удаления?
    const btn = e.target.closest('.btn-remove, .remove-btn, [onclick*="removeWord"]');
    if (!btn) return;
    
    console.log('[WORKING FIX] Перехвачен клик на кнопку удаления');
    
    // Получаем ID слова
    const wordId = btn.getAttribute('data-word-id') || 
                  btn.getAttribute('data-word') ||
                  btn.dataset?.wordId ||
                  btn.dataset?.word ||
                  (btn.onclick ? btn.onclick.toString().match(/removeWord\(['"]([^'"]+)['"]\)/)?.[1] : null);
    
    if (wordId) {
        console.log('[WORKING FIX] Найден wordId:', wordId);
        
        // Вызываем нашу функцию удаления
        window.removeWord(wordId);
        
        // Предотвращаем стандартное действие
        e.preventDefault();
        e.stopPropagation();
    }
}, true); // true для перехвата на фазе capture

// Для ReviewManager - переопределяем его метод если он существует
if (window.ReviewManager) {
    console.log('[WORKING FIX] Найден ReviewManager, переопределяем removeWord');
    
    const originalRemove = window.ReviewManager.removeWord;
    
    window.ReviewManager.removeWord = function(wordId) {
        console.log('[WORKING FIX] ReviewManager.removeWord вызван для:', wordId);
        
        // Вызываем нашу улучшенную версию
        const result = window.removeWord(wordId);
        
        // Обновляем отображение ReviewManager
        if (this.updateDisplay) {
            this.updateDisplay();
        }
        
        return result;
    };
}

console.log('[WORKING FIX] ✅ Исправление полностью активировано');
console.log('[WORKING FIX] Функция window.removeWord доступна глобально');
