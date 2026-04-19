import './styles.css';
import gsap from 'gsap';

// Presentation state
let currentSlide = 0;
let slides = [];
let totalSlides = 0;
let isAnimating = false;

// Initialize presentation
function init() {
    slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;

    document.getElementById('totalPages').textContent = totalSlides;

    // Show first slide with GSAP animation
    if (slides.length > 0) {
        const firstSlide = slides[0];
        firstSlide.classList.add('active');

        gsap.fromTo(firstSlide,
            { opacity: 0, x: 100 },
            { opacity: 1, x: 0, duration: 0.6, ease: 'power2.out' }
        );

        updateSlideCounter();
        animateSlideContent(0);
    }
}

// Navigate to specific slide
function goToSlide(index, direction = 'next') {
    if (index < 0 || index >= totalSlides || index === currentSlide || isAnimating) return;

    isAnimating = true;

    const current = slides[currentSlide];
    const next = slides[index];

    // Reset list item animations on current slide
    const currentListItems = current.querySelectorAll('li');
    gsap.set(currentListItems, { opacity: 0 });

    // Create timeline for smooth transition
    const tl = gsap.timeline({
        onComplete: () => {
            current.classList.remove('active', 'prev');
            isAnimating = false;
        }
    });

    // Animate out current slide
    tl.to(current, {
        opacity: 0,
        x: direction === 'next' ? -100 : 100,
        duration: 0.5,
        ease: 'power2.inOut',
        onStart: () => {
            if (direction === 'next') {
                current.classList.add('prev');
            }
        }
    });

    // Prepare and animate in next slide
    next.classList.remove('prev');
    next.classList.add('active');

    gsap.set(next, {
        opacity: 0,
        x: direction === 'next' ? 100 : -100
    });

    tl.to(next, {
        opacity: 1,
        x: 0,
        duration: 0.5,
        ease: 'power2.inOut'
    }, '-=0.3'); // Slight overlap for smoother transition

    currentSlide = index;
    updateSlideCounter();
    animateSlideContent(index);
}

// Go to next slide
function nextSlide() {
    if (currentSlide < totalSlides - 1) {
        goToSlide(currentSlide + 1, 'next');
    }
}

// Go to previous slide
function prevSlide() {
    if (currentSlide > 0) {
        goToSlide(currentSlide - 1, 'prev');
    }
}

// Update slide counter
function updateSlideCounter() {
    const counter = document.getElementById('currentPage');
    gsap.fromTo(counter,
        { scale: 1.3 },
        { scale: 1, duration: 0.3, ease: 'back.out(2)' }
    );
    counter.textContent = currentSlide + 1;

    // Update progress bar
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    gsap.to('.progress-bar', {
        width: `${progress}%`,
        duration: 0.5,
        ease: 'power2.out'
    });
}

// Animate slide content (list items, cards, etc.) with GSAP
function animateSlideContent(index) {
    const slide = slides[index];

    // Animate list items
    const listItems = slide.querySelectorAll('li');
    if (listItems.length > 0) {
        gsap.fromTo(listItems,
            { opacity: 0, x: -20 },
            {
                opacity: 1,
                x: 0,
                duration: 0.4,
                stagger: 0.15,
                ease: 'power2.out',
                delay: 0.3
            }
        );
    }

    // Animate cards
    const cards = slide.querySelectorAll('.card, .stat-card');
    if (cards.length > 0) {
        gsap.fromTo(cards,
            { opacity: 0, y: 30, scale: 0.95 },
            {
                opacity: 1,
                y: 0,
                scale: 1,
                duration: 0.5,
                stagger: 0.1,
                ease: 'back.out(1.5)',
                delay: 0.2
            }
        );
    }

    // Animate timeline items
    const timelineItems = slide.querySelectorAll('.timeline-item, .timeline-item-card');
    if (timelineItems.length > 0) {
        gsap.fromTo(timelineItems,
            { opacity: 0, x: -30 },
            {
                opacity: 1,
                x: 0,
                duration: 0.5,
                stagger: 0.2,
                ease: 'power2.out',
                delay: 0.3
            }
        );
    }

    // Animate headings
    const headings = slide.querySelectorAll('h1, h2, h3');
    if (headings.length > 0) {
        gsap.fromTo(headings,
            { opacity: 0, y: -20 },
            {
                opacity: 1,
                y: 0,
                duration: 0.6,
                stagger: 0.1,
                ease: 'power2.out',
                delay: 0.1
            }
        );
    }

    // Animate process steps
    const processSteps = slide.querySelectorAll('.process-step');
    if (processSteps.length > 0) {
        gsap.fromTo(processSteps,
            { opacity: 0, y: 30 },
            { opacity: 1, y: 0, duration: 0.5, stagger: 0.15, ease: 'power2.out', delay: 0.3 }
        );
    }

    // Animate comparison sides
    const comparisonSides = slide.querySelectorAll('.comparison-side');
    if (comparisonSides.length > 0) {
        gsap.fromTo(comparisonSides[0],
            { opacity: 0, x: -50 },
            { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay: 0.3 }
        );
        gsap.fromTo(comparisonSides[1],
            { opacity: 0, x: 50 },
            { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay: 0.3 }
        );
    }

    // Animate media text container
    const mediaContainer = slide.querySelector('.media-text-container');
    if (mediaContainer) {
        const image = mediaContainer.querySelector('.media-image');
        const content = mediaContainer.querySelector('.media-content');
        if (image) gsap.fromTo(image, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay: 0.3 });
        if (content) gsap.fromTo(content, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out', delay: 0.4 });
    }

    // Animate tags cloud
    const tags = slide.querySelectorAll('.tag-item');
    if (tags.length > 0) {
        gsap.fromTo(tags,
            { opacity: 0, scale: 0.8 },
            { opacity: 1, scale: 1, duration: 0.4, stagger: 0.05, ease: 'back.out(1.5)', delay: 0.3 }
        );
    }

    // Animate team members
    const teamMembers = slide.querySelectorAll('.team-member');
    if (teamMembers.length > 0) {
        gsap.fromTo(teamMembers,
            { opacity: 0, y: 40 },
            { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'power3.out', delay: 0.3 }
        );
    }

    // Animate quote highlight
    const quoteBox = slide.querySelector('.quote-highlight');
    if (quoteBox) {
        gsap.fromTo(quoteBox,
            { opacity: 0, scale: 0.95 },
            { opacity: 1, scale: 1, duration: 0.8, ease: 'power3.out', delay: 0.3 }
        );
    }

    // Animate progress items
    const progressItems = slide.querySelectorAll('.progress-item');
    if (progressItems.length > 0) {
        gsap.fromTo(progressItems,
            { opacity: 0, x: -30 },
            { opacity: 1, x: 0, duration: 0.5, stagger: 0.15, ease: 'power2.out', delay: 0.3 }
        );
        // Animate progress bars
        const progressBars = slide.querySelectorAll('.progress-bar-fill');
        progressBars.forEach((bar, i) => {
            const width = bar.style.width;
            bar.style.width = '0%';
            gsap.to(bar, {
                width: width,
                duration: 1,
                delay: 0.5 + (i * 0.2),
                ease: 'power2.out'
            });
        });
    }
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ':
        case 'PageDown':
            e.preventDefault();
            nextSlide();
            break;
        case 'ArrowLeft':
        case 'ArrowUp':
        case 'PageUp':
            e.preventDefault();
            prevSlide();
            break;
        case 'Home':
            e.preventDefault();
            goToSlide(0);
            break;
        case 'End':
            e.preventDefault();
            goToSlide(totalSlides - 1);
            break;
    }
});

// Touch/swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            nextSlide();
        } else {
            prevSlide();
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
