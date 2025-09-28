#!/usr/bin/env python
"""
Генератор кольорової мнемотехніки для німецьких артиклів
Версія: 1.0
"""
import json
from pathlib import Path
from typing import Dict, List, Optional

class MnemonicsGenerator:
    """Генератор кольорової мнемотехніки для німецьких артиклів"""
    
    # Кольорова схема для артиклів
    GENDER_COLORS = {
        'der': {
            'primary': '#2B6CB0',    # Синій
            'hover': '#2C5282',      # Темно-синій
            'bg': '#EBF4FF',         # Пастельно-синій
            'light': '#C3DAFE',      # Світло-синій
            'icon': '♂',             # Символ чоловічого роду
            'label': 'чоловічий',
            'name': 'der'
        },
        'die': {
            'primary': '#C53030',    # Червоний  
            'hover': '#9B2C2C',      # Темно-червоний
            'bg': '#FFE5E5',         # Пастельно-червоний
            'light': '#FED7D7',      # Світло-червоний
            'icon': '♀',             # Символ жіночого роду
            'label': 'жіночий',
            'name': 'die'
        },
        'das': {
            'primary': '#D69E2E',    # Золотий
            'hover': '#B7791F',      # Темно-золотий
            'bg': '#FFF9DB',         # Пастельно-жовтий
            'light': '#FEEBC8',      # Світло-жовтий
            'icon': '⚪',            # Символ середнього роду
            'label': 'середній',
            'name': 'das'
        }
    }
    
    def __init__(self, config):
        """Ініціалізація генератора"""
        self.config = config
        self.base_dir = Path(config.BASE_DIR)
        
    def extract_article(self, german_word: str) -> str:
        """Витягти артикль з німецького слова"""
        for article in ['der', 'die', 'das']:
            if german_word.lower().startswith(f"{article} "):
                return article
        return None
    
    def generate_css(self) -> str:
        """Генерація CSS стилів для мнемотехніки"""
        css = """
/* ========================================
   КОЛЬОРОВА МНЕМОТЕХНІКА ДЛЯ АРТИКЛІВ
   ======================================== */

/* CSS змінні для кольорів */
:root {
    /* Der - чоловічий */
    --der-primary: #2B6CB0;
    --der-hover: #2C5282;
    --der-bg: #EBF4FF;
    --der-light: #C3DAFE;
    
    /* Die - жіночий */
    --die-primary: #C53030;
    --die-hover: #9B2C2C;
    --die-bg: #FFE5E5;
    --die-light: #FED7D7;
    
    /* Das - середній */
    --das-primary: #D69E2E;
    --das-hover: #B7791F;
    --das-bg: #FFF9DB;
    --das-light: #FEEBC8;
}

/* Легенда артиклів */
.articles-legend {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding: 1.5rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 500;
}

.legend-item.legend-der {
    background: var(--der-bg);
    color: var(--der-primary);
}

.legend-item.legend-die {
    background: var(--die-bg);
    color: var(--die-primary);
}

.legend-item.legend-das {
    background: var(--das-bg);
    color: var(--das-primary);
}

.legend-icon {
    font-size: 1.25rem;
}

/* Картки словника з кольоровою кодировкою */
.vocabulary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    padding: 1rem;
}

.vocab-card {
    position: relative;
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.vocab-card.is-der {
    background: linear-gradient(135deg, var(--der-bg) 0%, white 100%);
    border-color: var(--der-primary);
}

.vocab-card.is-die {
    background: linear-gradient(135deg, var(--die-bg) 0%, white 100%);
    border-color: var(--die-primary);
}

.vocab-card.is-das {
    background: linear-gradient(135deg, var(--das-bg) 0%, white 100%);
    border-color: var(--das-primary);
}

.vocab-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.vocab-card.is-der:hover {
    background: linear-gradient(135deg, var(--der-bg) 0%, var(--der-light) 100%);
}

.vocab-card.is-die:hover {
    background: linear-gradient(135deg, var(--die-bg) 0%, var(--die-light) 100%);
}

.vocab-card.is-das:hover {
    background: linear-gradient(135deg, var(--das-bg) 0%, var(--das-light) 100%);
}

/* Заголовок картки з артиклем */
.vocab-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.article-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
}

.article-chip.der {
    background: var(--der-primary);
}

.article-chip.die {
    background: var(--die-primary);
}

.article-chip.das {
    background: var(--das-primary);
}

.article-icon {
    font-size: 1rem;
}

/* Слово в картці */
.vocab-word {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2D3748;
}

.vocab-translation {
    color: #718096;
    font-size: 1.125rem;
    margin-top: 0.5rem;
}

.vocab-transcription {
    color: #A0AEC0;
    font-size: 0.875rem;
    font-style: italic;
    margin-top: 0.25rem;
}

/* Упражнение на артикли */
.articles-quiz {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin: 2rem 0;
}

.quiz-header {
    text-align: center;
    margin-bottom: 2rem;
}

.quiz-title {
    font-size: 2rem;
    font-weight: 700;
    color: #2D3748;
    margin-bottom: 0.5rem;
}

.quiz-description {
    color: #718096;
    font-size: 1.125rem;
}

/* Прогрес-бар */
.quiz-progress {
    max-width: 500px;
    margin: 2rem auto;
}

.progress-count {
    display: flex;
    justify-content: center;
    font-size: 1.125rem;
    color: #4A5568;
    margin-bottom: 0.5rem;
}

.progress-count strong {
    color: #38A169;
    font-size: 1.5rem;
    margin: 0 0.25rem;
}

.progress-bar {
    width: 100%;
    height: 12px;
    background: #E2E8F0;
    border-radius: 6px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #805AD5 0%, #D53F8C 100%);
    transition: width 0.5s ease;
    border-radius: 6px;
}

/* Сітка питань */
.quiz-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.quiz-item {
    background: #F7FAFC;
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}

.quiz-item.item-solved {
    background: linear-gradient(135deg, rgba(56,161,105,0.12) 0%, rgba(72,187,120,0.18) 100%);
    pointer-events: none;
    opacity: 0.8;
}

.quiz-word {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2D3748;
    text-align: center;
    margin-bottom: 0.5rem;
}

.quiz-translation {
    color: #718096;
    text-align: center;
    margin-bottom: 1rem;
}

/* Кнопки артиклів */
.article-buttons {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
}

.article-btn {
    padding: 0.75rem 1.5rem;
    border: 2px solid currentColor;
    border-radius: 10px;
    background: white;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
}

.article-btn.der {
    color: var(--der-primary);
    border-color: var(--der-primary);
}

.article-btn.die {
    color: var(--die-primary);
    border-color: var(--die-primary);
}

.article-btn.das {
    color: var(--das-primary);
    border-color: var(--das-primary);
}

.article-btn:hover:not(:disabled) {
    background: currentColor;
    color: white;
    transform: scale(1.05);
}

.article-btn.der:hover {
    background: var(--der-primary);
}

.article-btn.die:hover {
    background: var(--die-primary);
}

.article-btn.das:hover {
    background: var(--das-primary);
}

/* Стани кнопок */
.article-btn.is-correct {
    background: linear-gradient(135deg, #48BB78 0%, #38A169 100%);
    color: white;
    border-color: #38A169;
    animation: correctPulse 0.5s ease;
}

.article-btn.is-wrong {
    background: linear-gradient(135deg, #F56565 0%, #E53E3E 100%);
    color: white;
    border-color: #E53E3E;
    animation: shake 0.5s ease;
}

.article-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Анімації */
@keyframes correctPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-4px); }
    75% { transform: translateX(4px); }
}

/* Повідомлення про завершення */
.completion-message {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    text-align: center;
    z-index: 1000;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translate(-50%, -60%);
    }
    to {
        opacity: 1;
        transform: translate(-50%, -50%);
    }
}

/* Адаптивність */
@media (max-width: 768px) {
    .articles-legend {
        flex-direction: column;
        gap: 1rem;
    }
    
    .vocabulary-grid {
        grid-template-columns: 1fr;
    }
    
    .quiz-grid {
        grid-template-columns: 1fr;
    }
    
    .article-buttons {
        flex-direction: column;
        width: 100%;
    }
    
    .article-btn {
        width: 100%;
    }
}
"""
        return css
    
    def generate_vocabulary_section(self, character_data: Dict) -> str:
        """Генерація секції словника з кольоровою кодировкою"""
        html = """
<section class="vocabulary-section">
    <h2 class="section-title">📚 Словник з кольоровою мнемотехнікою</h2>
    
    <!-- Легенда артиклів -->
    <div class="articles-legend">
        <div class="legend-item legend-der">
            <span class="legend-icon">♂</span>
            <span>der — чоловічий</span>
        </div>
        <div class="legend-item legend-die">
            <span class="legend-icon">♀</span>
            <span>die — жіночий</span>
        </div>
        <div class="legend-item legend-das">
            <span class="legend-icon">⚪</span>
            <span>das — середній</span>
        </div>
    </div>
    
    <!-- Сітка слів -->
    <div class="vocabulary-grid">
"""
        
        # Збираємо всі слова з усіх фаз
        all_words = []
        for phase in character_data.get('journey_phases', []):
            for word in phase.get('vocabulary', []):
                all_words.append(word)
        
        # Генеруємо картки для кожного слова
        for word in all_words:
            german = word['german']
            article = self.extract_article(german)
            
            if article and article in self.GENDER_COLORS:
                color_data = self.GENDER_COLORS[article]
                word_only = german.replace(f"{article} ", "")
                
                html += f"""
        <div class="vocab-card is-{article}" data-article="{article}">
            <div class="vocab-header">
                <span class="article-chip {article}">
                    <span class="article-icon">{color_data['icon']}</span>
                    <span>{article}</span>
                </span>
                <div class="vocab-word">{word_only}</div>
            </div>
            <div class="vocab-translation">{word['russian']}</div>
            <div class="vocab-transcription">{word['transcription']}</div>
        </div>
"""
        
        html += """
    </div>
</section>
"""
        return html
    
    def generate_articles_quiz(self, character_data: Dict) -> str:
        """Генерація інтерактивної вправи на артиклі"""
        html = """
<section class="articles-quiz" data-quiz="articles">
    <div class="quiz-header">
        <h2 class="quiz-title">🎯 Вправа: Артиклі та рід</h2>
        <p class="quiz-description">Виберіть правильний артикль для іменників з уроку</p>
    </div>
    
    <!-- Прогрес -->
    <div class="quiz-progress">
        <div class="progress-count">
            <strong>0</strong>/<span class="total">0</span> правильних
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: 0%"></div>
        </div>
    </div>
    
    <!-- Питання -->
    <div class="quiz-grid">
"""
        
        # Збираємо слова для вправи (максимум 18)
        quiz_words = []
        for phase in character_data.get('journey_phases', []):
            for word in phase.get('vocabulary', []):
                german = word['german']
                article = self.extract_article(german)
                if article:
                    word_only = german.replace(f"{article} ", "")
                    quiz_words.append({
                        'word': word_only,
                        'article': article,
                        'translation': word['russian']
                    })
                    if len(quiz_words) >= 18:
                        break
            if len(quiz_words) >= 18:
                break
        
        # Генеруємо картки питань
        for item in quiz_words:
            html += f"""
        <div class="quiz-item" data-correct="{item['article']}">
            <div class="quiz-word">{item['word']}</div>
            <div class="quiz-translation">{item['translation']}</div>
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
        </div>
"""
        
        html += """
    </div>
</section>
"""
        return html
    
    def generate_javascript(self) -> str:
        """Генерація JavaScript для інтерактивності"""
        js = """
// ========================================
// МНЕМОТЕХНІКА: ІНТЕРАКТИВНІСТЬ
// ========================================

(function() {
    'use strict';
    
    // Ініціалізація вправи на артиклі
    function initArticlesQuiz() {
        const quiz = document.querySelector('.articles-quiz');
        if (!quiz) return;
        
        const items = quiz.querySelectorAll('.quiz-item');
        const totalElement = quiz.querySelector('.total');
        const progressCount = quiz.querySelector('.progress-count strong');
        const progressFill = quiz.querySelector('.progress-fill');
        
        let correctCount = 0;
        const totalCount = items.length;
        
        // Встановлюємо загальну кількість
        if (totalElement) {
            totalElement.textContent = totalCount;
        }
        
        // Обробник для кожного питання
        items.forEach(item => {
            const buttons = item.querySelectorAll('.article-btn');
            const correctArticle = item.dataset.correct;
            let isAnswered = false;
            
            buttons.forEach(button => {
                button.addEventListener('click', function() {
                    if (isAnswered) return;
                    
                    const selectedArticle = button.dataset.article;
                    
                    if (selectedArticle === correctArticle) {
                        // Правильна відповідь
                        button.classList.add('is-correct');
                        item.classList.add('item-solved');
                        isAnswered = true;
                        
                        // Вимикаємо всі кнопки
                        buttons.forEach(btn => {
                            btn.disabled = true;
                        });
                        
                        // Оновлюємо прогрес
                        correctCount++;
                        updateProgress(correctCount, totalCount);
                        
                        // Перевірка завершення
                        if (correctCount === totalCount) {
                            setTimeout(showCompletionMessage, 500);
                        }
                    } else {
                        // Неправильна відповідь
                        button.classList.add('is-wrong');
                        setTimeout(() => {
                            button.classList.remove('is-wrong');
                        }, 500);
                    }
                });
            });
        });
        
        function updateProgress(correct, total) {
            const percentage = (correct / total) * 100;
            
            if (progressCount) {
                progressCount.textContent = correct;
            }
            
            if (progressFill) {
                progressFill.style.width = percentage + '%';
            }
        }
        
        function showCompletionMessage() {
            const message = document.createElement('div');
            message.className = 'completion-message';
            message.innerHTML = `
                <h2>🎉 Відмінно!</h2>
                <p>Ви правильно визначили всі артиклі!</p>
                <p>Правильних відповідей: ${correctCount}/${totalCount}</p>
            `;
            document.body.appendChild(message);
            
            setTimeout(() => {
                message.remove();
            }, 3000);
        }
    }
    
    // Запускаємо при завантаженні
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initArticlesQuiz);
    } else {
        initArticlesQuiz();
    }
    
    // Експортуємо для використання в інших модулях
    window.MnemonicQuiz = {
        init: initArticlesQuiz
    };
})();
"""
        return js
