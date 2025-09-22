(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", () => {
        initQuiz();
        initMatchGame();
        initTypingTask();
    });

    function initQuiz() {
        const quiz = document.querySelector('[data-component="quiz"]');
        if (!quiz) return;

        const options = Array.from(quiz.querySelectorAll('.quiz-option'));
        const feedback = quiz.querySelector('[data-role="quiz-feedback"]');
        let solved = false;

        options.forEach(option => {
            option.addEventListener('click', () => {
                if (solved) return;

                const isCorrect = option.dataset.correct === 'true';
                options.forEach(btn => btn.removeAttribute('data-state'));

                if (isCorrect) {
                    option.dataset.state = 'correct';
                    setFeedback(feedback, 'Отлично! Это правильный перевод.', true);
                    solved = true;
                } else {
                    option.dataset.state = 'incorrect';
                    setFeedback(feedback, 'Попробуйте ещё раз. Подумайте о примере.', false);
                }
            });
        });
    }

    function initMatchGame() {
        const match = document.querySelector('[data-component="match"]');
        if (!match) return;

        const tokens = Array.from(match.querySelectorAll('.match-token'));
        const dropzones = Array.from(match.querySelectorAll('.match-dropzone'));
        const feedback = match.querySelector('[data-role="match-feedback"]');
        let placedCount = 0;

        tokens.forEach(token => {
            token.addEventListener('dragstart', event => {
                if (token.dataset.state === 'placed') {
                    event.preventDefault();
                    return;
                }
                event.dataTransfer.effectAllowed = 'move';
                event.dataTransfer.setData('text/plain', token.dataset.key);
                token.classList.add('dragging');
            });

            token.addEventListener('dragend', () => {
                token.classList.remove('dragging');
            });
        });

        dropzones.forEach(zone => {
            zone.addEventListener('dragover', event => {
                event.preventDefault();
                zone.dataset.active = 'true';
            });

            zone.addEventListener('dragleave', () => {
                zone.dataset.active = 'false';
            });

            zone.addEventListener('drop', event => {
                event.preventDefault();
                const key = event.dataTransfer.getData('text/plain');
                zone.dataset.active = 'false';

                const draggedToken = tokens.find(token => token.classList.contains('dragging'));
                if (!draggedToken) return;

                if (zone.dataset.key === key) {
                    zone.textContent = draggedToken.textContent;
                    zone.dataset.filled = 'true';
                    draggedToken.dataset.state = 'placed';
                    draggedToken.setAttribute('draggable', 'false');
                    draggedToken.classList.remove('dragging');
                    draggedToken.classList.add('matched');
                    setFeedback(feedback, 'Есть совпадение! Так держать.', true);
                    placedCount += 1;

                    if (placedCount === dropzones.length) {
                        setFeedback(feedback, 'Карточка собрана полностью! 🎉', true);
                    }
                } else {
                    setFeedback(feedback, 'Это другое свойство. Попробуйте ещё.', false);
                }
            });
        });
    }

    function initTypingTask() {
        const typing = document.querySelector('[data-component="typing"]');
        if (!typing) return;

        const input = typing.querySelector('.typing-input');
        const checkButton = typing.querySelector('.typing-check');
        const hintButton = typing.querySelector('.typing-hint');
        const feedback = typing.querySelector('[data-role="typing-feedback"]');
        const correctAnswer = (typing.dataset.answer || '').trim();

        if (!input || !checkButton) return;

        const handleCheck = () => {
            const userAnswer = (input.value || '').trim().toUpperCase();
            if (!userAnswer) {
                setFeedback(feedback, 'Введите слово, прежде чем проверять ответ.', false);
                return;
            }

            if (userAnswer === correctAnswer) {
                setFeedback(feedback, 'Правильно! Слово закреплено.', true);
                input.setAttribute('disabled', 'disabled');
                checkButton.setAttribute('disabled', 'disabled');
            } else {
                setFeedback(feedback, 'Пока нет. Обрати внимание на артикль и пример.', false);
            }
        };

        checkButton.addEventListener('click', handleCheck);
        input.addEventListener('keydown', event => {
            if (event.key === 'Enter') {
                event.preventDefault();
                handleCheck();
            }
        });

        if (hintButton) {
            hintButton.addEventListener('click', () => {
                const hint = hintButton.dataset.hint;
                if (hint) {
                    setFeedback(feedback, hint, true);
                }
            });
        }
    }

    function setFeedback(element, message, isSuccess) {
        if (!element) return;
        element.textContent = message;
        element.classList.remove('success', 'error');
        element.classList.add(isSuccess ? 'success' : 'error');
    }
})();
