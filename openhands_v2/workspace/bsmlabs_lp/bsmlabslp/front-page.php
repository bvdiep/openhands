<?php get_header(); ?>

<div id="primary" class="content-area">
    <main id="main" class="site-main">
        
        <!-- Hero Section -->
        <section class="hero-section bg-gradient-to-br from-gray-50 to-white py-20">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-4xl mx-auto">
                    <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                        <?php echo get_theme_mod('hero_title', 'Enterprise Solutions for Modern Business'); ?>
                    </h1>
                    <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                        <?php echo get_theme_mod('hero_subtitle', 'Comprehensive platform for business management and growth'); ?>
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="#platforms" class="cta-button inline-flex items-center justify-center">
                            Get Started
                            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                            </svg>
                        </a>
                        <a href="#demo" class="bg-white text-gray-900 px-8 py-4 rounded-lg font-semibold border border-gray-200 hover:bg-gray-50 transition-all duration-200">
                            Watch Demo
                        </a>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Client Logos Section -->
        <section class="client-logos py-16 bg-white">
            <div class="container mx-auto px-4">
                <div class="text-center mb-12">
                    <h2 class="text-3xl font-bold text-gray-900 mb-4">
                        Trusted by <span class="text-blue-600">11,000+</span> businesses
                    </h2>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 items-center opacity-60">
                    <!-- Client logos will be populated via ACF -->
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                    <div class="flex items-center justify-center h-16 bg-gray-100 rounded-lg">
                        <span class="text-gray-400 text-sm">Client Logo</span>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Platform Showcase Section -->
        <section id="platforms" class="platforms-section py-20 bg-gray-50">
            <div class="container mx-auto px-4">
                <div class="text-center mb-16">
                    <h2 class="text-4xl font-bold text-gray-900 mb-4">
                        One Platform, <span class="text-blue-600">All Solutions</span>
                    </h2>
                    <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                        Comprehensive business management tools designed for modern enterprises
                    </p>
                </div>
                
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <!-- Platform cards will be populated via ACF -->
                    <div class="platform-card p-8">
                        <div class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">WORK+ Platform</h3>
                        <p class="text-gray-600 mb-6">Smart work management connecting departments effectively</p>
                        <a href="#" class="text-blue-600 font-semibold hover:text-blue-700 transition-colors">
                            Learn More →
                        </a>
                    </div>
                    
                    <div class="platform-card p-8">
                        <div class="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                            </svg>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">HRM+ Platform</h3>
                        <p class="text-gray-600 mb-6">Creating happy employee experiences</p>
                        <a href="#" class="text-blue-600 font-semibold hover:text-blue-700 transition-colors">
                            Learn More →
                        </a>
                    </div>
                    
                    <div class="platform-card p-8">
                        <div class="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                            <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                            </svg>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">FINANCE+ Platform</h3>
                        <p class="text-gray-600 mb-6">Real-time financial management</p>
                        <a href="#" class="text-blue-600 font-semibold hover:text-blue-700 transition-colors">
                            Learn More →
                        </a>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- CTA Section -->
        <section class="cta-section py-20 bg-blue-600">
            <div class="container mx-auto px-4 text-center">
                <h2 class="text-4xl font-bold text-white mb-6">
                    Ready to Transform Your Business?
                </h2>
                <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                    Join thousands of companies already using our platform to streamline operations and drive growth.
                </p>
                <a href="#contact" class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 inline-flex items-center">
                    Start Free Trial
                    <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                    </svg>
                </a>
            </div>
        </section>
        
    </main>
</div>

<?php get_footer(); ?>