/**
 * GSAP Animations for BSMLabs LP Theme
 * 
 * @package BSMLabs_LP
 * @version 1.0.0
 */

(function() {
    'use strict';

    // Wait for GSAP to load
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof gsap !== 'undefined') {
            initGSAPAnimations();
        }
    });

    /**
     * Initialize GSAP Animations
     */
    function initGSAPAnimations() {
        // Register ScrollTrigger plugin
        if (typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
        }

        // Hero section animations
        initHeroAnimations();
        
        // Platform cards animations
        initPlatformAnimations();
        
        // Statistics counter animations
        initCounterAnimations();
        
        // Testimonial animations
        initTestimonialAnimations();
        
        // General scroll animations
        initScrollAnimations();
    }

    /**
     * Hero Section Animations
     */
    function initHeroAnimations() {
        const heroTimeline = gsap.timeline();

        heroTimeline
            .from('.hero-section h1', {
                duration: 1,
                y: 50,
                opacity: 0,
                ease: 'power3.out'
            })
            .from('.hero-section p', {
                duration: 0.8,
                y: 30,
                opacity: 0,
                ease: 'power3.out'
            }, '-=0.5')
            .from('.hero-section .cta-button', {
                duration: 0.6,
                y: 20,
                opacity: 0,
                stagger: 0.2,
                ease: 'power3.out'
            }, '-=0.3');
    }

    /**
     * Platform Cards Animations
     */
    function initPlatformAnimations() {
        gsap.from('.platform-card', {
            duration: 0.8,
            y: 50,
            opacity: 0,
            stagger: 0.2,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: '.platforms-section',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        });

        // Hover animations for platform cards
        document.querySelectorAll('.platform-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                gsap.to(this, {
                    duration: 0.3,
                    y: -10,
                    scale: 1.02,
                    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                    ease: 'power2.out'
                });
            });

            card.addEventListener('mouseleave', function() {
                gsap.to(this, {
                    duration: 0.3,
                    y: 0,
                    scale: 1,
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                    ease: 'power2.out'
                });
            });
        });
    }

    /**
     * Counter Animations
     */
    function initCounterAnimations() {
        document.querySelectorAll('.counter').forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2;

            gsap.to(counter, {
                duration: duration,
                innerHTML: target,
                ease: 'power2.out',
                snap: { innerHTML: 1 },
                scrollTrigger: {
                    trigger: counter,
                    start: 'top 80%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
    }

    /**
     * Testimonial Animations
     */
    function initTestimonialAnimations() {
        gsap.from('.testimonial-card', {
            duration: 0.8,
            y: 30,
            opacity: 0,
            stagger: 0.3,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: '.testimonials-section',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });
    }

    /**
     * General Scroll Animations
     */
    function initScrollAnimations() {
        // Fade in animations for sections
        gsap.utils.toArray('.animate-on-scroll').forEach(element => {
            gsap.from(element, {
                duration: 0.8,
                y: 50,
                opacity: 0,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: element,
                    start: 'top 85%',
                    toggleActions: 'play none none reverse'
                }
            });
        });

        // Parallax effect for hero background
        gsap.to('.hero-bg', {
            yPercent: -50,
            ease: 'none',
            scrollTrigger: {
                trigger: '.hero-section',
                start: 'top bottom',
                end: 'bottom top',
                scrub: true
            }
        });

        // Header background on scroll
        ScrollTrigger.create({
            trigger: 'body',
            start: 'top -80',
            end: 'bottom bottom',
            onEnter: () => {
                gsap.to('.site-header', {
                    duration: 0.3,
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    ease: 'power2.out'
                });
            },
            onLeaveBack: () => {
                gsap.to('.site-header', {
                    duration: 0.3,
                    backgroundColor: 'rgba(255, 255, 255, 1)',
                    backdropFilter: 'blur(0px)',
                    ease: 'power2.out'
                });
            }
        });
    }

    /**
     * Button Hover Animations
     */
    function initButtonAnimations() {
        document.querySelectorAll('.cta-button').forEach(button => {
            button.addEventListener('mouseenter', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1.05,
                    ease: 'power2.out'
                });
            });

            button.addEventListener('mouseleave', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1,
                    ease: 'power2.out'
                });
            });
        });
    }

    /**
     * Loading Animation
     */
    function initLoadingAnimation() {
        gsap.from('body', {
            duration: 0.8,
            opacity: 0,
            ease: 'power2.out'
        });
    }

    // Initialize loading animation immediately
    initLoadingAnimation();

})();