export function prefersReducedMotion() {
    if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
        return false;
    }
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function vibrate(pattern = 10) {
    if (prefersReducedMotion()) {
        return;
    }
    if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
        try {
            navigator.vibrate(pattern);
        } catch (error) {
            console.warn('[Animation] Unable to vibrate', error);
        }
    }
}

export function staggeredAnimation(elements, callback, delay = 80) {
    if (!Array.isArray(elements)) {
        return;
    }
    elements.forEach((element, index) => {
        if (!(element instanceof HTMLElement)) {
            return;
        }
        const run = () => callback(element, index);
        if (prefersReducedMotion()) {
            run();
        } else {
            setTimeout(run, index * delay);
        }
    });
}
