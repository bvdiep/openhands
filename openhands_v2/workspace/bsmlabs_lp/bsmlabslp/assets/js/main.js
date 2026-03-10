/**
 * Main JavaScript for BSMLabs LP Theme
 * 
 * @package BSMLabs_LP
 * @version 1.0.0
 */

(function($) {
    'use strict';

    // DOM Ready
    $(document).ready(function() {
        initMobileMenu();
        initSmoothScrolling();
        initScrollAnimations();
        initPlatformTabs();
    });

    /**
     * Initialize Mobile Menu
     */
    function initMobileMenu() {
        $('.mobile-menu-toggle').on('click', function() {
            $('.mobile-menu').toggleClass('hidden');
            
            // Toggle hamburger icon
            const icon = $(this).find('svg');
            if ($('.mobile-menu').hasClass('hidden')) {
                icon.html('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>');
            } else {
                icon.html('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>');
            }
        });

        // Close mobile menu when clicking outside
        $(document).on('click', function(e) {
            if (!$(e.target).closest('.mobile-menu, .mobile-menu-toggle').length) {
                $('.mobile-menu').addClass('hidden');
                $('.mobile-menu-toggle svg').html('<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>');
            }
        });
    }

    /**
     * Initialize Smooth Scrolling
     */
    function initSmoothScrolling() {
        $('a[href^="#"]').on('click', function(e) {
            const target = $(this.getAttribute('href'));
            
            if (target.length) {
                e.preventDefault();
                
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 800, 'easeInOutCubic');
            }
        });
    }

    /**
     * Initialize Scroll Animations
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, observerOptions);

        // Observe elements with animation class
        document.querySelectorAll('.animate-on-scroll').forEach(function(el) {
            observer.observe(el);
        });
    }

    /**
     * Initialize Platform Tabs
     */
    function initPlatformTabs() {
        $('.industry-tab').on('click', function() {
            const $this = $(this);
            const target = $this.data('target');

            // Remove active class from all tabs
            $('.industry-tab').removeClass('active');
            
            // Add active class to clicked tab
            $this.addClass('active');

            // Hide all tab content
            $('.industry-content').addClass('hidden');
            
            // Show target content
            $(target).removeClass('hidden');
        });
    }

    /**
     * Initialize Counter Animation
     */
    function initCounters() {
        $('.counter').each(function() {
            const $this = $(this);
            const countTo = $this.attr('data-count');

            $({ countNum: $this.text() }).animate({
                countNum: countTo
            }, {
                duration: 2000,
                easing: 'linear',
                step: function() {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                    $this.text(this.countNum);
                }
            });
        });
    }

    /**
     * Initialize Testimonial Slider
     */
    function initTestimonialSlider() {
        if (typeof Swiper !== 'undefined') {
            new Swiper('.testimonial-slider', {
                slidesPerView: 1,
                spaceBetween: 30,
                loop: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                breakpoints: {
                    768: {
                        slidesPerView: 2,
                    },
                    1024: {
                        slidesPerView: 3,
                    }
                }
            });
        }
    }

    /**
     * Initialize Client Logo Slider
     */
    function initClientLogoSlider() {
        if (typeof Swiper !== 'undefined') {
            new Swiper('.client-logo-slider', {
                slidesPerView: 2,
                spaceBetween: 30,
                loop: true,
                autoplay: {
                    delay: 3000,
                    disableOnInteraction: false,
                },
                breakpoints: {
                    480: {
                        slidesPerView: 3,
                    },
                    768: {
                        slidesPerView: 4,
                    },
                    1024: {
                        slidesPerView: 6,
                    }
                }
            });
        }
    }

    // Initialize sliders when Swiper is loaded
    $(window).on('load', function() {
        initTestimonialSlider();
        initClientLogoSlider();
    });

    // Scroll to top functionality
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });

    $('.scroll-to-top').click(function() {
        $('html, body').animate({ scrollTop: 0 }, 800);
        return false;
    });

})(jQuery);