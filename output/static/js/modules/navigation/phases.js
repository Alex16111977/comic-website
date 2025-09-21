import { vibrate } from '../utils/animations.js';

export class PhaseNavigator {
    constructor(options) {
        this.vocabulary = options.vocabulary;
        this.display = options.display;
        this.progress = options.progress;
        this.isTouchDevice = Boolean(options.isTouchDevice);
        this.phaseKeys = this.vocabulary.getPhaseKeys();
        this.currentIndex = 0;
        this.isTransitioning = false;
        this.onPhaseChange = typeof options.onPhaseChange === 'function' ? options.onPhaseChange : null;
    }

    init() {
        this.progress.init();
        this.points = Array.from(document.querySelectorAll('.journey-point'));
        this.points.forEach((point, index) => {
            point.addEventListener('click', event => {
                event.preventDefault();
                event.stopPropagation();
                this.goTo(index);
            });
            if (this.isTouchDevice) {
                point.addEventListener('touchstart', () => { point.style.transform = 'scale(0.95)'; });
                point.addEventListener('touchend', () => {
                    setTimeout(() => { point.style.transform = 'scale(1)'; }, 100);
                });
            }
            point.style.cursor = 'pointer';
        });
        this.prevButton = this.progress.getPrevButton();
        this.nextButton = this.progress.getNextButton();
        if (this.prevButton) {
            this.prevButton.addEventListener('click', event => {
                event.preventDefault();
                event.stopPropagation();
                this.goTo(this.currentIndex - 1);
            });
        }
        if (this.nextButton) {
            this.nextButton.addEventListener('click', event => {
                event.preventDefault();
                event.stopPropagation();
                this.goTo(this.currentIndex + 1);
            });
        }
        if (this.isTouchDevice) {
            this.attachSwipeHandlers();
        }
        const initialPhase = this.phaseKeys[0];
        if (initialPhase) {
            this.points[0]?.classList.add('active');
            this.renderPhase(initialPhase, 0);
            this.currentIndex = 0;
        }
    }

    attachSwipeHandlers() {
        let startX = 0;
        let endX = 0;
        document.addEventListener('touchstart', event => {
            startX = event.changedTouches[0].screenX;
        }, false);
        document.addEventListener('touchend', event => {
            endX = event.changedTouches[0].screenX;
            this.handleSwipe(startX, endX);
        }, false);
    }

    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;
        if (Math.abs(diff) <= threshold) return;
        if (diff > 0) {
            if (this.nextButton && !this.nextButton.disabled) this.nextButton.click();
        } else if (this.prevButton && !this.prevButton.disabled) {
            this.prevButton.click();
        }
    }

    goTo(index) {
        if (this.isTransitioning) return;
        const clampedIndex = Math.max(0, Math.min(index, this.phaseKeys.length - 1));
        if (clampedIndex === this.currentIndex) {
            return;
        }
        this.isTransitioning = true;
        this.points.forEach((point, idx) => {
            point.classList.toggle('active', idx === clampedIndex);
        });
        const phaseKey = this.phaseKeys[clampedIndex];
        if (phaseKey) {
            this.renderPhase(phaseKey, clampedIndex);
            vibrate(10);
        }
        this.currentIndex = clampedIndex;
        setTimeout(() => { this.isTransitioning = false; }, 400);
    }

    renderPhase(phaseKey, index) {
        this.display.renderPhase(phaseKey);
        this.progress.update({
            index,
            total: this.phaseKeys.length,
            description: this.vocabulary.getPhase(phaseKey)?.description || '',
        });
        if (this.onPhaseChange) {
            this.onPhaseChange(phaseKey);
        }
    }
}
