import { MatchingExercise } from './matching.js';
import { ArticlesExercise } from './articles.js';
import { ContextExercise } from './context.js';

export class WordExercises {
    constructor() {
        this.matching = new MatchingExercise();
        this.articles = new ArticlesExercise();
        this.context = new ContextExercise();
    }

    render(phaseKey, phase) {
        const container = document.querySelector(`[data-matching-container][data-phase="${phaseKey}"]`);
        const pairs = this.buildPairs(phase);
        this.matching.render(container, pairs);
        const vocabulary = window.phaseData ? window.phaseData[phaseKey] : null;
        const articlesContainer = document.querySelector(`[data-articles-container][data-phase="${phaseKey}"]`);
        this.articles.render(articlesContainer, vocabulary);
        const contextContainer = document.querySelector(`[data-context-container][data-phase="${phaseKey}"]`);
        this.context.render(contextContainer, vocabulary);
    }

    buildPairs(phase) {
        const words = Array.isArray(phase?.words) ? phase.words : [];
        return words
            .filter(word => word.word && word.translation)
            .map((word, index) => ({
                id: `word-${index}`,
                prompt: word.word,
                match: word.russian_hint ? `${word.translation} (${word.russian_hint})` : word.translation,
            }));
    }
}
