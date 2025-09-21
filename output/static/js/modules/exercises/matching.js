import { refreshActiveExerciseContentHeight, updateWordColumnScrollIndicators } from '../utils/dom.js';
import { vibrate } from '../utils/animations.js';

function shuffleArray(array) {
    const copy = Array.isArray(array) ? array.slice() : [];
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
}

function createStatusElement(message) {
    const status = document.createElement('div');
    status.className = 'matching-status';
    status.textContent = message;
    return status;
}

export class MatchingExercise {
    render(container, pairs) {
        if (!(container instanceof HTMLElement)) {
            return;
        }
        if (!Array.isArray(pairs) || !pairs.length) {
            container.innerHTML = '<div class="exercise-empty-state">Слова для подбора отсутствуют.</div>';
            return;
        }
        container.innerHTML = '';
        const wrapper = document.createElement('div');
        wrapper.className = 'word-selection-container';
        wrapper.innerHTML = `
            <div class="word-columns">
                <div class="word-column" data-type="prompt">
                    <h4>Немецкие</h4>
                    <div class="word-list prompts"></div>
                </div>
                <div class="word-column" data-type="match">
                    <h4>Русские</h4>
                    <div class="word-list matches"></div>
                </div>
            </div>
        `;
        const status = createStatusElement('Выберите немецкое слово и его русский перевод');
        wrapper.appendChild(status);
        container.appendChild(wrapper);
        const promptsList = wrapper.querySelector('.prompts');
        const matchesList = wrapper.querySelector('.matches');
        const promptCards = pairs.map(pair => ({ label: pair.prompt, pairId: pair.id }));
        const matchCards = pairs.map(pair => ({ label: pair.match, pairId: pair.id }));
        let resolvedPairs = new Set();
        let activePrompt = null;
        let activeMatch = null;

        const updateStatus = message => {
            status.textContent = message;
        };

        const evaluateSelection = () => {
            if (!activePrompt || !activeMatch) {
                return;
            }
            const promptId = activePrompt.dataset.pairId;
            const matchId = activeMatch.dataset.pairId;
            if (promptId === matchId) {
                activePrompt.classList.add('matched');
                activeMatch.classList.add('matched');
                resolvedPairs.add(promptId);
                updateStatus('Правильно! Пара найдена.');
                vibrate(15);
                if (resolvedPairs.size === pairs.length) {
                    updateStatus('Отлично! Все слова подобраны!');
                }
            } else {
                activePrompt.classList.add('mismatch');
                activeMatch.classList.add('mismatch');
                updateStatus('Не совпало. Попробуйте ещё раз.');
                setTimeout(() => {
                    activePrompt.classList.remove('mismatch');
                    activeMatch.classList.remove('mismatch');
                }, 500);
            }
            activePrompt.classList.remove('selected');
            activeMatch.classList.remove('selected');
            activePrompt = null;
            activeMatch = null;
        };

        const toggleCard = (card, type) => {
            if (card.classList.contains('matched')) {
                return;
            }
            if (type === 'prompt') {
                if (activePrompt === card) {
                    card.classList.remove('selected');
                    activePrompt = null;
                    updateStatus('Выберите немецкое слово и его перевод.');
                    return;
                }
                if (activePrompt) {
                    activePrompt.classList.remove('selected');
                }
                activePrompt = card;
            } else {
                if (activeMatch === card) {
                    card.classList.remove('selected');
                    activeMatch = null;
                    updateStatus(activePrompt ? 'Теперь выберите русский перевод.' : 'Выберите немецкое слово.');
                    return;
                }
                if (activeMatch) {
                    activeMatch.classList.remove('selected');
                }
                activeMatch = card;
            }
            card.classList.add('selected');
            if (activePrompt && activeMatch) {
                evaluateSelection();
            } else if (activePrompt) {
                updateStatus('Теперь выберите русский перевод.');
            } else if (activeMatch) {
                updateStatus('Теперь выберите немецкое слово.');
            }
        };

        const appendCards = (list, cardsData, type) => {
            cardsData.forEach(data => {
                const card = document.createElement('button');
                card.className = 'word-item';
                card.type = 'button';
                card.textContent = data.label;
                card.dataset.pairId = data.pairId;
                card.addEventListener('click', () => toggleCard(card, type));
                list.appendChild(card);
            });
        };

        appendCards(promptsList, promptCards, 'prompt');
        appendCards(matchesList, matchCards, 'match');

        const shuffleChildren = list => {
            const children = shuffleArray(Array.from(list.children));
            children.forEach(child => list.appendChild(child));
        };

        shuffleChildren(promptsList);
        shuffleChildren(matchesList);

        wrapper.querySelectorAll('.word-column').forEach(column => {
            column.addEventListener('scroll', () => updateWordColumnScrollIndicators(wrapper));
        });

        updateWordColumnScrollIndicators(wrapper);
        refreshActiveExerciseContentHeight();
    }
}
