"""CSS Generator for Lira Journey style with mobile support"""

class LiraCSSGenerator:
    """Generate CSS in lira-journey style optimized for mobile devices"""
    
    @staticmethod
    def generate():
        """Return complete CSS as string with mobile optimizations"""
        return '''
/* LIRA JOURNEY STYLES - Mobile Optimized */
* { margin: 0; padding: 0; box-sizing: border-box; }

/* Prevent iOS zoom on input focus */
input, select, textarea, button {
    font-size: 16px !important;
}

/* Prevent text selection on mobile */
.no-select {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #333;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.page-header {
    text-align: center;
    color: white;
    margin-bottom: 40px;
    animation: fadeInDown 0.8s ease;
}

.page-header h1 {
    font-size: 3em;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.2em;
    opacity: 0.95;
}

.journey-section {
    background: white;
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
}

.journey-timeline {
    position: relative;
    margin-bottom: 30px;
}

.journey-line {
    position: absolute;
    top: 30px;
    left: 0;
    right: 0;
    z-index: 1;
}

.progress-line {
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    animation: drawLine 2s ease forwards;
    animation-delay: 1s;
}

.journey-points {
    display: flex;
    justify-content: space-between;
    position: relative;
    z-index: 2;
    padding: 0 30px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
}

.journey-point {
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 0.7;
    transform: scale(0.9);
    /* Mobile touch optimizations */
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    user-select: none;
    touch-action: manipulation;
    min-width: 80px;
    padding: 10px 5px;
    position: relative;
}

.journey-point.active {
    opacity: 1;
    transform: scale(1);
}

/* Touch feedback for mobile */
@media (hover: none) and (pointer: coarse) {
    .journey-point {
        min-width: 90px;
    }
    
    .journey-point:active {
        transform: scale(0.95);
        opacity: 0.9;
    }
}

.point-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: white;
    border: 3px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin: 0 auto 10px;
    transition: all 0.3s ease;
}

.journey-point.active .point-circle {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-color: #667eea;
    transform: scale(1.2);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.journey-point h4 {
    font-size: 0.9em;
    margin: 5px 0;
    color: #333;
}

.journey-point p {
    font-size: 0.75em;
    color: #666;
    display: none;
}

.journey-point.active p {
    display: block;
}

.journey-progress {
    margin-top: 20px;
}

.progress-track {
    height: 8px;
    background: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.5s ease;
}

.progress-text {
    text-align: center;
    margin-top: 10px;
    color: #666;
    font-size: 0.9em;
}

.vocabulary-section {
    background: white;
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
}

.vocabulary-section h2 {
    font-size: 2em;
    margin-bottom: 30px;
    text-align: center;
    color: #333;
}

.vocabulary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
    min-height: 200px;
}

.word-card {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    animation: slideIn 0.4s ease;
}

.word-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.word-german {
    font-size: 1.4em;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 8px;
}

.word-translation {
    font-size: 1.1em;
    color: #555;
    margin-bottom: 5px;
}

.word-transcription {
    font-size: 0.9em;
    color: #888;
    font-style: italic;
    margin-bottom: 15px;
}

.word-sentence {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #e0e0e0;
}

.sentence-german {
    font-size: 0.95em;
    color: #444;
    margin-bottom: 5px;
    font-style: italic;
}

.sentence-translation {
    font-size: 0.9em;
    color: #666;
}

.phase-navigation {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
    flex-wrap: wrap;
}

.change-phase-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    /* Mobile optimizations */
    -webkit-tap-highlight-color: transparent;
    -webkit-appearance: none;
    appearance: none;
    touch-action: manipulation;
    -webkit-user-select: none;
    user-select: none;
    min-height: 48px;
    min-width: 160px;
}

.change-phase-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.change-phase-btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.change-phase-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
}

/* Touch device specific button styles */
@media (hover: none) and (pointer: coarse) {
    .change-phase-btn {
        padding: 18px 36px;
        font-size: 1.15em;
        min-height: 56px;
    }
    
    .change-phase-btn:hover {
        transform: none;
    }
    
    .change-phase-btn:active:not(:disabled) {
        transform: scale(0.98);
        opacity: 0.9;
    }
}

.bottom-nav {
    text-align: center;
    margin-top: 40px;
    padding-bottom: 20px;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 1.1em;
    padding: 12px 24px;
    border: 2px solid white;
    border-radius: 8px;
    display: inline-block;
    transition: all 0.3s ease;
    /* Mobile optimizations */
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    min-height: 48px;
}

.nav-link:hover {
    background: white;
    color: #667eea;
}

/* Mobile responsive styles */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .page-header h1 {
        font-size: 2em;
    }
    
    .subtitle {
        font-size: 1em;
    }
    
    .journey-section {
        padding: 20px;
        border-radius: 15px;
    }
    
    .journey-points {
        padding: 0 10px;
        gap: 10px;
    }
    
    .journey-point {
        min-width: 70px;
    }
    
    .point-circle {
        width: 48px;
        height: 48px;
        font-size: 20px;
    }
    
    .journey-point h4 {
        font-size: 0.8em;
    }
    
    .vocabulary-section {
        padding: 20px;
    }
    
    .vocabulary-section h2 {
        font-size: 1.5em;
    }
    
    .vocabulary-grid {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .word-card {
        padding: 15px;
    }
    
    .phase-navigation {
        flex-direction: column;
        align-items: center;
    }
    
    .change-phase-btn {
        width: 90%;
        max-width: 300px;
    }
}

/* Small mobile devices */
@media (max-width: 480px) {
    .journey-points {
        overflow-x: scroll;
        scroll-snap-type: x mandatory;
        scroll-behavior: smooth;
        padding-bottom: 10px;
    }
    
    .journey-point {
        scroll-snap-align: center;
        flex: 0 0 auto;
    }
    
    /* Custom scrollbar for journey points */
    .journey-points::-webkit-scrollbar {
        height: 6px;
    }
    
    .journey-points::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .journey-points::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 3px;
    }
}

/* iOS specific fixes */
@supports (-webkit-touch-callout: none) {
    /* iOS only styles */
    button, .journey-point {
        -webkit-tap-highlight-color: transparent;
    }
    
    .change-phase-btn,
    .show-answer-btn,
    .nav-link {
        -webkit-appearance: none;
        appearance: none;
    }
    
    /* Fix iOS button radius */
    input[type="button"],
    input[type="submit"] {
        border-radius: 0;
    }
}

/* Android specific optimizations */
@media screen and (-webkit-min-device-pixel-ratio: 0) {
    .journey-points {
        -webkit-overflow-scrolling: touch;
    }
}

/* Animations */
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes drawLine {
    to {
        stroke-dashoffset: 0;
    }
}
'''
