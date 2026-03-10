<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
    <?php wp_body_open(); ?>
    
    <div id="page" class="site">
        <a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e('Skip to content', 'bsmlabslp'); ?></a>
        
        <header id="masthead" class="site-header">
            <div class="container mx-auto px-4">
                <div class="flex items-center justify-between py-4">
                    <!-- Logo Section -->
                    <div class="site-branding flex items-center">
                        <?php
                        if (has_custom_logo()) {
                            the_custom_logo();
                        } else {
                            ?>
                            <div class="logo-container">
                                <h1 class="site-title text-2xl font-bold text-gray-900 m-0">
                                    <a href="<?php echo esc_url(home_url('/')); ?>" rel="home" class="hover:text-blue-600 transition-colors duration-200">
                                        <?php bloginfo('name'); ?>
                                    </a>
                                </h1>
                                <?php
                                $description = get_bloginfo('description', 'display');
                                if ($description || is_customize_preview()) {
                                    ?>
                                    <p class="site-description text-sm text-gray-600 m-0"><?php echo $description; ?></p>
                                    <?php
                                }
                                ?>
                            </div>
                            <?php
                        }
                        ?>
                    </div>
                    
                    <!-- Desktop Navigation -->
                    <nav id="site-navigation" class="main-navigation hidden lg:block">
                        <?php
                        wp_nav_menu(array(
                            'theme_location' => 'primary',
                            'menu_id'        => 'primary-menu',
                            'container'      => false,
                            'menu_class'     => 'primary-menu flex items-center space-x-8',
                            'fallback_cb'    => false,
                        ));
                        ?>
                    </nav>
                    
                    <!-- Header Actions -->
                    <div class="header-actions flex items-center space-x-4">
                        <!-- CTA Button -->
                        <a href="#contact" class="cta-button hidden md:inline-flex">
                            Request Demo
                            <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                            </svg>
                        </a>
                        
                        <!-- Mobile menu button -->
                        <button class="lg:hidden mobile-menu-toggle p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors" aria-label="Toggle mobile menu" aria-expanded="false">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                    </div>
                </div>
                
                <!-- Mobile menu -->
                <div class="mobile-menu lg:hidden hidden">
                    <div class="py-4 border-t border-gray-200">
                        <?php
                        wp_nav_menu(array(
                            'theme_location' => 'primary',
                            'menu_id'        => 'mobile-menu',
                            'container'      => false,
                            'menu_class'     => 'mobile-menu-list space-y-2',
                            'fallback_cb'    => false,
                        ));
                        ?>
                        <div class="pt-4 border-t border-gray-200 mt-4">
                            <a href="#contact" class="cta-button block w-full text-center">
                                Request Demo
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        
        <div id="content" class="site-content">