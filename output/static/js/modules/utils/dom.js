const DEFAULT_SCOPE = typeof document !== 'undefined' ? document : null;

export function qs(selector, scope = DEFAULT_SCOPE) {
    if (!scope) return null;
    return scope.querySelector(selector);
}

export function qsa(selector, scope = DEFAULT_SCOPE) {
    if (!scope) return [];
    return Array.from(scope.querySelectorAll(selector));
}

export function clearChildren(element) {
    if (!(element instanceof Element)) {
        return;
    }
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

export function setText(element, value) {
    if (!(element instanceof Element)) {
        return;
    }
    element.textContent = value != null ? String(value) : '';
}

export function toggleClass(element, className, force) {
    if (!(element instanceof Element)) {
        return;
    }
    if (typeof force === 'boolean') {
        element.classList.toggle(className, force);
        return;
    }
    element.classList.toggle(className);
}

export function calculateExpandedExerciseContentHeight(content) {
    if (!(content instanceof HTMLElement)) {
        return 0;
    }

    const selectionContainer = content.querySelector('.word-selection-container');
    if (selectionContainer instanceof HTMLElement) {
        const contentStyles = window.getComputedStyle(content);
        const paddingTop = parseFloat(contentStyles.paddingTop) || 0;
        const paddingBottom = parseFloat(contentStyles.paddingBottom) || 0;

        const containerStyles = window.getComputedStyle(selectionContainer);
        const marginTop = parseFloat(containerStyles.marginTop) || 0;
        const marginBottom = parseFloat(containerStyles.marginBottom) || 0;
        const selectionHeight = selectionContainer.offsetHeight + marginTop + marginBottom;
        const baseHeight = content.scrollHeight;

        return Math.ceil(Math.max(baseHeight, selectionHeight + paddingTop + paddingBottom + 40));
    }

    return Math.ceil(content.scrollHeight);
}

export function updateWordColumnScrollIndicators(context = DEFAULT_SCOPE) {
    if (!context) {
        return;
    }
    const scope = context instanceof Document ? context : DEFAULT_SCOPE;
    const root = context instanceof HTMLElement || context instanceof Document ? context : scope;
    if (!root) {
        return;
    }
    const columns = qsa('.word-selection-container .word-column', root);
    columns.forEach(column => {
        if (!(column instanceof HTMLElement)) {
            return;
        }
        const hasOverflow = column.scrollHeight > column.clientHeight + 1;
        const reachedBottom = column.scrollTop + column.clientHeight >= column.scrollHeight - 1;
        column.classList.toggle('has-scroll', hasOverflow && !reachedBottom);
    });
}

export function refreshActiveExerciseContentHeight() {
    const activeToggle = qs('.exercise-toggle.active');
    if (!activeToggle) {
        return;
    }

    const content = activeToggle.nextElementSibling;
    if (!(content instanceof HTMLElement) || content.classList.contains('collapsed')) {
        return;
    }

    const previousTransition = content.style.transition;
    content.style.transition = 'none';
    content.style.maxHeight = 'none';
    const newHeight = calculateExpandedExerciseContentHeight(content);

    requestAnimationFrame(() => {
        content.style.transition = previousTransition || '';
        content.style.maxHeight = `${newHeight}px`;
        updateWordColumnScrollIndicators(content);
    });
}

export function disableTransitionTemporarily(element, callback) {
    if (!(element instanceof HTMLElement)) {
        return;
    }
    const previousTransition = element.style.transition;
    element.style.transition = 'none';
    try {
        callback();
    } finally {
        requestAnimationFrame(() => {
            element.style.transition = previousTransition || '';
        });
    }
}
