import { JourneyApp } from './pages/journey.js';

export function initializeJourney() {
    const app = new JourneyApp();
    app.init();
    return app;
}

if (typeof window !== 'undefined') {
    window.initializeJourney = initializeJourney;
}
