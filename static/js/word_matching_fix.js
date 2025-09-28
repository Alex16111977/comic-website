/**
 * ФІКС ДЛЯ УПРАЖНЕННЯ "ПОДБОР СЛОВ" - БЕЗ ПРОКРУТКИ
 * Проблема: В KingLearComic потрібна прокрутка для перегляду всіх слів
 * Рішення: Динамічно модифікуємо стилі для планшетів
 */

(function() {
    'use strict';
    
    console.log('[WordMatchingFix] Ініціалізація фіксу для упражнення');
    
    // Функція для застосування оптимізованих стилів
    function applyWordMatchingFix() {
        // Знаходимо всі контейнери упражнення
        const containers = document.querySelectorAll('.word-selection-container, .word-selection-host');
        
        containers.forEach(container => {
            console.log('[WordMatchingFix] Оптимізуємо контейнер');
            
            // Знаходимо колонки
            const wordColumns = container.querySelector('.word-columns');
            if (wordColumns) {
                // Застосовуємо стилі для контейнера колонок
                wordColumns.style.minHeight = '520px';
                wordColumns.style.maxHeight = 'none';
                wordColumns.style.overflow = 'visible';
                wordColumns.style.display = 'grid';
                wordColumns.style.gridTemplateColumns = '1fr 1fr';
                wordColumns.style.gap = '20px';
                
                console.log('[WordMatchingFix] Стилі контейнера застосовано');
            }
            
            // Знаходимо всі колонки
            const columns = container.querySelectorAll('.word-column');
            columns.forEach(column => {
                column.style.overflow = 'visible';
                column.style.maxHeight = 'none';
                column.style.height = 'auto';
                
                // Видаляємо індикатори прокрутки
                column.classList.remove('has-scroll');
            });
            
            // Знаходимо всі списки слів
            const wordLists = container.querySelectorAll('.word-list');
            wordLists.forEach(list => {
                list.style.overflow = 'visible';
                list.style.maxHeight = 'none';
                list.style.height = 'auto';
                
                // Видаляємо псевдоелементи з текстом про прокрутку
                const style = document.createElement('style');
                style.textContent = `
                    .word-list::after,
                    .word-list::before,
                    .word-column::after,
                    .word-column::before {
                        content: none !important;
                        display: none !important;
                    }
                `;
                document.head.appendChild(style);
                
                console.log('[WordMatchingFix] Список слів оптимізовано');
            });
            
            // Видаляємо всі тексти про прокрутку
            const scrollTexts = container.querySelectorAll('*');
            scrollTexts.forEach(element => {
                if (element.textContent && element.textContent.includes('Прокрутите для больше слов')) {
                    element.style.display = 'none';
                    console.log('[WordMatchingFix] Приховано текст про прокрутку');
                }
            });
        });
        
        // Адаптивність для різних екранів
        const applyResponsiveStyles = () => {
            const width = window.innerWidth;
            
            containers.forEach(container => {
                const wordColumns = container.querySelector('.word-columns');
                if (!wordColumns) return;
                
                if (width >= 768 && width <= 1024) {
                    // Планшети
                    wordColumns.style.minHeight = '480px';
                    console.log('[WordMatchingFix] Застосовано стилі для планшета');
                } else if (width < 768) {
                    // Мобільні
                    wordColumns.style.gridTemplateColumns = '1fr';
                    wordColumns.style.minHeight = 'auto';
                    
                    const lists = wordColumns.querySelectorAll('.word-list');
                    lists.forEach(list => {
                        list.style.maxHeight = '300px';
                        list.style.overflowY = 'auto';
                    });
                    console.log('[WordMatchingFix] Застосовано стилі для мобільного');
                } else {
                    // Десктоп
                    wordColumns.style.minHeight = '550px';
                    console.log('[WordMatchingFix] Застосовано стилі для десктопа');
                }
            });
        };
        
        // Застосовуємо адаптивні стилі
        applyResponsiveStyles();
        
        // Слухаємо зміну розміру вікна
        window.addEventListener('resize', applyResponsiveStyles);
    }
    
    // Функція для очікування завантаження елементів
    function waitForElements() {
        const checkInterval = setInterval(() => {
            const containers = document.querySelectorAll('.word-selection-container, .word-selection-host');
            if (containers.length > 0) {
                clearInterval(checkInterval);
                console.log('[WordMatchingFix] Знайдено контейнери, застосовуємо фікс');
                applyWordMatchingFix();
            }
        }, 500);
        
        // Зупиняємо перевірку через 10 секунд
        setTimeout(() => clearInterval(checkInterval), 10000);
    }
    
    // Застосовуємо фікс при завантаженні сторінки
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForElements);
    } else {
        waitForElements();
    }
    
    // Також слухаємо кліки на toggle кнопки упражнень
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList && e.target.classList.contains('exercise-toggle')) {
            setTimeout(applyWordMatchingFix, 100);
        }
    });
    
    // Експортуємо функцію для ручного виклику
    window.applyWordMatchingFix = applyWordMatchingFix;
    
    console.log('[WordMatchingFix] Скрипт завантажено і готовий до роботи');
})();
