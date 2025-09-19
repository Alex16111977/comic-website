"""
Тестирование мобильной совместимости упражнений
"""
import json
from pathlib import Path

# Создаем тестовую HTML страницу для проверки на мобильных устройствах
html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <title>Тест мобильной версии - King Lear</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #2d3748;
            font-size: 1.8em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .device-info {
            background: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            font-size: 0.9em;
            color: #4a5568;
        }
        
        .exercise-section {
            background: linear-gradient(135deg, #fff9e6 0%, #fff4d6 100%);
            border: 2px solid #f6ad55;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .exercise-title {
            color: #d97706;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .exercise-text {
            color: #4a5568;
            font-size: 1.05em;
            line-height: 1.8;
        }
        
        .blank {
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px solid #f6ad55;
            margin: 0 4px;
            padding: 2px 6px;
            color: #a0aec0;
            font-style: italic;
            transition: all 0.3s ease;
        }
        
        .show-answer-btn {
            background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            color: white;
            border: none;
            padding: 18px 36px;
            border-radius: 12px;
            font-size: 1.15em;
            font-weight: 600;
            cursor: pointer;
            margin: 20px auto;
            display: block;
            width: 90%;
            max-width: 300px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
            /* Mobile optimizations */
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
            min-height: 56px;
        }
        
        .show-answer-btn:active {
            transform: scale(0.98);
            opacity: 0.9;
            box-shadow: 0 2px 8px rgba(237, 137, 54, 0.3);
        }
        
        .test-info {
            background: #e6fffa;
            border: 1px solid #4fd1c5;
            padding: 15px;
            border-radius: 10px;
            margin-top: 30px;
            color: #234e52;
        }
        
        .test-info h3 {
            margin-bottom: 10px;
            color: #065666;
        }
        
        .test-info ul {
            margin-left: 20px;
        }
        
        .test-info li {
            margin: 5px 0;
        }
        
        @media (hover: none) and (pointer: coarse) {
            .show-answer-btn {
                background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
            }
        }
        
        /* iOS specific */
        @supports (-webkit-touch-callout: none) {
            .show-answer-btn {
                -webkit-appearance: none;
                appearance: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Тест мобильной версии</h1>
        
        <div class="device-info">
            <strong>Информация об устройстве:</strong>
            <div id="deviceInfo"></div>
        </div>
        
        <div class="exercise-section">
            <h2 class="exercise-title">📝 Тестовое упражнение</h2>
            <div class="exercise-text">
                Великолепный <span class="blank" data-answer="PRÄCHTIGER" data-hint="великолепный">_______ (великолепный)</span> 
                тронный зал. Король восседает на <span class="blank" data-answer="THRON" data-hint="троне">_______ (троне)</span>, 
                его <span class="blank" data-answer="KRONE" data-hint="корона">_______ (корона)</span> сверкает в свете факелов.
            </div>
            <button class="show-answer-btn" type="button" onclick="toggleAnswers(this)">
                Показать ответы
            </button>
        </div>
        
        <div class="test-info">
            <h3>✅ Протестируйте функциональность:</h3>
            <ul>
                <li>Нажмите кнопку "Показать ответы"</li>
                <li>Проверьте, что немецкие слова появляются</li>
                <li>Нажмите "Скрыть ответы"</li>
                <li>Убедитесь, что кнопка реагирует на касание</li>
                <li>Проверьте отсутствие двойных кликов</li>
                <li>Проверьте отсутствие масштабирования при двойном тапе</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Device detection
        function getDeviceInfo() {
            const info = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                touchSupport: 'ontouchstart' in window,
                screenWidth: screen.width,
                screenHeight: screen.height,
                devicePixelRatio: window.devicePixelRatio
            };
            
            let deviceType = 'Desktop';
            if (/iPhone|iPad|iPod/.test(info.userAgent)) {
                deviceType = 'iOS Device';
            } else if (/Android/.test(info.userAgent)) {
                deviceType = 'Android Device';
            } else if (info.touchSupport) {
                deviceType = 'Touch Device';
            }
            
            return `
                <p>Тип: <strong>${deviceType}</strong></p>
                <p>Экран: ${info.screenWidth}x${info.screenHeight} (DPR: ${info.devicePixelRatio})</p>
                <p>Touch: ${info.touchSupport ? '✅ Поддерживается' : '❌ Не поддерживается'}</p>
            `;
        }
        
        // Display device info
        document.getElementById('deviceInfo').innerHTML = getDeviceInfo();
        
        // Toggle answers function
        function toggleAnswers(button) {
            // Prevent double tap
            if (button.dataset.processing === 'true') return;
            button.dataset.processing = 'true';
            
            const exerciseSection = button.closest('.exercise-section');
            const blanks = exerciseSection.querySelectorAll('.blank');
            
            if (button.textContent.trim() === 'Показать ответы') {
                blanks.forEach(blank => {
                    const answer = blank.getAttribute('data-answer');
                    const hint = blank.getAttribute('data-hint');
                    if (answer && hint) {
                        blank.innerHTML = answer + ' (' + hint + ')';
                        blank.style.color = '#d97706';
                        blank.style.fontWeight = '600';
                        blank.style.fontStyle = 'normal';
                        blank.style.borderBottomColor = '#22c55e';
                    }
                });
                button.textContent = 'Скрыть ответы';
                button.style.background = 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)';
            } else {
                blanks.forEach(blank => {
                    const hint = blank.getAttribute('data-hint');
                    if (hint) {
                        blank.innerHTML = '_______ (' + hint + ')';
                        blank.style.color = '#a0aec0';
                        blank.style.fontWeight = 'normal';
                        blank.style.fontStyle = 'italic';
                        blank.style.borderBottomColor = '#f6ad55';
                    }
                });
                button.textContent = 'Показать ответы';
                button.style.background = 'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)';
            }
            
            // Reset processing flag
            setTimeout(() => {
                button.dataset.processing = 'false';
            }, 300);
            
            // Log for debugging
            console.log('Button clicked, answers toggled');
        }
        
        // Add touch event listeners
        document.addEventListener('DOMContentLoaded', function() {
            const button = document.querySelector('.show-answer-btn');
            
            // Prevent iOS double-tap zoom
            let lastTouchTime = 0;
            button.addEventListener('touchstart', function(e) {
                const currentTime = new Date().getTime();
                const tapLength = currentTime - lastTouchTime;
                if (tapLength < 500 && tapLength > 0) {
                    e.preventDefault();
                }
                lastTouchTime = currentTime;
            });
            
            // Add visual feedback for touch
            button.addEventListener('touchstart', function() {
                this.style.opacity = '0.8';
            });
            
            button.addEventListener('touchend', function() {
                this.style.opacity = '1';
            });
            
            console.log('Mobile test page loaded successfully');
        });
    </script>
</body>
</html>"""

# Сохраняем тестовую страницу
output_path = Path(r'F:\AiKlientBank\KingLearComic\output\mobile_test.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[OK] Создана тестовая страница: {output_path}")
print("\n[ИНСТРУКЦИЯ ДЛЯ ТЕСТИРОВАНИЯ]")
print("=" * 60)
print("1. Откройте на мобильном устройстве:")
print(f"   file:///{output_path}")
print("\n2. Или запустите локальный сервер:")
print("   python -m http.server 8000")
print("   И откройте: http://[ваш-ip]:8000/output/mobile_test.html")
print("\n3. Протестируйте на:")
print("   - iPhone (Safari)")
print("   - iPad (Safari)")
print("   - Android телефон (Chrome)")
print("   - Android планшет (Chrome)")
print("\n4. Проверьте:")
print("   ✓ Кнопка реагирует на первое касание")
print("   ✓ Нет двойных кликов")
print("   ✓ Нет масштабирования при двойном тапе")
print("   ✓ Ответы показываются/скрываются корректно")
print("   ✓ Кнопка достаточно большая для пальца")
print("=" * 60)
