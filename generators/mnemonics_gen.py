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
            'label': 'мужской',
            'name': 'der'
        },
        'die': {
            'primary': '#C53030',    # Червоний  
            'hover': '#9B2C2C',      # Темно-червоний
            'bg': '#FFE5E5',         # Пастельно-червоний
            'light': '#FED7D7',      # Світло-червоний
            'icon': '♀',             # Символ жіночого роду
            'label': 'женский',
            'name': 'die'
        },
        'das': {
            'primary': '#D69E2E',    # Золотий
            'hover': '#B7791F',      # Темно-золотий
            'bg': '#FFF9DB',         # Пастельно-жовтий
            'light': '#FEEBC8',      # Світло-жовтий
            'icon': '⚪',            # Символ середнього роду
            'label': 'средний',
            'name': 'das'
        }
    }
    
    def __init__(self, config):
        """Ініціалізація генератора"""
        self.config = config
        self.base_dir = Path(config.BASE_DIR)
    
    def get_phase_vocabulary(self, character_data, phase_id):
        """Отримує словник для конкретної фази"""
        for phase in character_data.get('journey_phases', []):
            if phase.get('id') == phase_id:
                return phase.get('vocabulary', [])
        return []
        
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
    background: linear-gradient(135deg, #e3f2fd, #bbdefb) !important;
    border-left: 4px solid #1976d2 !important;
    transition: all 0.3s ease;
}

.vocab-card.is-die {
    background: linear-gradient(135deg, #fce4ec, #f8bbd0) !important;
    border-left: 4px solid #d32f2f !important;
    transition: all 0.3s ease;
}

.vocab-card.is-das {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9) !important;
    border-left: 4px solid #388e3c !important;
    transition: all 0.3s ease;
}

.vocab-card.is-neutral {
    background: linear-gradient(135deg, #edf2f7, #e2e8f0) !important;
    border-left: 4px solid #718096 !important;
    transition: all 0.3s ease;
}

.vocab-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.vocab-card.is-der:hover {
    background: linear-gradient(135deg, #bbdefb, #90caf9) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(25, 118, 210, 0.3);
}

.vocab-card.is-die:hover {
    background: linear-gradient(135deg, #f8bbd0, #f48fb1) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(211, 47, 47, 0.3);
}

.vocab-card.is-das:hover {
    background: linear-gradient(135deg, #c8e6c9, #a5d6a7) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(56, 142, 60, 0.3);
}

.vocab-card.is-neutral:hover {
    background: linear-gradient(135deg, #e2e8f0, #cbd5e0) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(113, 128, 150, 0.3);
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

.article-chip.neutral {
    background: #4a5568;
}

.word-type-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    background: rgba(113, 128, 150, 0.15);
    color: #2d3748;
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
    
    def generate_vocabulary_section(self, character_data: Dict, phase_id: str = None) -> str:
        """Генерація секції словника з кольоровою кодировкою для конкретної фази"""
        html = """
<section class="vocabulary-section">
    <h2 class="section-title">📚 Словарь урока</h2>
    
    <!-- Легенда артиклів -->
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
    
    <!-- Сітка слів -->
    <div class="vocabulary-grid">
"""
        
        # Отримуємо слова конкретної фази
        if phase_id:
            vocabulary = self.get_phase_vocabulary(character_data, phase_id)
        else:
            # Якщо phase_id не вказано - беремо першу фазу
            phases = character_data.get('journey_phases', [])
            vocabulary = phases[0].get('vocabulary', []) if phases else []
        
        # Генеруємо картки для кожного слова
        for word in vocabulary:
            german = word['german']
            article = self.extract_article(german)
            color_data = self.GENDER_COLORS.get(article)

            if color_data:
                card_class = f"is-{article}"
                word_display = german.replace(f"{article} ", "", 1)
                badge_html = ''.join([
                    f'<span class="article-chip {article}">',
                    f'<span class="article-icon">{color_data["icon"]}</span>',
                    f'<span>{article}</span>',
                    '</span>'
                ])
                data_article = article
            else:
                card_class = "is-neutral"
                word_display = german
                neutral_label = word.get('part_of_speech') or word.get('pos') or word.get('type')
                if neutral_label:
                    label_text = neutral_label
                else:
                    label_text = "лексика без артикля"
                badge_html = f'<span class="word-type-chip">{label_text}</span>'
                data_article = ""

            data_article_attr = f" data-article=\"{data_article}\"" if data_article else ""

            html += f"""
        <div class=\"vocab-card {card_class}\" data-word=\"{word_display}\"{data_article_attr}>
            <div class=\"vocab-header\">
                {badge_html}
                <div class=\"vocab-word\">{word_display}</div>
            </div>
            <div class=\"vocab-translation\">{word['russian']}</div>
            <div class=\"vocab-transcription\">{word['transcription']}</div>
        </div>
"""
        
        html += """
    </div>
</section>
"""
        return html
    
    def generate_articles_quiz(self, character_data: Dict, phase_id: str = None) -> str:
        """Генерація інтерактивної вправи на артиклі зі словами з уроку"""
        html = """
<section class="articles-quiz" data-quiz="articles">
    <div class="quiz-header">
        <h3 class="quiz-title">🎯 Артикли и род</h3>
        <p class="quiz-description">Выберите правильный артикль для существительных из урока</p>
    </div>
    
    <!-- Прогрес -->
    <div class="quiz-progress">
        <div class="progress-count">
            <strong>0</strong>/<span class="total">0</span> правильных
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: 0%"></div>
        </div>
    </div>
    
    <!-- Питання -->
    <div class="quiz-grid">
"""
        
        # Збираємо слова з конкретної фази або всіх
        quiz_words = []
        
        if phase_id:
            # Якщо вказана фаза - беремо слова з неї
            vocab = self.get_phase_vocabulary(character_data, phase_id)
            for word in vocab:
                german = word['german']
                article = self.extract_article(german)
                if article:
                    word_only = german.replace(f"{article} ", "")
                    quiz_words.append({
                        'word': word_only,
                        'article': article,
                        'translation': word['russian']
                    })
        else:
            # Інакше беремо слова з усіх фаз (максимум 18)
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
                <h2>🎉 Отлично!</h2>
                <p>Вы правильно определили все артикли!</p>
                <p>Правильных ответов: ${correctCount}/${totalCount}</p>
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
