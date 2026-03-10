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
                    <div class="site-branding">
                        <?php
                        if (has_custom_logo()) {
                            the_custom_logo();
                        } else {
                            ?>
                            <h1 class="site-title">
                                <a href="<?php echo esc_url(home_url('/')); ?>" rel="home">
                                    <?php bloginfo('name'); ?>
                                </a>
                            </h1>
                            <?php
                            $description = get_bloginfo('description', 'display');
                            if ($description || is_customize_preview()) {
                                ?>
                                <p class="site-description"><?php echo $description; ?></p>
                                <?php
                            }
                        }
                        ?>
                    </div>
                    
                    <nav id="site-navigation" class="main-navigation">
                        <?php
                        wp_nav_menu(array(
                            'theme_location' => 'primary',
                            'menu_id'        => 'primary-menu',
                            'container'      => false,
                            'menu_class'     => 'primary-menu',
                            'fallback_cb'    => false,
                        ));
                        ?>
                    </nav>
                </div>
            </div>
        </header>
        
        <div id="content" class="site-content">
            <div id="primary" class="content-area">
                <main id="main" class="site-main">
                    <?php
                    if (have_posts()) {
                        while (have_posts()) {
                            the_post();
                            ?>
                            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                                <header class="entry-header">
                                    <h2 class="entry-title">
                                        <a href="<?php the_permalink(); ?>" rel="bookmark">
                                            <?php the_title(); ?>
                                        </a>
                                    </h2>
                                </header>
                                
                                <div class="entry-content">
                                    <?php the_excerpt(); ?>
                                </div>
                                
                                <footer class="entry-footer">
                                    <span class="posted-on">
                                        <?php echo get_the_date(); ?>
                                    </span>
                                </footer>
                            </article>
                            <?php
                        }
                        
                        the_posts_navigation();
                    } else {
                        ?>
                        <section class="no-results not-found">
                            <header class="page-header">
                                <h1 class="page-title"><?php esc_html_e('Nothing here', 'bsmlabslp'); ?></h1>
                            </header>
                            
                            <div class="page-content">
                                <p><?php esc_html_e('It looks like nothing was found at this location.', 'bsmlabslp'); ?></p>
                            </div>
                        </section>
                        <?php
                    }
                    ?>
                </main>
            </div>
        </div>
        
        <?php get_footer(); ?>
    </div>
    
    <?php wp_footer(); ?>
</body>
</html>