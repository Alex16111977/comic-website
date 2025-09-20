import { Timeline } from './timeline.js';

export class ProgressTracker {
    constructor(options = {}) {
        this.timeline = options.timeline || new Timeline();
        this.fill = null;
        this.textElement = null;
        this.prevButton = null;
        this.nextButton = null;
    }

    init() {
        this.fill = document.querySelector('.journey-progress .progress-fill');
        this.textElement = document.querySelector('.journey-progress .progress-text');
        this.prevButton = document.querySelector('.prev-btn');
        this.nextButton = document.querySelector('.next-btn');
        this.timeline.init();
    }

    update({ index = 0, total = 1, description = '' }) {
        const safeTotal = total <= 0 ? 1 : total;
        const percent = ((index + 1) / safeTotal) * 100;
        if (this.fill) this.fill.style.width = `${percent}%`;
        if (this.textElement) this.textElement.textContent = description || '';
        this.timeline.update(percent);
        this.updateButtons(index, total);
    }

    updateButtons(index, total) {
        const lastIndex = Math.max(0, total - 1);
        if (this.prevButton) {
            const disabled = index <= 0;
            this.prevButton.disabled = disabled;
            this.prevButton.style.opacity = disabled ? '0.5' : '1';
            this.prevButton.style.cursor = disabled ? 'not-allowed' : 'pointer';
        }
        if (this.nextButton) {
            const disabled = index >= lastIndex;
            this.nextButton.disabled = disabled;
            this.nextButton.style.opacity = disabled ? '0.5' : '1';
            this.nextButton.style.cursor = disabled ? 'not-allowed' : 'pointer';
        }
    }

    getPrevButton() {
        return this.prevButton;
    }

    getNextButton() {
        return this.nextButton;
    }
}
