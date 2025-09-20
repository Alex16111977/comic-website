function clamp(value) {
    if (Number.isNaN(value)) return 0;
    return Math.min(100, Math.max(0, value));
}

export class Timeline {
    constructor() {
        this.line = null;
        this.length = 0;
    }

    init() {
        this.line = document.querySelector('.progress-line');
        if (this.line) {
            const start = clamp(parseFloat(this.line.dataset.startProgress || '0'));
            this.ensureLength();
            this.update(start);
        }
    }

    ensureLength() {
        if (!this.line) {
            this.length = 0;
            return;
        }
        if (this.length) return this.length;
        if (typeof this.line.getTotalLength === 'function') {
            this.length = this.line.getTotalLength();
        }
        if (!this.length && typeof this.line.getBBox === 'function') {
            try {
                const bbox = this.line.getBBox();
                if (bbox && bbox.width) this.length = bbox.width;
            } catch (error) {
                console.warn('[Timeline] Unable to get bounding box length', error);
            }
        }
        if (!this.length) {
            const parent = this.line.parentElement;
            if (parent) {
                const width = parent.getBoundingClientRect().width;
                if (width) this.length = width;
            }
        }
        if (!this.length) this.length = 1;
        return this.length;
    }

    update(percent) {
        if (!this.line) return;
        const length = this.ensureLength();
        this.line.style.strokeDasharray = `${length} ${length}`;
        const clamped = clamp(percent);
        const offset = length - (length * clamped / 100);
        this.line.style.strokeDashoffset = offset;
    }
}
