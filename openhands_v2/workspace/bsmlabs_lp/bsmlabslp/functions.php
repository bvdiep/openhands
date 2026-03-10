<?php
/**
 * BSMLabs LP Theme Functions
 * 
 * @package BSMLabs_LP
 * @version 1.0.0
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme Setup
 */
function bsmlabslp_setup() {
    // Add theme support for various features
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ));
    
    // Add theme support for responsive embeds
    add_theme_support('responsive-embeds');
    
    // Add theme support for editor styles
    add_theme_support('editor-styles');
    
    // Add theme support for wide alignment
    add_theme_support('align-wide');
    
    // Add theme support for custom logo
    add_theme_support('custom-logo', array(
        'height'      => 60,
        'width'       => 200,
        'flex-height' => true,
        'flex-width'  => true,
    ));
    
    // Register navigation menus
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'bsmlabslp'),
        'footer'  => __('Footer Menu', 'bsmlabslp'),
    ));
    
    // Add theme support for custom background
    add_theme_support('custom-background', array(
        'default-color' => 'ffffff',
    ));
    
    // Set content width
    if (!isset($content_width)) {
        $content_width = 1200;
    }
}
add_action('after_setup_theme', 'bsmlabslp_setup');

/**
 * Enqueue styles and scripts
 */
function bsmlabslp_scripts() {
    // Theme version for cache busting
    $theme_version = wp_get_theme()->get('Version');
    
    // Google Fonts
    wp_enqueue_style(
        'bsmlabslp-google-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
        array(),
        null
    );
    
    // Main theme stylesheet
    wp_enqueue_style(
        'bsmlabslp-style',
        get_stylesheet_uri(),
        array('bsmlabslp-google-fonts'),
        $theme_version
    );
    
    // Tailwind CSS (will be compiled)
    wp_enqueue_style(
        'bsmlabslp-tailwind',
        get_template_directory_uri() . '/assets/css/tailwind.css',
        array(),
        $theme_version
    );
    
    // Custom components CSS
    wp_enqueue_style(
        'bsmlabslp-components',
        get_template_directory_uri() . '/assets/css/components.css',
        array('bsmlabslp-tailwind'),
        $theme_version
    );
    
    // GSAP Animation Library
    wp_enqueue_script(
        'gsap',
        'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.3/gsap.min.js',
        array(),
        '3.12.3',
        true
    );
    
    // GSAP ScrollTrigger
    wp_enqueue_script(
        'gsap-scrolltrigger',
        'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.3/ScrollTrigger.min.js',
        array('gsap'),
        '3.12.3',
        true
    );
    
    // Swiper.js for sliders
    wp_enqueue_style(
        'swiper-css',
        'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css',
        array(),
        '11.0.0'
    );
    
    wp_enqueue_script(
        'swiper-js',
        'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js',
        array(),
        '11.0.0',
        true
    );
    
    // Theme JavaScript files
    wp_enqueue_script(
        'bsmlabslp-animations',
        get_template_directory_uri() . '/assets/js/animations.js',
        array('gsap', 'gsap-scrolltrigger'),
        $theme_version,
        true
    );
    
    wp_enqueue_script(
        'bsmlabslp-main',
        get_template_directory_uri() . '/assets/js/main.js',
        array('jquery', 'swiper-js'),
        $theme_version,
        true
    );
    
    // Localize script for AJAX
    wp_localize_script('bsmlabslp-main', 'bsmlabslp_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce'    => wp_create_nonce('bsmlabslp_nonce'),
    ));
    
    // Comment reply script
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'bsmlabslp_scripts');

/**
 * Register widget areas
 */
function bsmlabslp_widgets_init() {
    register_sidebar(array(
        'name'          => __('Footer Widget Area 1', 'bsmlabslp'),
        'id'            => 'footer-1',
        'description'   => __('Add widgets here to appear in the first footer column.', 'bsmlabslp'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    register_sidebar(array(
        'name'          => __('Footer Widget Area 2', 'bsmlabslp'),
        'id'            => 'footer-2',
        'description'   => __('Add widgets here to appear in the second footer column.', 'bsmlabslp'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    register_sidebar(array(
        'name'          => __('Footer Widget Area 3', 'bsmlabslp'),
        'id'            => 'footer-3',
        'description'   => __('Add widgets here to appear in the third footer column.', 'bsmlabslp'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    register_sidebar(array(
        'name'          => __('Footer Widget Area 4', 'bsmlabslp'),
        'id'            => 'footer-4',
        'description'   => __('Add widgets here to appear in the fourth footer column.', 'bsmlabslp'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}
add_action('widgets_init', 'bsmlabslp_widgets_init');

/**
 * Custom excerpt length
 */
function bsmlabslp_excerpt_length($length) {
    return 30;
}
add_filter('excerpt_length', 'bsmlabslp_excerpt_length');

/**
 * Custom excerpt more
 */
function bsmlabslp_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'bsmlabslp_excerpt_more');

/**
 * Add Max Mega Menu support
 */
function bsmlabslp_megamenu_support() {
    add_theme_support('megamenu');
}
add_action('after_setup_theme', 'bsmlabslp_megamenu_support');

/**
 * Custom Post Types Registration
 */
function bsmlabslp_register_post_types() {
    // Platforms Post Type
    register_post_type('platforms', array(
        'labels' => array(
            'name'               => __('Platforms', 'bsmlabslp'),
            'singular_name'      => __('Platform', 'bsmlabslp'),
            'menu_name'          => __('Platforms', 'bsmlabslp'),
            'add_new'            => __('Add New', 'bsmlabslp'),
            'add_new_item'       => __('Add New Platform', 'bsmlabslp'),
            'edit_item'          => __('Edit Platform', 'bsmlabslp'),
            'new_item'           => __('New Platform', 'bsmlabslp'),
            'view_item'          => __('View Platform', 'bsmlabslp'),
            'search_items'       => __('Search Platforms', 'bsmlabslp'),
            'not_found'          => __('No platforms found', 'bsmlabslp'),
            'not_found_in_trash' => __('No platforms found in Trash', 'bsmlabslp'),
        ),
        'public'       => true,
        'has_archive'  => true,
        'show_in_rest' => true,
        'supports'     => array('title', 'editor', 'thumbnail', 'excerpt'),
        'menu_icon'    => 'dashicons-admin-tools',
    ));
    
    // Industries Post Type
    register_post_type('industries', array(
        'labels' => array(
            'name'               => __('Industries', 'bsmlabslp'),
            'singular_name'      => __('Industry', 'bsmlabslp'),
            'menu_name'          => __('Industries', 'bsmlabslp'),
            'add_new'            => __('Add New', 'bsmlabslp'),
            'add_new_item'       => __('Add New Industry', 'bsmlabslp'),
            'edit_item'          => __('Edit Industry', 'bsmlabslp'),
            'new_item'           => __('New Industry', 'bsmlabslp'),
            'view_item'          => __('View Industry', 'bsmlabslp'),
            'search_items'       => __('Search Industries', 'bsmlabslp'),
            'not_found'          => __('No industries found', 'bsmlabslp'),
            'not_found_in_trash' => __('No industries found in Trash', 'bsmlabslp'),
        ),
        'public'       => true,
        'has_archive'  => true,
        'show_in_rest' => true,
        'supports'     => array('title', 'editor', 'thumbnail', 'excerpt'),
        'menu_icon'    => 'dashicons-building',
    ));
    
    // Testimonials Post Type
    register_post_type('testimonials', array(
        'labels' => array(
            'name'               => __('Testimonials', 'bsmlabslp'),
            'singular_name'      => __('Testimonial', 'bsmlabslp'),
            'menu_name'          => __('Testimonials', 'bsmlabslp'),
            'add_new'            => __('Add New', 'bsmlabslp'),
            'add_new_item'       => __('Add New Testimonial', 'bsmlabslp'),
            'edit_item'          => __('Edit Testimonial', 'bsmlabslp'),
            'new_item'           => __('New Testimonial', 'bsmlabslp'),
            'view_item'          => __('View Testimonial', 'bsmlabslp'),
            'search_items'       => __('Search Testimonials', 'bsmlabslp'),
            'not_found'          => __('No testimonials found', 'bsmlabslp'),
            'not_found_in_trash' => __('No testimonials found in Trash', 'bsmlabslp'),
        ),
        'public'       => true,
        'has_archive'  => true,
        'show_in_rest' => true,
        'supports'     => array('title', 'editor', 'thumbnail'),
        'menu_icon'    => 'dashicons-format-quote',
    ));
}
add_action('init', 'bsmlabslp_register_post_types');

/**
 * Add theme customizer options
 */
function bsmlabslp_customize_register($wp_customize) {
    // Hero Section
    $wp_customize->add_section('bsmlabslp_hero', array(
        'title'    => __('Hero Section', 'bsmlabslp'),
        'priority' => 30,
    ));
    
    $wp_customize->add_setting('hero_title', array(
        'default'           => __('Enterprise Solutions for Modern Business', 'bsmlabslp'),
        'sanitize_callback' => 'sanitize_text_field',
    ));
    
    $wp_customize->add_control('hero_title', array(
        'label'   => __('Hero Title', 'bsmlabslp'),
        'section' => 'bsmlabslp_hero',
        'type'    => 'text',
    ));
    
    $wp_customize->add_setting('hero_subtitle', array(
        'default'           => __('Comprehensive platform for business management and growth', 'bsmlabslp'),
        'sanitize_callback' => 'sanitize_textarea_field',
    ));
    
    $wp_customize->add_control('hero_subtitle', array(
        'label'   => __('Hero Subtitle', 'bsmlabslp'),
        'section' => 'bsmlabslp_hero',
        'type'    => 'textarea',
    ));
}
add_action('customize_register', 'bsmlabslp_customize_register');

/**
 * Security enhancements
 */
function bsmlabslp_security_headers() {
    if (!is_admin()) {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
    }
}
add_action('send_headers', 'bsmlabslp_security_headers');