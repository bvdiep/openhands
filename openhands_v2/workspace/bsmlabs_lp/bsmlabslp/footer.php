        </div><!-- #content -->
        
        <footer id="colophon" class="site-footer bg-gray-900 text-white">
            <div class="footer-widgets py-16">
                <div class="container mx-auto px-4">
                    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <?php if (is_active_sidebar('footer-1')) : ?>
                            <div class="footer-widget-area">
                                <?php dynamic_sidebar('footer-1'); ?>
                            </div>
                        <?php else : ?>
                            <div class="footer-widget-area">
                                <h3 class="widget-title text-lg font-semibold mb-4">Company</h3>
                                <ul class="space-y-2">
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">About Us</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Careers</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Press</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Contact</a></li>
                                </ul>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (is_active_sidebar('footer-2')) : ?>
                            <div class="footer-widget-area">
                                <?php dynamic_sidebar('footer-2'); ?>
                            </div>
                        <?php else : ?>
                            <div class="footer-widget-area">
                                <h3 class="widget-title text-lg font-semibold mb-4">Products</h3>
                                <ul class="space-y-2">
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">WORK+ Platform</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">HRM+ Platform</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">FINANCE+ Platform</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">CRM Platform</a></li>
                                </ul>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (is_active_sidebar('footer-3')) : ?>
                            <div class="footer-widget-area">
                                <?php dynamic_sidebar('footer-3'); ?>
                            </div>
                        <?php else : ?>
                            <div class="footer-widget-area">
                                <h3 class="widget-title text-lg font-semibold mb-4">Resources</h3>
                                <ul class="space-y-2">
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Documentation</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Help Center</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">API Reference</a></li>
                                    <li><a href="#" class="text-gray-300 hover:text-white transition-colors">Community</a></li>
                                </ul>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (is_active_sidebar('footer-4')) : ?>
                            <div class="footer-widget-area">
                                <?php dynamic_sidebar('footer-4'); ?>
                            </div>
                        <?php else : ?>
                            <div class="footer-widget-area">
                                <h3 class="widget-title text-lg font-semibold mb-4">Connect</h3>
                                <div class="flex space-x-4 mb-4">
                                    <a href="#" class="text-gray-300 hover:text-white transition-colors" aria-label="Facebook">
                                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                                        </svg>
                                    </a>
                                    <a href="#" class="text-gray-300 hover:text-white transition-colors" aria-label="Twitter">
                                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                                        </svg>
                                    </a>
                                    <a href="#" class="text-gray-300 hover:text-white transition-colors" aria-label="LinkedIn">
                                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                                        </svg>
                                    </a>
                                </div>
                                <p class="text-sm text-gray-400">
                                    Stay updated with our latest news and updates.
                                </p>
                            </div>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom py-6 border-t border-gray-800">
                <div class="container mx-auto px-4">
                    <div class="flex flex-col md:flex-row justify-between items-center">
                        <div class="site-info text-sm text-gray-400">
                            <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
                        </div>
                        
                        <nav class="footer-navigation mt-4 md:mt-0">
                            <?php
                            wp_nav_menu(array(
                                'theme_location' => 'footer',
                                'menu_id'        => 'footer-menu',
                                'container'      => false,
                                'menu_class'     => 'footer-menu flex space-x-6 text-sm',
                                'fallback_cb'    => false,
                            ));
                            ?>
                            <?php if (!has_nav_menu('footer')) : ?>
                                <ul class="footer-menu flex space-x-6 text-sm">
                                    <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
                                    <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
                                    <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Cookie Policy</a></li>
                                </ul>
                            <?php endif; ?>
                        </nav>
                    </div>
                </div>
            </div>
        </footer>
    </div><!-- #page -->
    
    <?php wp_footer(); ?>
</body>
</html>